# AgentKit Docs

This `docs/` directory is the canonical documentation layer for the `agent-auth` plugin.

Use it for the durable AgentKit model:

- connectors
- connections
- connected accounts
- tools
- live tool discovery

The Claude Code plugin still includes adapter/runtime files such as `.claude-plugin/`, `.mcp.json`, `commands/`, `hooks/`, and `agents/`, but those are secondary to the content model here.

## How this directory is organized

- [connections.md](connections.md) explains how AgentKit connections are configured and named.
- [connected-accounts.md](connected-accounts.md) explains the per-user authorization lifecycle.
- [tool-discovery.md](tool-discovery.md) explains how to treat live AgentKit metadata as the source of truth for tools and schemas.
- [byoc.md](byoc.md) explains Bring Your Own Credentials.
- [code-samples.md](code-samples.md) points to implementation patterns and runnable examples.
- [connectors/README.md](connectors/README.md) is the curated connector-notes entrypoint.

## Source-of-truth rule

Use live AgentKit metadata as the source of truth for:

- current connector coverage
- tool names
- `input_schema`
- `output_schema`

Treat connector notes as curated guidance, not as a guaranteed exhaustive catalog.

## Relationship to skills and rules

- `skills/` contains task-oriented workflows that should stay thin and point here for deeper reference.
- `rules/` contains stable cross-cutting guidance such as terminology and tool-selection discipline.
