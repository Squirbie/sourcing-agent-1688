# 1688 Sourcing Agent

Agent-friendly JSON-first CLI, MCP server, and Codex/Claude/OpenClaw-compatible plugin bundle for Korean sellers doing targeted 1688 sourcing research.

- GitHub repo: `https://github.com/Squirbie/sourcing-agent-1688`
- Plugin id: `sourcing-agent-1688`
- Python package/import: `sourcing1688`
- CLI: `sourcing1688`, `sourcing-agent-1688`
- MCP CLI: `sourcing1688-mcp`

## What This Is

`1688 Sourcing Agent` helps agents run small sourcing workflows:

- expand Korean keywords into Chinese sourcing terms
- search, analyze, score, recommend, and shortlist product candidates
- parse rendered or SingleFile-style 1688 detail HTML
- create asset manifests and dry-run download plans
- expose the workflow as CLI commands and MCP tools

## What This Is Not

This is not a mass scraper. It does not bypass CAPTCHA, verification, login, anti-bot controls, robots, account boundaries, or 1688 terms. It does not implement stealth automation, proxy rotation, automatic login, cookie extraction, or credential logging.

Mock data is demo/test fixture data, not live 1688 data.

## Requirements

- Python 3.11+
- `uv`
- Codex, Claude Code, or OpenClaw
- For live use, either 1688 API credentials or a manually logged-in browser profile

## Quick Check

```powershell
uv sync --extra dev
uv run pytest -q -ra
uv run sourcing1688 provider-check --provider auto --json
uv run sourcing1688 search "암막우산" --top 2 --provider mock --json
```

## Codex Install

```powershell
codex plugin marketplace add https://github.com/Squirbie/sourcing-agent-1688.git
```

Open `/plugins`, install `sourcing-agent-1688`, then verify:

```powershell
uvx --from git+https://github.com/Squirbie/sourcing-agent-1688.git sourcing1688 provider-check --provider auto --json
```

Codex uses `.mcp.codex.json`.

## Claude Code Install

Claude Code plugins use `.claude-plugin/plugin.json` and root `.mcp.json`.

```powershell
claude plugin marketplace add Squirbie/sourcing-agent-1688
claude plugin install sourcing-agent-1688@sourcing-agent-1688-marketplace
```

For local testing:

```powershell
claude --plugin-dir .
```

Use `/mcp` or `claude plugin details sourcing-agent-1688` to verify the MCP server.

## OpenClaw Install

OpenClaw can detect Codex and Claude bundle markers and load supported stdio MCP tools from bundles. This repo only provides bundle compatibility and docs; it does not add OpenClaw-specific runtime code.

```powershell
openclaw plugins install https://github.com/Squirbie/sourcing-agent-1688.git
openclaw plugins inspect sourcing-agent-1688
```

Check `openclaw plugins --help` for the exact command supported by your OpenClaw version.

## Short Agent Install Prompts

Codex:

> Install https://github.com/Squirbie/sourcing-agent-1688 as a Codex plugin, verify the MCP tools, run provider-check auto, and use mock only for demo.

Claude Code:

> Install https://github.com/Squirbie/sourcing-agent-1688 as a Claude Code plugin, reload plugins, verify MCP tools, run provider-check auto, and do not treat mock results as live 1688 data.

OpenClaw:

> Install https://github.com/Squirbie/sourcing-agent-1688 as an OpenClaw plugin/bundle, inspect mapped skills and MCP tools, run provider-check auto, and use mock only for demo.

## Providers

| Provider | Use | Notes |
|---|---|---|
| `auto` | Real-use default. API first, browser profile second. | Never silently falls back to mock. |
| `api` | 1688 Open Platform API-style provider. | Requires AppKey/AppSecret/token. |
| `browser` | Playwright persistent profile. | Manual login/verification only. |
| `local_html` | Saved rendered/SingleFile HTML parsing. | No live search. |
| `mock` | Fixture-backed tests and demos. | Not live data. |

Always start with:

```powershell
sourcing1688 provider-check --provider auto --json
```

## 1688 API Credentials

1688 API credentials are issued through `open.1688.com / 1688开放平台`. Create an app, obtain AppKey/AppSecret, apply for required API permissions or solutions if needed, and prepare an OAuth access token or refresh token. Check the official 1688 Open Platform docs for current steps.

Without API credentials, use a browser profile or local HTML workflow when appropriate.

## Browser Profile

```powershell
sourcing1688 init-home --json
sourcing1688 browser-profile open --json
sourcing1688 browser-profile check --json
```

Log in and complete verification manually. No CAPTCHA or verification bypass is implemented.

## Local HTML

```powershell
sourcing1688 parse-html path/to/detail.html --json
sourcing1688 download-assets-from-html path/to/detail.html --dry-run --json
```

## CLI Examples

```powershell
sourcing1688 expand-keywords "암막우산" --json
sourcing1688 search "암막우산" --top 5 --provider mock --json
sourcing1688 recommend "암막우산" --top 5 --provider mock --json
sourcing-agent-1688 provider-check --provider auto --json
sourcing1688-mcp --help
```

## MCP Tools

The MCP server exposes keyword expansion, product search/detail/recommendation, asset download, rendered HTML parsing, image search, provider checks, hot keywords/rankings, shortlist save, and report export.

## Uninstall

```powershell
codex plugin marketplace remove sourcing-agent-1688-marketplace
claude plugin uninstall sourcing-agent-1688 --prune
sourcing1688 uninstall --yes
```

## Troubleshooting

- `missing_credentials`: API credentials or token cache missing
- `needs_human_login`: open the browser profile and log in manually
- `blocked_by_verification`: complete verification manually
- `live_not_verified`: provider exists but no live smoke has verified it
- `missing_live_provider`: `auto` found no API or browser provider

## Security / Privacy / Terms

Never share or commit AppKey, AppSecret, access tokens, refresh tokens, cookies, or browser profiles. Do not bypass 1688 terms, robots, account boundaries, login, or verification.

## References / Credits

See [docs/references.md](docs/references.md), [docs/API_CREDENTIALS.md](docs/API_CREDENTIALS.md), and [docs/PLUGIN_DISTRIBUTION.md](docs/PLUGIN_DISTRIBUTION.md).
