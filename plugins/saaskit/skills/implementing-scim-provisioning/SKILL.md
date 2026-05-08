---
name: implementing-scim-provisioning
description: Implements SCIM user provisioning using Scalekit directory API and webhooks for real-time user and group lifecycle management. Use when adding directory sync, user provisioning, or automated user lifecycle management.
---

# SaaSKit SCIM Provisioning

Implements automated user and group lifecycle management via SCIM directory sync and Scalekit webhooks.

## What SCIM covers

SCIM (System for Cross-domain Identity Management) automates the user lifecycle between an enterprise IdP and your app:

- **User provisioning** — new users in the IdP are automatically created in your app.
- **User deprovisioning** — removed users are deactivated (prefer deactivation over hard delete).
- **Profile updates** — name, email, and attribute changes sync automatically.
- **Group sync** — IdP groups map to roles/permissions in your app.

## Webhook setup overview

Scalekit delivers SCIM events to your webhook endpoint in real time:

1. **Register** a webhook endpoint in Scalekit dashboard or via SDK.
2. **Validate** every request using the webhook signature (HMAC).
3. **Handle** these event types:

| Event | Action |
|---|---|
| `user_created` | Create user in your DB, assign default role |
| `user_updated` | Update profile fields |
| `user_deleted` | Deactivate user (don't hard delete) |
| `group_created` | Create role/group mapping |
| `group_updated` | Update role assignments |
| `group_deleted` | Remove role mapping |

4. **Return 2xx quickly** — offload heavy processing to a background queue.
5. **Handle idempotently** — duplicate events must not create duplicate records.

## Retry behavior

Scalekit retries on non-2xx responses with exponential backoff (up to 8 attempts over ~10 hours).

## Integration with SSO

SCIM provisioning works alongside SSO — SSO handles authentication, SCIM handles the user lifecycle. For enterprises that use both, configure SCIM first so users exist before their first SSO login.

## Deep reference

- SCIM patterns and code: [../../docs/scim.md](../../docs/scim.md)
- SSO (complementary feature): [../../docs/sso.md](../../docs/sso.md)
- Access control (role mapping from groups): [../../docs/access-control.md](../../docs/access-control.md)

## When to switch skills

- Use `implementing-modular-sso` for SSO configuration alongside SCIM.
- Use `implementing-access-control` for mapping SCIM groups to app permissions.
- Use `production-readiness-saaskit` to validate SCIM webhooks before launch.
