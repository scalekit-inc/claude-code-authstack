# MCP OAuth Authorization Skill

A Claude Code skill that guides users through adding production-ready OAuth 2.1 authorization to Model Context Protocol (MCP) servers using Scalekit.

## What This Skill Does

This skill helps Claude assist users in:
- Setting up OAuth 2.1 authorization for MCP servers
- Implementing token validation middleware
- Configuring Scalekit as the authorization server
- Adding scope-based access control
- Testing and deploying secure MCP servers

When users ask about securing MCP servers, implementing authentication for AI hosts (Claude Desktop, Cursor, VS Code), or integrating Scalekit with MCP, Claude will automatically use this skill to provide step-by-step guidance.

## Installation

### Option 1: Part of Plugin (Recommended)

If this skill is part of the `mcp-auth` plugin, it will be automatically available when the plugin is loaded.

1. Ensure the plugin structure is correct:
```
claude-code-auth-plugin/
└── plugins/
    └── mcp-auth/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            └── mcp-auth/
                ├── SKILL.md
                └── README.md (this file)
```

2. Claude Code will automatically discover and load the skill when relevant.

### Option 2: Standalone Skill

Copy the `mcp-auth` directory to your Claude Code skills directory:

**macOS/Linux:**
```bash
cp -r mcp-auth ~/.claude/skills/
```

**Windows:**
```powershell
Copy-Item -Recurse mcp-auth "$env:USERPROFILE\.claude\skills\"
```

## Usage

### Trigger Phrases

Claude will activate this skill when users mention:
- "add OAuth to my MCP server"
- "secure my MCP server"
- "implement authentication for MCP"
- "use Scalekit with MCP"
- "add auth to Model Context Protocol server"
- "protect MCP tools"
- "MCP server security"

### Example Interactions

**User:** "I need to add authentication to my MCP server"

**Claude:** Will provide a complete workflow with:
1. Scalekit SDK installation instructions
2. Dashboard configuration steps
3. Discovery endpoint implementation
4. Token validation middleware setup
5. Testing and deployment checklists

**User:** "How do I implement scope-based authorization for my MCP tools?"

**Claude:** Will guide through:
1. Defining scopes in Scalekit dashboard
2. Adding scope validation to tool execution
3. Handling insufficient scope errors
4. Testing scope enforcement

## Prerequisites

Users working with this skill should have:
- An MCP server project (Node.js or Python)
- A Scalekit account (free tier available at app.scalekit.com)
- Basic understanding of:
  - REST APIs
  - OAuth 2.1 concepts (token-based authentication)
  - Express.js (Node.js) or FastAPI (Python)

## Supported Frameworks

The skill provides guidance for:
- **Node.js**: Express.js
- **Python**: FastAPI, FastMCP
- Both include complete code examples

## What's Included

### SKILL.md Structure

1. **Setup Workflow**: 6-step checklist for complete OAuth implementation
2. **Step-by-step Instructions**: Detailed guidance for each phase
3. **Code Examples**: Working implementations for Node.js and Python
4. **Optional Features**: Scope-based authorization, additional auth methods
5. **Testing Guidance**: Checklists for verification and deployment
6. **Troubleshooting**: Common issues and solutions

### Key Features

- ✅ Progressive disclosure (core steps first, advanced features optional)
- ✅ Framework-specific code examples
- ✅ Copy-paste ready code snippets
- ✅ Production deployment checklist
- ✅ Testing guidance for multiple AI hosts
- ✅ Troubleshooting common issues

## Skill Metadata

```yaml
name: adding-mcp-oauth
description: Guides users through adding OAuth 2.1 authorization to Model Context Protocol (MCP) servers using Scalekit. Use when setting up MCP servers, implementing authentication for AI hosts like Claude Desktop, Cursor, or VS Code, or when users mention MCP security, OAuth, or Scalekit integration.
```

## Design Philosophy

This skill follows Claude Code best practices:

1. **Concise**: Assumes Claude already understands OAuth and APIs
2. **Workflow-based**: Provides clear sequential steps with checklists
3. **Medium freedom**: Specific patterns for fragile operations (token validation), flexibility for implementation details
4. **Practical**: Working code examples over theoretical explanations
5. **Testing-focused**: Includes verification at every step

## Customization

### Adding Framework Support

To add support for additional frameworks:

1. Add a new code example section in SKILL.md
2. Follow the same pattern: initialization → middleware → validation
3. Keep examples concise (20-30 lines max)
4. Test with Claude to ensure discoverability

### Extending Authentication Methods

To add guidance for additional auth methods:

1. Add a new section under "Additional authentication methods"
2. Explain when to use the method
3. Link to relevant Scalekit documentation
4. Keep explanation under 5 lines

## Testing This Skill

### Manual Testing

1. Start a conversation with Claude Code
2. Ask: "How do I add OAuth to my MCP server?"
3. Verify Claude:
   - Provides the 6-step workflow
   - Offers code examples for your chosen framework
   - Includes testing and deployment checklists

### Evaluation Scenarios

**Scenario 1: New MCP server**
- Query: "I'm building a new MCP server and need to add authentication"
- Expected: Complete workflow from SDK installation through deployment

**Scenario 2: Existing server**
- Query: "I have an Express MCP server, how do I secure it with OAuth?"
- Expected: Framework-specific guidance, focus on middleware implementation

**Scenario 3: Scope-based auth**
- Query: "How do I restrict certain MCP tools to specific users?"
- Expected: Scope definition and validation guidance

## Troubleshooting

### Skill Not Triggering

**Issue**: Claude doesn't use the skill when asked about MCP authentication

**Solutions**:
- Verify SKILL.md has correct YAML frontmatter
- Check the description includes key terms: "MCP", "OAuth", "authorization"
- Try more specific phrases: "add OAuth to MCP server"

### Code Examples Not Working

**Issue**: Generated code doesn't match user's setup

**Solutions**:
- Remind Claude of your specific framework (Express, FastAPI, etc.)
- Ask Claude to adapt the example for your environment
- Check Scalekit dashboard values match code placeholders

## Contributing

### Improving This Skill

To enhance the skill:

1. Test with real MCP server projects
2. Note where Claude struggles or provides incomplete guidance
3. Add missing information to SKILL.md
4. Keep additions concise (challenge each sentence)
5. Test changes with fresh Claude instances

### Reporting Issues

If you find issues:
- Describe the user query that triggered unexpected behavior
- Share what Claude provided vs. what was needed
- Suggest specific improvements

## Related Resources

- [Scalekit MCP Documentation](https://docs.scalekit.com/authenticate/mcp/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/agent-skills)
- [Scalekit Dashboard](https://app.scalekit.com/)

## Version History

### v1.0.0 (February 2026)
- Initial release
- Support for Node.js (Express) and Python (FastAPI)
- 6-step OAuth implementation workflow
- Scope-based authorization guidance
- Testing and deployment checklists

## License

This skill is provided as part of the claude-code-auth-plugin. See the main plugin directory for license information.

## Author

Created by Saif Ali Shaik (@saif) for the Scalekit team.

## Feedback

For questions or suggestions about this skill:
- Open an issue in the plugin repository
- Reach out to the Scalekit team
- Test and iterate based on real usage

---

**Note**: This skill assumes users have basic familiarity with OAuth concepts and MCP servers. For users new to these concepts, Claude may need to provide additional context beyond what's in the skill.
