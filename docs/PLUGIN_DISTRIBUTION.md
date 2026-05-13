# Codex Desktop 배포 메모

이 repo는 Codex Desktop 전용 플러그인으로 배포합니다.

```text
https://github.com/Squirbie/sourcing-agent-1688
```

## 설치

```powershell
codex plugin marketplace add https://github.com/Squirbie/sourcing-agent-1688.git
```

Codex Desktop에서 `1688 Sourcing Agent`를 선택하고 `Codex에 추가`를 누릅니다.

## Plugin bundle

Codex marketplace가 읽는 실제 플러그인 root:

```text
plugins/sourcing-agent-1688/
```

Marketplace source path:

```text
path: "./plugins/sourcing-agent-1688"
```

필수 파일:

```text
plugins/sourcing-agent-1688/.codex-plugin/plugin.json
plugins/sourcing-agent-1688/.mcp.json
plugins/sourcing-agent-1688/skills/sourcing-agent-1688/SKILL.md
plugins/sourcing-agent-1688/README.md
```

## MCP

Codex plugin bundle의 MCP 설정은 GitHub 설치에서도 동작하도록 `uvx`를 사용합니다.

```json
{
  "mcpServers": {
    "sourcing1688": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Squirbie/sourcing-agent-1688.git",
        "sourcing1688-mcp"
      ]
    }
  }
}
```

## 검증

```powershell
uv sync --extra dev
uv run pytest -q -ra
uvx --from . sourcing-agent-1688 --help
uvx --from . sourcing1688-mcp --help
```

## 삭제

Codex Desktop에서 플러그인을 제거합니다. 로컬 런타임 상태까지 지우려면:

```powershell
sourcing1688 uninstall --yes
```
