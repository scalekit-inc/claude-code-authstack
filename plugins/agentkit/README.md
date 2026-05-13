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

The plugin treats live AgentKit metadata as the source of truth for tool names, `input_schema`, and `output_schema`. For per-connector details, see the [AgentKit connectors catalog](https://docs.scalekit.com/agentkit/connectors/).

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
- `/agentkit:discovering-connector-tools`
  Uses live AgentKit metadata to find tools, inspect schemas, and narrow the tool set.
- `/agentkit:exposing-agentkit-via-mcp`
  Exposes AgentKit tools through MCP for MCP-compatible runtimes.
- `/agentkit:production-readiness-agentkit`
  Runs a structured production-readiness checklist for AgentKit integrations.

## Configuration
Required environment variables (for SDK-based integrations):
- `SCALEKIT_ENV_URL`
- `SCALEKIT_CLIENT_ID`
- `SCALEKIT_CLIENT_SECRET`

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
4. Use `/agentkit:discovering-connector-tools` to inspect the live tool catalog and schema via the Scalekit MCP server.
5. Use the Scalekit MCP server tools directly to generate auth links, discover tools, and execute tool calls interactively.

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
