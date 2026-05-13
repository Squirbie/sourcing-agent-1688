---
name: sourcing-agent-1688
description: Use this skill when the user asks Codex Desktop to find, analyze, recommend, shortlist, or save assets from 1688 products.
---

# 1688 Sourcing Agent

Use this plugin for 1688 product sourcing inside Codex Desktop.

## Provider

Use `auto` only for API-backed live access. If API credentials are missing, do not call tools that would open the managed browser automatically.

- `api`: use when 1688 Open Platform credentials are configured.
- `browser`: use when the user needs to work through a logged-in browser profile.
- `local_html`: use when the user provides a saved 1688 detail HTML file.

The MCP browser provider cannot directly control the user's already-open Chrome session. If a host Chrome plugin can capture the current page HTML, use that Chrome session first, then call `parse_1688_rendered_html_content` with the captured HTML and source URL. Use the MCP browser provider only when the user explicitly asks for the managed browser profile.

Avoid repeated live browser calls for the same URL. For a product URL without API credentials, prefer Chrome-captured HTML over `analyze_1688_product_url`.

## Search Workflow

1. Call `provider_check_1688` or `check_1688_provider_capabilities`.
2. Expand Korean keywords with `expand_sourcing_keywords`.
3. If `auto` is `provider_unavailable`, do not retry with `browser` unless the user explicitly asks for the managed browser. Ask for API credentials, a saved 1688 HTML file, or Chrome-captured HTML.
4. Search with `search_1688_products` only when API access is ready.
5. Score with `recommend_1688_products`.
6. Show title, URL, image URL, price, MOQ, sales/trade volume, repurchase rate, seller score, risks, missing fields, provider, and `live_verified`.

Do not describe `live_verified=false` results as verified live data.

## URL Analysis

For a 1688 detail URL:

- If API credentials are ready, call `analyze_1688_product_url`.
- If API credentials are missing and Chrome can capture the rendered page HTML, open/use the user's Chrome page, then call `parse_1688_rendered_html_content`.
- If the user asks to save page assets from captured HTML, call `download_1688_product_assets_from_html_content`.
- If only a saved HTML file is available, call `parse_1688_rendered_html` or use `download_1688_product_assets` with `provider=local_html` and the HTML path.

When video metadata exists but no video URL is exposed, report that the public HTML did not expose the video URL and that a logged-in rendered page or captured network response may be needed.

## Local HTML

For a saved HTML file, call `parse_1688_rendered_html`. For HTML captured from Chrome, call `parse_1688_rendered_html_content`. For asset saving from captured HTML, call `download_1688_product_assets_from_html_content`.
