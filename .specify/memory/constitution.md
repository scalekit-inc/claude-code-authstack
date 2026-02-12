<!--
Sync Impact Report
- Version change: 1.1.0 → 1.2.0
- Modified principles:
  - Claude Code Plugin Conventions → Claude Code Plugin Conventions (expanded SKILL.md authoring best practices)
- Added sections:
  - None (existing SKILL.md section materially expanded)
- Removed sections: none
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (no change required for this amendment; already delegates to constitution)
  - ✅ .specify/templates/spec-template.md (no change required for this amendment; already delegates to constitution)
  - ✅ .specify/templates/tasks-template.md (no change required for this amendment; already delegates to constitution)
  - ⚠ .specify/templates/commands/*.md (directory missing; command templates to be added under Claude Code plugin layout)
- Follow-up TODOs:
  - None (all placeholders resolved; external docs and SKILL.md practices captured in conventions)
-->

# Claude Code Auth Plugin Constitution

## Core Principles

### I. Repository & Plugin Layout (NON-NEGOTIABLE)

The repository MUST follow Claude Code plugin layout defaults:
- Plugin manifest located at `.claude-plugin/plugin.json` and treated as the single source of plugin metadata.
- Commands defined as markdown files under `commands/`, one file per command, with clear frontmatter and examples.
- Skills defined under `skills/`, with each skill owning a `SKILL.md` at its root and optional `skills/**/references/` for long-form or supporting documentation.
- Agents defined under `agents/`, with one markdown file per agent including frontmatter and the system prompt body.
- MCP server configurations defined in `.mcp.json` at the plugin root; `.lsp.json` present only when language-server configuration is explicitly shipped.
- Repository structure, file naming, and plugin configuration MUST be kept in sync with this layout; deviations MUST be documented and justified in the constitution’s Governance section.

**Rationale**: A stable, predictable layout is critical for Claude Code, MCP servers, and humans to understand and extend the plugin safely. Enforcing a single, explicit layout enables tooling, documentation, and tests to remain deterministic and automatable.

### II. Single-Purpose Capabilities & Explicit Contracts (NON-NEGOTIABLE)

Every command, skill, and agent MUST:
- Have a single, clearly defined purpose that can be stated in one concise sentence.
- Declare explicit inputs and outputs (including side effects) in frontmatter or parameter sections, avoiding implied or hidden behavior.
- Include 1–2 concrete usage examples that demonstrate typical usage and expected outputs.
- Avoid hidden side effects, especially network calls, writes, or external process invocation not stated in the description and examples.
- Avoid overlapping responsibilities across commands/skills/agents; when overlap is unavoidable, document the boundaries and how users should choose between them.

**Rationale**: Claude Code plugins are orchestrated by LLMs and humans that rely on clear contracts. Single-purpose, explicitly documented capabilities minimize ambiguity, improve safety, and simplify composition into higher-level workflows.

### III. Security, Secrets, and Least Privilege (NON-NEGOTIABLE)

Security rules for this repository are:
- Secrets MUST NEVER be committed to the repository (including `.env` files, API keys, certificates, or tokens).
- MCP servers defined in `.mcp.json` MUST use least-privilege credentials and scopes; each server’s configuration MUST document what it can access and why.
- All required environment variables (for auth, MCP backends, external APIs, etc.) MUST be documented in a dedicated configuration section (e.g., in `README` or `SKILL.md`/agent docs), including whether they are optional or required.
- Network, filesystem, and tooling integrations MUST be treated as untrusted: validate inputs and handle failures conservatively, preferring explicit error reporting over silent degradation.
- Error handling MUST fail safely: on unexpected states or external failures, prefer explicit errors with actionable messages over partial or ambiguous results.

**Rationale**: Auth-focused plugins and MCP integrations handle sensitive configuration and access. Failing safely, documenting environment needs, and enforcing least privilege significantly reduces the blast radius of misconfiguration or compromise.

### IV. Quality, Testing, and Deterministic Tooling

Quality rules for this repository are:
- Lint and test commands MUST be defined and invocable in a CI-friendly way (e.g., `npm test`, `npm run lint`, or equivalent).
- Deterministic formatting MUST be enforced (e.g., Prettier, eslint with `--fix`, or language-appropriate formatter) and integrated into CI where possible.
- New commands/skills/agents MUST be covered by at least basic tests (unit, integration, or contract) where reasonably applicable; explicitly document any exceptions.
- Prefer small, composable skills and helpers over one giant skill or agent; when a capability grows beyond a single, coherent purpose, it MUST be factored into smaller parts.
- Any CI pipeline MUST treat failing tests, lint, or formatting checks as blocking for merge.

**Rationale**: Small, composable, well-tested units are easier to reason about, safer for automation, and more resilient to future changes. Deterministic tooling removes style debates and makes CI a reliable gate rather than a source of surprises.

### V. Maintainability, Naming, and Documentation-First Behavior

Maintainability rules for this repository are:
- Naming MUST be stable and consistent: file and command names use `kebab-case`, and directories follow the Claude Code layout defined in Principle I.
- The plugin MUST maintain a versioned changelog and explicit compatibility notes for both Claude Code and any MCP servers it integrates with.
- Documentation is first-class: any new capability (command/skill/agent) MUST ship with updated docs (usage, inputs, outputs, examples) in its markdown file and, where applicable, linked from higher-level docs.
- Backward-incompatible behavior changes MUST be recorded, with migration notes where needed, and tied to semantic version bumps.
- Internal implementation details may change, but the documented contracts for commands/skills/agents and MCP servers MUST remain stable across compatible versions.

**Rationale**: Stable naming, explicit versioning, and documentation-first workflows allow users and tooling to depend on this plugin without fear of silent breakage. Clear compatibility notes make upgrades predictable rather than risky.

## Claude Code Plugin Conventions

This section defines concrete conventions for authoring skills, agents, MCP server definitions, error handling, and repository structure.

### SKILL.md Authoring Rules

Each `SKILL.md` MUST:
- Begin with YAML frontmatter specifying at minimum: `name`, `description`, `inputs` (with types and required/optional flags), `outputs`, and any `dependencies` (e.g., MCP servers, external tools).
- Ensure the `name` field:
  - Uses only lowercase letters, numbers, and hyphens.
  - Is at most 64 characters.
  - Does not use reserved words such as `anthropic` or `claude`.
- Ensure the `description` field:
  - Is non-empty, at most 1024 characters, and free of XML tags.
  - Describes both what the skill does and when to use it.
  - Is written in third person (e.g., “Processes Excel files...”), not “I” or “you”.
- Prefer concise, high-signal content in the body:
  - Assume Claude already knows generic concepts and avoid long explanations.
  - Keep `SKILL.md` under roughly 500 lines and move large reference material into separate files.
- Clearly state whether the skill is safe to call repeatedly, may mutate state, or interacts with external systems.
- Include 1–2 concrete usage examples that show:
  - Example invocation context (e.g., which command or agent calls it, and with what arguments).
  - Representative input and the exact shape or structure of the expected output.
- Use progressive disclosure:
  - Reference long-form documentation or schemas from `skills/[skill-name]/references/` (or equivalent) instead of embedding large payloads directly.
  - Keep references one level deep from `SKILL.md` to avoid deeply nested chains of documents.
- Use consistent, descriptive naming and terminology:
  - Prefer gerund-style, activity-based names (e.g., `processing-pdfs`, `analyzing-spreadsheets`).
  - Avoid vague names like `helper` or `utils` and overly generic terms like `data` or `files`.
- Avoid time-sensitive instructions in the main flow; when historical context is needed, isolate it into clearly marked “legacy” or “old patterns” subsections.
- Where workflows are complex or fragile, include explicit checklists or step-by-step sequences that Claude can follow and mark progress against.

### Agent Prompt Style and Authoring Rules

Each agent markdown file under `agents/` MUST:
- Include frontmatter with: `name`, `description`, optional `model` selection, and any MCP or plugin-specific configuration it relies on.
- Contain a clear system prompt body that:
  - States the agent’s single purpose and boundaries.
  - References only the commands/skills it is expected to use, by stable, documented names.
  - Describes how the agent should handle errors (e.g., when to retry, when to surface errors to users).
- Avoid embedding secrets, API keys, or environment-specific values in the prompt.
- Include 1–2 example dialogues or invocations illustrating how the agent is expected to operate within Claude Code.

### MCP Server Definitions

The `.mcp.json` file at the repository root MUST:
- Define each MCP server with a unique, stable identifier and a concise description of its responsibility.
- Use least-privilege credentials, scopes, and resource access; any elevated access MUST be explicitly justified in comments or documentation.
- Document for each server:
  - Required environment variables (names, purpose, and whether they are required or optional).
  - The kinds of resources it can read or modify.
  - Expected latency or reliability considerations that may affect user experience.
- Avoid embedding secrets directly; instead, reference environment variables and secure configuration mechanisms.

### Error Handling Conventions

Across commands, skills, agents, and MCP servers:
- Errors MUST be explicit and structured where possible (e.g., standardized error shapes or clearly delimited messages).
- Validation errors (bad inputs, missing env vars) MUST be clearly distinguishable from system or external errors.
- When failing due to untrusted network or tooling behavior, components MUST:
  - Log or surface sufficient diagnostic information (without leaking secrets).
  - Avoid partial success that leaves users in an ambiguous state.
- Retry behavior MUST be documented and bounded; infinite or uncontrolled retries are prohibited.

### Repository Structure

The repository structure MUST, at minimum, include:
- `.claude-plugin/plugin.json` for plugin metadata.
- `commands/` for command markdown definitions.
- `skills/` for skill directories and `SKILL.md` files.
- `agents/` for agent markdown definitions.
- `.mcp.json` for MCP server configuration, present only when MCP servers are defined.
- `.lsp.json` ONLY when shipping language-server configuration as part of the plugin.
- A `README` that explains how to install, configure (including env vars), and test the plugin.

Any deviations from this structure MUST be documented in the Governance section and, where relevant, in `README`.

### Claude Code & MCP Reference Documentation

The following official documentation is considered authoritative for plugin, skills, hooks, sub-agents, discovery, troubleshooting, and MCP behavior:

- [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference#plugins-reference)
- [Create Claude Code plugins](https://code.claude.com/docs/en/plugins#create-plugins)
- [Skills](https://code.claude.com/docs/en/skills)
- [Hooks guide](https://code.claude.com/docs/en/hooks-guide)
- [Sub-agents](https://code.claude.com/docs/en/sub-agents)
- [Discover plugins](https://code.claude.com/docs/en/discover-plugins)
- [Troubleshooting](https://code.claude.com/docs/en/troubleshooting)
- [Model Context Protocol (MCP)](https://code.claude.com/docs/en/mcp)
- [Skill vs Subagent](https://code.claude.com/docs/en/features-overview#skill-vs-subagent)

When this constitution is ambiguous, these documents MAY be used to clarify expected Claude Code and MCP behavior, but MUST NOT be used to weaken the non-negotiable principles defined above.

## Development Workflow & Quality Gates

Development of this plugin MUST follow these workflow and quality gates:

- **Constitution Check**: For new features or changes, implementation plans MUST confirm:
  - Repo layout compliance with Principle I.
  - Capability design compliance with Principle II (single-purpose, explicit contracts, usage examples).
  - Security compliance with Principle III (no committed secrets, least-privilege MCP configs, documented env vars, safe failure modes).
  - Quality and testing compliance with Principle IV (lint/test/format commands defined and wired into CI).
  - Maintainability and documentation compliance with Principle V (naming, changelog, compatibility notes, and docs updated).
- **Review Process**:
  - Every PR MUST be reviewed for constitution compliance before merge.
  - Any intentional deviation MUST be explicitly documented in the PR description and, when long-lived, codified as a governance amendment.
- **CI & Automation**:
  - CI MUST run lint, tests, and format checks as non-optional gates for main branches.
  - Automated checks SHOULD validate `.claude-plugin/plugin.json`, `.mcp.json`, and directory layout for structural correctness where feasible.

## Governance

This constitution defines binding rules for the Claude Code Auth Plugin and supersedes ad-hoc practices when conflicts arise.

**Amendment Procedure**

- Any change to principles, conventions, or governance MUST be proposed via PR that:
  - Clearly describes the motivation and impact.
  - Updates this constitution file, including the Sync Impact Report and version metadata.
  - Updates affected templates and documentation (plan/spec/tasks/commands, README, and other guidance) or explicitly marks pending updates in the Sync Impact Report.
- Amendments are approved when:
  - At least one maintainer with repository write access reviews and approves the change.
  - All CI checks pass, including any constitution-specific validation if present.

**Versioning Policy**

- `CONSTITUTION_VERSION` follows semantic versioning:
  - MAJOR: Backward-incompatible governance changes or removals/redefinitions of non-negotiable principles.
  - MINOR: New principles or sections added, or materially expanded guidance that affects how work is executed.
  - PATCH: Clarifications, wording fixes, or non-semantic refinements.
- `RATIFICATION_DATE` is the original adoption date of this constitution.
- `LAST_AMENDED_DATE` is updated whenever the constitution is changed.

**Compliance Reviews**

- Implementation plans and specifications MUST explicitly call out a “Constitution Check” section that:
  - Summarizes how the proposed work satisfies each relevant principle.
  - Lists any requested exceptions or deviations and how they will be mitigated.
- Periodic reviews (at least quarterly for active development) SHOULD:
  - Verify that repository layout, documentation, and MCP configurations remain aligned with this constitution.
  - Identify and schedule work to close any gaps between practice and constitutional rules.

**Version**: 1.2.0 | **Ratified**: 2026-02-12 | **Last Amended**: 2026-02-12
