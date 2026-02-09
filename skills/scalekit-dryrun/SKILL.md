---
name: scalekit-dryrun
description: Quickly test Scalekit authentication setup end-to-end before writing integration code using the dryrun tool. Use when you need to validate Scalekit configuration, test authentication flows, verify credentials, or troubleshoot auth setup. Works with Full Stack Auth (FSA) and Modular SSO modes.
license: MIT
metadata:
  author: Scalekit
  version: 1.0.0
  category: testing
  tags: [testing, dryrun, scalekit, authentication, validation]
  documentation: https://docs.scalekit.com/dev-kit/tools/scalekit-dryrun/
---

# Scalekit Dryrun Testing

Quickly test your Scalekit authentication setup end-to-end before writing any integration code. The dryrun tool executes a complete authentication flow locally - spinning up a server, opening your browser, and displaying the authenticated user's profile and tokens, so you can catch configuration errors early.

Works with **Full Stack Authentication** and **Modular SSO**.

## Quick Start

### Prerequisites

Before running dryrun, ensure you have:

- **Node.js 20 or higher** installed locally
- **A Scalekit environment** with an OAuth client configured
- **A redirect URI** (`http://localhost:12456/auth/callback`) added in the Scalekit Dashboard under **Authentication > Redirect URIs**

### Run Dryrun

You can run dryrun interactively using the helper script, or manually with npx:

**Using the helper script:**
```bash
./skills/scalekit-dryrun/test-scalekit.sh
```

**Manual execution:**
```bash
npx @scalekit-sdk/dryrun \
  --env_url=<your-environment-url> \
  --client_id=<your-client-id> \
  [--mode=<sso|fsa>] \
  [--organization_id=<org-id>]
```

### Get Your Credentials

Find your environment URL and client ID in **Dashboard > Developers > Settings > API Credentials**.

## Usage Guide

### Testing Full Stack Auth (FSA)

Test your full-stack authentication configuration:

```bash
npx @scalekit-sdk/dryrun \
  --env_url=https://env-abc123.scalekit.cloud \
  --client_id=skc_xxxxxxxxxxxx \
  --mode=fsa
```

### Testing Modular SSO

Test your SSO configuration for a specific organization:

```bash
npx @scalekit-sdk/dryrun \
  --env_url=https://env-abc123.scalekit.cloud \
  --client_id=skc_xxxxxxxxxxxx \
  --mode=sso \
  --organization_id=org_xxxxxxxxxxxx
```

### Interactive Mode

When you invoke this skill, I'll help you:

1. **Detect your mode**: Ask if you want to test FSA or SSO
2. **Gather credentials**: Prompt for env_url and client_id (or read from environment variables if available)
3. **Validate prerequisites**: Check Node.js version, verify redirect URI is configured
4. **Execute dryrun**: Run the helper script which wraps `npx @scalekit-sdk/dryrun`
5. **Interpret results**: Help you understand the output and troubleshoot if needed

## What Dryrun Does

The dryrun command:

- Spins up a local server on `http://localhost:12456`
- Opens your browser automatically
- Executes a complete OAuth authentication flow
- Displays the authenticated user's profile, ID token claims, and token details
- Validates your Scalekit configuration end-to-end

**Local testing only**: Dryrun runs entirely on `localhost` and does not expose any public endpoints. It does not persist tokens or credentials after the process exits.

## Review Authentication Results

After successful authentication, the browser shows a local dashboard with:

- **User profile**: Name, email, avatar (when available)
- **ID token claims**: All claims returned in the ID token
- **Token details**: A view of the raw token response

Use this view to confirm:

- The correct user is returned for your test login
- Claims such as `email`, `sub`, and any custom claims are present as expected
- The flow works for both `fsa` and `sso` modes when configured

## Common Issues and Solutions

### Redirect URI Mismatch Error

**Symptoms**: `redirect_uri mismatch` error

**Solutions**:
- Verify that `http://localhost:12456/auth/callback` is added in the Scalekit Dashboard under **Authentication > Redirect URIs**
- Confirm that you spelled the URI exactly, including the port and path

### Invalid Client ID Error

**Symptoms**: CLI reports an invalid client ID

**Solutions**:
- Copy the client ID directly from the dashboard to avoid typos
- Make sure you are using a client from the same environment as `--env_url`

### Port Conflicts

**Symptoms**: Port `12456` is already in use

**Solutions**:
- Stop any process that is already listening on port `12456`
- Close other local tools or frameworks that use `http://localhost:12456` and try again

### Organization Issues in SSO Mode

**Symptoms**: Errors related to `--organization_id`

**Solutions**:
- Confirm that the organization exists in your Scalekit environment
- Verify that SSO is configured for that organization in the dashboard
- Ensure you are using the correct `org_...` identifier

### Missing Node.js or Wrong Version

**Symptoms**: Command not found or version errors

**Solutions**:
- Install Node.js 20 or higher from [nodejs.org](https://nodejs.org/)
- Verify installation: `node --version` should show v20.0.0 or higher

## Helper Script

The included `test-scalekit.sh` script provides:

- Automatic prerequisite checking (Node.js version, credentials)
- Interactive prompts for missing credentials
- Input validation before execution
- Better error messages with troubleshooting tips
- Port conflict detection

Run it directly:
```bash
./skills/scalekit-dryrun/test-scalekit.sh
```

Or let Claude execute it when you invoke this skill.

## Resources

- [Scalekit Dryrun Documentation](https://docs.scalekit.com/dev-kit/tools/scalekit-dryrun/)
- [Scalekit Dashboard](https://app.scalekit.com)
- [Dryrun on GitHub](https://github.com/scalekit-inc/scalekit-sdk/tree/main/packages/dryrun)
- [@scalekit-sdk/dryrun on npm](https://www.npmjs.com/package/@scalekit-sdk/dryrun)
