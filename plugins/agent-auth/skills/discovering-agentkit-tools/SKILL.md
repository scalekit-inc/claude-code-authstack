---
name: discovering-agentkit-tools
description: Discovers live Scalekit AgentKit tools for a connector and explains their input and output schemas. Use when a user asks what tools are available for Gmail, Slack, Salesforce, or another connector, wants to inspect `input_schema` or `output_schema`, or needs help narrowing the tool set for an agent.
---

# Discovering AgentKit Tools

Use live AgentKit metadata as the source of truth for tool names, required inputs, and output schemas.

Do not rely on the static connector notes as a complete catalog. Those files are curated reference material and may lag the live platform.

## When to use this skill

Use this skill when the user asks:

- what tools exist for a connector
- which tool should the agent use
- what inputs a tool requires
- what output shape a tool returns
- how to reduce the tool set before giving tools to an LLM

## Discovery workflow

1. Identify the target connector or exact tool name.
2. Prefer live lookup through `/agent-auth:testing-agentkit-tools get-tool --provider <PROVIDER>` or `/agent-auth:testing-agentkit-tools get-tool --tool-name <TOOL_NAME>`.
3. If older docs or muscle memory mention `/test-tool`, treat it as a legacy compatibility alias for the testing skill rather than the canonical workflow.
4. Summarize:
   - tool name
   - connector
   - what the tool does
   - required fields from `input_schema.required`
   - optional fields from `input_schema.properties`
   - important fields from `output_schema.properties`
5. Recommend the smallest useful tool set for the workflow.
6. If live credentials are unavailable, use the connector notes only as a fallback and say they may be stale.

## Terminology

- `connector`: Gmail, Slack, Salesforce, Notion, or a custom connector
- `connection`: the exact dashboard configuration name used for authorization
- `connected account`: the per-user authorized record
- `tool`: the executable action exposed by a connector

Use `connector` in explanations. Only use `provider` when the SDK or API filter field literally expects that name.

## What to emphasize

- `connection_name` is the exact dashboard value and may not equal the connector slug.
- Tool metadata is the durable way to determine current inputs and outputs.
- The preferred runnable surface is the testing skill in `skills/testing-agentkit-tools/`, not the legacy `commands/` alias.
- Restrict the tool set before handing it to an LLM. Fewer relevant tools improve tool selection and parameter filling.

## Deep reference

- Canonical docs entrypoint: [../../docs/index.md](../../docs/index.md)
- Live discovery model: [../../docs/tool-discovery.md](../../docs/tool-discovery.md)
- Runnable testing workflow: [../testing-agentkit-tools/SKILL.md](../testing-agentkit-tools/SKILL.md)
- Curated connector notes: [../../docs/connectors/README.md](../../docs/connectors/README.md)
- Broader implementation examples: [../../docs/code-samples.md](../../docs/code-samples.md)
