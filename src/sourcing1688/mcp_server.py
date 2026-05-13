from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from sourcing1688.browser_profile import open_browser_profile
from sourcing1688.config import get_settings
from sourcing1688.keyword_expander import expand_keywords
from sourcing1688.assets.downloader import download_assets as download_parsed_assets
from sourcing1688.parsers.rendered_html import PARSER_VERSION, parse_network_payload, parse_rendered_html, parse_rendered_html_file
from sourcing1688.services import (
    analyze_product_url,
    check_provider,
    download_product_assets,
    get_all_provider_capabilities,
    get_product_detail,
    get_provider,
    image_search_products,
    recommend_products,
    search_sourcing_products,
)
from sourcing1688.storage import SourcingStorage
from sourcing1688.utils import error_payload, jsonable

mcp = FastMCP("sourcing1688")


@mcp.tool()
def expand_sourcing_keywords(keyword: str) -> dict[str, Any]:
    """Expand a Korean product keyword into Chinese 1688 sourcing keywords."""
    return jsonable(expand_keywords(keyword))


@mcp.tool()
async def search_1688_products(
    keyword: str,
    top: int = 30,
    page: int = 1,
    page_size: int | None = None,
    provider: str | None = None,
    sort: str | None = None,
    filters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Search product candidates. Returns status ok, partial_data, missing_credentials, needs_human_login, blocked_by_verification, or provider_unavailable."""
    return jsonable(
        await search_sourcing_products(
            keyword,
            top=top,
            page=page,
            page_size=page_size,
            provider_name=provider,
            sort=sort,
            filters=filters,
        )
    )


@mcp.tool()
async def analyze_1688_product_url(url: str, provider: str | None = None) -> dict[str, Any]:
    """Analyze a 1688 product detail URL and return structured sourcing suitability."""
    try:
        return jsonable(await analyze_product_url(url, provider_name=provider))
    except ValueError as exc:
        if "offer_id" in str(exc) or "1688 offer" in str(exc):
            return error_payload("invalid_offer_id", str(exc))
        return error_payload("command_failed", str(exc))


@mcp.tool()
async def get_1688_product_detail(offer_id_or_url: str, provider: str | None = None) -> dict[str, Any]:
    """Fetch structured detail data for a 1688 offer id or URL."""
    return jsonable(await get_product_detail(offer_id_or_url, provider_name=provider))


@mcp.tool()
async def download_1688_product_assets(
    offer_id_or_url: str,
    output_dir: str | None = None,
    include: str | list[str] | None = None,
    provider: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Download product assets. Returns ok, dry_run, partial_success, missing_credentials, needs_human_login, blocked_by_verification, or provider_unavailable."""
    out = output_dir or str(get_settings().output_dir)
    response = await download_product_assets(offer_id_or_url, out, include=include, provider_name=provider, dry_run=dry_run)
    payload = response.model_dump(mode="json")
    if response.manifest:
        payload["counts"] = {
            "main_images": len(response.manifest.main_images),
            "detail_images": len(response.manifest.detail_images),
            "option_images": len(response.manifest.option_images),
            "videos": len(response.manifest.videos),
            "dry_run_assets": len(response.manifest.dry_run_assets),
            "failed_assets": len(response.manifest.failed_assets),
        }
        payload["manifest"] = {
            "offer_id": response.manifest.offer_id,
            "saved_dir": response.manifest.saved_dir,
            "manifest_path": response.manifest_path,
            "status": response.manifest.status,
            "failed_assets": [item.model_dump(mode="json") for item in response.manifest.failed_assets],
        }
    return payload


@mcp.tool()
def parse_1688_rendered_html(html_path: str) -> dict[str, Any]:
    """Parse a local rendered/SingleFile 1688 detail HTML file. Returns ok or partial_data with ProductDetail JSON."""
    try:
        return jsonable(parse_rendered_html_file(html_path))
    except Exception as exc:  # noqa: BLE001
        return error_payload("parse_html_failed", str(exc))


@mcp.tool()
def parse_1688_rendered_html_content(html: str, source_url: str | None = None) -> dict[str, Any]:
    """Parse rendered 1688 detail HTML content captured by a host browser tool."""
    if not html.strip():
        return error_payload("parse_html_failed", "HTML content is empty.")
    try:
        return jsonable(parse_rendered_html(html, source_url=source_url))
    except Exception as exc:  # noqa: BLE001
        return error_payload("parse_html_failed", str(exc))


@mcp.tool()
def parse_1688_network_payload_content(payload_json: str, source_url: str | None = None) -> dict[str, Any]:
    """Parse 1688 JSON/network responses captured from Chrome DevTools and return ProductDetail JSON."""
    if not payload_json.strip():
        return error_payload("parse_network_payload_failed", "Network payload JSON is empty.")
    try:
        return jsonable(parse_network_payload(payload_json, source_url=source_url))
    except Exception as exc:  # noqa: BLE001
        return error_payload("parse_network_payload_failed", str(exc))


@mcp.tool()
async def download_1688_product_assets_from_html_content(
    html: str,
    source_url: str | None = None,
    output_dir: str | None = None,
    include: str | list[str] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Parse rendered 1688 HTML content captured by Chrome and save/download its assets."""
    if not html.strip():
        return error_payload("parse_html_failed", "HTML content is empty.")
    try:
        parsed = parse_rendered_html(html, source_url=source_url)
        if parsed.item is None:
            return parsed.model_dump(mode="json")
        out = output_dir or str(get_settings().output_dir)
        manifest = await download_parsed_assets(
            parsed.item,
            out,
            include=include,
            html=html,
            source_url=source_url or parsed.item.url,
            parser_version=PARSER_VERSION,
            dry_run=dry_run,
        )
        payload = {
            "status": manifest.status,
            "provider": "local_html",
            "provider_version": PARSER_VERSION,
            "source_type": "local_html",
            "live_verified": True,
            "manifest_path": str(Path(manifest.saved_dir) / "manifest.json"),
            "counts": manifest.counts,
            "warnings": parsed.warnings,
            "manifest": {
                "offer_id": manifest.offer_id,
                "saved_dir": manifest.saved_dir,
                "manifest_path": str(Path(manifest.saved_dir) / "manifest.json"),
                "status": manifest.status,
                "failed_assets": [item.model_dump(mode="json") for item in manifest.failed_assets],
            },
        }
        return jsonable(payload)
    except Exception as exc:  # noqa: BLE001
        return error_payload("asset_download_failed", str(exc), status="partial_success")


@mcp.tool()
async def image_search_1688_products(
    image_url: str | None = None,
    image_path: str | None = None,
    top: int = 20,
    provider: str | None = None,
) -> dict[str, Any]:
    """Search 1688 by image. API provider is live-capable; browser support is unavailable."""
    try:
        return jsonable(await image_search_products(image_url=image_url, image_path=image_path, top=top, provider_name=provider))
    except Exception as exc:  # noqa: BLE001
        return error_payload("image_search_failed", str(exc))


@mcp.tool()
def check_1688_provider_capabilities(provider: str | None = None) -> dict[str, Any]:
    """Return provider capability matrix or a single provider capability record."""
    try:
        if provider:
            return check_provider(provider)
        response = get_all_provider_capabilities()
        return {"status": "ok", "providers": {key: value.model_dump(mode="json") for key, value in response.providers.items()}}
    except Exception as exc:  # noqa: BLE001
        return error_payload("provider_check_failed", str(exc))


@mcp.tool()
def provider_check_1688(provider: str | None = None) -> dict[str, Any]:
    """Alias for check_1688_provider_capabilities; useful when tools are searched by provider-check wording."""
    return check_1688_provider_capabilities(provider)


@mcp.tool()
async def check_1688_browser_profile() -> dict[str, Any]:
    """Check whether the configured Playwright browser profile path exists."""
    provider = get_provider("browser")
    if hasattr(provider, "check_profile"):
        return await provider.check_profile()
    return error_payload("provider_unavailable", "Browser provider profile check is unavailable.", status="provider_unavailable")


@mcp.tool()
async def open_1688_browser_profile(url: str = "https://www.1688.com") -> dict[str, Any]:
    """Open the default browser profile so the user can log in to 1688 manually. The call returns after the browser window is closed."""
    try:
        return await open_browser_profile(get_settings().browser_profile or get_settings().home / "browser-profile", url=url)
    except Exception as exc:  # noqa: BLE001
        return error_payload("browser_profile_open_failed", str(exc), status="provider_unavailable")


@mcp.tool()
def open_chrome_devtools_setup(open_1688: bool = True) -> dict[str, Any]:
    """Open Chrome pages needed for first-run DevTools MCP auto-connect setup."""
    setup_url = "chrome://inspect/#remote-debugging"
    product_url = "https://www.1688.com"
    try:
        if sys.platform.startswith("win"):
            subprocess.Popen(["cmd", "/c", "start", "", "chrome", setup_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if open_1688:
                subprocess.Popen(["cmd", "/c", "start", "", "chrome", product_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", "Google Chrome", setup_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if open_1688:
                subprocess.Popen(["open", "-a", "Google Chrome", product_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.Popen(["google-chrome", setup_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if open_1688:
                subprocess.Popen(["google-chrome", product_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as exc:  # noqa: BLE001
        return error_payload(
            "chrome_devtools_setup_failed",
            str(exc),
            status="provider_unavailable",
            suggested_action="Open chrome://inspect/#remote-debugging in Chrome, enable the local debugging connection, then open the 1688 page again.",
        )
    return {
        "status": "ok",
        "opened": [setup_url, product_url] if open_1688 else [setup_url],
        "next_steps": [
            "In Chrome, allow or start the local DevTools debugging connection if prompted.",
            "Open the target 1688 page in the same Chrome profile and log in normally if needed.",
            "If chrome-devtools failed earlier in this Codex session, restart Codex or open a new chat after enabling the Chrome connection.",
        ],
    }


@mcp.tool()
async def get_1688_hot_keywords(
    category_id: str | None = None,
    limit: int = 20,
    provider: str | None = None,
) -> dict[str, Any]:
    """Return hot keywords if provider access is available."""
    selected = get_provider(provider)
    return jsonable(await selected.get_hot_keywords(category_id=category_id, limit=limit))


@mcp.tool()
async def get_1688_rankings(
    category_id: str | None = None,
    rank_type: str = "hot",
    limit: int = 20,
    provider: str | None = None,
) -> dict[str, Any]:
    """Return 1688 ranking data if provider access is available."""
    selected = get_provider(provider)
    return jsonable(await selected.get_rankings(category_id=category_id, rank_type=rank_type, limit=limit))


@mcp.tool()
async def recommend_1688_products(
    keyword: str,
    top: int = 10,
    save: bool = False,
    project: str | None = None,
    provider: str | None = None,
) -> dict[str, Any]:
    """Search and score products for Korean seller sourcing."""
    return jsonable(await recommend_products(keyword, top=top, save=save, project=project, provider_name=provider))


@mcp.tool()
def save_1688_shortlist(project: str, offer_id: str, notes: str | None = None) -> dict[str, Any]:
    """Save an offer id to a local shortlist."""
    storage = SourcingStorage(get_settings().db_path)
    storage.add_to_shortlist(project, offer_id, notes)
    storage.close()
    return {"status": "ok", "project": project, "offer_id": offer_id}


@mcp.tool()
def export_1688_sourcing_report(project: str, format: str = "json") -> dict[str, Any]:
    """Export a shortlist project as JSON, Markdown, or CSV content."""
    storage = SourcingStorage(get_settings().db_path)
    payload = storage.export_project(project, format)
    storage.close()
    return payload


def main() -> None:
    if any(arg in {"--help", "-h"} for arg in sys.argv[1:]):
        print("sourcing1688-mcp: run the sourcing1688 MCP server over stdio.")
        print("Example: uv run sourcing1688-mcp")
        return
    mcp.run()


if __name__ == "__main__":
    main()
