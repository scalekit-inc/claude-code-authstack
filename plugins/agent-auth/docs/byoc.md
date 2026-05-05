# Bring Your Own Credentials

Bring Your Own Credentials (BYOC) lets you use your own OAuth applications and credentials instead of shared Scalekit defaults.

## Why teams use BYOC

Common reasons:

- your branding appears during consent flows
- you want your own quotas and provider relationship
- you need stricter compliance or audit ownership
- you want a more fully whitelabeled production experience

## What changes

With BYOC:

- the connection is still managed in AgentKit
- connected accounts still authorize users in the same model
- tools are still discovered and executed through AgentKit

Only the credentials and upstream app ownership change.

## Operational impact

Moving to BYOC can require users to re-authorize, because the underlying OAuth application has changed.

Plan for:

- re-authentication
- updated consent screens
- different quotas or limits
- provider-specific app verification steps

## Where it fits in the plugin

BYOC is a connection-level concern, not a tool-discovery concern.

Set up the connection correctly first, then discover tools and test execution as usual.

## Related docs

- [connections.md](connections.md)
- [connected-accounts.md](connected-accounts.md)
