# 1688 Sourcing Agent

Codex Desktop에서 `@sourcing-agent-1688`로 Chrome에 열린 1688 상품 페이지를 읽고, 상품 분석과 이미지/영상 자료 저장을 도와주는 소싱 에이전트입니다. Windows와 macOS 둘 다 같은 설치 명령을 사용합니다.

사용자가 Chrome에서 보고 있는 1688 페이지의 화면, DOM, 네트워크 응답을 Codex가 함께 읽어서 상품 정보, 판매자 정보, 이미지, 영상 후보, 상세 자료를 정리합니다.

## 설치

아래 명령 하나만 실행하세요.

```powershell
uvx --from git+https://github.com/Squirbie/sourcing-agent-1688.git sourcing-agent-1688 install-codex
```

이 명령이 하는 일:

- Codex marketplace 등록
- `1688 Sourcing Agent` 플러그인 활성화
- 플러그인에 포함된 `sourcing1688`, `chrome-devtools` MCP 구성 설치
- 예전 설치에서 남은 전역 MCP 등록 정리
- 현재 OS에 맞는 방식으로 Chrome DevTools 연결 설정 페이지 열기

설치가 끝나면 Codex Desktop을 완전히 종료한 뒤 다시 켜고, 새 채팅에서 `@sourcing-agent-1688`를 선택하면 됩니다.

## 처음 한 번: Chrome 연결

설치 명령이 Chrome 연결 설정 페이지를 엽니다.

Chrome에서 연결을 허용한 뒤, 같은 Chrome 프로필로 1688 상품 페이지나 검색 페이지를 직접 열어두세요. 그 다음 Codex에서 `@sourcing-agent-1688`를 호출하면 됩니다.

첫 연결에서 Chrome이 원격 디버깅 허용창을 띄울 수 있습니다. 이때 바로 실패로 판단하지 말고 `Allow`를 누른 뒤 같은 요청을 다시 실행하면 됩니다. 플러그인 MCP 설정은 이 첫 허용을 기다릴 수 있게 Chrome DevTools 호출 시간을 길게 잡아둡니다.

필요하면 나중에 다시 열 수 있습니다.

```text
@sourcing-agent-1688 Chrome DevTools 연결 세팅 열어줘.
```

## 이렇게 쓰면 됩니다

```text
@sourcing-agent-1688 지금 Chrome에 열어둔 1688 상품을 셀러 입장에서 분석해줘.
```

```text
@sourcing-agent-1688 이 상품의 이미지, 옵션, 판매자 정보, 영상 자료 확인해줘.
```

```text
@sourcing-agent-1688 1688에서 스마트폰 거치대 소싱 후보 찾아보고 비교해줘.
```

```text
@sourcing-agent-1688 이 페이지 자료 저장하고 manifest 경로 알려줘.
```

## 플러그인이 하는 일

- Chrome에 열린 1688 페이지 확인
- 상품명, 가격, 판매량, 옵션, 판매자 정보 추출
- 대표 이미지, 상세 이미지, 영상 URL 추출
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

Codex 설정과 MCP 등록을 한 번에 지우려면:

```powershell
uvx --from git+https://github.com/Squirbie/sourcing-agent-1688.git sourcing-agent-1688 uninstall-codex
```

저장 데이터까지 같이 지우려면:

```powershell
uvx --from git+https://github.com/Squirbie/sourcing-agent-1688.git sourcing-agent-1688 uninstall-codex --remove-runtime
```
