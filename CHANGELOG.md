# Changelog

## Unreleased

- Align Claude marketplace metadata with current Build with AI docs:
  - Updated plugin categories to match product taxonomy used in docs and marketplaces.
  - Pointed marketplace plugin homepages to feature-specific Build with AI guide URLs.
  - Refined marketplace description to clearly cover all supported auth flows.
- Align Claude plugin manifests with current Build with AI docs:
  - Pointed each plugin's `homepage` to the matching Build with AI guide URL.
- Refresh README install and discovery content:
  - Removed stale `Dryrun` plugin references from plugin lists and repo structure.
  - Updated install commands to explicit plugin + marketplace format (`plugin@scalekit-auth-stack`).
  - Corrected plugin wizard command from `/plugin` to `/plugins`.
  - Replaced legacy docs links with current Build with AI and auth guide URLs.
- Harden skill/reference quality across plugins:
  - Removed an accidental injected external snippet from the Modular SSO skill.
  - Fixed broken relative references in Agent Auth and Modular SCIM skills.
  - Aligned provider catalog entries with connector references currently documented in the repo.
  - Updated outdated Python and Go SDK install commands in skill docs.
- Bump Claude plugin manifest patch versions:
  - `mcp-auth`: `1.3.1` -> `1.3.2`
  - `agent-auth`: `1.8.1` -> `1.8.2`
  - `modular-sso`: `1.2.0` -> `1.2.1`
  - `modular-scim`: `1.2.0` -> `1.2.1`
  - `full-stack-auth`: `1.4.0` -> `1.4.1`

- Improve Scalekit dryrun Skill documentation and discovery:
  - Clarified prerequisites and limitations, including default use of the local project with Scalekit development credentials.
  - Added auth setup checklist and links to canonical Scalekit dryrun and environment setup documentation.
  - Introduced a `skills/dryrun/SKILL.md` entry point to align with the repository constitution’s Skill layout.
  - Added documentation-driven contract and quickstart documents for the dryrun Skill.

