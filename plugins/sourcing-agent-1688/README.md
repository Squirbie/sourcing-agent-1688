# 1688 Sourcing Agent

Codex Desktop에서 1688 상품을 찾고, Chrome에 열린 상품 페이지를 분석하고, 이미지/영상 자료 저장까지 도와주는 소싱 에이전트입니다. Windows와 macOS 둘 다 같은 설치 명령을 사용합니다.

권장 설치 명령:

```powershell
uvx --from git+https://github.com/Squirbie/sourcing-agent-1688.git sourcing-agent-1688 install-codex
```

설치 후 Codex Desktop을 다시 켜고 새 채팅에서 `@sourcing-agent-1688`를 선택하세요.

처음 연결할 때 Chrome이 허용창을 띄울 수 있습니다. 보이면 `Allow`를 누르고 Codex Desktop을 다시 시작하세요.

상품 링크를 주면 기존 Chrome 세션에서 그 페이지를 열어 분석합니다. 키워드 검색을 요청하면 1688 탭이 없어도 기존 Chrome 세션에 검색 탭을 열고 후보를 찾습니다.

포함 항목:

- `sourcing1688` MCP 서버
- `chrome-devtools` MCP 서버
- 1688 Sourcing Agent Skill
