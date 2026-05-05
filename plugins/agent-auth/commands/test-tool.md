---
description: Legacy compatibility alias for the AgentKit testing skill
argument-hint: "[generate-link|get-tool|execute-tool] [args...]"
allowed-tools: Bash
---

# Legacy AgentKit Tool Tester

This command is a legacy compatibility alias for `/agent-auth:testing-agentkit-tools`.

Prefer invoking the skill directly:

```text
/agent-auth:testing-agentkit-tools $ARGUMENTS
```

**Arguments:** $ARGUMENTS

## Your task

Parse `$ARGUMENTS` exactly as the testing skill would and run the same bundled script from the plugin root:

```bash
skills/testing-agentkit-tools/scripts/connect.py
```

Keep this command behavior aligned with the skill:

- use `uv run python` when `uv` exists, otherwise `python3`, otherwise `python`
- accept both `SCALEKIT_*` and legacy `TOOL_*` credential variables
- inspect live metadata before guessing `tool_input`
- show the command output, exact command, resolved parameters, and exact payload for `execute-tool`

Do not maintain separate workflow rules here. The testing skill is the source of truth.
