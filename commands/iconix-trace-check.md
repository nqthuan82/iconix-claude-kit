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
4. Before running, detect execution context:
   - **Meta-project context** (`iconix.config.yaml` is present in the current directory): run normally — `ARTIFACT_ROOT` inside the script defaults to `.` (correct). No env var needed.
   - **Service-repo context** (no `iconix.config.yaml` in CWD, but the user is working in an external container repo): the script needs `ICONIX_CONFIG_PATH` pointing to the meta-project so it can find artifact folders. Check the environment for `ICONIX_CONFIG_PATH`. If unset, tell the user: *"Set `ICONIX_CONFIG_PATH=/path/to/meta-project` before running — the traceability artifacts live in the meta-project, not in this service repo."*
   Run: `ICONIX_CONFIG_PATH=<value> .ci/validate-traceability.sh <base-ref> HEAD` (or unset when in meta-project context).
5. Stream output to the user. On failure, summarise the violation count and remind them which file to fix first.
6. Exit codes:
   - 0 → "Traceability gate: PASS — N files checked"
   - 1 → list violations, suggest fixes
   - 2 → setup error (e.g., base ref not fetched); tell the user to `git fetch origin`

Do not modify any ICONIX artifacts or source files. This is a read-only check.
