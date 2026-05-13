---
name: sourcing-agent-1688
description: Use this skill when the user asks to find, analyze, compare, recommend, shortlist, or download assets from 1688 products for Korean seller sourcing workflows.
---

# 1688 Sourcing Agent Skill

Use this skill when the user asks to find, analyze, compare, recommend, shortlist, or download assets from 1688 products.

## Provider Selection

Read `references/provider-capabilities.md` when choosing a provider. For real 1688 requests, use `auto` unless the user selected `api`, `browser`, or `local_html`.

1. Call `check_1688_provider_capabilities` for `auto` or the selected provider.
2. Prefer `api` when credentials are present.
3. If API credentials are missing and a host Chrome/Browser tool is available, prefer the user's existing browser session.
4. If no host browser tool is available, use `browser`.
5. If the browser profile is missing, call or suggest `open_1688_browser_profile` so the user can log in manually, then retry.
6. Use `local_html` when the user provides a rendered/SingleFile HTML file.
7. Return the structured provider status when setup or verification is required.

If a result has `live_verified=false`, do not describe it as a verified live 1688 result.

If API setup is required, guide the user to `sourcing1688 auth status`, `sourcing1688 auth url`, `sourcing1688 auth exchange`, and `docs/API_CREDENTIALS.md`. If browser setup is required inside Codex and a Chrome/Browser plugin is available, use that first. Otherwise use `open_1688_browser_profile` when available or guide the user to `sourcing1688 browser-profile open --json` so they can log in manually.

Downloads should save under `SOURCING1688_HOME/assets` unless the user explicitly chooses another output directory. Results must always show `provider` and `live_verified`.

For fields and scoring meaning, read `references/1688-fields.md`. For live procedures, read `references/live-workflows.md`.

## Workflow: Korean keyword sourcing

When the user gives a Korean product keyword:

1. Call `check_1688_provider_capabilities` with `provider="auto"` or the selected live provider.
2. If API is missing and browser setup is needed, open or guide the browser profile login flow.
3. Call `expand_sourcing_keywords`.
4. Search each Chinese keyword with `search_1688_products`.
5. Deduplicate by `offer_id`.
6. Call `recommend_1688_products` or score candidates.
7. Present top candidates with:
   - title
   - price
   - MOQ
   - monthly sales or trade volume
   - repurchase rate
   - seller score
   - badges
   - why_good
   - risks
   - missing_fields
   - next_action
   - source_provider
   - live_verified

Do not claim a product is good if key fields are missing. Say what is missing.

## Workflow: Analyze 1688 URL

When the user gives a 1688 detail URL:

1. Extract `offer_id`.
2. Use API or browser detail if available.
3. Use `parse_1688_rendered_html` if the input is local HTML.
4. Summarize sourcing suitability with `live_verified`.
5. If the user asks for images/detail page, call `download_1688_product_assets`.

## Workflow: Download product assets

When the user asks to save images, videos, detail page, HTML, or assets:

1. Call `download_1688_product_assets`. Use `dry_run=true` when the user wants to preview what would be saved before downloading files.
2. Return `saved_dir`, `manifest_path`, counts, and `failed_assets`.
3. When `dry_run_assets` are present, say downloads were planned but not fetched.
4. Do not hide failed downloads.

## Workflow: Hot keywords and recommendations

When the user asks what is popular on 1688:

1. Call `get_1688_hot_keywords`.
2. For promising keywords, call `search_1688_products`.
3. Score candidates.
4. Recommend only products with enough data.
5. If ranking data is unavailable or `live_not_verified`, say so clearly.

## Safety

Never bypass CAPTCHA, verification, or login checks.
If the tool returns `needs_human_login` or `blocked_by_verification`, tell the user plainly.
Prefer small, targeted searches.
Do not run aggressive scraping.
