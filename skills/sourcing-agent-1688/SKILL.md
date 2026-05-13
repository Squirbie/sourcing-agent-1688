---
name: sourcing-agent-1688
description: Use this skill when the user asks Codex Desktop to find, analyze, recommend, shortlist, or save assets from 1688 products.
---

# 1688 Sourcing Agent

Use this plugin for 1688 sourcing inside Codex Desktop.

The plugin installs two MCP servers:

- `chrome-devtools`: lets Codex inspect the user's Chrome page, DOM, network responses, screenshots, and JavaScript state.
- `sourcing1688`: turns 1688 page HTML or captured network JSON into sourcing-friendly product data, assets, scores, and reports.

Prefer the user's already-open Chrome tab over managed browser launches. Do not repeatedly open and close Playwright browser windows for the same page.

## Product URL Workflow

When the user gives a 1688 product URL:

1. Use Chrome DevTools tools to find or open the product page in Chrome.
2. Wait for the product content to load.
3. Inspect visible page state and network requests. Useful 1688 signals often appear in responses containing names like `offerDetail`, `offerWarnService`, `mtop.1688`, `getVideoById`, `video`, `trade`, `sku`, or `seller`.
4. Evaluate `document.documentElement.outerHTML` or otherwise capture rendered HTML, then call `parse_1688_rendered_html_content`.
5. For useful JSON responses, pass the response body to `parse_1688_network_payload_content`.
6. Combine the parsed HTML and network result in the final answer. Prefer network values for trade, seller, SKU, and video data when present.
7. If the user asks to save assets, call `download_1688_product_assets_from_html_content` with the rendered HTML and source URL.

Report product title, URL, price tiers, MOQ if present, sales/trade volume, repurchase rate, seller score, SKU/options, main/detail images, video findings, risks, and next checks for a Korean seller.

If video UI is visible but the captured payload has `videoId=0`, empty `videoUrl`, or no `mp4`/`m3u8`, say that the page shows video metadata but the downloadable video URL was not exposed in the captured data. Keep looking at network responses before concluding that no video exists.

## Keyword Sourcing Workflow

When the user asks to find products from a Korean keyword:

1. Call `provider_check_1688` and `expand_sourcing_keywords`.
2. If API credentials are ready, use `search_1688_products` or `recommend_1688_products`.
3. If API credentials are not ready, use Chrome DevTools to open 1688 search/ranking pages in the user's Chrome session, then parse visible cards and captured network payloads.
4. Do not fabricate candidates. If Chrome/API access is not ready, explain the one setup step needed.

Always show which source was used: API, Chrome visible page/network, or local HTML.

## Asset Saving Workflow

For images, detail HTML, attributes, and videos:

1. Capture rendered HTML from Chrome DevTools.
2. Call `download_1688_product_assets_from_html_content`.
3. If network JSON contains video addresses, also call `parse_1688_network_payload_content` and include those video URLs in the analysis.
4. Return the manifest path, saved directory, counts, failed assets, and video status.

## Provider Notes

- `api`: use when 1688 Open Platform credentials are configured.
- `chrome-devtools`: primary non-API path for what the user can actually see in Chrome.
- `browser`: managed Playwright browser profile; use only when the user explicitly asks for that profile.
- `local_html`: saved or copied page HTML.

Keep the final answer practical for a seller: what looks promising, what is missing, what to verify before buying samples, and what data came from the page.
