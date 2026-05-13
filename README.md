# 1688 Sourcing Agent

Codex Desktop에서 1688 상품을 찾고, 상품 링크를 분석하고, 상세페이지 이미지/영상/HTML을 저장하는 플러그인입니다.

## 할 수 있는 일

- 한국어 상품명을 1688 검색어로 바꾸기
- 1688 상품 검색
- 1688 상품 링크 분석
- 상세페이지 이미지, 영상, HTML, 속성 JSON 저장
- 후보 상품 점수화
- shortlist 저장과 리포트 export

## 설치

```powershell
codex plugin marketplace add https://github.com/Squirbie/sourcing-agent-1688.git
```

그 다음 Codex Desktop에서:

1. 플러그인 화면을 엽니다.
2. `1688 Sourcing Agent`를 선택합니다.
3. `Codex에 추가`를 누릅니다.
4. 새 채팅을 엽니다.
5. `@sourcing-agent-1688`를 입력해서 플러그인을 부릅니다.

## 바로 써보기

```text
@sourcing-agent-1688 1688에서 암막우산 찾아줘.
```

```text
@sourcing-agent-1688 이 상품 링크 분석해줘:
https://detail.1688.com/offer/123456789.html
```

```text
@sourcing-agent-1688 이 상품페이지 이미지, 영상, HTML, 속성 JSON 저장해줘.
```

```text
@sourcing-agent-1688 provider 준비 상태 확인해줘.
```

## 실제 1688 검색 준비

가장 좋은 방식은 1688 Open Platform API입니다.

```powershell
sourcing1688 auth status --json
sourcing1688 auth url --redirect-uri "https://example.com/callback" --json
sourcing1688 auth exchange --code CODE --redirect-uri "https://example.com/callback" --json
```

API가 없으면 Codex Desktop의 Chrome/Browser 연결을 우선 사용하세요. 사용자가 이미 로그인한 브라우저 세션을 쓰는 방식이 가장 자연스럽습니다.

CLI만 사용할 때는 별도 브라우저 프로필을 열 수 있습니다.

```powershell
sourcing1688 browser-profile open --json
```

열린 브라우저에서 1688에 직접 로그인하고 창을 닫은 뒤 다시 검색합니다.

## CLI 예시

```powershell
sourcing1688 provider-check --provider auto --json
sourcing1688 search "암막우산" --top 5 --provider auto --json
sourcing1688 recommend "암막우산" --top 5 --provider auto --json
sourcing1688 analyze-url "https://detail.1688.com/offer/123456789.html" --provider auto --json
sourcing1688 parse-html path/to/1688-detail.html --json
sourcing1688 download-assets-from-html path/to/1688-detail.html --dry-run --json
```

## Provider

| provider | 용도 |
|---|---|
| `auto` | 기본값. API가 있으면 API, 없으면 browser 흐름 사용 |
| `api` | 1688 Open Platform API |
| `browser` | 로그인한 브라우저 프로필로 1688 접속 |
| `local_html` | 저장해둔 상세페이지 HTML 분석 |

## 저장 위치

기본 런타임 파일은 `SOURCING1688_HOME` 아래에 저장됩니다.

```text
~/.sourcing1688/
  assets/
  data/
  raw/
  browser-profile/
  token-cache/
```

## 삭제

Codex Desktop에서 플러그인을 제거한 뒤, 로컬 상태까지 지우려면:

```powershell
sourcing1688 uninstall --yes
```

## 참고

- 1688 API 키는 `open.1688.com / 1688开放平台`에서 발급합니다.
- 앱 생성 후 AppKey/AppSecret을 확인하고 필요한 API 권한을 신청합니다.
- OAuth로 access token 또는 refresh token을 준비합니다.
- 로그인이나 확인 화면이 나오면 사용자가 브라우저에서 직접 처리해야 합니다.
