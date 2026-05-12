# 1688 Sourcing Agent

한국 셀러가 1688 상품을 소량 리서치할 때 에이전트가 호출할 수 있는 JSON-first CLI, MCP server, Codex/Claude/OpenClaw 호환 플러그인 번들입니다.

- GitHub repo: `https://github.com/Squirbie/sourcing-agent-1688`
- Plugin id: `sourcing-agent-1688`
- Python package/import: `sourcing1688`
- CLI: `sourcing1688`, `sourcing-agent-1688`
- MCP CLI: `sourcing1688-mcp`
- English: [README.en.md](README.en.md)

## 이게 뭐야

`1688 Sourcing Agent`는 다음 작업을 구조화된 JSON으로 수행합니다.

- 한국어 키워드를 중국어 소싱 키워드로 확장
- mock/API/browser/local HTML provider로 상품 검색, 상세 분석, 추천
- 1688 상세 HTML에서 이미지, 영상, 속성, SKU 후보 추출
- asset manifest 생성과 dry-run 다운로드 계획
- shortlist 저장과 markdown/csv/json export
- Codex, Claude Code, OpenClaw에서 MCP tool로 사용

## 이게 아닌 것

대량 크롤러가 아닙니다. CAPTCHA, 로그인 검증, anti-bot, robots, 약관, 계정 권한을 우회하지 않습니다. stealth, proxy rotation, 자동 로그인, 쿠키 탈취, token logging 기능도 없습니다.

`mock` 결과는 데모/테스트 fixture이며 실제 1688 live 데이터처럼 말하면 안 됩니다.

## 준비물

- Python 3.11+
- `uv`
- Codex, Claude Code, 또는 OpenClaw 중 사용할 에이전트
- live 사용 시 둘 중 하나:
  - 1688 Open Platform API credentials
  - 사람이 로그인/검증을 완료한 browser profile

## 빠른 확인

```powershell
uv sync --extra dev
uv run pytest -q -ra
uv run sourcing1688 provider-check --provider auto --json
uv run sourcing1688 search "암막우산" --top 2 --provider mock --json
```

## Codex 설치

```powershell
codex plugin marketplace add https://github.com/Squirbie/sourcing-agent-1688.git
```

Codex에서 `/plugins`를 열고 `sourcing-agent-1688`를 설치한 뒤 확인합니다.

```powershell
uvx --from git+https://github.com/Squirbie/sourcing-agent-1688.git sourcing1688 provider-check --provider auto --json
```

Codex용 MCP 설정은 `.mcp.codex.json`입니다. Codex plugin manifest가 이 파일을 가리킵니다.

## Claude Code 설치

Claude Code 공식 plugin 구조는 `.claude-plugin/plugin.json`과 root `.mcp.json`을 사용합니다.

```powershell
claude plugin marketplace add Squirbie/sourcing-agent-1688
claude plugin install sourcing-agent-1688@sourcing-agent-1688-marketplace
```

로컬 테스트는 다음처럼 할 수 있습니다.

```powershell
claude --plugin-dir .
```

설치 후 `/mcp` 또는 `claude plugin details sourcing-agent-1688`로 MCP server가 보이는지 확인하세요.

## OpenClaw 설치

OpenClaw는 Codex bundle marker(`.codex-plugin/plugin.json`)와 Claude bundle marker(`.claude-plugin/plugin.json`)를 감지할 수 있습니다. 이 repo는 별도 OpenClaw 전용 기능을 넣지 않고, skill root와 stdio MCP 구성을 bundle로 노출합니다.

```powershell
openclaw plugins install https://github.com/Squirbie/sourcing-agent-1688.git
openclaw plugins inspect sourcing-agent-1688
```

OpenClaw 환경별 marketplace 명령은 버전에 따라 다를 수 있으니 설치 전 `openclaw plugins --help`로 확인하세요.

## 에이전트에게 복붙해서 설치시키기

Codex:

> Install https://github.com/Squirbie/sourcing-agent-1688 as a Codex plugin, verify the MCP tools, run provider-check auto, and use mock only for demo.

> 이 repo를 Codex 플러그인으로 설치하고 MCP 도구 확인, provider-check auto 실행, 데모 때만 mock 사용까지 확인해줘.

Claude Code:

> Install https://github.com/Squirbie/sourcing-agent-1688 as a Claude Code plugin, reload plugins, verify MCP tools, run provider-check auto, and do not treat mock results as live 1688 data.

> 이 repo를 Claude Code 플러그인으로 설치하고 plugin reload, MCP 도구 확인, provider-check auto 실행, mock 결과를 live처럼 말하지 않도록 확인해줘.

OpenClaw:

> Install https://github.com/Squirbie/sourcing-agent-1688 as an OpenClaw plugin/bundle, inspect mapped skills and MCP tools, run provider-check auto, and use mock only for demo.

> 이 repo를 OpenClaw 플러그인/bundle로 설치하고 skill/MCP mapping 확인, provider-check auto 실행, 데모 때만 mock 사용하게 설정해줘.

## Provider

| Provider | 용도 | 주의 |
|---|---|---|
| `auto` | 실사용 기본값. API credentials가 있으면 API, 없으면 browser profile 확인 | 절대 mock으로 조용히 fallback하지 않음 |
| `api` | 1688 Open Platform API형 provider | AppKey/AppSecret/token 필요 |
| `browser` | Playwright persistent profile | 사람의 로그인/검증 필요, 우회 없음 |
| `local_html` | 저장된 rendered HTML/SingleFile 분석 | live 검색 불가 |
| `mock` | fixture 기반 테스트/데모 | live 데이터 아님 |

항상 먼저 확인하세요.

```powershell
sourcing1688 provider-check --provider auto --json
```

## 1688 API는 어디서 받아?

1688 API credentials는 `open.1688.com / 1688开放平台`에서 발급합니다. 1688 계정으로 앱을 만들고 AppKey/AppSecret을 확인한 뒤, 필요한 API 권한/솔루션을 신청해야 할 수 있습니다. OAuth로 access token 또는 refresh token을 준비합니다. 자세한 절차와 최신 메뉴는 공식 1688 Open Platform 문서를 확인하세요.

API가 없으면 `browser` profile 또는 `local_html` 방식으로도 일부 작업이 가능합니다.

```powershell
sourcing1688 auth status --json
sourcing1688 auth url --redirect-uri "https://example.com/callback" --json
sourcing1688 auth exchange --code CODE --redirect-uri "https://example.com/callback" --json
```

## Browser profile 방식

```powershell
sourcing1688 init-home --json
sourcing1688 browser-profile open --json
sourcing1688 browser-profile check --json
```

열린 브라우저에서 사용자가 직접 1688 로그인과 검증을 끝냅니다. 이 도구는 CAPTCHA나 verification을 우회하지 않습니다.

## Local HTML 방식

브라우저나 SingleFile 등으로 저장한 1688 상세 HTML을 분석합니다.

```powershell
sourcing1688 parse-html path/to/detail.html --json
sourcing1688 download-assets-from-html path/to/detail.html --dry-run --json
```

## CLI 예시

```powershell
sourcing1688 expand-keywords "암막우산" --json
sourcing1688 search "암막우산" --top 5 --provider mock --json
sourcing1688 recommend "암막우산" --top 5 --provider mock --json
sourcing1688 analyze-url "https://detail.1688.com/offer/123456789.html" --provider mock --json
sourcing-agent-1688 provider-check --provider auto --json
sourcing1688-mcp --help
```

## MCP tools 요약

MCP server는 keyword expansion, product search/detail/recommendation, asset download, rendered HTML parsing, image search, provider checks, hot keywords/rankings, shortlist save, report export를 제공합니다.

- Codex MCP config: `.mcp.codex.json` (`mcp_servers`)
- Claude/OpenClaw-compatible MCP config: `.mcp.json` (`mcpServers`)

## 삭제 방법

```powershell
codex plugin marketplace remove sourcing-agent-1688-marketplace
claude plugin uninstall sourcing-agent-1688 --prune
sourcing1688 uninstall --yes
```

browser profile이나 token cache를 보존하려면:

```powershell
sourcing1688 uninstall --yes --keep-browser-profile --keep-token-cache
```

## Troubleshooting

- `missing_credentials`: API env 또는 token cache가 없음
- `needs_human_login`: browser profile을 열고 수동 로그인 필요
- `blocked_by_verification`: 검증을 직접 완료한 뒤 재시도
- `live_not_verified`: provider는 있으나 live smoke 미검증
- `missing_live_provider`: `auto`가 API/browser provider를 찾지 못함
- asset 테스트는 외부 다운로드 방지를 위해 `--dry-run` 사용

## Security / Privacy / Terms

AppKey, AppSecret, access token, refresh token, cookie, browser profile을 공유하거나 commit하지 마세요. `.env`, token cache, browser profile, raw snapshots, assets runtime output은 gitignore에 포함되어 있습니다. 1688 약관, robots, 계정 권한, 검증 절차를 우회하지 마세요.

## References / Credits

참고한 repo와 주의사항은 [docs/references.md](docs/references.md)에 정리했습니다. API 요약은 [docs/API_CREDENTIALS.md](docs/API_CREDENTIALS.md), 배포 메모는 [docs/PLUGIN_DISTRIBUTION.md](docs/PLUGIN_DISTRIBUTION.md)를 보세요.
