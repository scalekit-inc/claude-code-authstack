---
description: Test live AgentKit discovery and tool execution from Claude Code
argument-hint: "[generate-link|get-tool|execute-tool] [args...]"
allowed-tools: Bash
---

# AgentKit Tool Tester

Test live AgentKit flows using the bundled Python playground script.

**Arguments:** $ARGUMENTS

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

Parse `$ARGUMENTS` to determine the operation, then run the bundled script from the plugin root:

```bash
skills/testing-agentkit-tools/scripts/connect.py
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
<runner> skills/testing-agentkit-tools/scripts/connect.py --generate-link --connection-name <connection_name> --identifier <identifier>
```

If operation is `get-tool`, run:

```bash
<runner> skills/testing-agentkit-tools/scripts/connect.py --get-tool [--tool-name <name>] [--provider <provider>] [--page-size <n>] [--page-token <token>]
```

If operation is `execute-tool`, run:

```bash
<runner> skills/testing-agentkit-tools/scripts/connect.py --execute-tool --tool-name <tool_name> --connection-name <connection_name> --identifier <identifier> --tool-input '<tool_input_json>'
```

If `tool_input` is missing for `execute-tool`, inspect the live tool metadata first or ask the user for the missing input values.

### After running

Show:

1. the command output
2. the exact command that was run
3. the resolved parameters in a small structured summary
4. for `execute-tool`, the exact JSON payload that was passed to AgentKit
