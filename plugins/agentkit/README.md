# AgentKit for Claude Code

## Purpose
This plugin brings Scalekit AgentKit into Claude Code so an agent can connect users to third-party apps, discover the right tools, and execute authenticated tool calls on their behalf. It is organized as a hybrid structure: a Tessl-like canonical content layer and a Claude-specific adapter layer.

Canonical content lives in:
- `docs/` for durable AgentKit knowledge
- `skills/` for task-oriented workflows
- `rules/` for cross-cutting guidance

Claude runtime files remain in place as adapters:
- `.claude-plugin/`
- `.mcp.json`
- `commands/` for legacy slash-command aliases and compatibility shims
- `hooks/`
- `agents/`

The plugin treats live AgentKit metadata as the source of truth for tool names, `input_schema`, and `output_schema`. Connector notes are curated guidance, not a guaranteed exhaustive catalog.

## Installation
```sh
claude /plugin install agentkit@scalekit-auth-stack
```

Start with the canonical docs entrypoint at [`docs/index.md`](docs/index.md).

Official Scalekit docs:
- [LLM docs map](https://docs.scalekit.com/llms.txt)
- [Docs sitemap](https://docs.scalekit.com/sitemap-0.xml)
- [AgentKit overview](https://docs.scalekit.com/agentkit/overview.md)
- [AgentKit quickstart](https://docs.scalekit.com/agentkit/quickstart.md)
- [AgentKit connectors](https://docs.scalekit.com/agentkit/connectors.md)
- [AgentKit examples](https://docs.scalekit.com/agentkit/examples.md)

## Skills Reference
- `/agentkit:integrating-agentkit`
  Integrates AgentKit into app code or an agent workflow and routes into the core docs.
- `/agentkit:discovering-agentkit-tools`
  Uses live AgentKit metadata to find tools, inspect schemas, and narrow the tool set.
- `/agentkit:testing-agentkit-tools`
  Generates authorization links, fetches live tool metadata, and executes tools from Claude Code. This is the preferred runnable playground surface.
- `/agentkit:exposing-agentkit-via-mcp`
  Exposes AgentKit tools through MCP for MCP-compatible runtimes.
- `/agentkit:production-readiness-agentkit`
  Runs a structured production-readiness checklist for AgentKit integrations.

Legacy command alias:
- `/test-tool [generate-link|get-tool|execute-tool ...]`
  Compatibility wrapper for older usage. Prefer `/agentkit:testing-agentkit-tools ...`.

## Configuration
Required environment variables:
- `SCALEKIT_ENV_URL`
- `SCALEKIT_CLIENT_ID`
- `SCALEKIT_CLIENT_SECRET`

Optional sample variable:
- `GMAIL_CONNECTION_NAME`

Legacy aliases supported by the testing command:
- `TOOL_ENV_URL`
- `TOOL_CLIENT_ID`
- `TOOL_CLIENT_SECRET`

Example `.mcp.json`:

```json
{
  "mcpServers": {
    "scalekit": {
      "type": "http",
      "url": "https://mcp.scalekit.com"
    }
  }
}
```

## Usage Examples
Typical flow for a new connector integration:
1. Read [`docs/index.md`](docs/index.md) for the canonical model and [`docs/connections.md`](docs/connections.md) for connection naming.
2. Create the connection in `AgentKit -> Connections`.
3. Use `/agentkit:integrating-agentkit` to scaffold connected-account creation and authorization.
4. Use `/agentkit:discovering-agentkit-tools` or `/agentkit:testing-agentkit-tools get-tool --provider GMAIL` to inspect the live tool catalog and schema.
5. Use `/agentkit:testing-agentkit-tools generate-link --connection-name <dashboard-connection-name> --identifier user_123` if the user still needs to authorize.
6. Use `/agentkit:testing-agentkit-tools execute-tool --tool-name gmail_fetch_mails --connection-name <dashboard-connection-name> --identifier user_123 --tool-input '{"query":"is:unread","max_results":5}'` to validate the payload before wiring it into application code.

## Troubleshooting
1. No tools show up for a connector:
   Use live discovery first. The current tool inventory comes from AgentKit metadata, not static connector notes.
2. The connection exists but auth or execution fails:
   Verify that `connection_name` matches the exact dashboard value. It is not always the connector slug such as `gmail`.
3. Tool execution fails after a user already connected:
   Re-check the connected account status and re-authorize if the account is not `ACTIVE`.

## Security
This plugin needs AgentKit API credentials for your Scalekit environment. Store them in environment variables or a local secret manager, and never commit them to source control.

Connected accounts are per-user authorization boundaries. Use the correct identifier, request minimum necessary scopes, and keep the tool set constrained before handing tools to an LLM.
