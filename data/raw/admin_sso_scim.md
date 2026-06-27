---
doc_type: admin_guide
plan_tier: enterprise
product_area: identity
doc_version: 1.0
---

# SSO and SCIM Administration

Enterprise workspaces can configure single sign-on and automated user provisioning.

## Single Sign-On (SSO)

**SSO is available on the Enterprise plan only.**

RelayBoard supports SAML 2.0 identity providers including Okta, Azure AD, Google Workspace, and OneLogin.

### Configuring SSO

1. Navigate to Settings → Security → SSO
2. Upload your IdP metadata XML or enter the SSO URL and certificate manually
3. Configure attribute mapping for email, first name, and last name
4. Enable SSO enforcement to require SAML for all users

### SSO Enforcement

When enforcement is enabled, password login is disabled for all workspace members. Break-glass admin accounts can be configured for emergency access.

## SCIM Provisioning

**SCIM 2.0 provisioning is available on the Enterprise plan only.**

SCIM enables automatic user and group synchronization from your identity provider.

### SCIM Endpoints

- Base URL: `https://api.relayboard.io/scim/v2`
- Bearer token: generated in Settings → Security → SCIM

### Supported Operations

- Create, update, and deactivate users
- Sync group memberships
- Push role assignments based on IdP groups

## Just-in-Time Provisioning

JIT provisioning automatically creates RelayBoard accounts on first SSO login when the user's email domain matches a verified domain.

## Domain Verification

Add DNS TXT records to verify ownership of email domains before enabling JIT or SSO enforcement.
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
