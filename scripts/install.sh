#!/usr/bin/env bash

set -euo pipefail

if ! command -v claude >/dev/null 2>&1; then
  echo "Claude Code CLI is not installed or not on PATH." >&2
  echo "Install Claude Code first, then re-run this installer." >&2
  exit 1
fi

MARKETPLACE_SLUG="${CLAUDE_CODE_AUTHSTACK_MARKETPLACE:-scalekit-inc/claude-code-authstack}"
OLD_PLUGINS=("agent-auth" "full-stack-auth" "mcp-auth" "modular-sso" "modular-scim")

echo "Installing Scalekit Auth Stack for Claude Code"
echo "Marketplace: $MARKETPLACE_SLUG"
echo

if ! claude plugin marketplace add "$MARKETPLACE_SLUG" 2>/dev/null; then
  echo "Marketplace \"scalekit-auth-stack\" is already registered."
  echo "To get the latest plugins, enable auto-update or run:"
  echo "  claude plugin update --all"
  echo
fi

# Remove old plugin names from v1.x (now consolidated into agentkit + saaskit)
for old in "${OLD_PLUGINS[@]}"; do
  claude plugin uninstall "${old}@scalekit-auth-stack" 2>/dev/null || true
done

claude plugin install agentkit@scalekit-auth-stack
claude plugin install saaskit@scalekit-auth-stack

cat <<EOF

Installed Scalekit Auth Stack for Claude Code.

Installed plugins:
  agentkit  — AI agent authentication (connectors, tool discovery, token vault)
  saaskit   — B2B SaaS authentication (login, SSO, SCIM, RBAC, MCP server auth)

What to do next in Claude Code:
- Look for the "scalekit-auth-stack" marketplace in your plugin settings.
- Install both plugins: "agentkit" and "saaskit".
- Set the update policy to auto-update so you always have the latest skills.

To verify it works:
  Ask Claude Code to "help me integrate agentkit" or "test my auth setup".
EOF
