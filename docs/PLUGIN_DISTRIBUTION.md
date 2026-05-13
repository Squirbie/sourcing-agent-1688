# 플러그인 배포 메모

제품 이름은 `1688 Sourcing Agent`이고, repo는 아래 주소를 기준으로 합니다.

```text
https://github.com/Squirbie/sourcing-agent-1688
```

## Codex

Codex용 파일:

- `plugins/sourcing-agent-1688/.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`
- `plugins/sourcing-agent-1688/.mcp.codex.json`
- `plugins/sourcing-agent-1688/skills/`

repo root의 `.codex-plugin`, `.mcp.codex.json`, `skills/`는 local/dev 호환용으로 유지합니다. Codex marketplace entry는 앱 UI가 plugin root를 더 명확히 찾도록 `path: "./plugins/sourcing-agent-1688"`를 사용합니다.

설치:

```powershell
codex plugin marketplace add https://github.com/Squirbie/sourcing-agent-1688.git
```

이 marketplace는 `1688 Sourcing Agent`를 기본 설치 대상으로 표시합니다. 앱 버전에 따라 자동으로 추가되거나, `/plugins`에서 설치 완료 상태로 보입니다.

앱에 보이지 않거나 여전히 `+`가 보이면 Codex 앱을 완전히 재시작한 뒤 marketplace를 remove/add로 다시 받아오세요. private repo는 앱 UI가 Git credential을 CLI와 다르게 다룰 수 있으니, 빠른 확인은 public 테스트나 local marketplace/direct MCP 연결을 권장합니다.

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

Codex marketplace bundle의 `.mcp.codex.json`은 GitHub 설치 위치와 무관하게 실행되도록 `uvx --from git+https://github.com/Squirbie/sourcing-agent-1688.git sourcing1688-mcp` 방식을 사용합니다. root local-dev용 `.mcp.codex.json`은 repo root에서 `uv run`으로 실행하는 개발용 설정입니다.

직접 MCP fallback 예시:

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
