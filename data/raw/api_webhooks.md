---
doc_type: api_reference
plan_tier: all
product_area: webhooks
doc_version: 1.0
---

# Webhooks API Reference

RelayBoard webhooks deliver real-time event notifications to your HTTPS endpoints.

## Authentication

Webhook management endpoints require OAuth 2.0 bearer tokens with the following scopes:

- `webhooks:read` — list and retrieve webhook configurations
- `webhooks:write` — create, update, and delete webhooks

Both scopes are required for full webhook lifecycle management. Read-only integrations may use `webhooks:read` alone.

## Retry Policy

When your endpoint returns a non-2xx status code or times out, RelayBoard automatically retries delivery.

**Maximum retry attempts: 5**

Retries use exponential backoff starting at 1 second, doubling each attempt (1s, 2s, 4s, 8s, 16s). After the fifth failed attempt, the event is marked as permanently failed and surfaced in the delivery log.

## Endpoint Requirements

Your endpoint must respond within 10 seconds with a 2xx status code. TLS 1.2 or higher is required.

## Event Types

Supported event types include `workflow.completed`, `workflow.failed`, `approval.requested`, and `user.invited`.

## Payload Signing

All webhook payloads include an `X-RelayBoard-Signature` header using HMAC-SHA256. Verify signatures using your webhook secret.

## Creating a Webhook

```
POST /v1/webhooks
{
  "url": "https://example.com/hooks/relayboard",
  "events": ["workflow.completed"],
  "secret": "whsec_..."
}
```

## Listing Webhooks

```
GET /v1/webhooks
```

Returns paginated webhook configurations for your workspace.
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
