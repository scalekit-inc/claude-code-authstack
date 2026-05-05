# Connections

Connections are the environment-level AgentKit configurations that tell Scalekit how to authenticate to a connector.

One connection is created once in the dashboard, then reused across many users through connected accounts.

## Core idea

A connection defines:

- which connector is being used
- which credentials or auth settings back it
- which scopes or permissions are requested
- the exact dashboard `connection_name` used later in SDK calls

## Important distinction

Do not confuse:

- `connection_name`: the exact dashboard value used for authorization and connected-account flows
- connector slug or provider filter: the identifier used to group tools in live metadata

They are related, but they are not always the same string.

## Official Scalekit docs

- [Configure a connection](https://docs.scalekit.com/agentkit/connections.md)
- [Scopes and permissions](https://docs.scalekit.com/agentkit/authentication/scopes-permissions.md)

## Typical setup flow

1. Go to `AgentKit -> Connections` in the Scalekit Dashboard.
2. Choose the connector you want to expose to the agent.
3. Configure credentials, scopes, and any connector-specific settings.
4. Save the connection with a stable `connection_name`.
5. Reuse that `connection_name` in your SDK code and testing commands.

## Connection types

Common patterns include:

- OAuth 2.0 connectors
- API key connectors
- other connector-specific auth models supported by AgentKit

Use the connector-specific notes in [connectors/README.md](connectors/README.md) for quirks, but treat live tool metadata as the source of truth for available tools.

## Practical guidance

- Use clear environment-specific names such as `MY_GMAIL` or `SALESFORCE_PROD`.
- Keep scopes minimal and workflow-specific.
- Do not assume Gmail is representative of every connector; Gmail is a special-case quickstart in several examples.

## Related docs

- [connected-accounts.md](connected-accounts.md)
- [tool-discovery.md](tool-discovery.md)
- [byoc.md](byoc.md)
