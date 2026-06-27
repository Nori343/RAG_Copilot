---
doc_type: onboarding
plan_tier: all
product_area: troubleshooting
doc_version: 1.0
---

# Troubleshooting Guide

## Webhook Delivery Issues

If webhooks aren't arriving:

1. Verify your endpoint returns 2xx within 10 seconds
2. Check the delivery log in Settings → Webhooks → Delivery Log
3. Ensure your firewall allows inbound HTTPS from RelayBoard IPs
4. Verify TLS certificate is valid and not self-signed

RelayBoard will retry failed deliveries automatically. If problems persist after multiple retries, check your endpoint logs.

## API Rate Limiting

If you receive HTTP 429:

1. Check your current plan's rate limit
2. Implement request queuing or backoff
3. Consider upgrading if you consistently hit limits

## SSO Login Failures

1. Verify IdP metadata is current
2. Check attribute mapping matches your IdP configuration
3. Ensure the user's email domain is verified
4. Contact support if SAML assertion validation fails

## Workflow Execution Errors

Check the execution log for node-level error details. Common issues include expired integration tokens and invalid JSON in HTTP action bodies.
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
