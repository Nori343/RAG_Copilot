---
doc_type: api_reference
plan_tier: all
product_area: authentication
doc_version: 1.0
---

# API Authentication

RelayBoard uses OAuth 2.0 and API keys for programmatic access.

## OAuth 2.0

Use the authorization code flow for user-delegated access. Token endpoints are at `https://auth.relayboard.io/oauth/token`.

## API Keys

Server-to-server integrations can use API keys prefixed with `rb_live_` or `rb_test_`. Keys are scoped to a workspace.

## Rate Limits

Rate limits apply per API key or OAuth token, measured per minute.

| Plan       | Rate Limit        |
|------------|-------------------|
| Starter    | 100 req/min       |
| Pro        | 1000 req/min      |
| Enterprise | 10000 req/min     |

When you exceed your limit, the API returns HTTP 429 with a `Retry-After` header.

## Rate Limit Headers

Every response includes:

- `X-RateLimit-Limit` — your plan's per-minute limit
- `X-RateLimit-Remaining` — requests remaining in the current window
- `X-RateLimit-Reset` — Unix timestamp when the window resets

## Token Refresh

Access tokens expire after 3600 seconds. Use the refresh token to obtain a new access token without user interaction.

## Scopes

Common scopes include `workflows:read`, `workflows:write`, `users:read`, `webhooks:read`, and `webhooks:write`.
## Best Practices

Follow these recommendations when implementing RelayBoard integrations in production environments.

Always use idempotency keys for mutating API requests to prevent duplicate operations during retries.
Store API keys in a secrets manager rather than environment variables in source code.
Enable audit logging and review logs regularly for anomalous access patterns.
Use webhook signature verification on every inbound payload before processing.
Implement circuit breakers for downstream services called from workflow actions.
Test workflows in draft mode before publishing to production.
Monitor API rate limit headers and implement client-side throttling.
Document your workflow dependencies and maintain runbooks for failure scenarios.

## Error Handling

RelayBoard APIs return standard HTTP status codes with structured error bodies.

| Code | Meaning |
|------|---------|
| 400  | Bad request — invalid parameters |
| 401  | Unauthorized — missing or invalid credentials |
| 403  | Forbidden — insufficient permissions |
| 404  | Not found — resource does not exist |
| 429  | Rate limited — retry after delay |
| 500  | Internal server error — contact support |

Error responses include a `code`, `message`, and optional `details` array with field-level validation errors.
Always log the `X-Request-Id` header when reporting issues to support for faster resolution.
