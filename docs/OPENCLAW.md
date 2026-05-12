# OpenClaw

OpenClaw can inspect compatible plugin bundles. This repo provides Codex and Claude bundle markers plus a stdio MCP server; it does not add OpenClaw-native runtime code.

Try:

```powershell
openclaw plugins install https://github.com/Squirbie/sourcing-agent-1688.git
openclaw plugins inspect sourcing-agent-1688
```

Then check provider readiness:

```powershell
sourcing1688 provider-check --provider auto --json
```

OpenClaw may register MCP tools with provider-safe names such as `serverName__toolName`. Exact install commands can vary by OpenClaw version, so confirm with:

```powershell
openclaw plugins --help
```

Reference:

- https://docs.openclaw.ai/plugins/bundles
