# Provider Capabilities

| Provider | Source type | Search | Detail | Download | Hot keywords | Rankings | Image search | Parse HTML | Live verified | Required env |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| auto | auto | live provider only | live provider only | live provider only | live provider only | live provider only | api if configured | no | no | API credentials or `SOURCING1688_BROWSER_PROFILE` |
| mock | mock | yes | yes | yes | fixture | fixture | fixture | no | yes | none |
| api | api | yes | yes | yes via detail assets | yes | yes | yes | no | no | `ALI1688_APP_KEY`, `ALI1688_APP_SECRET`, `ALI1688_REFRESH_TOKEN` or `ALI1688_ACCESS_TOKEN` |
| browser | browser | yes | yes | yes via detail parser | live_not_verified | live_not_verified | no | rendered page | no | `SOURCING1688_BROWSER_PROFILE` |
| local_html | local_html | no | yes from file | yes | no | no | no | yes | yes | local HTML path |

Do not silently fall back from a selected live provider to mock. If API/browser access fails, return the provider's structured status. `auto` must return `provider_unavailable` with `error.code=missing_live_provider` when no live provider is configured.
