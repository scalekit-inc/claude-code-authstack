# Code Samples

This page is the canonical code-sample entrypoint for the plugin.

Use it to choose an implementation style before opening a larger sample repository.

## Common paths

| Goal | Recommended path |
|---|---|
| Validate one tool quickly | Use the Scalekit MCP server tools directly |
| Integrate AgentKit into app code | Use `integrating-agentkit` |
| Build an agent with a framework | Use framework-specific examples below |
| Expose tools over MCP | Use `exposing-agentkit-via-mcp` |

## Framework directions

- LangChain: fetch a narrow tool set and hand only the relevant tools to the agent
- Google ADK: use AgentKit-authenticated tool wrappers for Gemini-based agents
- Direct SDK usage: best for deterministic or single-tool flows
- MCP: best when you want tools exposed to MCP-compatible runtimes

## Official Scalekit docs

- [AgentKit examples](https://docs.scalekit.com/agentkit/examples.md)
- [Code samples](https://docs.scalekit.com/agentkit/code-samples.md)
- [LangChain example](https://docs.scalekit.com/agentkit/examples/langchain.md)
- [Google ADK example](https://docs.scalekit.com/agentkit/examples/google-adk.md)

## Important rule

Do not treat example code as a fixed tool catalog.

Examples show patterns, not the current truth of:

- which tools exist
- what their schemas look like
- which fields are required today

Use [tool-discovery.md](tool-discovery.md) first when the exact tool surface matters.

## Suggested sample flow

1. Set up a connection.
2. Create or fetch the connected account.
3. Discover the exact tool and schema.
4. Test it with the live playground.
5. Move the validated payload into application or agent code.

## Related docs

- [tool-discovery.md](tool-discovery.md)
- [connections.md](connections.md)
- [connected-accounts.md](connected-accounts.md)
