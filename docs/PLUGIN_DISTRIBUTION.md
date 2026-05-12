# 플러그인 배포 메모

제품 이름은 `1688 Sourcing Agent`이고, repo는 아래 주소를 기준으로 합니다.

```text
https://github.com/Squirbie/sourcing-agent-1688
```

## Codex

Codex용 파일:

- `.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`
- `.mcp.codex.json`
- `skills/`

설치:

```powershell
codex plugin marketplace add https://github.com/Squirbie/sourcing-agent-1688.git
```

설치 후 `/plugins`에서 `1688 Sourcing Agent`를 설치하고 `/mcp`에서 도구가 보이는지 확인합니다.

## Claude Code

Claude Code용 파일:

- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.mcp.json`

설치 예시:

```powershell
claude plugin marketplace add Squirbie/sourcing-agent-1688
claude plugin install sourcing-agent-1688@sourcing-agent-1688-marketplace
```

## OpenClaw

OpenClaw는 Codex/Claude bundle marker와 stdio MCP 구성을 읽는 방식으로 사용할 수 있습니다. 환경마다 명령 이름이 다를 수 있으니 설치 전 `openclaw plugins --help`를 확인하세요.

```powershell
openclaw plugins install https://github.com/Squirbie/sourcing-agent-1688.git
openclaw plugins inspect sourcing-agent-1688
```

## MCP 파일 차이

- Codex: `.mcp.codex.json` (`mcp_servers`)
- Claude Code / OpenClaw 호환: `.mcp.json` (`mcpServers`)

Codex marketplace entry는 repo root가 plugin root라서 `path: "./"`를 사용합니다.

## 로컬 검증

```powershell
uv sync --extra dev
uv run pytest -q -ra
uvx --from . sourcing-agent-1688 --help
uvx --from . sourcing1688-mcp --help
```

## 삭제

```powershell
codex plugin marketplace remove sourcing-agent-1688-marketplace
claude plugin uninstall sourcing-agent-1688 --prune
sourcing1688 uninstall --yes
```
