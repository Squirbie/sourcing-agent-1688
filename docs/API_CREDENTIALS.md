# 1688 API Credentials

1688 API credentials are issued from `open.1688.com / 1688开放平台`.

Short flow:

1. Log in with a 1688 account.
2. Create an app in the Open Platform console.
3. Check the app AppKey and AppSecret after review.
4. Apply for or bind the required API permissions/solutions if your account needs them.
5. Prepare an OAuth access token or refresh token.
6. Store credentials in environment variables or local token cache.

```env
ALI1688_APP_KEY=
ALI1688_APP_SECRET=
ALI1688_REFRESH_TOKEN=
ALI1688_ACCESS_TOKEN=
SOURCING1688_HOME=
```

Helper commands:

```powershell
sourcing1688 auth status --json
sourcing1688 auth url --redirect-uri "https://example.com/callback" --json
sourcing1688 auth exchange --code CODE --redirect-uri "https://example.com/callback" --json
```

The CLI never prints raw token values. Token cache is stored under:

```text
SOURCING1688_HOME/token-cache/.1688_token_cache.json
```

Common statuses:

- `missing_credentials`: AppKey/AppSecret/token is missing.
- `no_api_permission`: app/account lacks the required API permission or solution.
- `invalid_app_secret`: AppSecret is wrong or mismatched.
- `token_expired`: access token expired and refresh did not succeed.
- `refresh_token_expired`: refresh token expired or was revoked.
- `redirect_uri_mismatch`: redirect URI differs from the app setting.

Always check the official 1688 Open Platform docs for the latest UI, permissions, and OAuth details. If API setup is not ready, use `browser` or `local_html` workflows where appropriate.
