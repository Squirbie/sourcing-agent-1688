# 1688 API 준비 요약

1688 live 검색을 안정적으로 쓰려면 API provider를 준비하는 것이 좋습니다.

## 어디서 받나요?

1688 API credentials는 `open.1688.com / 1688开放平台`에서 발급합니다.

기본 흐름:

1. 1688 계정으로 Open Platform에 로그인합니다.
2. 앱을 생성합니다.
3. AppKey와 AppSecret을 확인합니다.
4. 필요한 API 권한이나 솔루션을 신청합니다.
5. OAuth로 access token 또는 refresh token을 준비합니다.

정확한 메뉴와 권한 이름은 계정 상태와 1688 정책에 따라 달라질 수 있으니, 최신 절차는 공식 1688 Open Platform 문서를 확인하세요.

## CLI에서 확인하기

```powershell
sourcing1688 auth status --json
sourcing1688 auth url --redirect-uri "https://example.com/callback" --json
sourcing1688 auth exchange --code CODE --redirect-uri "https://example.com/callback" --json
```

환경변수 예시:

```env
ALI1688_APP_KEY=
ALI1688_APP_SECRET=
ALI1688_REFRESH_TOKEN=
ALI1688_ACCESS_TOKEN=
SOURCING1688_HOME=
```

token cache는 기본적으로 아래에 저장됩니다.

```text
SOURCING1688_HOME/token-cache/.1688_token_cache.json
```

## API가 아직 없다면

- API가 없으면 `browser` provider 또는 `local_html` 방식을 사용하세요.
- 사용자가 직접 로그인한 브라우저 프로필이 있으면 `browser` provider를 사용할 수 있습니다.
- 이미 저장해둔 상세페이지 HTML이 있으면 `local_html` provider로 분석할 수 있습니다.
