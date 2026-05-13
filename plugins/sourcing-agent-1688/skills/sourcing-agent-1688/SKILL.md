---
name: sourcing-agent-1688
description: Use this skill when the user asks Codex Desktop to find, analyze, recommend, shortlist, or save assets from 1688 products.
---

# 1688 Sourcing Agent

Use this plugin for 1688 product sourcing inside Codex Desktop.

## Provider

Use `auto` by default.

- `api`: use when 1688 Open Platform credentials are configured.
- `browser`: use when the user needs to work through a logged-in browser profile.
- `local_html`: use when the user provides a saved 1688 detail HTML file.

If the host Chrome plugin is available, prefer the user's existing Chrome session for live browsing. If the MCP returns `needs_human_login` or `blocked_by_verification`, tell the user to complete that step in the browser and retry.

## Search Workflow

1. Call `check_1688_provider_capabilities`.
2. Expand Korean keywords with `expand_sourcing_keywords`.
3. Search with `search_1688_products`.
4. Score with `recommend_1688_products`.
5. Show title, URL, image URL, price, MOQ, sales/trade volume, repurchase rate, seller score, risks, missing fields, provider, and `live_verified`.

Do not describe `live_verified=false` results as verified live data.

## URL Analysis

For a 1688 detail URL, call `analyze_1688_product_url` or `get_1688_product_detail`. If the user asks to save page assets, call `download_1688_product_assets` and return `saved_dir`, `manifest_path`, counts, and failures.

## Local HTML

For a saved HTML file, call `parse_1688_rendered_html`. For asset saving from that HTML, use `download_1688_product_assets` or the CLI helper if needed.
