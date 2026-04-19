---
description: "Reverse-engineer ICONIX artifacts from an existing codebase. Usage: /iconix-migrate [path-or-module]"
argument-hint: "<path or module, or 'all' for whole repo>"
---

Invoke the iconix-migration agent with scope: $ARGUMENTS

The agent will run the 7-phase migration workflow:
1. Code survey (entry points, layering, stack)
2. Class model extraction (draft class-model.puml)
3. Sequence diagram extraction (one per entry point)
4. Robustness diagram synthesis (validate against ICONIX rules)
5. Use case draft (two-column format with [VERIFY] markers)
6. Test coverage mapping
7. Handoff report with what was inferred vs observed

All reverse-engineered artifacts are prefixed `DRAFT` until human review.

Warn the user upfront: reverse-engineered artifacts are drafts, not
equivalents of greenfield ICONIX artifacts. Business intent, NFRs, and
hidden alternate courses require human input.
