from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup

from sourcing1688.models import DetailResponse, PriceTier, ProductDetail, SellerInfo, SkuOption
from sourcing1688.parsers.asset_extractor import extract_assets
from sourcing1688.parsers.embedded_json import extract_embedded_json_candidates, merge_candidates
from sourcing1688.utils import extract_offer_id, structured_error


PARSER_VERSION = "0.2.0"


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


def _extract_offer_id(html: str, path: Path | None) -> str | None:
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
    raw_attrs = embedded.get("productAttribute") or embedded.get("attributes")
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
    raw_ranges = embedded.get("priceRange") or embedded.get("priceRanges") or []
    tiers: list[PriceTier] = []
    if isinstance(raw_ranges, list):
        for item in raw_ranges:
            if not isinstance(item, dict):
                continue
            price = _float(item.get("price"))
            if price is None:
                continue
            tiers.append(PriceTier(min_quantity=_int(item.get("startQuantity") or item.get("minQuantity")) or 1, price=price))
    return tiers


def _extract_sku_options(embedded: dict) -> list[SkuOption]:
    raw_options = embedded.get("skuOptions") or embedded.get("sku_options") or []
    options: list[SkuOption] = []
    if isinstance(raw_options, list):
        for item in raw_options:
            if isinstance(item, dict) and item.get("name"):
                values = item.get("values") or []
                options.append(SkuOption(name=str(item["name"]), values=[str(value) for value in values]))
    return options


def parse_rendered_html(html: str, *, source_path: str | Path | None = None) -> DetailResponse:
    path = Path(source_path) if source_path else None
    soup = BeautifulSoup(html, "html.parser")
    embedded = merge_candidates(extract_embedded_json_candidates(soup, html))
    offer_id = str(embedded.get("offerId") or embedded.get("offer_id") or _extract_offer_id(html, path) or "")
    if not offer_id:
        message = "Could not extract 1688 offer_id from rendered HTML."
        return DetailResponse(status="partial_data", message=message, error=structured_error("invalid_offer_id", message), provider="local_html", provider_version=PARSER_VERSION, source_type="local_html", live_verified=False)
    title = embedded.get("subject") or embedded.get("title") or (soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else None) or (soup.title.string.strip() if soup.title and soup.title.string else None) or f"1688 offer {offer_id}"
    assets = extract_assets(soup, html)
    seller_raw = embedded.get("seller") if isinstance(embedded.get("seller"), dict) else {}
    detail = ProductDetail(
        offer_id=offer_id,
        url=f"https://detail.1688.com/offer/{offer_id}.html",
        title_zh=str(title),
        title_ko_optional=embedded.get("subjectTrans") or embedded.get("titleTrans"),
        price_tiers=_extract_price_tiers(embedded),
        sku_options=_extract_sku_options(embedded),
        attributes=_extract_attributes(soup, embedded),
        stock=_int(embedded.get("stock")),
        month_sold=_int(embedded.get("monthSold")),
        trade_volume=_int(embedded.get("tradeVolume")),
        repurchase_rate=_rate(embedded.get("repurchaseRate")),
        seller=SellerInfo(name=seller_raw.get("name"), score=_float(seller_raw.get("score"))) if seller_raw else None,
        main_image_urls=assets["main_images"],
        detail_image_urls=assets["detail_images"],
        option_image_urls=assets["option_images"],
        video_urls=assets["videos"],
        raw_source_summary={"provider": "local_html", "parser_version": PARSER_VERSION, "source_path": str(path) if path else None},
        provider="local_html",
        provider_version=PARSER_VERSION,
        live_verified=True,
        source_type="local_html",
        fetched_at=datetime.now(timezone.utc),
        raw_reference_path=str(path) if path else None,
    )
    missing = []
    for field in ["price_tiers", "main_image_urls", "detail_image_urls", "attributes", "seller", "category", "stock"]:
        value = getattr(detail, field)
        if not value:
            missing.append(field)
    detail.missing_fields = missing
    return DetailResponse(status="ok" if not missing else "partial_data", item=detail, provider="local_html", provider_version=PARSER_VERSION, source_type="local_html", live_verified=True, fetched_at=datetime.now(timezone.utc), missing_fields=missing, raw_reference_path=str(path) if path else None)


def parse_rendered_html_file(path: str | Path) -> DetailResponse:
    file_path = Path(path)
    return parse_rendered_html(file_path.read_text(encoding="utf-8"), source_path=file_path)
