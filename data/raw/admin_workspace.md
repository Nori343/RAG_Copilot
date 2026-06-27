---
doc_type: admin_guide
plan_tier: all
product_area: workspace
doc_version: 1.0
---

# Workspace Administration

Manage your RelayBoard workspace settings and members.

## Workspace Settings

Configure workspace name, logo, and default timezone in Settings → General.

## Member Management

Invite members via email or bulk CSV import (Pro and Enterprise). Set default roles for new members.

## Billing

View current plan, usage, and invoices in Settings → Billing. Upgrade or downgrade plans at any time.

## Deletion

Workspace deletion requires owner confirmation and a 14-day grace period. All data is permanently removed after the grace period.
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

## Monitoring and Observability

Track these metrics for healthy RelayBoard integrations:

- API response latency (p50, p95, p99)
- Webhook delivery success rate
- Workflow execution duration and failure rate
- Rate limit utilization percentage
- Authentication failure count

RelayBoard provides execution logs in the dashboard and via the API. Enterprise customers can stream
metrics to Datadog, Prometheus, or CloudWatch using the observability integration.
