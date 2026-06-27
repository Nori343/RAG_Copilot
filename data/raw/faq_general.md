---
doc_type: onboarding
plan_tier: all
product_area: faq
doc_version: 1.0
---

# Frequently Asked Questions

## General

**Q: What is RelayBoard?**
A: RelayBoard is a B2B workflow automation platform for dev-tools and operations teams.

**Q: Is there a free trial?**
A: Yes, 14-day free trial on Pro features. No credit card required.

**Q: Can I change plans?**
A: Yes, upgrade or downgrade anytime from Settings → Billing.

## Webhooks

**Q: How many times will RelayBoard retry a failed webhook?**
A: RelayBoard retries failed deliveries several times before giving up. Check the Webhooks API reference for exact retry behavior.

**Q: What OAuth scopes do webhooks need?**
A: Webhook endpoints typically require read and write scopes. See the API documentation for details.

## Security

**Q: Is RelayBoard SOC 2 certified?**
A: Yes, SOC 2 Type II. Reports available to Enterprise customers.

**Q: Do you support SSO?**
A: SSO is available on higher-tier plans. Contact sales for details.
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
