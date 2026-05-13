# 1688 Sourcing Agent

Codex Desktop에서 `@sourcing-agent-1688`로 호출해서 1688 상품을 찾고, 상품 페이지를 분석하고, 이미지/상세 HTML/속성 JSON을 저장하는 플러그인입니다.

## 이렇게 말하면 됩니다

```text
@sourcing-agent-1688 1688에서 요즘 인기있는 상품 찾아줘.
```

```text
@sourcing-agent-1688 이 1688 상품 분석해줘:
https://detail.1688.com/offer/123456789.html
```

```text
@sourcing-agent-1688 이 상품페이지 이미지, 상세 HTML, 속성 JSON 저장해줘.
```

## 설치

Codex Desktop 플러그인 화면에서 이 GitHub repo를 추가합니다.

```text
https://github.com/Squirbie/sourcing-agent-1688
```

설치 후 새 채팅에서 `@sourcing-agent-1688`를 선택해서 사용합니다.

## Provider

| provider | 용도 | 준비물 |
|---|---|---|
| `auto` | 기본 진단 및 API 우선 사용 | 1688 API 키가 있으면 API 사용. 키가 없으면 브라우저를 자동으로 열지 않음 |
| `api` | 1688 Open Platform API 사용 | AppKey, AppSecret, access token 또는 refresh token |
| `browser` | 관리형 브라우저 프로필 사용 | 사용자가 직접 로그인한 1688 브라우저 프로필 |
| `local_html` | 저장된 1688 상세 HTML 분석 | HTML 파일 |

API 키가 없을 때는 `auto`가 Chrome 창을 자동으로 열지 않습니다. 이미 로그인된 Chrome 페이지를 쓰려면 Chrome 플러그인이 현재 탭 HTML을 가져오고, 1688 Sourcing Agent가 그 HTML을 `parse_1688_rendered_html_content`로 분석하는 흐름을 사용합니다.

## 한국어 키워드 확장

한국어 상품명을 1688 검색에 맞는 중국어 후보로 확장합니다.

예:

- 월드컵 축구 유니폼 → `世界杯球衣`, `足球服`, `国家队球衣`, `2026世界杯球衣`, `足球训练服`
- 운동 양말 → `运动袜`, `跑步袜`, `毛巾底袜`, `中筒运动袜`
- 남성 벨트 → `男士皮带`, `自动扣皮带`, `腰带`, `商务皮带`
- 크라프트 포장봉투 → `牛皮纸袋`, `外卖包装袋`, `食品包装袋`, `手提牛皮纸袋`
- 러닝화 → `跑步鞋`, `运动鞋`, `透气跑鞋`, `休闲运动鞋`
- 남성 속옷 → `男士内裤`, `平角裤`, `纯棉男内裤`, `男士四角裤`

## Chrome HTML 기반 분석

API가 없거나 1688이 로그인 상태에서만 정보를 보여주는 경우, 이미 로그인된 Chrome에서 상품 페이지를 열고 현재 탭 HTML을 플러그인에 넘기는 방식이 가장 안정적입니다.

사용되는 MCP 도구:

- `parse_1688_rendered_html_content`: Chrome이 가져온 HTML을 상품 상세 JSON으로 분석
- `download_1688_product_assets_from_html_content`: Chrome이 가져온 HTML에서 이미지/상세 HTML/속성 JSON 저장

영상 버튼이 화면에 보여도 HTML 안에 실제 `mp4`/`m3u8` URL이 없을 수 있습니다. 이 경우 플러그인은 “영상 URL이 공개 HTML에 노출되지 않았다”는 경고를 반환합니다.

## CLI 예시

```powershell
sourcing1688 provider-check --provider auto --json
sourcing1688 expand-keywords "월드컵 축구 유니폼" --json
sourcing1688 parse-html product.html --json
sourcing1688 download-assets-from-html product.html --dry-run --json
```

API 키가 있을 때:

```powershell
sourcing1688 analyze-url "https://detail.1688.com/offer/123456789.html" --provider api --json
```

1688 API 키는 `open.1688.com / 1688开放平台`에서 앱을 만들고 필요한 권한을 받은 뒤 준비합니다.

관리형 브라우저 프로필을 명시적으로 쓸 때:

```powershell
sourcing1688 browser-profile open --json
sourcing1688 provider-check --provider browser --json
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
