---
name: scalekit-agent-auth
description: Implements Scalekit Agent Auth to enable AI agents to take actions in third-party applications (Gmail, Slack, Calendar, Notion) on behalf of users. Use when building agent authentication, OAuth workflows, managing connected accounts, or fetching access tokens for third-party APIs. Use when the user mentions Scalekit, Agent Auth, connected accounts, or authorizing agents.
---

# Scalekit Agent Auth Implementation

Helps AI agents authenticate users and execute actions in third-party applications like Gmail, Calendar, Slack, and Notion using Scalekit's Agent Auth.

## Quick Start

### Setup Scalekit SDK

**Get credentials**: Navigate to [app.scalekit.com](https://app.scalekit.com) → Developers → Settings → API Credentials

**Python installation**:
```bash
pip install scalekit-sdk-python
```

**Node.js installation**:
```bash
npm install @scalekit-sdk/node@2.2.0-beta.1
```

**Initialize client**:

Python:
```python
import scalekit.client
from dotenv import load_dotenv
load_dotenv()

scalekit = scalekit.client.ScalekitClient(
    client_id=os.getenv("SCALEKIT_CLIENT_ID"),
    client_secret=os.getenv("SCALEKIT_CLIENT_SECRET"),
    env_url=os.getenv("SCALEKIT_ENV_URL"),
)
actions = scalekit.actions
```

Node.js:
```typescript
import { ScalekitClient } from '@scalekit-sdk/node';
import 'dotenv/config';

const scalekitClient = new ScalekitClient(
  process.env.SCALEKIT_ENV_URL,
  process.env.SCALEKIT_CLIENT_ID,
  process.env.SCALEKIT_CLIENT_SECRET
);

const { connectedAccounts, tools } = scalekitClient;
```

## Core Workflow

Copy this checklist for implementation:

```
Agent Auth Implementation:
- [ ] Step 1: Create connected account
- [ ] Step 2: Check authorization status
- [ ] Step 3: Generate authorization link (if needed)
- [ ] Step 4: Fetch OAuth tokens
- [ ] Step 5: Execute third-party API calls
```

### Step 1: Create Connected Account

A connected account represents a user's connection to a third-party service.

Python:
```python
response = actions.get_or_create_connected_account(
    connection_name="gmail",  # or "slack", "calendar", "notion"
    identifier="user_123"     # unique ID from your system
)
connected_account = response.connected_account
```

Node.js:
```typescript
const response = await connectedAccounts.getOrCreateConnectedAccount({
  connector: 'gmail',
  identifier: 'user_123',
});
const connectedAccount = response.connectedAccount;
```

### Step 2: Check Authorization Status

Verify if the user has authorized access. Status values: `ACTIVE`, `INACTIVE`, `EXPIRED`.

Python:
```python
if connected_account.status != "ACTIVE":
    # User needs to authorize
```

Node.js:
```typescript
if (connectedAccount?.status !== 'ACTIVE') {
  // User needs to authorize
}
```

### Step 3: Generate Authorization Link

Create a magic link for users to complete OAuth authorization.

Python:
```python
link_response = actions.get_authorization_link(
    connection_name="gmail",
    identifier="user_123"
)
authorization_url = link_response.link
# Redirect user to authorization_url
```

Node.js:
```typescript
const linkResponse = await connectedAccounts.getMagicLinkForConnectedAccount({
  connector: 'gmail',
  identifier: 'user_123',
});
// Redirect user to linkResponse.link
```

**In production**: Redirect users to this URL. Scalekit handles the complete OAuth flow, token management, and automatic token refresh.

### Step 4: Fetch OAuth Tokens

Retrieve current access and refresh tokens. Scalekit automatically refreshes tokens when needed.

Python:
```python
response = actions.get_connected_account(
    connection_name="gmail",
    identifier="user_123"
)
tokens = response.connected_account.authorization_details["oauth_token"]
access_token = tokens["access_token"]
refresh_token = tokens["refresh_token"]
```

Node.js:
```typescript
const accountResponse = await connectedAccounts.getConnectedAccountByIdentifier({
  connector: 'gmail',
  identifier: 'user_123',
});

const authDetails = accountResponse?.connectedAccount?.authorizationDetails;
const accessToken = (authDetails && authDetails.details?.case === "oauthToken")
  ? authDetails.details.value?.accessToken
  : undefined;
```

### Step 5: Execute Third-Party API Calls

Use the access token to make authenticated API requests.

**Example: Fetch Gmail unread emails**:
```python
headers = {"Authorization": f"Bearer {access_token}"}
list_url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
params = {"q": "is:unread", "maxResults": 5}

response = requests.get(list_url, headers=headers, params=params)
messages = response.json().get("messages", [])
```

For complete API examples, see [GMAIL_EXAMPLE.md](GMAIL_EXAMPLE.md)

## Supported Connectors

Common connector values:
- `gmail` - Gmail API access
- `google-calendar` - Google Calendar
- `slack` - Slack workspace
- `notion` - Notion workspace
- `microsoft-outlook` - Outlook email
- `microsoft-calendar` - Microsoft Calendar

## Connection States

**ACTIVE**: User authorized, tokens valid
→ Proceed with API calls

**INACTIVE**: No authorization yet
→ Generate authorization link

**EXPIRED**: Authorization expired
→ Generate new authorization link

**Token refresh**: Automatic
→ Scalekit refreshes tokens before expiry

## Error Handling

**Connection not found**:
```python
try:
    response = actions.get_connected_account(...)
except Exception as e:
    # Create new connected account
    response = actions.get_or_create_connected_account(...)
```

**Authorization required**:
```python
if connected_account.status != "ACTIVE":
    link = actions.get_authorization_link(...)
    return {"authorization_required": True, "link": link.link}
```

**API call failures**:
- Check token validity first
- Verify connector permissions
- Review API rate limits

## Best Practices

**Security**:
- Store credentials in environment variables
- Never log access tokens
- Use HTTPS for authorization redirects

**User Experience**:
- Check authorization status before operations
- Provide clear authorization prompts
- Handle token expiration gracefully

**Performance**:
- Cache connected account status
- Reuse access tokens until expiry
- Batch API requests when possible

## Common Patterns

**Check before execute**:
```python
def execute_with_auth(connector, identifier, api_call):
    account = actions.get_connected_account(
        connection_name=connector,
        identifier=identifier
    )

    if account.connected_account.status != "ACTIVE":
        link = actions.get_authorization_link(connector, identifier)
        return {"error": "Authorization required", "link": link.link}

    tokens = account.connected_account.authorization_details["oauth_token"]
    return api_call(tokens["access_token"])
```

**Multi-connector support**:
```python
connectors = ["gmail", "slack", "calendar"]
for connector in connectors:
    response = actions.get_or_create_connected_account(
        connection_name=connector,
        identifier=user_id
    )
    # Check and authorize as needed
```

## Advanced Topics

**Custom scopes**: See [CUSTOM_SCOPES.md](CUSTOM_SCOPES.md)

**Webhook notifications**: See [WEBHOOKS.md](WEBHOOKS.md)

**Token lifecycle management**: See [TOKEN_MANAGEMENT.md](TOKEN_MANAGEMENT.md)

**Multi-tenant architecture**: See [MULTI_TENANT.md](MULTI_TENANT.md)

## Troubleshooting

**"Connected account not found"**:
→ Use `get_or_create_connected_account` instead of `get_connected_account`

**"Invalid credentials"**:
→ Verify API credentials at app.scalekit.com

**"Authorization failed"**:
→ Check connector configuration in Scalekit dashboard
→ Verify redirect URLs are whitelisted

**"Token expired"**:
→ Scalekit auto-refreshes tokens; check connection status
→ Regenerate authorization link if status is EXPIRED

## Reference

**Scalekit Documentation**: [docs.scalekit.com](https://docs.scalekit.com)

**API Reference**: [docs.scalekit.com/apis](https://docs.scalekit.com/apis)

**Supported Connectors**: [docs.scalekit.com/connectors](https://docs.scalekit.com/connectors)s