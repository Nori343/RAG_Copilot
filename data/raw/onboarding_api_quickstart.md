---
doc_type: onboarding
plan_tier: all
product_area: api
doc_version: 1.0
---

# API Quickstart

Get started with the RelayBoard REST API in minutes.

## 1. Generate an API Key

Settings → API Keys → Create Key. Copy the key immediately — it won't be shown again.

## 2. Make Your First Request

```bash
curl -H "Authorization: Bearer rb_live_xxx" \
  https://api.relayboard.io/v1/workflows
```

## 3. Handle Rate Limits

Check `X-RateLimit-Remaining` in response headers. Implement exponential backoff on 429 responses.

## 4. Use the SDK

Official SDKs are available for Python, Node.js, and Go.

```python
from relayboard import Client
client = Client(api_key="rb_live_xxx")
workflows = client.workflows.list()
```

## Pagination

List endpoints return cursor-based pagination. Use the `cursor` parameter for subsequent pages.
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
