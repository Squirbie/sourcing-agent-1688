# 1688 Sourcing Agent

Codex Desktop에서 `@sourcing-agent-1688`로 호출해서 1688 상품을 찾고, 링크를 분석하고, 상세페이지 자료를 저장하는 플러그인입니다.

## 이렇게 말하면 됩니다

```text
@sourcing-agent-1688 1688에서 암막우산 찾아줘.
```

```text
@sourcing-agent-1688 이 1688 상품 링크 분석해줘:
https://detail.1688.com/offer/123456789.html
```

```text
@sourcing-agent-1688 이 상품페이지 이미지, 영상, HTML, 속성 JSON 저장해줘.
```

```text
@sourcing-agent-1688 잘 팔릴 만한 후보를 추천하고 shortlist에 저장해줘.
```

## 설치

Codex Desktop의 플러그인 추가 화면에서 아래 GitHub repo를 추가합니다.

```text
https://github.com/Squirbie/sourcing-agent-1688
```

설치 후 새 채팅에서 `@sourcing-agent-1688`를 입력하면 플러그인을 호출할 수 있습니다.

## 실제 1688 연결

기본 provider는 `auto`입니다.

| provider | 쓰는 상황 | 준비물 |
|---|---|---|
| `auto` | 기본값 | API 설정 또는 브라우저 설정 |
| `api` | 1688 Open Platform API로 검색 | AppKey, AppSecret, access token 또는 refresh token |
| `browser` | 로그인한 브라우저 세션으로 확인 | 사용자가 직접 로그인한 1688 브라우저 프로필 |
| `local_html` | 저장해둔 상세페이지 HTML 분석 | 1688 상세페이지 HTML 파일 |

API 키와 토큰은 `open.1688.com / 1688开放平台`에서 앱을 만들고 발급받습니다.

```powershell
sourcing1688 auth status --json
sourcing1688 auth url --redirect-uri "https://example.com/callback" --json
sourcing1688 auth exchange --code CODE --redirect-uri "https://example.com/callback" --json
```

API가 없으면 브라우저 방식으로 쓸 수 있습니다. 1688은 headless 브라우저에서 로그인 상태가 다르게 보일 수 있어서 기본값은 눈에 보이는 브라우저입니다.

```powershell
sourcing1688 browser-profile open --json
sourcing1688 provider-check --provider browser --json
```

창을 띄우지 않고 시도하려면 `SOURCING1688_BROWSER_HEADLESS=true`를 설정할 수 있지만, 1688이 다시 로그인을 요구할 수 있습니다.

## CLI

```powershell
sourcing1688 provider-check --provider auto --json
sourcing1688 search "암막우산" --top 5 --provider auto --json
sourcing1688 recommend "암막우산" --top 5 --provider auto --json
sourcing1688 analyze-url "https://detail.1688.com/offer/123456789.html" --provider auto --json
sourcing1688 parse-html path/to/1688-detail.html --json
sourcing1688 download-assets-from-html path/to/1688-detail.html --dry-run --json
```

## 저장 위치

런타임 데이터는 `SOURCING1688_HOME` 아래에 모입니다.

```text
~/.sourcing1688/
  assets/
  data/
  raw/
  browser-profile/
  token-cache/
```

## 삭제

Codex Desktop에서는 플러그인 화면에서 제거합니다. 로컬 데이터까지 지우려면:

```powershell
sourcing1688 uninstall --yes
```
