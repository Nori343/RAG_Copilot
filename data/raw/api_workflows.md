---
doc_type: api_reference
plan_tier: all
product_area: workflows
doc_version: 1.0
---

# Workflows API

Create, manage, and execute RelayBoard workflows programmatically.

## Endpoints

```
GET    /v1/workflows
POST   /v1/workflows
GET    /v1/workflows/{id}
PUT    /v1/workflows/{id}
DELETE /v1/workflows/{id}
POST   /v1/workflows/{id}/execute
```

## Workflow Schema

Workflows are defined as JSON graphs with nodes and edges. Each node has a `type` (trigger, action, condition) and `config` object.

## Execution

Trigger execution via API or schedule. Executions return an `execution_id` for status polling.

```
GET /v1/executions/{execution_id}
```

## Versioning

Workflows support draft and published versions. Only published versions can be triggered in production.

## Permissions

Requires `workflows:read` for GET operations and `workflows:write` for mutations.
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
