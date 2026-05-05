# Connectors Overview

> Canonical docs: [../docs/index.md](../docs/index.md) and [../docs/connectors/README.md](../docs/connectors/README.md)

This page is a high-level connector overview for AgentKit. Use it for category-level guidance and terminology, not as the exhaustive source of truth for current tools. The live AgentKit tool metadata is the source of truth for tool names plus `input_schema` and `output_schema`.

## What are connectors?

Connectors are pre-configured integrations with popular third-party applications that enable your users to:

- **Connect their accounts** using secure authentication methods
- **Execute tools and actions** through a unified API interface
- **Access data and functionality** from external applications
- **Maintain secure connections** with proper authorization scopes

## Supported connectors

AgentKit supports a wide range of popular business applications:

| Category | Providers |
|---|---|
| **Google Workspace** | Gmail, Google Calendar, Google Drive, Google Docs, Google Sheets, Google Slides, Google Forms, Google Meet, Google Ads |
| **Microsoft 365** | Outlook, OneDrive, SharePoint, Microsoft Teams, Microsoft Excel, Microsoft Word, OneNote |
| **Communication** | Slack, Zoom |
| **Project Management** | Jira, Asana, Trello, Monday.com, ClickUp, Linear, Confluence |
| **CRM & Sales** | Salesforce, HubSpot, Zendesk, Freshdesk, Intercom, Gong, Attention, Chorus, Clari Copilot |
| **Development** | GitHub |
| **Productivity** | Notion, Airtable, Dropbox |
| **Data & Analytics** | BigQuery, Snowflake, Fathom |
| **Service Management** | ServiceNow |

For curated connector notes, see [agent-connectors/README.md](agent-connectors/README.md).
For live tool discovery, see [tool-discovery.md](tool-discovery.md).

## Connector capabilities

Each connector offers different capabilities based on its API and authentication model.

### Authentication methods

- **OAuth 2.0**: Standard method for all supported providers

### Available tools

Connectors expose various tools that can be executed through AgentKit:

> **Note:** Tool availability depends on the specific connector, the current live catalog, and the user's permissions within that application.

**Common tool categories:**

- **Data retrieval**: Fetch emails, calendar events, files, or records
- **Data creation**: Create new items, send messages, or schedule events
- **Data modification**: Update existing records or settings
- **File operations**: Upload, download, or manage files
- **Communication**: Send notifications, messages, or alerts

### Rate limits and quotas

Each provider has different rate limits and quotas:

- **API rate limits**: Requests per minute/hour limitations
- **Data quotas**: Storage or transfer limitations
- **Feature restrictions**: Premium features or enterprise-only capabilities

## Connector configuration

### Adding a connector

1. **Navigate to connections** in your AgentKit dashboard
2. **Select connector** from the available options
3. **Configure settings** such as scopes and permissions
4. **Set up authentication** — configure OAuth client credentials if using custom OAuth apps
5. **Test connection** to verify provider setup

### Connector settings

Each provider can be configured with:

**Authentication settings:**
- OAuth client credentials (if using custom OAuth apps)
- API endpoint URLs
- Supported scopes and permissions
- Token refresh settings

**Rate limiting:**
- Request throttling settings
- Backoff strategies for rate limit errors

## Working with connector APIs

### API integration

The Scalekit SDK abstracts connector-specific APIs. In AgentKit, prefer live tool discovery plus `execute_tool` over hand-coding upstream REST calls when a tool already exists.

```python
# Step 3: Fetch token (always call this immediately before the API call)
response = actions.get_connected_account(
    connection_name="slack",   # Replace with any connector name
    identifier="user_123"
)
tokens = response.connected_account.authorization_details["oauth_token"]
access_token = tokens["access_token"]

# Step 4: Call the connector API with the token
headers = {"Authorization": f"Bearer {access_token}"}
```

Scalekit automatically refreshes expired tokens on `get_connected_account` — no manual refresh logic needed.

### Error handling

AgentKit normalizes connector-specific errors into consistent error responses:

```javascript
{
  error: {
    code: 'RATE_LIMIT_EXCEEDED',
    message: 'Provider rate limit exceeded',
    provider: 'gmail',
    details: {
      retryAfter: 60,
      limitType: 'requests_per_minute'
    }
  }
}
```

## Connector-specific considerations

### Google Workspace

- **OAuth scopes**: Requires specific scopes for different Google services
- **Rate limits**: Generous limits but varies by service
- **Data access**: Supports both personal and organization data
- **Security**: Supports domain-wide delegation for enterprise

### Microsoft 365

- **Authentication**: Supports both personal and work accounts
- **Graph API**: Unified API for all Microsoft services
- **Permissions**: Granular permission model
- **Compliance**: Built-in compliance and audit features

### Slack

- **Workspace apps**: Requires installation in each workspace
- **Bot tokens**: Different capabilities for bot vs user tokens
- **Rate limits**: Tier-based limits depending on workspace size
- **Channels**: Requires specific permissions for private channels

### Jira

- **Project access**: Permissions are project-specific
- **Issue types**: Different issue types have different fields
- **Workflows**: Custom workflows affect available actions

## Best practices

### Authentication setup

- **Use minimal scopes**: Request only necessary permissions
- **Token refresh**: Scalekit handles this automatically — call `get_connected_account` before every API call
- **Monitor auth status**: Track connected account status; re-authorize if status is not `ACTIVE`

### Tool execution

- **Respect rate limits**: Implement throttling and exponential backoff for 429 errors
- **Cache results**: Cache frequently accessed data to avoid redundant API calls
- **Error recovery**: Retry transient failures; surface permanent errors to users

## Monitoring and analytics

### Provider health

- **API uptime**: Track provider API availability
- **Response times**: Monitor latency for different operations
- **Error rates**: Track errors by provider and tool type
- **Rate limit usage**: Monitor quota consumption

### Usage analytics

- **Popular providers**: Which providers are used most
- **Tool usage**: Which tools are executed most frequently
- **User adoption**: How many users connect to each provider
- **Error patterns**: Common failure modes by provider

## Related documentation

- [connections.md](connections.md) — how to configure authentication credentials for a connector
- [connected-accounts.md](connected-accounts.md) — per-user account lifecycle and token management
- [agent-connectors/README.md](agent-connectors/README.md) — curated connector notes and examples
- [tool-discovery.md](tool-discovery.md) — live discovery model for current tools and schemas
- [code-samples.md](code-samples.md) — implementation examples by framework
