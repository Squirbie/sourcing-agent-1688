# 1688 Sourcing Agent

Codex Desktop에서 `@sourcing-agent-1688`로 1688 상품 페이지를 보고 분석하는 플러그인입니다.

핵심은 단순 HTML 저장이 아니라 **사용자가 보고 있는 Chrome 탭의 화면, DOM, 네트워크 응답을 Codex가 함께 읽는 것**입니다.

## 설치

Codex Desktop 플러그인 화면에 이 repo를 추가합니다.

```text
https://github.com/Squirbie/sourcing-agent-1688
```

설치 후 새 채팅에서 `@sourcing-agent-1688`를 선택합니다.

## 처음 한 번: Chrome 연결

Chrome DevTools 연결이 준비되지 않았으면 에이전트에게 이렇게 말합니다.

```text
@sourcing-agent-1688 Chrome DevTools 연결 세팅 열어줘.
```

플러그인이 Chrome 개발자 연결 설정 페이지를 엽니다. Chrome에서 연결을 허용한 뒤, 같은 Chrome 프로필에서 1688 상품 페이지를 직접 열어두고 다시 요청하면 됩니다.

## 이렇게 쓰면 됩니다

```text
@sourcing-agent-1688 이 1688 상품 셀러 입장에서 분석해줘:
https://detail.1688.com/offer/123456789.html
```

```text
@sourcing-agent-1688 지금 Chrome에 열어둔 1688 상품 페이지 이미지, 옵션, 판매자 정보, 영상 자료 확인해줘.
```

```text
@sourcing-agent-1688 스마트폰 거치대 소싱 후보를 1688에서 찾아보고 비교해줘.
```

```text
@sourcing-agent-1688 이 페이지 자료 저장하고 manifest 경로 알려줘.
```

## 플러그인이 하는 일

- Chrome에 열린 1688 페이지 확인
- 상품명, 가격, 판매량, 옵션, 판매자 정보 추출
- 대표 이미지와 상세 이미지 추출
- Chrome 네트워크 응답에서 추가 상품 데이터 확인
- 저장 요청 시 HTML, 이미지, 속성 JSON, manifest 저장
- 한국어 키워드를 1688 검색용 중국어 키워드로 확장

## 저장 위치

기본 저장 위치는 사용자 홈 아래입니다.

```text
~/.sourcing1688/
  assets/
  data/
  raw/
```

## 삭제

Codex Desktop 플러그인 화면에서 제거합니다.

로컬 저장 데이터까지 지우려면:

```powershell
sourcing1688 uninstall --yes
```
