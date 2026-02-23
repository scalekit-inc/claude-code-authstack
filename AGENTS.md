# AGENTS.md

> This repository builds Claude Code plugins for marketplace distribution.
> Read this before writing any code. These rules are non-negotiable.

---

## What Lives Here

Every artifact in this repo is a **Claude Code plugin** — installable via
`claude /plugin install <source>` and shareable across teams.

A plugin bundles any combination of: skills, sub-agents, hooks, and MCP server configs.

---

## Repository Layout

```
.
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json           # Manifest — REQUIRED
│       ├── skills/
│       │   └── <skill-name>/
│       │       ├── SKILL.md          # Skill entrypoint — REQUIRED
│       │       ├── reference.md      # Deep docs — loaded on demand only
│       │       ├── examples.md       # Input/output pairs — loaded on demand only
│       │       └── scripts/
│       │           └── *.py / *.sh   # Executed by Claude, never loaded into context
│       ├── agents/
│       │   └── <agent-name>.md       # Custom sub-agent definitions
│       ├── hooks/
│       │   └── hooks.json            # Lifecycle event handlers
│       ├── .mcp.json                 # MCP server configurations
│       ├── settings.json             # Default plugin settings
│       └── README.md                 # Required
└── AGENTS.md                         # This file
```

---

## Plugin Manifest (`plugin.json`)

Required at `.claude-plugin/plugin.json`. The directory lives at the plugin root,
not inside `.claude-plugin/`.

```json
{
  "name": "my-plugin",
  "description": "One-line description shown in the plugin manager",
  "version": "1.0.0",
  "author": { "name": "Author Name" },
  "homepage": "https://github.com/org/repo",
  "repository": "https://github.com/org/repo",
  "license": "MIT"
}
```

Rules:
- `name` becomes the skill namespace: `/my-plugin:skill-name`
- Lowercase letters, numbers, hyphens only
- Never use "anthropic" or "claude" as part of the name
- Follow semantic versioning: `major.minor.patch`

---

## Skill Rules

Skills are the primary unit of functionality.
Each skill gets its own directory. `SKILL.md` is the required entrypoint.
All other files are optional and loaded by Claude only when relevant.

### Frontmatter Reference

```yaml
***
name: verb-ing-noun              # gerund form, max 64 chars, lowercase + hyphens only
description: >                   # REQUIRED — third person, what + when
  Generates X from Y. Use when the user asks about Z or mentions A.
disable-model-invocation: false  # true = user-only /slash invocation
user-invocable: true             # false = Claude-only, hidden from / menu
context: fork                    # omit unless skill needs isolated subagent
agent: Explore                   # only with context: fork — Explore | Plan | general-purpose
allowed-tools: Read, Grep        # restrict tools available while skill is active
model: claude-sonnet-4-5         # override model — use sparingly
argument-hint: "[filename]"      # shown in / autocomplete
***
```

### Naming Convention

Use **gerund form** (verb + -ing). The `name` becomes the `/slash-command`.

| Good | Acceptable | Bad |
|---|---|---|
| `reviewing-prs` | `pr-review` | `helper` |
| `generating-migrations` | `migration-generator` | `utils` |
| `analyzing-logs` | `log-analysis` | `tools` |
| `writing-commit-messages` | `commit-helper` | `files` |

### Description Rules

- Always write in **third person** — it's injected into the system prompt
- Include keywords users would naturally say
- State both **what it does** and **when to use it**
- Max 1024 characters, no XML tags

```yaml
# BAD
description: Helps with code

# GOOD
description: >
  Reviews staged git diffs and generates conventional commit messages.
  Use when the user asks for a commit message, wants to summarize staged
  changes, or needs to follow conventional commit format.
```

### Context Budget

`SKILL.md` loads into the shared context window every time the skill activates.

- Keep body **under 500 lines**
- Only add context Claude does not already have
- Split into reference files before approaching the limit
- Keep all reference links **one level deep** — no chained references

```
# GOOD — one level deep
SKILL.md → reference.md
SKILL.md → examples.md

# BAD — Claude may partially read chained files
SKILL.md → advanced.md → details.md → actual-content.md
```

### Progressive Disclosure Pattern

```
my-skill/
├── SKILL.md          # Navigation layer + quick start (≤500 lines)
├── reference.md      # Full docs — loaded only when Claude needs it
├── examples.md       # Input/output pairs — loaded only when needed
└── scripts/
    └── validate.py   # Executed by Claude, never loaded into context
```

Point to supporting files explicitly from `SKILL.md`:

```markdown
## Deep reference
- Full API docs: see [reference.md](reference.md)
- Usage examples: see [examples.md](examples.md)
```

For any reference file over 100 lines, add a table of contents at the top.

### Degrees of Freedom

| Task type | Instruction style | Example use case |
|---|---|---|
| Fragile, exact sequence | Low — exact command, no variation | DB migration, deploy script |
| Preferred pattern exists | Medium — template with parameters | Report generation |
| Many valid approaches | High — heuristics, trust Claude | Code review, research |

### Invocation Modes

| Frontmatter | User invokes | Claude invokes |
|---|---|---|
| (default) | Yes | Yes |
| `disable-model-invocation: true` | Yes | No |
| `user-invocable: false` | No | Yes |

Use `disable-model-invocation: true` for skills with side effects (deploys, commits, sends).
Use `user-invocable: false` for background knowledge skills.

### Arguments

```markdown
***
name: fixing-issue
argument-hint: "[issue-number]"
disable-model-invocation: true
***

Fix GitHub issue $ARGUMENTS following project coding standards.

1. Read the issue
2. Implement the fix with tests
3. Write a conventional commit
```

Multi-argument shorthand: `$0`, `$1`, `$2` (aliases for `$ARGUMENTS[0]`, etc)
Session ID for logging: `${CLAUDE_SESSION_ID}`

### Dynamic Context Injection

Use `!`command`` to inject live data before Claude sees the prompt:

```markdown
***
name: summarizing-prs
context: fork
agent: Explore
allowed-tools: Bash(gh *)
***

Diff: !`gh pr diff`
Files changed: !`gh pr diff --name-only`
Comments: !`gh pr view --comments`

Summarize this PR. Focus on intent, approach, and risks.
```

### Skill Anti-patterns

- Never use Windows-style paths (`scripts\file.py`) — always forward slashes
- Never offer 3+ tool options without a clear recommended default
- Never hardcode credentials, tokens, or API keys
- Never use time-sensitive language ("before August 2025, use the old API")
- Never nest reference chains deeper than one level from `SKILL.md`
- Never explain concepts Claude already knows (what a JSON file is, how imports work)

---

## Sub-agent / Agent Rules

Define agents in `agents/<agent-name>.md`:

```markdown
***
name: security-reviewer
description: >
  Reviews code for security vulnerabilities. Use for pre-merge audits or when
  the user asks about injection risks, auth logic, or exposed secrets.
model: claude-opus-4-5
allowed-tools: Read, Grep, Glob
disable-model-invocation: true
***

You are an expert security reviewer.

For each review:
1. Check for injection vulnerabilities (SQL, command, XSS, path traversal)
2. Verify authentication and authorization patterns
3. Look for hardcoded credentials or secrets in code and configs
4. Review error messages for information leakage

Report each finding as: [CRITICAL|HIGH|MEDIUM|LOW] — description — file:line
```

Reference a custom agent from a skill:

```yaml
***
name: auditing-security
context: fork
agent: security-reviewer
allowed-tools: Read, Grep, Glob
***

Audit $ARGUMENTS for security vulnerabilities.
Output a prioritized findings report with file and line references.
```

---

## Hooks

Hooks live in `plugins/<name>/hooks/hooks.json`.
Hook commands receive the full tool call as JSON on stdin.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix"
        }]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "jq -r '.tool_input.command' | ./hooks/validate-command.sh"
        }]
      }
    ]
  }
}
```

| Event | When | Common uses |
|---|---|---|
| `SessionStart` | Session opens | Load context, initialize state |
| `PreToolUse` | Before any tool runs | Validate inputs, block unsafe commands |
| `PostToolUse` | After tool completes | Lint, format, log |
| `Stop` | Agent exits | Cleanup, write summary |

---

## MCP Server Rules

Configure external MCP servers in `plugins/<name>/.mcp.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["./mcp-servers/my-server/dist/index.js"],
      "env": {
        "API_TOKEN": "${MY_API_TOKEN}"
      }
    }
  }
}
```

### TypeScript Server Pattern

```typescript
import { z } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';

// Define schemas first
const InputSchema = z.object({
  ticketId: z.string().describe("Ticket ID to resolve"),
  resolution: z.string().describe("Resolution message to post before closing"),
});

// Inject dependencies via constructor — no module-level globals
class TicketService {
  constructor(private api: ApiClient, private cache: Cache) {}

  async resolveTicket(input: z.infer<typeof InputSchema>) {
    try {
      // Outcome-focused: do the whole job in one tool call
      await this.api.ensureExists(input.ticketId);
      await this.api.assign(input.ticketId);
      await this.api.postResolution(input.ticketId, input.resolution);
      await this.api.close(input.ticketId);
      return { status: 'resolved', ticketId: input.ticketId };
    } catch (err) {
      // Actionable error — never a raw stack trace
      throw new Error(`Failed to resolve ${input.ticketId}: ${(err as Error).message}`);
    }
  }
}

// Outcome-focused tool name and description
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: 'resolve_ticket',
    description: 'Resolves a support ticket end-to-end: ensures existence, assigns agent, posts resolution, and closes.',
    inputSchema: zodToJsonSchema(InputSchema),
  }]
}));
```

### Python Server Pattern (FastMCP)

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("server-name")

class ResolveInput(BaseModel):
    ticket_id: str = Field(description="Ticket ID to resolve")
    resolution: str = Field(description="Resolution message to post before closing")

@mcp.tool()
async def resolve_ticket(input: ResolveInput) -> dict:
    """
    Resolves a support ticket end-to-end.
    Use when completing a full ticket resolution flow.
    """
    try:
        await api.ensure_exists(input.ticket_id)
        await api.assign(input.ticket_id)
        await api.post_resolution(input.ticket_id, input.resolution)
        await api.close(input.ticket_id)
        return {"status": "resolved", "ticket_id": input.ticket_id}
    except TicketNotFoundError:
        await api.create(input.ticket_id)
        return await resolve_ticket(input)  # retry once after creation
    except Exception as e:
        return {
            "error": str(e),
            "action": f"Check that {input.ticket_id} is accessible and retry"
        }
```

### MCP Design Rules

- **Outcome-focused names**: `resolve_ticket` not `post_to_tickets_endpoint`
- **Solve, don't punt**: handle error conditions inside the tool, not in the agent
- **Inject services via constructor**: never module-level globals
- **Self-documenting constants**: no magic numbers

```typescript
const REQUEST_TIMEOUT_MS = 30_000; // typical API max + slow network buffer
const MAX_RETRIES = 3;             // resolves most intermittent failures
```

---

## Security (Non-negotiable)

- Never hardcode credentials — use `${ENV_VAR}` in configs, `process.env.X` in code
- Validate all tool inputs with Zod (TS) or Pydantic (Python) at every boundary
- Use JSON-RPC 2.0 structured errors — never raw exception messages
- No `eval()` or dynamic `exec()` — reject any generated code execution
- Sanitize all file paths — prevent path traversal
- Validate before processing, not after

---

## Testing & Iteration

### Evaluation-Driven Development

Write evaluations **before** writing `SKILL.md`. This keeps skills focused on real gaps.

```json
{
  "skills": ["reviewing-prs"],
  "query": "Review this PR for security issues",
  "files": ["src/auth/login.ts"],
  "expected_behavior": [
    "Identifies JWT validation logic and checks correctness",
    "Flags missing rate limiting on the login endpoint",
    "Reports findings with file and line number references"
  ]
}
```

Order of operations:
1. Run Claude on the task without any skill — document specific failures
2. Write 3 evaluation scenarios targeting those exact gaps
3. Establish baseline performance
4. Write minimum `SKILL.md` content to pass the evaluations
5. Test → observe → refine → repeat

### Two-Claude Iteration Method

- **Claude A** (with you): designs and refines skill instructions
- **Claude B** (fresh session, skill loaded): performs real tasks
- Watch where Claude B fails or makes wrong decisions
- Bring specific observations to Claude A: "Claude B skipped input validation on the second step"

### Testing Commands

```bash
# Load plugin locally
claude --plugin-dir ./plugins/my-plugin

# Invoke a skill
/my-plugin:reviewing-prs 456

# Check context usage
/context

# List available skills
What skills are available?
```

| Model | What to check |
|---|---|
| Claude Haiku | Does the skill give enough guidance? |
| Claude Sonnet | Is it clear and efficient? |
| Claude Opus | Does it avoid over-explaining? |

---

## Documentation Requirements

Every plugin `README.md` must include:

1. **Purpose** — what problem this solves (2–3 sentences)
2. **Installation** — `claude /plugin install <source>`
3. **Skills reference** — every `/plugin:skill-name [args]`
4. **Configuration** — required env vars + `.mcp.json` example
5. **Usage examples** — at least one end-to-end walkthrough
6. **Troubleshooting** — the 3 most common failure modes
7. **Security** — what credentials are needed and how to store them

---

## Pre-publish Checklist

```
Manifest
- [ ] plugin.json has name, description, version, homepage, license
- [ ] name is lowercase, hyphens only, no reserved words

Skills
- [ ] All descriptions are in third person
- [ ] All skill names are in gerund form
- [ ] No skill named helper, utils, tools, data, or files
- [ ] Every SKILL.md is under 500 lines
- [ ] All reference links are one level deep
- [ ] Forward slashes in all file paths

Security
- [ ] Zero hardcoded credentials anywhere in the repo
- [ ] All tool inputs validated with Zod or Pydantic
- [ ] MCP server returns actionable errors on auth failure

Testing
- [ ] All skills tested with at least Claude Sonnet
- [ ] Plugin loaded with --plugin-dir and confirmed working
- [ ] Hook side effects tested manually

Documentation
- [ ] README covers all 7 required sections
```

---

## Naming Conventions

| Artifact | Convention | Example |
|---|---|---|
| Plugin name | `kebab-case` | `code-quality` |
| Skill name | gerund `verb-ing-noun` | `reviewing-prs` |
| MCP tool | `snake_case`, outcome-focused | `resolve_ticket` |
| Agent name | `kebab-case` role | `security-reviewer` |
| Script files | `verb_noun.py` | `analyze_form.py` |
| Hook scripts | `verb-noun.sh` | `validate-command.sh` |
