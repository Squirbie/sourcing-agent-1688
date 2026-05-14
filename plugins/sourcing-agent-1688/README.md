# 1688 Sourcing Agent

Codex Desktop에서 Chrome에 열린 1688 상품 페이지를 함께 보고 분석하는 소싱 에이전트입니다. Windows와 macOS 둘 다 같은 설치 명령을 사용합니다.

권장 설치 명령:

```powershell
uvx --from git+https://github.com/Squirbie/sourcing-agent-1688.git sourcing-agent-1688 install-codex
```

설치 후 Codex Desktop을 다시 켜고 새 채팅에서 `@sourcing-agent-1688`를 선택하세요.

처음 연결할 때 Chrome이 원격 디버깅 허용창을 띄울 수 있습니다. 허용창이 보이면 `Allow`를 누르고 같은 요청을 다시 실행하세요.

포함 항목:

- `sourcing1688` MCP 서버
- `chrome-devtools` MCP 서버
- 1688 Sourcing Agent Skill
