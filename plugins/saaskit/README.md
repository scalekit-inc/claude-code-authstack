# SaaSKit for Claude Code

## Purpose
This plugin brings Scalekit SaaSKit into Claude Code so agents can build production-ready B2B authentication into web applications. It covers the entire auth lifecycle: login, sessions, SSO, SCIM provisioning, RBAC, MCP server auth, and API key management across Node.js, Python, Go, Java, and PHP frameworks.

Canonical content lives in:
- `docs/` for durable SaaSKit knowledge (auth flows, sessions, SSO, SCIM, etc.)
- `docs/frameworks/` for framework-specific guides (Python, Next.js, Go, Spring Boot, Laravel)
- `skills/` for task-oriented workflows (thin routing layers into docs/)
- `rules/` for cross-cutting guidance (terminology, redirect URLs)

Claude runtime files:
- `.claude-plugin/`
- `commands/` for slash-command aliases
- `hooks/`
- `agents/`
- `references/`

## Installation

Run the install script (macOS/Linux):
```sh
curl -fsSL https://raw.githubusercontent.com/scalekit-inc/claude-code-authstack/main/scripts/install.sh | bash
```

Or inside Claude Code, run:
```
/plugin install saaskit@scalekit-auth-stack
```

Official Scalekit docs:
- [LLM docs map](https://docs.scalekit.com/llms.txt)
- [Full-stack auth quickstart](https://docs.scalekit.com/authenticate/fsa/quickstart/)
- [Modular SSO guide](https://docs.scalekit.com/authenticate/sso/add-modular-sso/)
- [SCIM directory sync](https://docs.scalekit.com/directory/scim/quickstart/)
- [MCP Auth quickstart](https://docs.scalekit.com/authenticate/mcp/quickstart/)

## Skills Reference
- `/saaskit:setup`
  New to SaaSKit? Start here — answers 3 questions and routes you to the right skill.
- `/saaskit:implementing-saaskit` — Core auth flow: login, signup, callback, token exchange, logout. Framework reference files for Go, Spring Boot, Laravel.
- `/saaskit:managing-saaskit-sessions` — Secure session storage, token refresh middleware, session revocation.
- `/saaskit:implementing-access-control` — RBAC and permission checks using Scalekit access tokens.
- `/saaskit:implementing-saaskit-python` — Auth for Django, FastAPI, or Flask using scalekit-sdk-python.
- `/saaskit:implementing-saaskit-nextjs` — Auth for Next.js App Router using @scalekit-sdk/node.
- `/saaskit:implementing-modular-sso` — Enterprise SSO (SAML/OIDC), IdP-initiated login, admin portal.
- `/saaskit:implementing-scim-provisioning` — SCIM webhooks, user/group lifecycle, directory API.
- `/saaskit:adding-mcp-oauth` — OAuth 2.1 for MCP servers. Reference files for FastMCP, Express, FastAPI.
- `/saaskit:adding-api-auth` — API keys (org/user scoped) and OAuth 2.0 client credentials.
- `/saaskit:migrating-to-saaskit` — Migration planning from Auth0, Firebase, Cognito, or custom auth.
- `/saaskit:production-readiness-saaskit` — Unified production checklist across all SaaSKit domains.
- `/saaskit:testing-auth-setup` — Validates auth configuration end-to-end using the Scalekit dryrun CLI.
- `/saaskit:scalekit-code-doctor` — Diagnoses SDK usage issues, import errors, and common mistakes across AgentKit and SaaSKit.

## Configuration
Required environment variables:
- `SCALEKIT_ENVIRONMENT_URL`
- `SCALEKIT_CLIENT_ID`
- `SCALEKIT_CLIENT_SECRET`

Get these from [app.scalekit.com](https://app.scalekit.com): Developers → Settings → API Credentials.

See [`.env.example`](.env.example) for a template.

## Usage Examples

### Add login to a Next.js app
```
/saaskit:implementing-saaskit-nextjs
```
The skill detects your Next.js project and guides you through adding Scalekit auth routes, middleware, and session management.

### Add SSO for enterprise customers
```
/saaskit:implementing-modular-sso
```
Adds SAML/OIDC SSO with self-serve configuration via the admin portal iframe.

### Secure an MCP server
```
/saaskit:adding-mcp-oauth
```
Adds OAuth 2.1 authorization middleware to your MCP server (Node.js or Python).

## Troubleshooting

1. **Redirect URL mismatch** — The `redirect_uri` in your authorization request must exactly match a URL registered in the Scalekit dashboard. Check for trailing slash, scheme, and port mismatches.
2. **Token refresh fails** — Ensure the refresh token is stored securely (encrypted, HttpOnly cookie) and hasn't expired. Check `SCALEKIT_ENVIRONMENT_URL` is correct.
3. **SSO callback returns error** — Verify the SSO connection is active in the Scalekit dashboard and the IdP metadata (ACS URL, Entity ID) matches your app configuration.

## Security

- Store `SCALEKIT_CLIENT_SECRET` in environment variables or a secrets manager. Never commit it to version control.
- All tokens (access, refresh, ID) should be stored in HttpOnly, Secure, SameSite cookies or encrypted server-side storage.
- Validate access tokens on every request before trusting embedded roles/permissions.
- Use the admin portal iframe for customer self-serve SSO configuration rather than building custom SSO management UI.