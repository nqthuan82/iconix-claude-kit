---
description: "Open a phase-appropriate pull request for the current branch (GitHub or Azure DevOps; generic providers print the suggested URL)."
argument-hint: "[draft|ready] [--reviewers <user1,user2>]"
---

Invoke the iconix-git agent with: $ARGUMENTS

The agent should:

1. Read `iconix.config.yaml` `git:` section. If missing or `git.provider` is not set, refuse and tell the user to add it (and offer to do so via `iconix-init` re-run or manual edit).
2. Detect the current branch and validate its name against the convention in `templates/git-integration/branch-conventions.md` (or its installed copy at `docs/iconix/templates/branch-conventions.md`). Reject branches that don't carry an artifact ID (e.g., `place-bet` without `UC-XXX`).
3. Detect the current phase by inspecting the diff against `git.default_branch`:
   - `requirements/` + `use-cases/` + initial `domain-model/` → **M1**
   - `robustness/` + refined `domain-model/` + `container-mapping/` + `adrs/` → **M2**
   - `sequence/` + `class-model/` + `test-cases/` + `test-plan/` → **M3**
   - `src/` + `tests/` → **Implementation**
   - Mixed → refuse and ask user to split commits.
4. Open a draft PR using the matching template (`m1.md` / `m2.md` / `m3.md` / `implementation.md`) via the configured `git.pr_cli`:
   - `gh` (GitHub) → `gh pr create --draft --title <title> --body-file <template>`
   - `az` (Azure DevOps) → `az repos pr create --draft --title <title> --description-from-file <template>`
   - `none` / generic → print the suggested branch push and PR URL; do not create.
5. Append the work-item ref (if `git.work_item_prefix` is non-empty) to the PR description.
6. If `$ARGUMENTS` includes `ready`, mark the PR ready-for-review after creation.
7. If `$ARGUMENTS` includes `--reviewers <list>`, set requested reviewers via the CLI.
8. Print the PR URL and a one-line summary of what was opened.

Do not modify ICONIX artifacts. Do not force-push. Do not bypass branch protection.

If the milestone gate hasn't been validated, recommend the user run `/iconix-status` first; do not block the PR (the gate runs in CI), but warn in the PR body.
