---
name: implementing-saaskit
description: Implements Scalekit SaaSKit authentication (sign-up, login, logout, sessions) using JWT tokens across Node.js, Python, Go, Java, or PHP. Use when building or integrating user authentication with Scalekit, setting up OAuth callbacks, token refresh, or session handling.
---

# SaaSKit Authentication

Use this skill as the auth integration entrypoint. It should stay thin and route into the canonical docs in `docs/`.

## Mental model

SaaSKit is Scalekit-managed login, session, and RBAC for SaaS apps. Scalekit acts as an OIDC/OAuth 2.0 provider — your app implements the authorization code flow against it. The SDK handles token exchange, validation, and refresh.

Key concepts:
- **Auth URL**: Scalekit-hosted login page your app redirects to
- **Callback**: Your endpoint that receives the authorization code
- **Access token**: JWT carrying user identity, org, roles, and permissions
- **Refresh token**: Long-lived token used to renew access tokens silently

## Default workflow

1. Set `SCALEKIT_ENV_URL`, `SCALEKIT_CLIENT_ID`, `SCALEKIT_CLIENT_SECRET` in env.
2. Initialize the SDK client (once, at startup).
3. Build the authorization URL and redirect the user to Scalekit.
4. Handle the callback — exchange the code for tokens.
5. Store tokens in a secure session (httpOnly cookies or server-side store).
6. On logout, clear the session and redirect to Scalekit's end-session endpoint.

## Quick skeleton

### Node.js
```bash
npm install @scalekit-sdk/node
```
```typescript
import { ScalekitClient } from '@scalekit-sdk/node';
const sc = new ScalekitClient(
  process.env.SCALEKIT_ENV_URL!,
  process.env.SCALEKIT_CLIENT_ID!,
  process.env.SCALEKIT_CLIENT_SECRET!
);
// Step 3 — redirect to auth URL
// Step 4 — sc.authenticateWithCode(code, redirectUri)
// Step 5 — store tokens in session
// Step 6 — sc.getLogoutUrl(options)
```

### Python
```bash
pip install scalekit-sdk-python
```
```python
from scalekit import ScalekitClient
sc = ScalekitClient(env_url, client_id, client_secret)
# Same 6-step flow — see docs/auth-flows.md for full patterns
```

## Framework-specific references

- Go (Gin): [go-reference.md](go-reference.md)
- Spring Boot: [springboot-reference.md](springboot-reference.md)
- Laravel: [laravel-reference.md](laravel-reference.md)
- Python (Django/FastAPI/Flask): use `implementing-saaskit-python` skill
- Next.js: use `implementing-saaskit-nextjs` skill

## Deep reference

- Auth flows: [../../docs/auth-flows.md](../../docs/auth-flows.md)
- Sessions: [../../docs/sessions.md](../../docs/sessions.md)
- Access control: [../../docs/access-control.md](../../docs/access-control.md)
- API auth: [../../docs/api-auth.md](../../docs/api-auth.md)
- All frameworks: [../../docs/frameworks/](../../docs/frameworks/)

## When to switch skills

- Use `managing-saaskit-sessions` for token storage, refresh middleware, and session auditing.
- Use `implementing-access-control` for RBAC and permission enforcement.
- Use `migrating-to-saaskit` when replacing an existing auth system.
- Use `production-readiness-saaskit` before going live.
