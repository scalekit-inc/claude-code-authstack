---
name: testing-agentkit-tools
description: Tests live Scalekit AgentKit flows from Claude Code by generating authorization links, fetching tool metadata, and executing a tool for a connected account. Use when a user wants to validate a connector, inspect the exact payload for `execute_tool`, or build a workflow step by step in the editor.
---

# Testing AgentKit Tools

This skill is the live playground layer for AgentKit inside Claude Code.

Use it to:

- generate an authorization link for a connection
- fetch live tool metadata for a connector or tool name
- execute a tool with real inputs
- inspect the exact JSON payload sent to AgentKit

## Default workflow

1. Confirm the environment variables are available:
   - `SCALEKIT_ENV_URL`
   - `SCALEKIT_CLIENT_ID`
   - `SCALEKIT_CLIENT_SECRET`
   - legacy `TOOL_*` aliases are accepted for backward compatibility
2. Discover the tool first when the schema is unknown.
3. Generate an authorization link if the connected account is not `ACTIVE`.
4. Execute the tool with the smallest valid `tool_input`.
5. Show the exact command and payload used so the user can translate it into app code.

## Command surface

Use `/test-tool` for the runnable playground:

- `/test-tool get-tool --provider GMAIL`
- `/test-tool get-tool --tool-name gmail_fetch_mails`
- `/test-tool generate-link --connection-name MY_GMAIL --identifier user_123`
- `/test-tool execute-tool --tool-name gmail_fetch_mails --connection-name MY_GMAIL --identifier user_123 --tool-input '{"query":"is:unread","max_results":5}'`

## Guardrails

- Treat live metadata as the source of truth for `input_schema` and `output_schema`.
- Do not assume the dashboard `connection_name` matches the connector slug.
- Ask for missing credentials instead of inventing placeholder values.
- Keep the tool set constrained to the current workflow.

## Deep reference

- Playground command: [../../commands/test-tool.md](../../commands/test-tool.md)
- Canonical docs entrypoint: [../../docs/index.md](../../docs/index.md)
- Live discovery model: [../../docs/tool-discovery.md](../../docs/tool-discovery.md)
- Integration workflow: [../agent-auth/SKILL.md](../agent-auth/SKILL.md)
