---
name: implementing-modular-sso
description: Implements enterprise SSO and authentication flows using Scalekit, including modular SSO (SAML/OIDC), IdP-initiated login, and admin portal for self-serve configuration. Use when adding SSO, integrating identity providers like Okta or Azure AD, or embedding the Scalekit admin portal.
---

# SaaSKit Enterprise SSO

Implements enterprise SSO (SAML/OIDC) via Scalekit's modular SSO feature, including IdP-initiated login and the self-serve admin portal.

## When to use

- Enterprise customers require SSO with their identity provider (Okta, Azure AD, Google Workspace, etc.).
- You need to support both SP-initiated and IdP-initiated login flows.
- You want a self-serve admin portal where customer IT admins configure SSO themselves.

## SSO flow overview

### SP-initiated (your app starts the login)

```
User clicks login → Your app → Scalekit (with organization_id or connection_id)
  → IdP (Okta, Azure AD, etc.) → Scalekit callback → Your app callback
```

### IdP-initiated (IdP starts the login)

```
User clicks app tile in IdP → Scalekit (signed JWT) → Your app's IdP-initiated handler
  → Build auth URL with claims → Scalekit → IdP → Callback → Your app
```

## Key integration points

1. **Authorization URL** — pass `organization_id` or `connection_id` to scope to the right SSO connection.
2. **Callback handler** — same as standard auth; SSO tokens contain the same claims.
3. **IdP-initiated handler** — validate the signed JWT from Scalekit, extract org/connection hints, redirect to auth URL.
4. **Admin portal** — embed or link to Scalekit's admin portal for self-serve SSO configuration.

## Admin portal

The admin portal lets your enterprise customers configure SSO without your intervention:

- Generate a portal link via the SDK: `sc.organization.generatePortalLink(orgId)`
- Embed it in your app's settings page or send it to the customer's IT admin.
- Customers can configure SAML/OIDC connections, test them, and manage user attribute mapping.

## Deep reference

- SSO patterns and code: [../../docs/sso.md](../../docs/sso.md)
- Auth flows (shared callback): [../../docs/auth-flows.md](../../docs/auth-flows.md)
- Framework-specific IdP-initiated handling: [../../docs/frameworks/](../../docs/frameworks/)

## When to switch skills

- Use `implementing-saaskit` for the base auth flow that SSO builds on.
- Use `implementing-scim-provisioning` for automated user provisioning alongside SSO.
- Use `production-readiness-saaskit` to validate SSO configuration before launch.
