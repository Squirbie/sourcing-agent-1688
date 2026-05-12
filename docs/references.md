# References and Credits

This project uses the following public repositories as design references. Code was not copied from these repositories; only public workflow ideas, field names, endpoint naming, and safety lessons were used.

## Referenced Repositories

- Claude Code plugin docs: https://code.claude.com/docs/en/plugins
  - Used for `.claude-plugin/plugin.json`, root `skills/`, and root `.mcp.json` packaging shape.

- Claude Code plugin marketplace docs: https://code.claude.com/docs/en/plugin-marketplaces
  - Used for marketplace install wording and the `.claude-plugin/marketplace.json` distribution model.

- OpenClaw plugin bundle docs: https://docs.openclaw.ai/plugins/bundles
  - Used for Codex/Claude bundle compatibility notes and stdio MCP bundle expectations.

- OpenClaw 1688 product search skill: https://github.com/openclaw/skills/tree/main/skills/1688aiinfra/1688-product-search
  - Used for API-style endpoint naming, token-cache workflow, keyword search, image search, detail, sort/filter names, language/country caveats, and field normalization ideas.
  - License observed: MIT in `openclaw/skills`.

- OpenClaw 1688 ranking skill: https://github.com/openclaw/skills/tree/main/skills/1688aiinfra/1688-ranking
  - Used for ranking and hot keyword API concepts, ranking types, and top keyword fields.
  - License observed: MIT in `openclaw/skills`.

- jiyun/1688: https://github.com/jiyun/1688
  - Used for local rendered HTML and SingleFile-style workflow ideas: extract main/detail/option images, videos, attributes, SKU/price data, DuckDB storage, manifests, and local packaging.
  - License observed: GPL-3.0. No code was copied.

- resphinas/1688-selenium-spider: https://github.com/resphinas/1688-selenium-spider
  - Used only as historical context for Selenium/browser automation and AJAX parsing ideas.
  - License not confirmed in this implementation pass.

- MarketSpider: https://github.com/zhangjiancong/MarketSpider
  - Used for browser workflow, search result field ideas, and privacy warnings around cookies, LocalStorage, logs, and account data.
  - License not confirmed from a standard license file during this pass.

- jeff2go/1688-Crawler: https://github.com/jeff2go/1688-Crawler
  - Used only for API endpoint style and crawler architecture context.
  - License not confirmed in this implementation pass.

- search1688api: https://github.com/netkaruma/search1688api
  - Used for text/image search interface ideas.
  - License not confirmed in this implementation pass.

## Official 1688/Open Platform Notes

OpenClaw references the 1688 Open Platform docs for API invocation, signatures, authorization, console, and solution subscription:

- https://open.1688.com/console
- https://open.1688.com/doc/apiInvoke.htm
- https://open.1688.com/doc/signature.htm
- https://open.1688.com/doc/apiAuth.htm

The current API client is live-capable and fixture tested, but live credentials were not available here. Signature behavior is implemented conservatively and marked `live_verified=false` until verified with a real 1688 app and subscribed solution.

## Safety Policy

- Do not implement CAPTCHA bypass, verification bypass, anti-bot evasion, stealth automation, proxy rotation, or credential/cookie extraction.
- If login, verification, or blocking is detected, return structured status such as `needs_human_login`, `blocked_by_verification`, `provider_unavailable`, or `live_not_verified`.
- Do not log tokens, cookies, browser profile contents, or private account data.
- Keep searches small and targeted; this is an agent sourcing tool, not a bulk crawler.

## Live Integration Uncertainty

Mock and local HTML workflows are fixture verified. API and browser providers are implemented for real use but are not live verified in this environment because no 1688 API credentials or logged-in browser profile were available.
