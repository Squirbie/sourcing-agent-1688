# Plugin Distribution

Product name: `1688 Sourcing Agent`

Repository:

```text
https://github.com/Squirbie/sourcing-agent-1688
```

## Codex

Codex uses `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `skills/`, and `.mcp.codex.json`.

The Codex marketplace entry uses a local root plugin source with `path: "./"` because this repository root is the plugin root.

```powershell
codex plugin marketplace add https://github.com/Squirbie/sourcing-agent-1688.git
```

Then open `/plugins`, install `sourcing-agent-1688`, and run:

```powershell
sourcing1688 provider-check --provider auto --json
```

## Claude Code

Claude Code uses `.claude-plugin/plugin.json` and root `.mcp.json`. The marketplace file is `.claude-plugin/marketplace.json`.

```powershell
claude plugin marketplace add Squirbie/sourcing-agent-1688
claude plugin install sourcing-agent-1688@sourcing-agent-1688-marketplace
```

For local validation:

```powershell
claude --plugin-dir .
claude plugin details sourcing-agent-1688
```

## OpenClaw

OpenClaw can detect Codex and Claude bundle markers and load supported stdio MCP tools from bundles. This repo does not ship OpenClaw-native runtime code.

```powershell
openclaw plugins install https://github.com/Squirbie/sourcing-agent-1688.git
openclaw plugins inspect sourcing-agent-1688
```

Confirm exact commands with `openclaw plugins --help` in your installed version.

## MCP Config Files

- Codex: `.mcp.codex.json` with `mcp_servers`
- Claude Code/OpenClaw-compatible: `.mcp.json` with `mcpServers`

## Local Verification

```powershell
uv sync --extra dev
uv run pytest -q -ra
uvx --from . sourcing-agent-1688 --help
uvx --from . sourcing1688-mcp --help
```

## Uninstall

```powershell
codex plugin marketplace remove sourcing-agent-1688-marketplace
claude plugin uninstall sourcing-agent-1688 --prune
sourcing1688 uninstall --yes
```

`sourcing1688 uninstall` deletes local runtime state under `SOURCING1688_HOME`. Use `--keep-browser-profile` or `--keep-token-cache` when needed.

## Notes

Official plugin directory/self-publishing programs can change. The stable release path for this repo is GitHub-hosted marketplace/bundle installation.
