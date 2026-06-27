---
doc_type: api_reference
plan_tier: all
product_area: events
doc_version: 1.0
---

# Events API

Subscribe to and query platform events.

## Event Types

| Event                  | Description                    |
|------------------------|--------------------------------|
| workflow.completed     | Workflow finished successfully |
| workflow.failed        | Workflow ended with error      |
| approval.requested     | Human approval needed          |
| user.invited           | New user invited               |
| integration.connected  | New integration authorized     |

## Querying Events

```
GET /v1/events?type=workflow.completed&since=2024-01-01T00:00:00Z
```

## Webhook Delivery

Configure webhooks to receive events in real-time. See the Webhooks API reference for delivery and retry details.
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
