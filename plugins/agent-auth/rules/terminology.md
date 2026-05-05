# Terminology

Use these terms consistently in user-facing documentation and skills:

- `connector`: the integration, such as Gmail, Slack, or Salesforce
- `connection`: the environment-level dashboard configuration
- `connected account`: the per-user authorization record
- `tool`: the executable action exposed by a connector

## Preferred wording

- Prefer `connector` in explanations to users.
- Use `provider` only when the SDK or API field literally uses that name.
- Do not imply that `connection_name` is always the same as the connector slug.

## Why this rule exists

The old language mixed `provider`, `connector`, and `connection_name` too freely. This rule keeps the AgentKit model stable across skills and docs.
