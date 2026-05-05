#!/usr/bin/env python3
"""
AgentKit playground for Claude Code.

Supports:
- generate-link
- get-tool
- execute-tool
"""

import argparse
import json
import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from google.protobuf.json_format import MessageToDict
except ImportError:
    MessageToDict = None

import scalekit.client as scalekit_sdk


BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def env_value(primary: str, legacy: str) -> str:
    return os.getenv(primary) or os.getenv(legacy) or ""


SCALEKIT_ENV_URL = env_value("SCALEKIT_ENV_URL", "TOOL_ENV_URL")
SCALEKIT_CLIENT_ID = env_value("SCALEKIT_CLIENT_ID", "TOOL_CLIENT_ID")
SCALEKIT_CLIENT_SECRET = env_value("SCALEKIT_CLIENT_SECRET", "TOOL_CLIENT_SECRET")


def require_env() -> None:
    missing = []
    if not SCALEKIT_ENV_URL:
        missing.append("SCALEKIT_ENV_URL")
    if not SCALEKIT_CLIENT_ID:
        missing.append("SCALEKIT_CLIENT_ID")
    if not SCALEKIT_CLIENT_SECRET:
        missing.append("SCALEKIT_CLIENT_SECRET")
    if missing:
        print(f"{RED}Missing required environment variables: {', '.join(missing)}{RESET}")
        print("Legacy TOOL_* aliases are also supported.")
        sys.exit(1)


def get_scalekit_client():
    require_env()
    return scalekit_sdk.ScalekitClient(
        SCALEKIT_ENV_URL,
        SCALEKIT_CLIENT_ID,
        SCALEKIT_CLIENT_SECRET,
    )


def get_connect_client():
    client = get_scalekit_client()
    return client.actions if hasattr(client, "actions") else client.connect


def to_jsonable(value):
    if MessageToDict is not None and hasattr(value, "DESCRIPTOR"):
        return MessageToDict(value, preserving_proto_field_name=True)
    if isinstance(value, (dict, list, str, int, float, bool)) or value is None:
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if hasattr(value, "__dict__"):
        return {key: to_jsonable(val) for key, val in vars(value).items() if not key.startswith("_")}
    return str(value)


def print_json(value) -> None:
    print(json.dumps(to_jsonable(value), indent=2))


def get_or_create_account(connection_name: str, identifier: str):
    connect = get_connect_client()
    response = connect.get_or_create_connected_account(
        connection_name=connection_name,
        identifier=identifier,
    )
    return response.connected_account


def generate_link(connection_name: str, identifier: str) -> None:
    connect = get_connect_client()

    print(f"   Connection: {connection_name}")
    print(f"   Identifier: {identifier}")
    print()

    try:
        connected_account = get_or_create_account(connection_name, identifier)
        print(f"   Connected Account ID: {connected_account.id}")
        print(f"   Status: {connected_account.status}")

        if connected_account.status != "ACTIVE":
            link_response = connect.get_authorization_link(
                connection_name=connection_name,
                identifier=identifier,
            )
            print(f"\n{YELLOW}⚠ Connected account is not ACTIVE yet.{RESET}")
            print(f"\n🔗 Click the link to authorize {connection_name}:")
            print(f"   {BLUE}{link_response.link}{RESET}")
        else:
            print(f"\n{GREEN}✅ {connection_name} is already connected and active.{RESET}")

    except Exception as exc:
        print(f"\n{RED}❌ Error: {exc}{RESET}")
        sys.exit(1)


def execute_tool(tool_name: str, connection_name: str, identifier: str, tool_input: dict) -> None:
    connect = get_connect_client()

    print(f"   Tool: {tool_name}")
    print(f"   Connection: {connection_name}")
    print(f"   Identifier: {identifier}")
    print(f"   Input: {json.dumps(tool_input, indent=2)}")
    print()

    try:
        connected_account = get_or_create_account(connection_name, identifier)
        print(f"   Connected Account ID: {connected_account.id}")
        print(f"   Status: {connected_account.status}")

        if connected_account.status != "ACTIVE":
            link_response = connect.get_authorization_link(
                connection_name=connection_name,
                identifier=identifier,
            )
            print(f"\n{YELLOW}⚠ Connected account is not ACTIVE yet.{RESET}")
            print(f"\n🔗 Authorize {connection_name} here:")
            print(f"   {BLUE}{link_response.link}{RESET}")
            print(f"\n{YELLOW}Re-run this command after the user completes authorization.{RESET}")
            sys.exit(0)

        print(f"\n🔧 Executing tool: {BOLD}{tool_name}{RESET}")
        result = connect.execute_tool(
            tool_name=tool_name,
            identifier=identifier,
            connected_account_id=connected_account.id,
            tool_input=tool_input,
        )

        print(f"\n{GREEN}✅ Result:{RESET}")
        print_json(result)

    except Exception as exc:
        print(f"\n{RED}❌ Error: {exc}{RESET}")
        sys.exit(1)


def get_tool(tool_name: str = None, provider: str = None, page_size: int = None, page_token: str = None) -> None:
    client = get_scalekit_client()

    try:
        from scalekit.v1.tools.tools_pb2 import Filter

        filter_kwargs = {}
        if tool_name:
            filter_kwargs["tool_name"] = [tool_name]
        if provider:
            filter_kwargs["provider"] = provider

        list_kwargs = {}
        if filter_kwargs:
            list_kwargs["filter"] = Filter(**filter_kwargs)
        if page_size is not None:
            list_kwargs["page_size"] = page_size
        if page_token:
            list_kwargs["page_token"] = page_token

        response, _ = client.tools.list_tools(**list_kwargs)
        print_json(response)

    except Exception as exc:
        print(f"\n{RED}❌ Error: {exc}{RESET}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AgentKit playground - generate auth links, fetch tool metadata, and execute tools",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--generate-link", action="store_true", help="Generate authorization link if needed")
    group.add_argument("--get-tool", action="store_true", help="Fetch live tool metadata")
    group.add_argument("--execute-tool", action="store_true", help="Execute a live tool")

    parser.add_argument("--connection-name", help="Exact dashboard connection name")
    parser.add_argument("--identifier", help="User or account identifier")
    parser.add_argument("--tool-name", help="Tool name to fetch or execute")
    parser.add_argument("--tool-input", help="JSON string passed to the tool")
    parser.add_argument("--provider", help="Provider filter for live tool discovery")
    parser.add_argument("--page-size", type=int, help="Page size for tool listing")
    parser.add_argument("--page-token", help="Pagination token for tool listing")

    args = parser.parse_args()

    if args.generate_link:
        if not args.connection_name or not args.identifier:
            parser.error("--connection-name and --identifier are required for --generate-link")
        generate_link(args.connection_name, args.identifier)
        return

    if args.get_tool:
        get_tool(
            tool_name=args.tool_name,
            provider=args.provider,
            page_size=args.page_size,
            page_token=args.page_token,
        )
        return

    if not args.connection_name or not args.identifier or not args.tool_name or not args.tool_input:
        parser.error("--connection-name, --identifier, --tool-name, and --tool-input are required for --execute-tool")

    try:
        tool_input = json.loads(args.tool_input)
    except json.JSONDecodeError as exc:
        print(f"{RED}❌ Invalid JSON for --tool-input: {exc}{RESET}")
        sys.exit(1)

    execute_tool(
        tool_name=args.tool_name,
        connection_name=args.connection_name,
        identifier=args.identifier,
        tool_input=tool_input,
    )


if __name__ == "__main__":
    main()
