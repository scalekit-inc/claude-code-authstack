# Scalekit AuthStack for Claude Code

Setting up auth stack for B2B and AI apps is complex. Between auth flows, SSO providers, SCIM provisioning, MCP auth and securing AI agents, most developers spend weeks on auth instead of building features that they can go live with with confidence; even if it's vibe coded. T

![Scalekit AuthStack demo](./images/scalekit-authstack-demo.gif)


This is a plugin to add auth stack for your projects whether that's B2B app, Agent or MCP servers.

To add this to your claude code

```sh
# Start Claude REPL
claude

# Add Scalekit Auth Stack marketplace
/plugin marketplace add scalekit-inc/claude-code-authstack
#Run the plugins wizard
/plugin
```

Plugins for:

**🔍 Dryrun** - Validate auth and provisioning flows before deployment
Test your configuration against real identity providers without touching production. Catches misconfigurations early.

**🔐 MCP Auth** - Add OAuth 2.1 authorization to Model Context Protocol servers
Secure your MCP servers with production-ready OAuth. Guides you through token handling, refresh flows, and scope management.

**🏢 Modular SSO** - Integrate enterprise SSO providers (Okta, JumpCloud, Entra ID, etc.)
Support 20+ identity providers without writing SAML parsers. Handles connection setup, attribute mapping, and JIT provisioning.

**👥 Modular SCIM** - Enable user provisioning and directory sync
Let customers provision users automatically from their identity provider. Implements SCIM 2.0 with automatic schema mapping.

**⚡ Full Stack Auth** - Complete authentication setup for web applications
End-to-end auth implementation including login pages, session management, and protected routes. Works with Next.js, React, and Node.js.

**🤖 Agent Auth** - Secure authentication for AI agents and services
OAuth flows designed for AI agents—handles token persistence, refresh logic, and service-to-service auth.

