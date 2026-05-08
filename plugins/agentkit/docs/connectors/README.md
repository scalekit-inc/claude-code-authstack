# Connector Notes

This directory is the canonical connector-notes entrypoint for the plugin.

Connector notes are intentionally curated and lightweight. They should explain:

- what the connector is useful for
- auth quirks or setup gotchas
- example workflows
- guidance that is not obvious from live metadata

They should not claim to be the exhaustive current tool catalog.

## Official Scalekit docs

- [Agent connectors](https://docs.scalekit.com/agentkit/connectors.md)

## Source of truth

Use live AgentKit metadata for:

- tool names
- `input_schema`
- `output_schema`
- current connector coverage

Use connector notes for:

- workflow hints
- product context
- authentication caveats
- examples that help users orient quickly

## Current connector coverage in the plugin

The plugin already contains curated notes for connectors such as:

- Gmail
- Google Calendar
- Google Sheets
- Slack
- Salesforce
- GitHub
- Notion
- Zendesk

and many others in the legacy connector-notes set.

During this hybrid migration, those existing notes remain available in the plugin as the backing source for connector-specific guidance while `docs/` becomes the canonical entry layer.

## Related docs

- [../tool-discovery.md](../tool-discovery.md)
- [../connections.md](../connections.md)
- [../connected-accounts.md](../connected-accounts.md)
