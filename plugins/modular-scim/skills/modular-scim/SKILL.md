---
name: scim-webhook-provisioning
description: Implements webhook listeners for real-time SCIM user provisioning with Scalekit. Handles user and group lifecycle events. Use when adding automated user provisioning, directory sync webhooks, or real-time user management.
---

# SCIM Webhook Provisioning

## What This Does

Automatically sync users and groups from your customers' directory providers (Okta, Azure AD, Google Workspace) to your application in real-time.

**When a user is created/updated/deleted in their directory → Your app is notified instantly → You update your database**

## Implementation Checklist

```
- [ ] Install Scalekit SDK
- [ ] Create webhook endpoint
- [ ] Verify webhook signatures
- [ ] Process user events
- [ ] Process group events
- [ ] Register webhook in Scalekit dashboard
- [ ] Test with directory provider
```

## Step 1: Install SDK and Configure

**Node.js:**
```bash
npm install @scalekit-sdk/node
```

**Python:**
```bash
pip install scalekit-sdk
```

**Environment variables** (`.env`):
```env
SCALEKIT_ENVIRONMENT_URL=https://your-env.scalekit.com
SCALEKIT_CLIENT_ID=skc_1234567890
SCALEKIT_CLIENT_SECRET=test_1234567890
SCALEKIT_WEBHOOK_SECRET=whsec_1234567890  # Get this after registering webhook
```

## Step 2: Create Webhook Endpoint

### Node.js (Express)

```javascript
import express from 'express';
import { ScalekitClient } from '@scalekit-sdk/node';

const app = express();

// IMPORTANT: Use raw body for signature verification
app.use(express.raw({ type: 'application/json' }));

const scalekit = new ScalekitClient(
  process.env.SCALEKIT_ENVIRONMENT_URL,
  process.env.SCALEKIT_CLIENT_ID,
  process.env.SCALEKIT_CLIENT_SECRET
);

app.post('/webhooks/scalekit', async (req, res) => {
  const webhookSecret = process.env.SCALEKIT_WEBHOOK_SECRET;

  // STEP 1: Verify signature (NEVER skip this!)
  try {
    await scalekit.verifyWebhookPayload(
      webhookSecret,
      req.headers,
      req.body
    );
  } catch (error) {
    console.error('Invalid webhook signature');
    return res.status(400).send('Invalid signature');
  }

  // STEP 2: Parse the event
  const event = JSON.parse(req.body.toString());

  // STEP 3: Process based on event type
  try {
    switch (event.type) {
      case 'organization.directory.user_created':
        await handleUserCreated(event.data);
        break;

      case 'organization.directory.user_updated':
        await handleUserUpdated(event.data);
        break;

      case 'organization.directory.user_deleted':
        await handleUserDeleted(event.data);
        break;

      case 'organization.directory.group_created':
        await handleGroupCreated(event.data);
        break;

      case 'organization.directory.group_membership_updated':
        await handleGroupMembershipUpdated(event.data);
        break;

      default:
        console.log(`Unhandled event: ${event.type}`);
    }

    res.status(200).send('OK');
  } catch (error) {
    console.error('Processing failed:', error);
    res.status(500).send('Processing failed');
  }
});

app.listen(3000);
```

### Python (FastAPI)

```python
from fastapi import FastAPI, Request, HTTPException
from scalekit import ScalekitClient
import os
import json

app = FastAPI()

scalekit = ScalekitClient(
    env_url=os.getenv("SCALEKIT_ENVIRONMENT_URL"),
    client_id=os.getenv("SCALEKIT_CLIENT_ID"),
    client_secret=os.getenv("SCALEKIT_CLIENT_SECRET")
)

@app.post("/webhooks/scalekit")
async def webhook_handler(request: Request):
    webhook_secret = os.getenv("SCALEKIT_WEBHOOK_SECRET")
    raw_body = await request.body()

    # STEP 1: Verify signature (NEVER skip this!)
    try:
        scalekit.verify_webhook_payload(
            secret=webhook_secret,
            headers=request.headers,
            payload=raw_body
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # STEP 2: Parse the event
    event = json.loads(raw_body.decode('utf-8'))

    # STEP 3: Process based on event type
    try:
        event_type = event.get("type")
        data = event.get("data")

        if event_type == "organization.directory.user_created":
            await handle_user_created(data)
        elif event_type == "organization.directory.user_updated":
            await handle_user_updated(data)
        elif event_type == "organization.directory.user_deleted":
            await handle_user_deleted(data)
        elif event_type == "organization.directory.group_created":
            await handle_group_created(data)
        elif event_type == "organization.directory.group_membership_updated":
            await handle_group_membership_updated(data)

        return {"status": "ok"}
    except Exception as e:
        print(f"Processing failed: {e}")
        raise HTTPException(status_code=500, detail="Processing failed")
```

### Go

```go
package main

import (
    "encoding/json"
    "io"
    "net/http"
    "os"

    "github.com/scalekit-inc/scalekit-sdk-go"
)

func webhookHandler(w http.ResponseWriter, r *http.Request) {
    // STEP 1: Read body
    body, _ := io.ReadAll(r.Body)
    defer r.Body.Close()

    // STEP 2: Verify signature (NEVER skip this!)
    headers := map[string]string{
        "webhook-id":        r.Header.Get("webhook-id"),
        "webhook-signature": r.Header.Get("webhook-signature"),
        "webhook-timestamp": r.Header.Get("webhook-timestamp"),
    }

    _, err := scalekitClient.VerifyWebhookPayload(
        os.Getenv("SCALEKIT_WEBHOOK_SECRET"),
        headers,
        body,
    )
    if err != nil {
        http.Error(w, "Invalid signature", http.StatusBadRequest)
        return
    }

    // STEP 3: Parse event
    var event WebhookEvent
    json.Unmarshal(body, &event)

    // STEP 4: Process based on type
    switch event.Type {
    case "organization.directory.user_created":
        handleUserCreated(event.Data)
    case "organization.directory.user_updated":
        handleUserUpdated(event.Data)
    case "organization.directory.user_deleted":
        handleUserDeleted(event.Data)
    case "organization.directory.group_created":
        handleGroupCreated(event.Data)
    case "organization.directory.group_membership_updated":
        handleGroupMembershipUpdated(event.Data)
    }

    w.WriteHeader(http.StatusOK)
}

func main() {
    http.HandleFunc("/webhooks/scalekit", webhookHandler)
    http.ListenAndServe(":3000", nil)
}
```

## Step 3: Implement Event Handlers

### User Created

```javascript
async function handleUserCreated(data) {
  const { id, email, given_name, family_name, organization_id } = data;

  // Create user in your database
  await db.users.create({
    external_id: id,
    email: email,
    first_name: given_name,
    last_name: family_name,
    organization_id: organization_id,
    active: true
  });

  console.log(`User created: ${email}`);

  // TODO: Send welcome email
  // TODO: Assign default permissions
  // TODO: Add to default groups
}
```

### User Updated

```javascript
async function handleUserUpdated(data) {
  const { id, email, given_name, family_name, active } = data;

  // Update user in your database
  await db.users.update(
    { external_id: id },
    {
      email: email,
      first_name: given_name,
      last_name: family_name,
      active: active
    }
  );

  // If deactivated, revoke their sessions
  if (!active) {
    await revokeUserSessions(id);
  }

  console.log(`User updated: ${email}`);

  // TODO: Send notification if role changed
  // TODO: Update cached user data
}
```

### User Deleted

```javascript
async function handleUserDeleted(data) {
  const { id, email } = data;

  // Soft delete (recommended for audit trail)
  await db.users.update(
    { external_id: id },
    {
      active: false,
      deleted_at: new Date()
    }
  );

  // Revoke all sessions immediately
  await revokeUserSessions(id);

  console.log(`User deleted: ${email}`);

  // TODO: Archive user data
  // TODO: Remove from all groups
  // TODO: Send offboarding notification
}
```

### Group Created

```javascript
async function handleGroupCreated(data) {
  const { id, name, organization_id } = data;

  // Create group in your database
  await db.groups.create({
    external_id: id,
    name: name,
    organization_id: organization_id
  });

  console.log(`Group created: ${name}`);

  // TODO: Map group to application roles
  // TODO: Set default permissions for group
}
```

### Group Membership Updated

```javascript
async function handleGroupMembershipUpdated(data) {
  const { group_id, added_members, removed_members } = data;

  // Add new members
  for (const userId of added_members || []) {
    await db.group_members.create({
      group_external_id: group_id,
      user_external_id: userId
    });

    // TODO: Update user permissions based on group
  }

  // Remove members
  for (const userId of removed_members || []) {
    await db.group_members.delete({
      group_external_id: group_id,
      user_external_id: userId
    });

    // TODO: Revoke group-based permissions
  }

  console.log(`Group membership updated`);
}
```

## Step 4: Register Webhook in Dashboard

1. Go to **Dashboard > Webhooks**
2. Click **+Add Endpoint**
3. Enter URL: `https://your-app.com/webhooks/scalekit`
4. Select events:
   - ✅ `organization.directory.user_created`
   - ✅ `organization.directory.user_updated`
   - ✅ `organization.directory.user_deleted`
   - ✅ `organization.directory.group_created`
   - ✅ `organization.directory.group_membership_updated`
5. **Copy the webhook secret** → Add to `.env` as `SCALEKIT_WEBHOOK_SECRET`

## Step 5: Test Your Integration

### Using Dashboard

1. Go to **Dashboard > Webhooks > Your Endpoint**
2. Click **Send Test Event**
3. Check your application logs

### With Real Directory Provider

1. Configure test organization in Dashboard
2. Connect test directory (Okta/Azure AD/Google)
3. Create/update/delete test user in directory
4. Verify webhook received and user synced

## Database Schema

### Users Table

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  external_id VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) NOT NULL,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  active BOOLEAN DEFAULT true,
  organization_id VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP
);

CREATE INDEX idx_user_external_id ON users(external_id);
CREATE INDEX idx_user_email ON users(email);
```

### Groups Table

```sql
CREATE TABLE groups (
  id SERIAL PRIMARY KEY,
  external_id VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  organization_id VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_group_external_id ON groups(external_id);
```

### Group Members Table

```sql
CREATE TABLE group_members (
  id SERIAL PRIMARY KEY,
  group_external_id VARCHAR(255) NOT NULL,
  user_external_id VARCHAR(255) NOT NULL,
  added_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(group_external_id, user_external_id)
);
```

## Important Notes

### Security

**ALWAYS verify webhook signatures** - This prevents unauthorized access to your provisioning system.

**Use HTTPS** - Webhook endpoint must use HTTPS in production.

**Validate data** - Sanitize inputs before database operations.

### Error Handling

**Return 200/201 for success** - Scalekit stops retrying on success.

**Return 500 for failures** - Scalekit will retry with exponential backoff.

**Don't return 4xx** - Unless the event is truly invalid (prevents retries).

### Retry Policy

Scalekit retries failed webhooks:
- Immediately
- After 5 seconds
- After 5 minutes
- After 30 minutes
- After 2+ hours (multiple attempts)

## Troubleshooting

### Webhook Not Receiving Events

Check:
- Endpoint URL is publicly accessible
- HTTPS certificate is valid
- Webhook registered in dashboard
- Events are selected

### Signature Verification Fails

Check:
- Using correct `SCALEKIT_WEBHOOK_SECRET`
- Not parsing body before verification
- Headers passed correctly to verification

### Users Not Syncing

Check:
- Database connection working
- Event handler not throwing errors
- External IDs stored correctly

## Next Steps (TODOs)

After basic webhook is working, consider:

**Performance:**
- [ ] Add async job queue (Bull, Sidekiq, etc.)
- [ ] Batch database operations
- [ ] Add caching layer

**Reliability:**
- [ ] Track processed event IDs (prevent duplicates)
- [ ] Add database transactions
- [ ] Implement retry logic for failed DB operations

**Monitoring:**
- [ ] Log all webhook events
- [ ] Track processing latency
- [ ] Alert on failures

**Advanced Features:**
- [ ] Bulk user import API endpoint
- [ ] Scheduled reconciliation job
- [ ] User role mapping from groups
- [ ] Custom attribute syncing

## Common Event Types

- `organization.directory.user_created` - New user added
- `organization.directory.user_updated` - User profile changed
- `organization.directory.user_deleted` - User removed
- `organization.directory.group_created` - New group added
- `organization.directory.group_updated` - Group modified
- `organization.directory.group_deleted` - Group removed
- `organization.directory.group_membership_updated` - Members added/removed

## Sample Webhook Payload

```json
{
  "id": "evt_1234567890",
  "type": "organization.directory.user_created",
  "data": {
    "id": "user_abc123",
    "email": "john@company.com",
    "given_name": "John",
    "family_name": "Doe",
    "active": true,
    "organization_id": "org_xyz789",
    "directory_id": "dir_456"
  },
  "timestamp": "2026-02-09T10:30:00Z"
}
```

## Reference

**Documentation:** https://docs.scalekit.com/directory/webhooks
**Dashboard:** https://app.scalekit.com
**Webhook Events Reference:** https://docs.scalekit.com/directory/reference/directory-events