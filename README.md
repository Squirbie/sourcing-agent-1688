# 1688 Sourcing Agent

Codex, Claude Code, OpenClaw 같은 에이전트가 1688 상품을 찾고, 분석하고, 상세페이지 이미지/영상/HTML을 저장하도록 도와주는 MCP 플러그인/CLI 도구입니다.

- GitHub repo: `https://github.com/Squirbie/sourcing-agent-1688`
- Plugin id: `sourcing-agent-1688`
- CLI: `sourcing1688`, `sourcing-agent-1688`
- MCP CLI: `sourcing1688-mcp`
- English: [README.en.md](README.en.md)

## 이런 식으로 쓸 수 있어요

```text
1688에서 암막우산 찾아줘.
```

```text
이 1688 상품 링크 분석해줘:
https://detail.1688.com/offer/123456789.html
```

```text
이 상품페이지 이미지랑 상세페이지 자료 저장해줘.
```

```text
잘 팔릴 만한 후보를 추천하고 shortlist에 저장해줘.
```

## 주요 기능

- 한국어 키워드를 중국어 검색어 후보로 확장
- 1688 상품 검색
- 상품 상세 분석
- 이미지, 영상, HTML, 속성 JSON 저장
- 후보 상품 점수화
- shortlist 저장과 리포트 export
- Codex / Claude Code / OpenClaw에서 MCP 도구로 사용

## 설치: Codex

```powershell
codex plugin marketplace add https://github.com/Squirbie/sourcing-agent-1688.git
```

그 다음:

1. Codex에서 `/plugins`
2. `1688 Sourcing Agent`가 추가되어 있는지 확인
3. 새 세션에서 `/mcp` 확인
4. provider 준비 상태 확인

```powershell
sourcing1688 provider-check --provider auto --json
```

## Codex 앱에 안 보일 때

`codex plugin marketplace add`는 marketplace를 내려받는 단계입니다. 이 repo는 기본 설치 대상으로 설정되어 있지만, 앱의 플러그인 화면에 바로 반영되지 않으면 아래 순서로 확인하세요.

1. Codex 앱을 완전히 종료한 뒤 다시 엽니다.
2. `/plugins`에서 `1688 Sourcing Agent`를 다시 검색합니다.
3. 여전히 `+`가 보이면 한 번 눌러 수동 추가하거나, marketplace를 remove/add로 다시 받아옵니다.
4. repo가 private이면 Codex 앱 UI가 marketplace를 읽지 못할 수 있습니다. 이때는 잠깐 public으로 테스트하거나 local marketplace/direct MCP 방식으로 먼저 확인하세요.
5. 그래도 안 보이면 아래 직접 MCP 연결 방식으로 도구부터 테스트합니다.

직접 MCP 연결 예시:

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

## 에이전트에게 복붙해서 설치시키기

Codex:

```text
이 repo를 Codex 플러그인으로 설치하고 MCP 도구 확인, provider-check auto 실행, 데모 때만 mock 사용까지 확인해줘: https://github.com/Squirbie/sourcing-agent-1688
```

Claude Code:

```text
이 repo를 Claude Code 플러그인으로 설치하고 plugin reload, MCP 도구 확인, provider-check auto 실행, mock 결과는 데모 샘플이라는 점까지 확인해줘: https://github.com/Squirbie/sourcing-agent-1688
```

OpenClaw:

```text
이 repo를 OpenClaw 플러그인/bundle로 설치하고 skill/MCP mapping 확인, provider-check auto 실행, 데모 때만 mock 사용하게 확인해줘: https://github.com/Squirbie/sourcing-agent-1688
```

## 실제 사용 예시

에이전트에게 말하기:

```text
1688 Sourcing Agent provider 준비 상태 확인해줘.
```

```text
mock provider로 "암막우산" 소싱 후보 5개 추천해줘.
```

```text
auto provider로 "黑胶伞" 검색해줘. live provider가 준비 안 됐으면 필요한 설정만 알려줘.
```

```text
이 1688 링크 상품 분석해줘: https://detail.1688.com/offer/123456789.html
```

```text
이 상품페이지의 이미지, 영상, HTML, 속성 JSON을 저장하고 manifest 경로를 알려줘.
```

CLI 예시:

```powershell
sourcing1688 provider-check --provider auto --json
sourcing1688 search "암막우산" --top 5 --provider mock --json
sourcing1688 recommend "암막우산" --top 5 --provider mock --json
sourcing1688 parse-html path/to/1688-detail.html --json
sourcing1688 download-assets-from-html path/to/1688-detail.html --dry-run --json
```

## provider는 이렇게 쓰면 됩니다

| provider | 용도 | 준비물 |
|---|---|---|
| `auto` | 실사용 기본값 | `api` 또는 `browser` 설정 |
| `api` | 1688 Open Platform API 사용 | AppKey, AppSecret, token |
| `browser` | 로그인한 브라우저 프로필로 보기 | 직접 로그인한 1688 profile |
| `local_html` | 저장해둔 상세페이지 HTML 분석 | HTML 파일 |
| `mock` | 설치 확인/데모 | 없음 |

`mock`은 설치 확인과 데모용 샘플 데이터입니다. 실제 1688 확인은 `api`, `browser`, `local_html` provider를 사용하세요.

## 1688 API는 꼭 필요한가요?

- 설치와 mock 데모에는 필요 없습니다.
- 실제 1688 live 검색을 안정적으로 하려면 API 방식이 좋습니다.
- API 키/토큰은 `open.1688.com / 1688开放平台`에서 발급합니다.
- 앱 생성 후 AppKey/AppSecret을 확인하고, 필요한 API 권한/솔루션을 신청할 수 있습니다.
- OAuth로 access token 또는 refresh token을 준비합니다.
- API가 없으면 browser profile 방식이나 local HTML 방식도 사용할 수 있습니다.

자세한 절차는 공식 1688 Open Platform 문서를 확인하세요.

## browser profile 방식

API가 없어도 사용자가 직접 로그인한 브라우저 프로필을 활용할 수 있습니다. 로그인과 확인 절차는 열린 브라우저에서 직접 처리합니다.

```powershell
sourcing1688 browser-profile open --json
sourcing1688 provider-check --provider browser --json
```

## local HTML 방식

1688 상세페이지 HTML을 저장해두고 분석하는 방식입니다. live 접속 없이 이미지/영상/속성 URL을 추출할 수 있습니다.

```powershell
sourcing1688 parse-html product.html --json
sourcing1688 download-assets-from-html product.html --dry-run --json
```

## 저장 위치

기본 저장 위치는 `SOURCING1688_HOME` 아래입니다.

```text
~/.sourcing1688/
  assets/
  data/
  raw/
  browser-profile/
  token-cache/
```

## 삭제

```powershell
sourcing1688 uninstall --yes
```

플러그인은 Codex, Claude Code, OpenClaw의 plugin 화면이나 명령에서 제거하면 됩니다.

## 더 보기

- Codex 설치 자세히 보기: [docs/CODEX.md](docs/CODEX.md)
- Claude Code 설치 자세히 보기: [docs/CLAUDE_CODE.md](docs/CLAUDE_CODE.md)
- OpenClaw 설치 자세히 보기: [docs/OPENCLAW.md](docs/OPENCLAW.md)
- 1688 API 준비 요약: [docs/API_CREDENTIALS.md](docs/API_CREDENTIALS.md)
- 배포 메모: [docs/PLUGIN_DISTRIBUTION.md](docs/PLUGIN_DISTRIBUTION.md)
- 참고한 오픈소스: [docs/references.md](docs/references.md)
