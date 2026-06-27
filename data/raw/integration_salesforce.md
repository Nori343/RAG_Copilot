---
doc_type: integration
plan_tier: enterprise
product_area: salesforce
doc_version: 1.0
---

# Salesforce Integration

Connect RelayBoard workflows to Salesforce objects and events.

## Setup

Install the RelayBoard managed package from the Salesforce AppExchange, then connect via OAuth.

## Triggers

- Record created or updated (Account, Contact, Opportunity, Case)
- Platform events

## Actions

- Create or update records
- Query SOQL
- Send email alerts

## Enterprise Features

Bulk API support and custom object mapping require Enterprise plan.
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
