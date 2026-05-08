---
name: testing-agentkit-tools
description: Tests live Scalekit AgentKit flows from Claude Code by generating authorization links, fetching tool metadata, and executing a tool for a connected account. Use when a user wants to validate a connector, inspect the exact payload for `execute_tool`, or build a workflow step by step in the editor.
argument-hint: "[generate-link|get-tool|execute-tool] [args...]"
disable-model-invocation: true
allowed-tools: Bash
---

# Testing AgentKit Tools

This skill is the canonical live playground layer for AgentKit inside Claude Code.

**Arguments:** $ARGUMENTS

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

## Preferred invocation

Invoke this skill directly for the runnable playground:

- `/agentkit:testing-agentkit-tools get-tool --provider GMAIL`
- `/agentkit:testing-agentkit-tools get-tool --tool-name gmail_fetch_mails`
- `/agentkit:testing-agentkit-tools generate-link --connection-name MY_GMAIL --identifier user_123`
- `/agentkit:testing-agentkit-tools execute-tool --tool-name gmail_fetch_mails --connection-name MY_GMAIL --identifier user_123 --tool-input '{"query":"is:unread","max_results":5}'`

`/test-tool` remains available only as a legacy compatibility alias.

## Operations

### generate-link
Usage: `generate-link --connection-name <connection_name> --identifier <identifier>`

Creates or fetches the connected account and prints an authorization link if the account is not yet `ACTIVE`.

### get-tool
Usage: `get-tool [--tool-name <tool_name>] [--provider <provider>] [--page-size <n>] [--page-token <token>]`

Fetches live tool metadata and prints the raw JSON response. Omitting `--tool-name` returns all matching tools for the filter.

### execute-tool
Usage: `execute-tool --tool-name <tool_name> --connection-name <connection_name> --identifier <identifier> --tool-input '<json>'`

Creates or fetches the connected account, prints an authorization link if needed, and executes the tool.

## Your task

Parse `$ARGUMENTS` to determine the operation, then run the bundled script from this skill directory:

```bash
${CLAUDE_SKILL_DIR}/scripts/connect.py
```

### Runner selection

Check which runner is available by running `which uv` once before any Python command:

- if `uv` exists, use `uv run python`
- otherwise use `python3`
- if `python3` is unavailable, fall back to `python`

### Credentials

Before running any operation, check for these environment variables:

- `SCALEKIT_ENV_URL`
- `SCALEKIT_CLIENT_ID`
- `SCALEKIT_CLIENT_SECRET`

Also accept legacy aliases:

- `TOOL_ENV_URL`
- `TOOL_CLIENT_ID`
- `TOOL_CLIENT_SECRET`

If none of the supported variables are available, ask the user for the missing values before proceeding. Do not write secrets into source-controlled files unless the user explicitly asks you to.

### Commands to run

If operation is `generate-link`, run:

```bash
<runner> "${CLAUDE_SKILL_DIR}/scripts/connect.py" --generate-link --connection-name <connection_name> --identifier <identifier>
```

If operation is `get-tool`, run:

```bash
<runner> "${CLAUDE_SKILL_DIR}/scripts/connect.py" --get-tool [--tool-name <name>] [--provider <provider>] [--page-size <n>] [--page-token <token>]
```

If operation is `execute-tool`, run:

```bash
<runner> "${CLAUDE_SKILL_DIR}/scripts/connect.py" --execute-tool --tool-name <tool_name> --connection-name <connection_name> --identifier <identifier> --tool-input '<tool_input_json>'
```

If `tool_input` is missing for `execute-tool`, inspect the live tool metadata first or ask the user for the missing input values.

### After running

Show:

1. the command output
2. the exact command that was run
3. the resolved parameters in a small structured summary
4. for `execute-tool`, the exact JSON payload that was passed to AgentKit

## Guardrails

- Treat live metadata as the source of truth for `input_schema` and `output_schema`.
- Do not assume the dashboard `connection_name` matches the connector slug.
- Ask for missing credentials instead of inventing placeholder values.
- Keep the tool set constrained to the current workflow.

## Deep reference

- Legacy alias: [../../commands/test-tool.md](../../commands/test-tool.md)
- Canonical docs entrypoint: [../../docs/index.md](../../docs/index.md)
- Live discovery model: [../../docs/tool-discovery.md](../../docs/tool-discovery.md)
- Integration workflow: [../integrating-agentkit/SKILL.md](../integrating-agentkit/SKILL.md)
