---
name: sourcing-agent-1688
description: Use this skill when the user asks Codex Desktop to find, analyze, recommend, shortlist, or save assets from 1688 products.
---

# 1688 Sourcing Agent

Use this plugin for 1688 sourcing inside Codex Desktop.

The normal path is Chrome-first:

- `chrome-devtools` reads the user's Chrome tab, DOM, screenshots, and network responses.
- `sourcing1688` turns captured 1688 HTML/network JSON into product, seller, option, image, video, score, and asset manifest data.

Do not start by telling the user to set API credentials. Use the visible Chrome page and captured network data first.

## First-Run Chrome Setup

If Chrome DevTools reports `DevToolsActivePort`, cannot connect, or has no pages:

1. Call `open_chrome_devtools_setup`.
2. Tell the user to allow/start the Chrome DevTools connection on the opened Chrome setup page.
3. Have the user open or keep the 1688 page in that Chrome profile.
4. Continue with Chrome DevTools page/network tools. If the MCP server failed before setup, use a new chat after Chrome is ready.

## Product URL Workflow

When the user gives a 1688 product URL:

1. Use Chrome DevTools `list_pages`; if the product page is already open, select it.
2. If it is not open, use Chrome DevTools to open the URL.
3. Wait for the page to load and inspect visible page state.
4. Capture rendered HTML and call `parse_1688_rendered_html_content`.
5. Inspect network responses. Useful names include `mtop.1688`, `offerDetail`, `offerWarnService`, `getVideoById`, `trade`, `sku`, `seller`, and `video`.
6. Pass useful JSON response bodies to `parse_1688_network_payload_content`.
7. Combine HTML and network results. Prefer network values for trade, seller, SKU, and video when present.
8. If the user asks to save assets, call `download_1688_product_assets_from_html_content`.

Report the result like a Korean seller would need it: price tiers, MOQ if present, sales/trade volume, seller score, repurchase rate, options, image/video status, risks, and what to check before ordering a sample.

If a video button is visible but captured data has no `mp4`/`m3u8`, keep checking network responses before concluding there is no video.

## Keyword Sourcing Workflow

When the user asks for products from a Korean keyword:

1. Call `expand_sourcing_keywords`.
2. Use Chrome DevTools to open 1688 search pages with the Chinese keywords.
3. Parse visible product cards and captured network payloads.
4. Score candidates with the available product data.
5. Do not invent products. If Chrome DevTools is not connected, call `open_chrome_devtools_setup` first.

## Asset Saving Workflow

1. Capture rendered HTML from Chrome DevTools.
2. Capture relevant network JSON if available.
3. Call `download_1688_product_assets_from_html_content`.
4. Return manifest path, saved directory, counts, failed assets, and video status.

Keep the final answer practical and source-aware: say whether data came from Chrome visible page, Chrome network, or saved HTML.
