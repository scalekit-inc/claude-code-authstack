#!/usr/bin/env bash

set -euo pipefail

REPO_SLUG="${CLAUDE_CODE_AUTHSTACK_REPO:-scalekit-inc/claude-code-authstack}"
REPO_REF="${CLAUDE_CODE_AUTHSTACK_REF:-main}"
SOURCE_DIR="${CLAUDE_CODE_AUTHSTACK_SOURCE_DIR:-}"

if [[ -n "$SOURCE_DIR" ]]; then
  exec "${SOURCE_DIR%/}/scripts/install.sh"
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

ARCHIVE_URL="https://github.com/${REPO_SLUG}/archive/refs/heads/${REPO_REF}.tar.gz"
ARCHIVE_PATH="$TMP_DIR/claude-code-authstack.tar.gz"

echo "Downloading Scalekit Auth Stack for Claude Code from:"
echo "  $ARCHIVE_URL"

curl -fsSL "$ARCHIVE_URL" -o "$ARCHIVE_PATH"
tar -xzf "$ARCHIVE_PATH" -C "$TMP_DIR"

EXTRACTED_DIR="$(find "$TMP_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 1)"

if [[ -z "$EXTRACTED_DIR" ]] || [[ ! -x "$EXTRACTED_DIR/scripts/install.sh" ]]; then
  echo "Failed to find installer in downloaded archive." >&2
  exit 1
fi

exec "$EXTRACTED_DIR/scripts/install.sh"
