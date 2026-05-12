# 참고한 오픈소스와 문서

이 프로젝트는 아래 공개 repo와 문서를 구조, 필드명, 워크플로 참고용으로 봤습니다. 코드를 그대로 복사하지 않았고, 구현은 이 repo의 provider/model/test 구조에 맞춰 새로 작성했습니다.

## 플러그인/에이전트 문서

- Claude Code plugin docs: https://code.claude.com/docs/en/plugins
- Claude Code plugin marketplace docs: https://code.claude.com/docs/en/plugin-marketplaces
- OpenClaw plugin bundle docs: https://docs.openclaw.ai/plugins/bundles

## 1688 관련 참고 repo

- OpenClaw 1688 product search skill: https://github.com/openclaw/skills/tree/main/skills/1688aiinfra/1688-product-search
  - API형 검색, field normalization, sort/filter 설계 참고
- OpenClaw 1688 ranking skill: https://github.com/openclaw/skills/tree/main/skills/1688aiinfra/1688-ranking
  - 인기 키워드와 랭킹 workflow 참고
- jiyun/1688: https://github.com/jiyun/1688
  - 저장된 상세페이지 HTML, 이미지/영상/속성 추출 workflow 참고
- resphinas/1688-selenium-spider: https://github.com/resphinas/1688-selenium-spider
  - 브라우저 기반 페이지 확인과 AJAX response 관찰 아이디어 참고
- MarketSpider: https://github.com/zhangjiancong/MarketSpider
  - 검색 결과 필드와 브라우저 workflow 참고
- jeff2go/1688-Crawler: https://github.com/jeff2go/1688-Crawler
  - API endpoint style 참고
- search1688api: https://github.com/netkaruma/search1688api
  - text/image search interface 참고

## 공식 1688 Open Platform

- https://open.1688.com/console
- https://open.1688.com/doc/apiInvoke.htm
- https://open.1688.com/doc/signature.htm
- https://open.1688.com/doc/apiAuth.htm

API provider는 fixture 기반 테스트와 response normalization을 포함합니다. 실제 계정 권한과 token 설정은 사용자의 1688 Open Platform 환경에서 확인해야 합니다.
