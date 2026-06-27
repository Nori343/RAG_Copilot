---
doc_type: security
plan_tier: enterprise
product_area: compliance
doc_version: 1.0
---

# Data Residency and Compliance

RelayBoard maintains strict data handling practices for regulated industries.

## Data Residency

Enterprise customers can select their data residency region during onboarding:

- **US** — data stored in AWS us-east-1
- **EU** — data stored in AWS eu-west-1
- **APAC** — data stored in AWS ap-southeast-1

All customer data, including workflow definitions, execution logs, and file attachments, resides in the selected region.

## HIPAA Business Associate Agreement

**A HIPAA Business Associate Agreement (BAA) is available for Enterprise customers in the US region only.**

To request a BAA:

1. Contact your account executive or support@relayboard.io
2. Complete the HIPAA configuration checklist in the admin console
3. Enable encryption-at-rest and audit logging (enabled by default on Enterprise)

RelayBoard's HIPAA environment includes access controls, audit trails, and automatic session timeouts compliant with HIPAA technical safeguards.

## SOC 2 Type II

RelayBoard maintains SOC 2 Type II certification. Reports are available to Enterprise customers under NDA.

## Encryption

- At rest: AES-256
- In transit: TLS 1.2+
- Key management: AWS KMS with customer-managed keys available on Enterprise

## Data Retention

Default data retention follows your plan's audit log settings. Custom retention policies are available on Enterprise.
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
