# Live Workflows

## Korean Keyword Sourcing

1. Call `check_1688_provider_capabilities`.
2. If Korean input, call `expand_sourcing_keywords`.
3. Prefer API provider when credentials are configured.
4. Otherwise use browser provider only when a human-managed profile exists.
5. If neither live provider is ready, return the structured provider status and guide browser profile or API setup.
6. Score candidates and show `live_verified`, `source_provider`, `missing_fields`, and risks.

## URL Analysis

1. Extract `offer_id`.
2. Prefer browser detail when a browser profile is ready.
3. Use `parse_1688_rendered_html` for local SingleFile/rendered HTML.
4. Use API detail when credentials are available.
5. Return `partial_data` when images/SKU/seller fields are incomplete.

## Asset Download

1. Get detail via API/browser/local_html.
2. Call `download_1688_product_assets` or `download-assets-from-html`.
3. Return `saved_dir`, `manifest_path`, counts, and failed assets.
4. Do not hide failed downloads.

## Hot Keyword and Ranking

1. Prefer API provider.
2. Browser ranking currently returns `live_not_verified` unless a reachable ranking/XHR workflow is confirmed.
3. If ranking or hot keyword access is unavailable, return the provider status clearly.

## Verification/Login Failure

Return `needs_human_login` or `blocked_by_verification` with `needs_human_action=true`. Never bypass CAPTCHA, verification, anti-bot checks, or login controls.
