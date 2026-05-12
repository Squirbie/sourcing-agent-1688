# Claude Code

Claude Code plugins use a `.claude-plugin/plugin.json` manifest and can bundle MCP servers through a root `.mcp.json` file.

Install:

```powershell
claude plugin marketplace add Squirbie/sourcing-agent-1688
claude plugin install sourcing-agent-1688@sourcing-agent-1688-marketplace
```

Local test:

```powershell
claude --plugin-dir .
```

Verify:

```powershell
claude plugin details sourcing-agent-1688
```

Then run:

```powershell
sourcing1688 provider-check --provider auto --json
```

The bundled `.mcp.json` uses `mcpServers`, which is the Claude Code MCP config shape. Do not treat `mock` provider results as live 1688 data.

References:

- https://code.claude.com/docs/en/plugins
- https://code.claude.com/docs/en/plugins-reference
- https://code.claude.com/docs/en/plugin-marketplaces
