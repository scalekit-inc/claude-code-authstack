---
name: adding-mcp-oauth
description: Adds OAuth 2.1 authorization to Model Context Protocol servers using Scalekit. Covers Streamable HTTP transport, token validation middleware, and scope-based authorization for Node.js and Python. Use when securing MCP servers, implementing authentication for AI hosts like Claude Desktop or Cursor.
---

# SaaSKit MCP Server Auth

Adds OAuth 2.1 authorization to MCP servers using Scalekit for token validation and scope enforcement.

## Critical prereqs

- **Streamable HTTP transport only** — MCP OAuth requires HTTP. The stdio transport does not support authentication.
- **Scalekit MCP server registration** — register your server in Dashboard > MCP Servers to get a `resource_id`.
- **HTTPS in production** — token validation requires secure transport.

## Setup workflow

1. Register MCP server in Scalekit dashboard (get `resource_id`).
2. Set env vars: `SCALEKIT_ENV_URL`, `SCALEKIT_CLIENT_ID`, `SCALEKIT_CLIENT_SECRET`, `SCALEKIT_RESOURCE_ID`.
3. Add token validation middleware (validates JWT on every request).
4. Publish `/.well-known/oauth-protected-resource` metadata endpoint.
5. Add scope checks to individual tools.
6. Test with MCP Inspector: `npx @modelcontextprotocol/inspector@latest`.

## Implementation approaches

| Approach | Framework | Complexity | Best for |
|---|---|---|---|
| FastMCP + ScalekitProvider | Python | Low (~5 lines) | New Python MCP servers |
| FastAPI + FastMCP | Python | Medium | Existing FastAPI apps adding MCP |
| Express.js + MCP SDK | Node.js | Medium | Node.js MCP servers |

## Framework-specific references

- FastMCP (Python, simplest): [fastmcp-reference.md](fastmcp-reference.md)
- Express.js (Node.js): [express-reference.md](express-reference.md)
- FastAPI + FastMCP (Python, custom middleware): [fastapi-reference.md](fastapi-reference.md)

## Deep reference

- MCP server auth patterns: [../../docs/mcp-server-auth.md](../../docs/mcp-server-auth.md)
- API auth (related — client credentials): [../../docs/api-auth.md](../../docs/api-auth.md)

## When to switch skills

- Use `implementing-saaskit` for user-facing browser authentication.
- Use `adding-api-auth` for non-MCP machine-to-machine auth.
- Use `production-readiness-saaskit` to validate MCP auth before launch.
