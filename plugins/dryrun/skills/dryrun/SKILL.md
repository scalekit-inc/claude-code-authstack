---
name: scalekit-dryrun
description: Validate Scalekit authentication setup end-to-end before writing integration code using the dryrun CLI.
argument-hint: "[mode] [env_url] [client_id] [organization_id?]"
disable-model-invocation: true
allowed-tools: Bash(node *), Bash(npx *)
---

# Scalekit Dryrun Testing

Quickly test your Scalekit authentication setup end-to-end before writing any integration code. The dryrun tool executes a complete authentication flow locally - spinning up a server, opening your browser, and displaying the authenticated user's profile and tokens.

Whether you’re building full stack authentication (authorization, user management, sessions, hosted login pages, and more) or using SSO in a modular way (Modular SSO), dryrun lets you validate your entire auth setup end‑to‑end before writing any integration code.


## When to use this skill

Use when:

- Testing a new Scalekit environment before integration
- Verifying FSA or SSO configuration works correctly
- Debugging redirect URI errors, invalid credentials, or org setup
- Validating user profiles and token claims for a specific environment

Do not use when:

- Writing production integration code (use SDK quickstarts instead)
- Only browsing documentation without running commands
- Troubleshooting non-authentication features

## Prerequisites

Before running dryrun, ensure:

- **Node.js 20 or higher** installed (`node --version`)
- **Scalekit environment** with OAuth client configured
- **Redirect URI** `http://localhost:12456/auth/callback` added in Dashboard under **Authentication > Redirect URIs**
- Access to your `env_url`, `client_id`, and optional `organization_id`

## Quick Start

Run dryrun with either mode:

**Full Stack Authentication:**
```bash
npx @scalekit-sdk/dryrun \
  --env_url=https://env-abc123.scalekit.com \
  --client_id=skc_xxxxxxxxxxxx \
  --mode=fsa
```

**Modular SSO:**
```bash
npx @scalekit-sdk/dryrun \
  --env_url=https://env-abc123.scalekit.com \
  --client_id=skc_xxxxxxxxxxxx \
  --mode=sso \
  --organization_id=org_xxxxxxxxxxxx
```

Get credentials from **Dashboard > Developers > Settings > API Credentials**.

## How this skill works

When you invoke `/scalekit-dryrun $ARGUMENTS`, I will:

1. **Parse arguments or prompt for missing values**
   - Extract mode, env_url, client_id, and optional organization_id from $ARGUMENTS
   - If incomplete, ask for missing configuration

2. **Validate prerequisites**
   - Confirm Node.js 20+ is installed
   - Verify redirect URI is configured in dashboard
   - Check port 12456 availability

3. **Execute dryrun**
   - Use helper script if available: `./skills/dryrun/test-scalekit.sh`
   - Otherwise construct npx command with provided credentials

4. **Guide browser flow**
   - Instruct you to complete authentication in opened browser
   - Ask you to verify displayed user profile and claims

5. **Interpret results**
   - Confirm expected user, email, and token claims appear
   - Map any errors to troubleshooting steps below

## What Dryrun Does

The dryrun command:

- Spins up local server on `http://localhost:12456`
- Opens browser automatically
- Executes complete OAuth flow
- Displays user profile, ID token claims, and token details
- Validates configuration end-to-end

**Local only**: Runs entirely on localhost, no public endpoints, does not persist tokens.

## Common Issues

### Redirect URI mismatch

**Symptoms**: `redirect_uri mismatch` error

**Fix**:
- Add `http://localhost:12456/auth/callback` in **Authentication > Redirect URIs**
- Verify exact spelling including port and path

### Invalid client ID

**Symptoms**: Invalid client ID error

**Fix**:
- Copy client ID from dashboard to avoid typos
- Ensure client ID and env_url are from same environment

### Port 12456 in use

**Symptoms**: Port already in use error

**Fix**:
- Stop processes using port 12456
- Retry dryrun

### Organization issues (SSO mode)

**Symptoms**: Errors about organization_id

**Fix**:
- Verify organization exists in environment
- Confirm SSO is configured for that organization
- Check you're using correct `org_...` identifier
- Try `fsa` mode if not testing SSO

### Node.js version

**Symptoms**: Command not found or version errors

**Fix**:
- Install Node.js 20+ from nodejs.org
- Verify with `node --version`

## Helper Script

If `./skills/dryrun/test-scalekit.sh` exists, it provides:

- Automatic prerequisite checking
- Interactive prompts for missing values
- Input validation
- Better error messages
- Port conflict detection

## Example Invocations

**Test FSA for new environment:**
```
/scalekit-dryrun fsa https://env-abc123.scalekit.cloud skc_xxxxxxxxxxxx
```

**Debug SSO for customer org:**
```
/scalekit-dryrun sso https://env-xyz789.scalekit.cloud skc_yyyyyyyyyyyy org_acme123
```

## Resources

- [Scalekit Dryrun Documentation](https://docs.scalekit.com/dev-kit/tools/scalekit-dryrun/)
- [Scalekit Dashboard](https://app.scalekit.com)
- [@scalekit-sdk/dryrun on npm](https://www.npmjs.com/package/@scalekit-sdk/dryrun)
- [FSA Quickstart](https://docs.scalekit.com/authenticate/fsa/quickstart/)
```