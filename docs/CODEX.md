# Codex

Install:

```powershell
codex plugin marketplace add https://github.com/Squirbie/sourcing-agent-1688.git
```

Then open `/plugins`, install `sourcing-agent-1688`, and check MCP tools.

```powershell
sourcing1688 provider-check --provider auto --json
```

Codex uses:

- `.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`
- `.mcp.codex.json`
- `skills/`

Use `mock` only for demo/test prompts.
