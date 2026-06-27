---
doc_type: admin_guide
plan_tier: all
product_area: audit
doc_version: 1.0
---

# Audit Logs

Audit logs capture security-relevant events across your RelayBoard workspace.

## What Is Logged

Audit events include:

- User login and logout (success and failure)
- Permission changes and role assignments
- API key creation and revocation
- Workflow publish and unpublish
- SSO configuration changes
- Data export requests

## Retention by Plan

| Plan       | Audit Log Retention |
|------------|---------------------|
| Starter    | 30 days             |
| Pro        | 90 days             |
| Enterprise | 365 days            |

**Pro plan audit logs are retained for 90 days.**
**Enterprise plan audit logs are retained for 365 days.**

After the retention period, logs are permanently deleted and cannot be recovered.

## Accessing Audit Logs

Navigate to Settings → Security → Audit Logs. Enterprise customers can also stream logs to a SIEM via the log streaming integration.

## Export

Audit logs can be exported as CSV or JSON. Exports are limited to 10,000 events per request.

## Log Streaming

Enterprise customers can configure real-time log streaming to Splunk, Datadog, or a custom HTTPS endpoint.

## Search and Filter

Filter audit logs by actor, event type, date range, and IP address. Full-text search is available on Enterprise.
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
