# 1688 Sourcing Agent

Codex Desktop에서 `@sourcing-agent-1688`로 호출해 1688 상품을 찾고, 사람이 보는 Chrome 상품 페이지와 네트워크 응답을 읽어 소싱 판단용 JSON/리포트로 정리하는 플러그인입니다.

이 플러그인은 두 MCP 서버를 함께 설치합니다.

- `chrome-devtools`: Chrome 탭, DOM, 네트워크 응답, 스크린샷, JS 상태를 확인
- `sourcing1688`: 1688 HTML/네트워크 JSON을 상품 상세, 이미지, 영상, 옵션, 판매자, 점수 데이터로 정리

## 이렇게 말하면 됩니다

```text
@sourcing-agent-1688 1688에서 요즘 소싱하기 좋은 상품 찾아줘.
```

```text
@sourcing-agent-1688 이 상품 셀러 입장에서 어때?
https://detail.1688.com/offer/123456789.html
```

```text
@sourcing-agent-1688 이 페이지의 대표 이미지, 상세 이미지, 영상, HTML, 속성 JSON 저장해줘.
```

## 설치

Codex Desktop 플러그인 화면에서 이 GitHub repo를 추가합니다.

```text
https://github.com/Squirbie/sourcing-agent-1688
```

설치 후 새 채팅에서 `@sourcing-agent-1688`를 선택해서 사용합니다.

Chrome DevTools MCP가 같이 켜져야 1688에서 실제로 보이는 탭과 네트워크 응답을 읽을 수 있습니다. 플러그인 상세 화면의 포함 항목에 `Sourcing1688` MCP 서버와 `Chrome DevTools` MCP 서버가 함께 보이는지 확인하세요.

Chrome 연결은 `chrome-devtools-mcp@latest --auto-connect`를 사용합니다. Chrome이 연결 허용 창을 띄우면 허용하고, 1688 페이지를 로그인된 Chrome 탭에서 열어둔 뒤 `@sourcing-agent-1688`로 분석을 요청하세요.

## 실제 분석 흐름

상품 링크를 주면 에이전트는 이렇게 처리합니다.

1. Chrome에서 해당 1688 페이지를 찾거나 엽니다.
2. 화면에 보이는 상품 정보와 DOM을 읽습니다.
3. `mtop.1688`, `offerDetail`, `offerWarnService`, `getVideoById`, `sku`, `seller`, `trade` 같은 네트워크 응답을 확인합니다.
4. HTML은 `parse_1688_rendered_html_content`로 분석합니다.
5. 네트워크 JSON은 `parse_1688_network_payload_content`로 분석합니다.
6. 이미지/영상/HTML/속성 저장은 `download_1688_product_assets_from_html_content`로 manifest까지 만듭니다.

영상 버튼이 화면에 보여도 `mp4`나 `m3u8` 주소가 HTML에 바로 들어있지 않을 수 있습니다. 이때는 Chrome 네트워크 응답까지 확인해서 영상 주소가 따로 내려오는지 봅니다.

## provider

| provider | 용도 | 준비물 |
|---|---|---|
| `api` | 1688 Open Platform API 사용 | AppKey, AppSecret, access token 또는 refresh token |
| `chrome-devtools` | Codex가 Chrome 탭/네트워크를 읽는 기본 실사용 경로 | Chrome, Node/npx |
| `browser` | 별도 Playwright 프로필을 직접 열어 쓰는 경로 | 사용자가 로그인한 1688 브라우저 프로필 |
| `local_html` | 저장된 HTML 분석 | HTML 파일 |
| `auto` | API 준비 상태 진단과 API 우선 사용 | API 키가 있으면 API 사용 |

API가 없으면 Chrome DevTools 경로가 핵심입니다. 별도 Playwright 창을 반복해서 여는 방식보다, 사용자가 보고 있는 Chrome 페이지와 네트워크를 읽는 흐름을 우선합니다.

## 1688 API

API 키는 `open.1688.com / 1688开放平台`에서 앱을 만들고 필요한 권한을 받은 뒤 준비합니다.

```powershell
sourcing1688 auth status --json
sourcing1688 auth url --redirect-uri "https://example.com/callback" --json
sourcing1688 provider-check --provider api --json
```

## CLI

```powershell
sourcing1688 provider-check --provider auto --json
sourcing1688 expand-keywords "월드컵 축구 유니폼" --json
sourcing1688 analyze-url "https://detail.1688.com/offer/123456789.html" --provider api --json
sourcing1688 parse-html product.html --json
sourcing1688 download-assets-from-html product.html --dry-run --json
```

## 저장 위치

기본 runtime 데이터는 `SOURCING1688_HOME` 아래에 저장됩니다.

```text
~/.sourcing1688/
  assets/
  data/
  raw/
  browser-profile/
  token-cache/
```

## 삭제

Codex Desktop에서는 플러그인 화면에서 제거합니다. 로컬 runtime 데이터까지 지우려면:

```powershell
sourcing1688 uninstall --yes
```
