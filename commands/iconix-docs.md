---
description: "Generate user-facing documentation from ICONIX artifacts. Usage: /iconix-docs user|dev|api|release|ops [UC-ID|all]"
argument-hint: "<type> [scope]"
---

Invoke the iconix-docs agent with arguments: $ARGUMENTS

Supported types:
- `user` — end-user guide (docs/user-guide/)
- `dev` — developer onboarding (docs/dev-guide/)
- `api` — API reference (docs/api/)
- `release` — release notes (docs/releases/)
- `ops` — operations / SRE runbook (docs/ops/)

Scope is optional: a specific UC-ID (e.g., `UC-017`) or `all`.

The agent must:
- Transform, not copy, source artifacts
- Cite source artifacts in a footer comment for traceability
- Keep internal IDs out of end-user docs
- Update docs/index.md with new page links
