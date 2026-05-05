# Connected Accounts

Connected accounts are the per-user authorization records in AgentKit.

If a connection is the reusable environment configuration, a connected account is the user-specific runtime object that lets the agent act on behalf of a particular user or identifier.

## What a connected account stores

A connected account tracks:

- the linked connection
- the user or tenant identifier
- current authorization status
- granted scopes and token state

## Lifecycle

Typical lifecycle:

1. Create or fetch the connected account for a user.
2. If the account is not `ACTIVE`, generate an authorization link.
3. The user completes the auth flow.
4. The account becomes `ACTIVE`.
5. AgentKit can execute tools on behalf of that user.

## Operational rules

- Always use the correct user identifier from your own system.
- Treat the connected account as the per-user boundary for tool execution.
- If tool execution fails unexpectedly, check the connected account status again before debugging deeper.

## Why this matters for tool execution

The tool catalog is connector-level, but execution is user-scoped through a connected account.

That means:

- tool discovery tells you what is possible
- the connected account determines whether the current user is actually authorized to do it

## Common failure modes

- `connection_name` does not match the dashboard value
- user never completed authorization
- account is no longer `ACTIVE`
- scopes are too narrow for the requested tool

## Related docs

- [connections.md](connections.md)
- [tool-discovery.md](tool-discovery.md)
