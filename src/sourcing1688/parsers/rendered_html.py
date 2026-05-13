from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup

from sourcing1688.models import DetailResponse, PriceTier, ProductDetail, SellerInfo, SkuOption
from sourcing1688.parsers.asset_extractor import dedupe_urls, extract_assets
from sourcing1688.parsers.embedded_json import extract_embedded_json_candidates, merge_candidates
from sourcing1688.utils import extract_offer_id, structured_error


PARSER_VERSION = "0.3.0"


def _dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def _float(value) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace("%", "").replace(",", "").strip())
    except ValueError:
        return None


def _int(value) -> int | None:
    parsed = _float(value)
    return int(parsed) if parsed is not None else None


def _rate(value) -> float | None:
    parsed = _float(value)
    if parsed is None:
        return None
    return parsed / 100 if parsed > 1 else parsed


def _extract_offer_id(html: str, path: Path | None, source_url: str | None = None) -> str | None:
    if source_url:
        try:
            return extract_offer_id(source_url)
        except ValueError:
            pass
    for pattern in [
        r"detail\.1688\.com/offer/(\d+)\.html",
        r'"offerId"\s*:\s*"?(\d+)"?',
        r'"offer_id"\s*:\s*"?(\d+)"?',
        r"offer/(\d+)\.html",
    ]:
        if match := re.search(pattern, html):
            return match.group(1)
    if path and (match := re.search(r"(\d{6,})", path.name)):
        return match.group(1)
    return None


def _extract_attributes(soup: BeautifulSoup, embedded: dict) -> dict[str, object]:
    attrs: dict[str, object] = {}
    offer_model = _dict(embedded.get("offerModel"))
    raw_attrs = (
        embedded.get("productAttribute")
        or embedded.get("attributes")
        or offer_model.get("productAttribute")
        or offer_model.get("productAttributes")
        or offer_model.get("productFeatureList")
    )
    if isinstance(raw_attrs, dict):
        attrs.update(raw_attrs)
    elif isinstance(raw_attrs, list):
        for item in raw_attrs:
            if isinstance(item, dict):
                key = item.get("attributeName") or item.get("name")
                if key:
                    attrs[str(key)] = item.get("value")
    for row in soup.find_all("tr"):
        cells = [cell.get_text(" ", strip=True) for cell in row.find_all(["th", "td"])]
        if len(cells) >= 2 and cells[0] and len(cells[0]) <= 30:
            attrs.setdefault(cells[0], cells[1])
    return attrs


def _extract_price_tiers(embedded: dict) -> list[PriceTier]:
    trade_model = _dict(embedded.get("tradeModel"))
    offer_price_model = _dict(trade_model.get("offerPriceModel"))
    raw_ranges = embedded.get("priceRange") or embedded.get("priceRanges") or []
    raw_current_prices = offer_price_model.get("currentPrices") or []
    tiers: list[PriceTier] = []
    for raw_items in [raw_ranges, raw_current_prices]:
        if not isinstance(raw_items, list):
            continue
        for item in raw_items:
            if not isinstance(item, dict):
                continue
            price = _float(item.get("price"))
            if price is None:
                continue
            min_quantity = _int(item.get("startQuantity") or item.get("minQuantity") or item.get("beginAmount")) or 1
            if not any(tier.min_quantity == min_quantity and tier.price == price for tier in tiers):
                tiers.append(PriceTier(min_quantity=min_quantity, price=price))
    if not tiers:
        price = _float(trade_model.get("priceDisplay") or trade_model.get("minPrice") or trade_model.get("maxPrice"))
        if price is not None:
            tiers.append(PriceTier(min_quantity=_int(trade_model.get("beginAmount")) or 1, price=price))
    return tiers


def _extract_sku_options(embedded: dict) -> list[SkuOption]:
    sku_model = _dict(embedded.get("skuModel"))
    raw_options = embedded.get("skuOptions") or embedded.get("sku_options") or sku_model.get("skuProps") or embedded.get("skuProps") or []
    options: list[SkuOption] = []
    if isinstance(raw_options, list):
        for item in raw_options:
            if not isinstance(item, dict):
                continue
            name = item.get("name") or item.get("prop")
            if not name:
                continue
            raw_values = item.get("values") or item.get("value") or []
            values: list[str] = []
            if isinstance(raw_values, list):
                for value in raw_values:
                    if isinstance(value, dict):
                        option_name = value.get("name") or value.get("value")
                        if option_name:
                            values.append(str(option_name))
                    else:
                        values.append(str(value))
            options.append(SkuOption(name=str(name), values=values))
    return options


def _extract_option_images(embedded: dict) -> list[str]:
    sku_model = _dict(embedded.get("skuModel"))
    raw_options = sku_model.get("skuProps") or embedded.get("skuProps") or []
    urls: list[str] = []
    if isinstance(raw_options, list):
        for item in raw_options:
            if not isinstance(item, dict):
                continue
            raw_values = item.get("value") or item.get("values") or []
            if not isinstance(raw_values, list):
                continue
            for value in raw_values:
                if isinstance(value, dict) and value.get("imageUrl"):
                    urls.append(str(value["imageUrl"]))
    return dedupe_urls(urls)


def _extract_seller(embedded: dict) -> SellerInfo | None:
    seller_raw = _dict(embedded.get("seller")) or _dict(embedded.get("sellerModel"))
    if not seller_raw:
        return None
    winport_urls = _dict(seller_raw.get("sellerWinportUrlMap"))
    signs = _dict(_dict(seller_raw.get("sellerSign")).get("signs"))
    badges = [key for key, enabled in signs.items() if enabled]
    name = seller_raw.get("name") or seller_raw.get("companyName") or seller_raw.get("loginId")
    url = seller_raw.get("url") or seller_raw.get("winportUrl") or winport_urls.get("defaultUrl") or winport_urls.get("indexUrl")
    if not (name or url):
        return None
    return SellerInfo(
        name=str(name) if name else None,
        url=str(url) if url else None,
        score=_float(seller_raw.get("score")),
        level=str(seller_raw.get("level") or seller_raw.get("sellerIdentity") or "") or None,
        badges=badges,
    )


def _extract_category(embedded: dict) -> str | None:
    offer_model = _dict(embedded.get("offerModel"))
    category = embedded.get("category") or embedded.get("leafCategoryName") or offer_model.get("leafCategoryName")
    return str(category) if category else None


def _extract_stock(embedded: dict) -> int | None:
    trade_model = _dict(embedded.get("tradeModel"))
    trade_without_promotion = _dict(trade_model.get("tradeWithoutPromotion"))
    return _int(embedded.get("stock") or trade_model.get("canBookedAmount") or trade_without_promotion.get("canBookedAmountOriginal"))


def _extract_trade_volume(embedded: dict) -> int | None:
    trade_model = _dict(embedded.get("tradeModel"))
    return _int(embedded.get("tradeVolume") or trade_model.get("saleCount"))


def parse_rendered_html(html: str, *, source_path: str | Path | None = None, source_url: str | None = None) -> DetailResponse:
    path = Path(source_path) if source_path else None
    soup = BeautifulSoup(html, "html.parser")
    embedded = merge_candidates(extract_embedded_json_candidates(soup, html))
    offer_id = str(embedded.get("offerId") or embedded.get("offer_id") or _extract_offer_id(html, path, source_url) or "")
    if not offer_id:
        message = "Could not extract 1688 offer_id from rendered HTML."
        return DetailResponse(status="partial_data", message=message, error=structured_error("invalid_offer_id", message), provider="local_html", provider_version=PARSER_VERSION, source_type="local_html", live_verified=False)
    title = embedded.get("subject") or embedded.get("title") or (soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else None) or (soup.title.string.strip() if soup.title and soup.title.string else None) or f"1688 offer {offer_id}"
    assets = extract_assets(soup, html)
    option_images = dedupe_urls(assets["option_images"] + _extract_option_images(embedded))
    warnings = []
    if not assets["videos"] and re.search(r"(videoId|videoUrl|wirelessVideo|rox-wap-detail-video)", html):
        warnings.append("Video metadata was present, but no downloadable video URL was exposed in this HTML. A logged-in rendered page or captured network response may be needed.")
    detail = ProductDetail(
        offer_id=offer_id,
        url=source_url or f"https://detail.1688.com/offer/{offer_id}.html",
        title_zh=str(title),
        title_ko_optional=embedded.get("subjectTrans") or embedded.get("titleTrans"),
        price_tiers=_extract_price_tiers(embedded),
        sku_options=_extract_sku_options(embedded),
        attributes=_extract_attributes(soup, embedded),
        category=_extract_category(embedded),
        stock=_extract_stock(embedded),
        month_sold=_int(embedded.get("monthSold")),
        trade_volume=_extract_trade_volume(embedded),
        repurchase_rate=_rate(embedded.get("repurchaseRate")),
        seller=_extract_seller(embedded),
        main_image_urls=assets["main_images"],
        detail_image_urls=assets["detail_images"],
        option_image_urls=option_images,
        video_urls=assets["videos"],
        raw_source_summary={"provider": "local_html", "parser_version": PARSER_VERSION, "source_path": str(path) if path else None, "source_url": source_url},
        provider="local_html",
        provider_version=PARSER_VERSION,
        live_verified=True,
        source_type="local_html",
        fetched_at=datetime.now(timezone.utc),
        raw_reference_path=str(path) if path else None,
        warnings=warnings,
    )
    missing = []
    for field in ["price_tiers", "main_image_urls", "detail_image_urls", "attributes", "seller", "category", "stock"]:
        value = getattr(detail, field)
        if not value:
            missing.append(field)
    detail.missing_fields = missing
    return DetailResponse(status="ok" if not missing else "partial_data", item=detail, provider="local_html", provider_version=PARSER_VERSION, source_type="local_html", live_verified=True, fetched_at=datetime.now(timezone.utc), missing_fields=missing, raw_reference_path=str(path) if path else None, warnings=warnings)


def parse_rendered_html_file(path: str | Path) -> DetailResponse:
    file_path = Path(path)
    return parse_rendered_html(file_path.read_text(encoding="utf-8"), source_path=file_path)
