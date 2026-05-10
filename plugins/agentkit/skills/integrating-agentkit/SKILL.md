---
name: integrating-agentkit
description: Integrates Scalekit AgentKit into a project so an agent can create connections, authorize users, discover tools, and execute authenticated tool calls on their behalf. Use when a user needs to set up a connection, create a connected account, generate an authorization link, or wire AgentKit tools into application code or an agent framework.
---

# AgentKit Integration

Use this skill as the integration entrypoint for the plugin. It should stay thin and route into the canonical docs in `docs/`.

## Mental model

Keep these terms straight:

- `connector`: the integration, such as Gmail or Slack
- `connection`: the environment-level dashboard configuration
- `connected account`: the per-user authorization record
- `tool`: the executable action exposed by a connector

Prefer live tool discovery over hand-maintained catalogs. If the user needs the current tool list or schema, switch to `discovering-connector-tools` or `testing-agentkit-tools`.

## Default workflow

1. Confirm `SCALEKIT_ENV_URL`, `SCALEKIT_CLIENT_ID`, and `SCALEKIT_CLIENT_SECRET`.
2. Verify the connection exists in `AgentKit -> Connections`.
3. Create or fetch the connected account for the user.
4. If the account is not `ACTIVE`, generate an authorization link.
5. Discover the exact tool and schema before execution.
6. Execute the tool directly or hand only the needed tools to an agent framework.

## Quick integration skeleton

### Python
```bash
pip install scalekit-sdk-python
```

```python
import scalekit.client, os
from dotenv import load_dotenv
load_dotenv()

client = scalekit.client.ScalekitClient(
    client_id=os.getenv("SCALEKIT_CLIENT_ID"),
    client_secret=os.getenv("SCALEKIT_CLIENT_SECRET"),
    env_url=os.getenv("SCALEKIT_ENV_URL"),
)
actions = client.actions
response = actions.get_or_create_connected_account(
    connection_name="MY_GMAIL",
    identifier="user_123"
)
connected_account = response.connected_account
if connected_account.status != "ACTIVE":
    link_response = actions.get_authorization_link(
        connection_name="MY_GMAIL",
        identifier="user_123"
    )
    print("Authorize here:", link_response.link)
result = actions.execute_tool(
    tool_name="gmail_fetch_mails",
    identifier="user_123",
    connected_account_id=connected_account.id,
    tool_input={
        "query": "is:unread",
        "max_results": 5,
    },
)
print(result)
```

### Node.js
```bash
npm install @scalekit-sdk/node
```

```typescript
import { ScalekitClient } from '@scalekit-sdk/node';
import 'dotenv/config';

const client = new ScalekitClient(
  process.env.SCALEKIT_ENV_URL!,
  process.env.SCALEKIT_CLIENT_ID!,
  process.env.SCALEKIT_CLIENT_SECRET!
);
const actions = client.actions;

const response = await actions.getOrCreateConnectedAccount({
  connectionName: 'MY_GMAIL',
  identifier: 'user_123',
});
const connectedAccount = response.connectedAccount;

if (connectedAccount?.status !== 'ACTIVE') {
  const linkResponse = await actions.getAuthorizationLink({
    connectionName: 'MY_GMAIL',
    identifier: 'user_123',
  });
  console.log(linkResponse.link);
}

const result = await actions.executeTool({
  toolName: 'gmail_fetch_mails',
  connectedAccountId: connectedAccount?.id,
  identifier: 'user_123',
  toolInput: { query: 'is:unread', max_results: 5 },
});
console.log(result);
```

## Deep reference

- Core docs: [../../docs/index.md](../../docs/index.md)
- Connections: [../../docs/connections.md](../../docs/connections.md)
- Connected accounts: [../../docs/connected-accounts.md](../../docs/connected-accounts.md)
- Tool discovery: [../../docs/tool-discovery.md](../../docs/tool-discovery.md)
- Code-sample entrypoint: [../../docs/code-samples.md](../../docs/code-samples.md)
- BYOC: [../../docs/byoc.md](../../docs/byoc.md)
- Connector notes: [../../docs/connectors/README.md](../../docs/connectors/README.md)

## When to switch skills

- Use `discovering-connector-tools` when the user needs the current tool catalog or schema.
- Use `testing-agentkit-tools` when the user wants to validate a tool call in Claude Code.
- Use `exposing-agentkit-via-mcp` when the user wants AgentKit tools exposed over MCP.
