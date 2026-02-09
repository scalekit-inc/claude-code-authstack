#!/bin/bash

# Scalekit Dryrun Testing Helper Script
# Tests Scalekit authentication configuration end-to-end before writing integration code

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored messages
error() {
    echo -e "${RED}✗ Error:${NC} $1" >&2
}

success() {
    echo -e "${GREEN}✓${NC} $1"
}

info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    info "Checking prerequisites..."

    # Check Node.js
    if ! command -v node &> /dev/null; then
        error "Node.js is not installed. Please install Node.js 20 or higher from https://nodejs.org/"
        exit 1
    fi

    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 20 ]; then
        error "Node.js version 20 or higher is required. Current version: $(node --version)"
        exit 1
    fi

    success "Node.js $(node --version) detected"

    # Check npx
    if ! command -v npx &> /dev/null; then
        error "npx is not installed. Please install npm (comes with Node.js)"
        exit 1
    fi

    success "Prerequisites check passed"
}

# Check if port is in use
check_port() {
    if lsof -Pi :12456 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        warning "Port 12456 is already in use"
        read -p "Do you want to continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            info "Please stop the process using port 12456 and try again"
            exit 1
        fi
    fi
}

# Prompt for input with default value
prompt_input() {
    local prompt_text=$1
    local var_name=$2
    local default_value=$3
    local is_secret=${4:-false}

    if [ -n "$default_value" ]; then
        if [ "$is_secret" = true ]; then
            read -p "$prompt_text [$default_value]: " input_value
        else
            read -p "$prompt_text [$default_value]: " input_value
        fi
    else
        read -p "$prompt_text: " input_value
    fi

    if [ -z "$input_value" ] && [ -n "$default_value" ]; then
        eval "$var_name='$default_value'"
    else
        eval "$var_name='$input_value'"
    fi
}

# Validate URL format
validate_url() {
    local url=$1
    if [[ ! $url =~ ^https?:// ]]; then
        error "Invalid URL format. Must start with http:// or https://"
        return 1
    fi
    return 0
}

# Validate client ID format
validate_client_id() {
    local client_id=$1
    if [[ ! $client_id =~ ^skc_ ]]; then
        warning "Client ID should start with 'skc_'. Please verify you're using the correct client ID."
    fi
}

# Main execution
main() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Scalekit Dryrun Testing Tool"
    echo "  Test your authentication setup end-to-end before writing integration code"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo

    check_prerequisites
    check_port

    # Get credentials from environment or prompt
    ENV_URL=${SCALEKIT_ENVIRONMENT_URL:-""}
    CLIENT_ID=${SCALEKIT_CLIENT_ID:-""}

    if [ -z "$ENV_URL" ]; then
        info "Environment URL not found in SCALEKIT_ENVIRONMENT_URL"
        prompt_input "Enter your Scalekit environment URL" "ENV_URL" ""
    else
        success "Using environment URL from SCALEKIT_ENVIRONMENT_URL"
    fi

    if [ -z "$CLIENT_ID" ]; then
        info "Client ID not found in SCALEKIT_CLIENT_ID"
        prompt_input "Enter your OAuth client ID (starts with skc_)" "CLIENT_ID" ""
    else
        success "Using client ID from SCALEKIT_CLIENT_ID"
    fi

    # Validate inputs
    if [ -z "$ENV_URL" ] || [ -z "$CLIENT_ID" ]; then
        error "Environment URL and Client ID are required"
        exit 1
    fi

    validate_url "$ENV_URL" || exit 1
    validate_client_id "$CLIENT_ID"

    # Prompt for mode
    echo
    info "Select authentication mode:"
    echo "  1) Full Stack Auth (FSA) - Default"
    echo "  2) Modular SSO"
    read -p "Enter choice [1]: " mode_choice
    mode_choice=${mode_choice:-1}

    MODE="fsa"
    ORG_ID=""

    if [ "$mode_choice" = "2" ]; then
        MODE="sso"
        prompt_input "Enter organization ID (org_...)" "ORG_ID" ""
        if [ -z "$ORG_ID" ]; then
            error "Organization ID is required for SSO mode"
            exit 1
        fi
    fi

    # Build command
    CMD="npx @scalekit-sdk/dryrun --env_url=$ENV_URL --client_id=$CLIENT_ID --mode=$MODE"

    if [ -n "$ORG_ID" ]; then
        CMD="$CMD --organization_id=$ORG_ID"
    fi

    # Show what will be executed
    echo
    info "Ready to execute dryrun with the following configuration:"
    echo "  Environment URL: $ENV_URL"
    echo "  Client ID: $CLIENT_ID"
    echo "  Mode: $MODE"
    if [ -n "$ORG_ID" ]; then
        echo "  Organization ID: $ORG_ID"
    fi
    echo

    read -p "Continue? (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        info "Cancelled"
        exit 0
    fi

    # Reminder about redirect URI
    echo
    warning "Make sure you have added this redirect URI in your Scalekit Dashboard:"
    echo "  http://localhost:12456/auth/callback"
    echo "  (Dashboard > Authentication > Redirect URIs)"
    echo
    read -p "Press Enter to continue..."

    # Execute dryrun
    echo
    info "Executing dryrun..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo

    eval "$CMD" || {
        echo
        error "Dryrun failed. Common issues:"
        echo "  1. Redirect URI mismatch - verify http://localhost:12456/auth/callback is added in Dashboard"
        echo "  2. Invalid client ID - check you're using the correct client from the same environment"
        echo "  3. Port conflict - ensure port 12456 is available"
        echo "  4. Organization not found (SSO mode) - verify org ID exists and SSO is configured"
        echo
        echo "See https://docs.scalekit.com/dev-kit/tools/scalekit-dryrun/ for troubleshooting"
        exit 1
    }
}

# Run main function
main "$@"
