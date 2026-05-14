---
name: sourcing-agent-1688
description: Use this skill when the user asks Codex Desktop to inspect, analyze, compare, or save data from 1688 product pages.
---

# 1688 Sourcing Agent

Use this plugin as a Chrome DevTools-first 1688 sourcing agent.

Primary path:

1. Use `chrome-devtools` to inspect the user's Chrome tab.
2. Read visible page state, DOM, screenshots, and network responses.
3. Use `sourcing1688` tools to normalize 1688 HTML and network JSON into seller-facing product data.

Use Chrome DevTools first. Do not open a separate window unless the user explicitly asks.
Do not run synthetic fixture, demo, or parser self-tests during a user sourcing task.

## First-Run Chrome Setup

If Chrome DevTools cannot connect, has no pages, or reports `DevToolsActivePort`:

1. Call `open_chrome_devtools_setup`.
2. Tell the user that the Chrome setup tab was opened.
3. Ask the user to allow the Chrome DevTools connection in the opened Chrome settings page.
4. Ask the user to open the target 1688 page in that same Chrome profile.
5. Stop there until the user confirms setup is done or provides the target page.

## Product Page

When the user gives a 1688 product URL or asks about the current Chrome page:

1. Use `list_pages` and select the 1688 page.
2. If needed, navigate Chrome to the provided URL.
3. Use `take_snapshot`, `take_screenshot`, and `evaluate_script` to inspect the visible page.
4. Capture rendered HTML and call `parse_1688_rendered_html_content`.
5. Use `list_network_requests` and `get_network_request` for relevant 1688 responses.
6. Pass useful JSON bodies to `parse_1688_network_payload_content`.
7. Summarize product fit for a Korean seller: product type, price, options, seller signals, visible demand signals, image/video assets, risks, and next buying checks.

## Search

When the user asks for sourcing candidates:

1. Call `expand_sourcing_keywords`.
2. Use Chrome DevTools to search 1688 with the Chinese keywords. For `s.1688.com` search URLs, GBK-percent-encode Chinese keywords; UTF-8 encoded Chinese keywords can render as broken text and return unrelated results.
3. Inspect visible results and network responses.
4. Compare candidates using price, MOQ if visible, seller signals, assets, and page quality.

## Save Assets

When the user asks to save images or page data:

1. Capture rendered HTML from Chrome.
2. Call `download_1688_product_assets_from_html_content`.
3. Return saved directory, manifest path, counts, and failures.
