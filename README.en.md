# 1688 Sourcing Agent

An MCP plugin and CLI tool that helps Codex, Claude Code, and OpenClaw find 1688 products, analyze listings, save product page assets, and export sourcing shortlists.

- GitHub repo: `https://github.com/Squirbie/sourcing-agent-1688`
- Plugin id: `sourcing-agent-1688`
- CLI: `sourcing1688`, `sourcing-agent-1688`
- MCP CLI: `sourcing1688-mcp`

## Example Prompts

```text
Find blackout umbrellas on 1688.
```

```text
Analyze this 1688 listing:
https://detail.1688.com/offer/123456789.html
```

```text
Save this product page's images, video, HTML, and attributes.
```

```text
Recommend promising candidates and save them to a shortlist.
```

## Features

- Expand Korean keywords into Chinese sourcing search terms
- Search 1688 product candidates
- Analyze product detail pages
- Save images, video URLs, HTML, and attributes JSON
- Score candidates for Korean seller sourcing
- Save shortlists and export reports
- Use the workflow through MCP tools in Codex, Claude Code, and OpenClaw

## Install: Codex

```powershell
codex plugin marketplace add https://github.com/Squirbie/sourcing-agent-1688.git
```

Then:

1. Open `/plugins` in Codex
2. Install `1688 Sourcing Agent`
3. Start a new session and check `/mcp`
4. Check provider readiness

```powershell
sourcing1688 provider-check --provider auto --json
```

## Short Agent Install Prompts

Codex:

```text
Install https://github.com/Squirbie/sourcing-agent-1688 as a Codex plugin, verify the MCP tools, run provider-check auto, and use mock only for demo.
```

Claude Code:

```text
Install https://github.com/Squirbie/sourcing-agent-1688 as a Claude Code plugin, reload plugins, verify MCP tools, run provider-check auto, and confirm mock is demo sample data.
```

OpenClaw:

```text
Install https://github.com/Squirbie/sourcing-agent-1688 as an OpenClaw plugin/bundle, inspect mapped skills and MCP tools, run provider-check auto, and use mock only for demo.
```

## Usage Examples

Ask your agent:

```text
Check 1688 Sourcing Agent provider readiness.
```

```text
Use the mock provider to recommend 5 sourcing candidates for "암막우산".
```

```text
Search "黑胶伞" with the auto provider. If live providers are not ready, tell me what setup is needed.
```

```text
Analyze this 1688 product URL: https://detail.1688.com/offer/123456789.html
```

CLI examples:

```powershell
sourcing1688 provider-check --provider auto --json
sourcing1688 search "암막우산" --top 5 --provider mock --json
sourcing1688 recommend "암막우산" --top 5 --provider mock --json
sourcing1688 parse-html path/to/1688-detail.html --json
sourcing1688 download-assets-from-html path/to/1688-detail.html --dry-run --json
```

## Providers

| provider | Use | Requires |
|---|---|---|
| `auto` | Default for real use | `api` or `browser` setup |
| `api` | 1688 Open Platform API | AppKey, AppSecret, token |
| `browser` | Use a logged-in browser profile | 1688 profile you logged into |
| `local_html` | Analyze saved detail page HTML | HTML file |
| `mock` | Install checks and demos | Nothing |

Mock is sample data for demos and tests. For live 1688 data, configure `api`, `browser`, or use `local_html`.

## Do I Need 1688 API Access?

- Not for installation or mock demos.
- API mode is the best option for stable live 1688 searches.
- API credentials come from `open.1688.com / 1688开放平台`.
- Create an app, get AppKey/AppSecret, apply for required API permissions if needed, and prepare an OAuth access token or refresh token.
- Without API credentials, you can use a browser profile or local HTML workflow.

Check the official 1688 Open Platform docs for current setup details.

## Browser Profile

Use a browser profile you log into manually:

```powershell
sourcing1688 browser-profile open --json
sourcing1688 provider-check --provider browser --json
```

## Local HTML

Analyze a saved 1688 detail page without live browsing:

```powershell
sourcing1688 parse-html product.html --json
sourcing1688 download-assets-from-html product.html --dry-run --json
```

## Storage

Runtime data is stored under `SOURCING1688_HOME`:

```text
~/.sourcing1688/
  assets/
  data/
  raw/
  browser-profile/
  token-cache/
```

## Uninstall

```powershell
sourcing1688 uninstall --yes
```

Remove the plugin from your Codex, Claude Code, or OpenClaw plugin screen or command.

## More

- Codex details: [docs/CODEX.md](docs/CODEX.md)
- Claude Code details: [docs/CLAUDE_CODE.md](docs/CLAUDE_CODE.md)
- OpenClaw details: [docs/OPENCLAW.md](docs/OPENCLAW.md)
- 1688 API setup summary: [docs/API_CREDENTIALS.md](docs/API_CREDENTIALS.md)
- Distribution notes: [docs/PLUGIN_DISTRIBUTION.md](docs/PLUGIN_DISTRIBUTION.md)
- Open-source references: [docs/references.md](docs/references.md)
