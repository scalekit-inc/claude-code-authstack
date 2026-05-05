#!/usr/bin/env bash

set -euo pipefail

if ! command -v claude >/dev/null 2>&1; then
  echo "Claude Code CLI is not installed or not on PATH." >&2
  echo "Install Claude Code first, then re-run this installer." >&2
  exit 1
fi

MARKETPLACE_SLUG="${CLAUDE_CODE_AUTHSTACK_MARKETPLACE:-scalekit-inc/claude-code-authstack}"
PLUGIN_SOURCE="${CLAUDE_CODE_AUTHSTACK_PLUGIN_SOURCE:-agent-auth@scalekit-auth-stack}"

echo "Installing Scalekit Auth Stack for Claude Code"
echo "Marketplace: $MARKETPLACE_SLUG"
echo "Plugin: $PLUGIN_SOURCE"
echo

claude plugin marketplace add "$MARKETPLACE_SLUG"
claude plugin install "$PLUGIN_SOURCE"

cat <<EOF

Installed Agent Auth from Scalekit Auth Stack.

Next steps:
1. Run \`/plugins\` in Claude Code.
2. Open \`Marketplaces\`.
3. Select \`scalekit-auth-stack\`.
4. Enable auto-update.
EOF
