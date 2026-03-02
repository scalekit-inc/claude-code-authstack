# CLAUDE.md (Repo guide for agents)

This repository contains multiple Claude Code plugins for marketplace distribution.
It is a monorepo. Always work inside one plugin directory at a time.

If you are making changes, read AGENTS.md first and follow it as the source of truth.

## Quick orientation

Top level:

- plugins/ Monorepo root for all plugins
- AGENTS.md Non negotiable rules for manifests, skills, hooks, MCP, security
- README.md Repo overview
- CHANGELOG.md Repo level changelog (also check plugin level changelogs if present)
- .lsp.json LSP configuration for this repo

Plugins (examples you may see here):

- plugins/agent-auth/
- plugins/full-stack-auth/
- plugins/mcp-auth/

Each plugin is expected to look like:
plugins/<plugin-name>/
.claude-plugin/plugin.json Plugin manifest
README.md Required docs for that plugin
skills/<skill-name>/SKILL.md Skill entrypoint
agents/ Optional sub agents
hooks/ Optional hooks.json
.mcp.json Optional MCP config
settings.json Optional default settings

## Golden rules

- Do not edit multiple plugins in one change unless explicitly requested.
- Prefer smallest viable change that improves correctness, safety, or docs.
- Never add secrets, tokens, or credentials to this repo.
- Follow naming rules from AGENTS.md for plugin names and skill names.
- Keep SKILL.md concise and push deep docs into reference.md or examples.md.

## Workflow for improvements

1. Identify the target plugin directory under plugins/<plugin-name>.
2. Read these files before coding:
   - plugins/<plugin-name>/.claude-plugin/plugin.json
   - plugins/<plugin-name>/README.md
   - Any relevant skills/<skill>/SKILL.md
3. Decide the change type:
   - Skill change: update SKILL.md, and add or update reference.md or examples.md if needed.
   - Agent change: update agents/<agent>.md, and ensure allowed-tools and model settings are intentional.
   - Hook change: update hooks/hooks.json, and keep hooks safe and non destructive by default.
   - MCP change: update .mcp.json and any server code, validate inputs and return actionable errors.
4. Update documentation:
   - Always update plugins/<plugin-name>/README.md when behavior changes.
   - Update CHANGELOG.md if the change is user visible.
5. Local verification:
   - Load plugin locally from its folder:
     claude --plugin-dir ./plugins/<plugin-name>
   - Invoke the relevant skill:
     /<plugin-name>:<skill-name> [args]
6. Definition of done:
   - Clear docs for how to use the change
   - No secrets added
   - Naming and frontmatter follow AGENTS.md
   - Minimal surface area change

## Common pitfalls to avoid

- Chained references (SKILL.md -> advanced.md -> details.md). Keep references one hop from SKILL.md.
- Over long SKILL.md files. Use progressive disclosure with reference.md and examples.md.
- Multiple tool choices without a default. Provide one recommended approach and one escape hatch if needed.
- Time sensitive instructions. Write stable guidance instead.

## When uncertain

If the request is ambiguous, ask which plugin folder under plugins/ is the target before making changes.
