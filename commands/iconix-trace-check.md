---
description: "Run the ICONIX traceability validator locally — same checks as the CI merge-gate."
argument-hint: "[<base-ref>]"
---

Invoke the iconix-git agent with: $ARGUMENTS

The agent should:

1. Read `iconix.config.yaml` `git.default_branch` (defaults to `main` if missing).
2. Resolve the base ref:
   - If `$ARGUMENTS` is non-empty, use it as the base ref.
   - Otherwise, use `origin/<default_branch>`.
3. Verify `.ci/validate-traceability.sh` exists. If not, tell the user to re-run `iconix-init` (it copies the script from `templates/git-integration/generic/`).
4. Run: `.ci/validate-traceability.sh <base-ref> HEAD`
5. Stream output to the user. On failure, summarise the violation count and remind them which file to fix first.
6. Exit codes:
   - 0 → "Traceability gate: PASS — N files checked"
   - 1 → list violations, suggest fixes
   - 2 → setup error (e.g., base ref not fetched); tell the user to `git fetch origin`

Do not modify any ICONIX artifacts or source files. This is a read-only check.
