# Scalekit Dryrun Plugin

Validate Scalekit authentication setup end-to-end from Claude Code before writing integration code.

## Includes

- Slash command: `/scalekit-dryrun`
- Skill: `scalekit-dryrun`

## Quick usage

```bash
/scalekit-dryrun fsa https://env-abc123.scalekit.com skc_xxxxxxxxxxxx
```

```bash
/scalekit-dryrun sso https://env-abc123.scalekit.com skc_xxxxxxxxxxxx org_xxxxxxxxxxxx
```

The plugin runs `npx @scalekit-sdk/dryrun` to verify OAuth flow, redirect URI setup, and token/profile output locally.
