# Codex

Install:

```powershell
codex plugin marketplace add https://github.com/Squirbie/sourcing-agent-1688.git
```

Then open `/plugins`, choose `1688 Sourcing Agent`, click `Add to Codex`, open a new chat, and check MCP tools.

If the plugin does not appear in the Codex app, restart the app completely and check `/plugins` again. Private repositories can behave differently between the CLI and Desktop app. For a quick tool-level check, add the MCP server directly:

```toml
[mcp_servers.sourcing1688]
command = "uv"
args = ["run", "sourcing1688-mcp"]
cwd = "C:/path/to/sourcing-agent-1688"
startup_timeout_sec = 60
tool_timeout_sec = 120

[mcp_servers.sourcing1688.env]
SOURCING1688_PROVIDER = "auto"
SOURCING1688_HOME = "~/.sourcing1688"
```

```powershell
sourcing1688 provider-check --provider auto --json
```

Codex uses:

- `plugins/sourcing-agent-1688/.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`
- `plugins/sourcing-agent-1688/.mcp.json` with `mcpServers`
- `plugins/sourcing-agent-1688/skills/`

The root `.codex-plugin`, `.mcp.codex.json`, and `skills/` folders remain for local/dev compatibility.

Use `mock` only for demo/test prompts.
