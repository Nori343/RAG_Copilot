---
doc_type: pricing
plan_tier: all
product_area: pricing
doc_version: 1.0
---

# Plans and Pricing

RelayBoard offers three plans to fit teams of all sizes.

## Starter — $29/user/month

- Up to 10 workflows
- 100 API requests per minute
- 30-day audit log retention
- Email support

## Pro — $79/user/month

- Unlimited workflows
- 1000 API requests per minute
- 90-day audit log retention
- Priority email support
- Jira integration

## Enterprise — Custom pricing

- Unlimited everything
- 10000 API requests per minute
- 365-day audit log retention
- SSO and SCIM
- HIPAA BAA (US region)
- Dedicated support and SLA

Contact sales@relayboard.io for Enterprise pricing.
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
