# Terminology

Use these terms consistently in user-facing documentation and skills:

- `SaaSKit`: the Scalekit product for B2B SaaS authentication (login, sessions, SSO, SCIM, RBAC). Previously called `Full Stack Auth` or `FSA`.
- `Modular SSO`: enterprise SSO integration where the app manages its own users and sessions. Scalekit handles only the SSO handshake.
- `Full Stack Auth`: Scalekit manages the entire auth lifecycle (login, sessions, users). Also referred to as `SaaSKit` in current docs.
- `SCIM provisioning`: directory sync for automatic user and group lifecycle management via webhooks.
- `Admin portal`: customer-facing iframe for self-serve SSO and SCIM configuration.
- `MCP server auth`: OAuth 2.1 authorization for Model Context Protocol servers.

## Preferred wording

- Prefer `SaaSKit` over `FSA` or `Full Stack Auth` in new content.
- Use `Modular SSO` when the app manages its own sessions. Use `SaaSKit SSO` when Scalekit manages everything.
- Do not mix `AgentKit` terminology in SaaSKit contexts. AgentKit is about agent-to-tool authentication via connectors.

## Why this rule exists

The product naming shifted from feature-specific names (`Full Stack Auth`, `Modular SSO`) to kit-based names (`SaaSKit`, `AgentKit`). This rule keeps the SaaSKit plugin aligned with current docs at `docs.scalekit.com/llms.txt`.