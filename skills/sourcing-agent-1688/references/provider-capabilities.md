# Provider Capabilities

| Provider | Source type | Search | Detail | Download | Hot keywords | Rankings | Image search | Parse HTML | Live verified | Required env |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| auto | auto | api first, then browser | api first, then browser | api first, then browser | api/browser status | api/browser status | api if configured | no | no | API credentials or browser profile login |
| api | api | yes | yes | yes via detail assets | yes | yes | yes | no | no | `ALI1688_APP_KEY`, `ALI1688_APP_SECRET`, `ALI1688_REFRESH_TOKEN` or `ALI1688_ACCESS_TOKEN` |
| browser | browser | yes | yes | yes via detail parser | live_not_verified | live_not_verified | no | rendered page | no | optional; defaults to `SOURCING1688_HOME/browser-profile` |
| local_html | local_html | no | yes from file | yes | no | no | no | yes | yes | local HTML path |

If API credentials are missing, `auto` should route to `browser`. If the browser profile is missing, return `needs_human_login` and ask the user to open the browser profile login flow.
