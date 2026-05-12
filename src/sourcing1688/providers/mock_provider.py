from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx

from sourcing1688.assets.downloader import download_assets
from sourcing1688.models import (
    AssetDownloadResponse,
    DetailResponse,
    HotKeyword,
    HotKeywordsResponse,
    ProductDetail,
    ProductSearchResult,
    RankingItem,
    RankingsResponse,
    SearchResponse,
    ImageSearchResponse,
    ProviderCapability,
)
from sourcing1688.providers.base import Base1688Provider
from sourcing1688.utils import extract_offer_id
from sourcing1688.utils import structured_error


class Mock1688Provider(Base1688Provider):
    name = "mock"
    provider_version = "0.2.0"
    source_type = "mock"

    def __init__(self, fixture_dir: str | Path | None = None) -> None:
        self.fixture_dir = Path(fixture_dir) if fixture_dir else Path(__file__).resolve().parents[3] / "tests" / "fixtures"

    def _read_json(self, filename: str) -> dict[str, Any]:
        return json.loads((self.fixture_dir / filename).read_text(encoding="utf-8"))

    def _read_text(self, filename: str) -> str:
        return (self.fixture_dir / filename).read_text(encoding="utf-8")

    def capabilities(self) -> ProviderCapability:
        return ProviderCapability(
            provider=self.name,
            provider_version=self.provider_version,
            source_type="mock",
            live_verified=True,
            search=True,
            detail=True,
            download_assets=True,
            hot_keywords=True,
            rankings=True,
            image_search=True,
            notes=["Fixture-backed provider for deterministic development and tests."],
        )

    async def search_products(
        self,
        keyword: str,
        page: int = 1,
        page_size: int = 30,
        sort: str | None = None,
        filters: dict[str, Any] | None = None,
    ) -> SearchResponse:
        data = self._read_json("search_result_sample.json")
        metadata = {"provider": self.name, "provider_version": self.provider_version, "source_type": "mock", "live_verified": True}
        items = [ProductSearchResult.model_validate(item | {"source_keyword": keyword} | metadata) for item in data["items"]]
        start = max(page - 1, 0) * page_size
        return SearchResponse(status="ok", items=items[start : start + page_size], keyword=keyword, provider=self.name, provider_version=self.provider_version, source_type="mock", live_verified=True)

    async def get_product_detail(self, offer_id_or_url: str) -> DetailResponse:
        try:
            offer_id = extract_offer_id(offer_id_or_url)
        except ValueError as exc:
            return DetailResponse(
                status="error",
                message=str(exc),
                error=structured_error("invalid_offer_id", str(exc)),
                provider=self.name,
            )
        data = self._read_json("product_detail_sample.json")
        data["offer_id"] = offer_id
        data["url"] = f"https://detail.1688.com/offer/{offer_id}.html"
        detail = ProductDetail.model_validate(data | {"provider": self.name, "provider_version": self.provider_version, "source_type": "mock", "live_verified": True})
        return DetailResponse(status="ok", item=detail, provider=self.name, provider_version=self.provider_version, source_type="mock", live_verified=True)

    async def download_product_assets(
        self,
        offer_id_or_url: str,
        output_dir: str | Path,
        include: str | set[str] | list[str] | None = None,
        dry_run: bool = False,
    ) -> AssetDownloadResponse:
        detail_response = await self.get_product_detail(offer_id_or_url)
        if detail_response.item is None:
            return AssetDownloadResponse(
                status="error",
                message=detail_response.message,
                error=detail_response.error,
                provider=self.name,
            )

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, content=f"mock asset for {request.url}".encode("utf-8"))

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            manifest = await download_assets(
                detail_response.item,
                output_dir,
                include=include,
                client=client,
                html=self._read_text("product_detail_sample.html"),
                dry_run=dry_run,
            )
        return AssetDownloadResponse(status=manifest.status, manifest=manifest, manifest_path=str(Path(manifest.saved_dir) / "manifest.json"), provider=self.name, provider_version=self.provider_version, source_type="mock", live_verified=True)

    async def get_hot_keywords(self, category_id: str | None = None, limit: int = 20) -> HotKeywordsResponse:
        data = self._read_json("ranking_sample.json")
        items = [HotKeyword.model_validate(item) for item in data["hot_keywords"]]
        if category_id:
            items = [item for item in items if item.category_id == category_id]
        return HotKeywordsResponse(status="ok", items=items[:limit], provider=self.name, provider_version=self.provider_version, source_type="mock", live_verified=True)

    async def get_rankings(
        self,
        category_id: str | None = None,
        rank_type: str = "hot",
        limit: int = 20,
    ) -> RankingsResponse:
        data = self._read_json("ranking_sample.json")
        items = [RankingItem.model_validate(item) for item in data["rankings"]]
        return RankingsResponse(status="ok", items=items[:limit], provider=self.name, provider_version=self.provider_version, source_type="mock", live_verified=True, message=f"mock {rank_type} rankings")

    async def image_search(self, image_url: str | None = None, image_path: str | None = None, page: int = 1, page_size: int = 20) -> ImageSearchResponse:
        data = self._read_json("image_search_sample.json")
        items = [ProductSearchResult.model_validate(item | {"provider": self.name, "provider_version": self.provider_version, "source_type": "mock", "live_verified": True}) for item in data["items"]]
        return ImageSearchResponse(status="ok", items=items[:page_size], image_url=image_url, image_path=image_path, provider=self.name, provider_version=self.provider_version, source_type="mock", live_verified=True)
