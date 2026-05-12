# 1688 Sourcing Agent AGENTS.md

This repo is an agent-friendly CLI plus MCP server project for targeted 1688 sourcing research.

## Core Rules

- Preserve JSON-first output. CLI commands with `--json` must emit valid JSON on success and expected failure.
- Keep fixture/mock tests passing without live 1688 access.
- Default pytest must not perform external network downloads. Use `--dry-run`, mocked transports, or fixture-only parsers in tests.
- Never implement CAPTCHA bypass, verification bypass, stealth bypass, anti-bot evasion, proxy rotation, or aggressive crawling.
- Never commit secrets, cookies, tokens, personal data, or browser profile contents.
- Do not break the provider contract in `Base1688Provider`.
- Keep selector changes concentrated in `src/sourcing1688/providers/selectors.py`.
- Do not modify provider/parser behavior without adding or updating tests.
- Return structured states for blocked access: `needs_human_login`, `blocked_by_verification`, `provider_unavailable`, `missing_credentials`, or `partial_data`.

## Provider Scope

- Mock provider is implemented and is the only provider expected to pass complete fixture-based workflows.
- Auto provider is for real-use resolution only: API credentials first, browser profile second, never silent mock fallback.
- API provider includes live-capable endpoint calls, token cache support, and response normalizers, but must be marked `live_verified=false` until tested with real 1688 credentials and API permissions.
- Browser provider includes Playwright persistent-profile navigation, login/verification detection, raw snapshots, and DOM/rendered HTML parsers, but must be marked `live_verified=false` until tested with a logged-in profile.
- Local HTML provider parses rendered/SingleFile detail HTML without live network access.
- Current mock `hot-keywords` and `rankings` results are fixture data. API ranking/hot keyword is live-capable but not live verified.

## Development Notes

- Prefer Pydantic models for all tool outputs.
- Keep API and browser providers conservative when live behavior is uncertain.
- Mock provider is for development and automated tests; real Codex/MCP configs should prefer `auto`, `api`, `browser`, or `local_html`.
- Asset download failures should be recorded in `failed_assets` and should not kill the whole batch.
- Asset preflight and fixture tests should use `dry_run=true` so `dry_run_assets` are recorded without external requests.
- Use `uv run pytest` and at least one CLI JSON smoke command before claiming completion.
- Add or update parser fixtures before changing browser/local HTML parser behavior.
- Store raw snapshots without cookies, tokens, or browser profile data.
- Claims about live 1688 behavior must follow `live_verified`; do not infer live success from mock tests.
