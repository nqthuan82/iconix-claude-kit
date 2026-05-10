---
description: "Migrate an existing iconix-kit installation to the current version. Auto-applies safe additive changes (folders, config sections with conservative defaults, reference templates, CI files); produces a detect-and-report for project artifacts. Read-only on UCs / source / tests / bug reports."
argument-hint: "[--dry-run] [--from <version>] [--source <kit-path>] [--layers <A,B,C,D,E>]"
---

Invoke the iconix-upgrade agent with: $ARGUMENTS

The agent should:

1. Resolve the target kit version (from `--source <kit-path>` if provided, otherwise from the kit source path used during the original install). Read the kit's `CHANGELOG.md` for the latest version and `templates/iconix.config.yaml` for the current config shape.

2. Detect the project's current installed version:
   - Read `iconix.config.yaml` `kit_version: "X.Y.Z"` field if present
   - Otherwise, use heuristic detection (presence of `phase9-cycles/` → v0.9.8+; `metrics/` → v0.9.7+; `concurrent-touch-template.md` → v0.9.6+; `.ci/validate-traceability.sh` → v0.9.5+; `bug-report-template.md` → v0.9.4+; etc.)
   - If `--from <version>` is in `$ARGUMENTS`, use that explicitly

3. Compute the diff and apply (or dry-run):
   - **Layer A — folders:** `mkdir -p` for any missing structural folder (e.g., `metrics/`, `phase9-cycles/`)
   - **Layer B — config sections:** add missing sections to `iconix.config.yaml` with **conservative defaults** (every new boolean toggle defaults to `false`, even if the kit's seeded template has `true`); set/update `kit_version`
   - **Layer C — reference templates:** refresh `docs/iconix/templates/` files; warn before overwriting any user-edited copy (consider `.backup` suffix)
   - **Layer D — project artifacts:** **DETECT ONLY** — never modify UCs, RBs, SDs, source files, tests, or bug reports; produce findings for the report
   - **Layer E — CI / git integration:** apply based on `git.provider` (github / azure-devops / generic); don't overwrite existing CI workflow files (warn on drift instead)

4. Produce `upgrades/upgrade-<from>-to-<to>-<today>.md` from `templates/upgrade-report-template.md`. Sections: Auto-applied / Detected for review / Suggested config flips / Recommended manual actions / Rollback notes.

5. Print summary to terminal: from→to, counts per layer, top 3 manual actions, path to full report.

If `$ARGUMENTS` includes `--dry-run`, do all the analysis but apply nothing — only the report is written. Useful for previewing.

If `$ARGUMENTS` includes `--layers <list>` (comma-separated subset of `A,B,C,D,E`), restrict the diff to only those layers. Default: all layers. Useful combinations:
- `--dry-run --layers D` — detection-only preview (CI scheduled scans)
- `--layers A,B` — structural setup only (folders + config); skip templates, artifacts, CI
- `--layers A,B,C,D` — everything except CI (when CI is handled separately)

If the detected version is older than v0.9.0, refuse and tell the user to run a fresh `iconix-init` instead. v0.9.x is the supported upgrade range.

If no `iconix.config.yaml` is found at the project root, refuse with a clear message — see the agent's Step 1a for resolution rules. The upgrade agent operates on installed projects only; kit examples (`iconix.config.example.yaml`) are not valid targets.

Do not modify any project artifacts. The agent's safety guarantee is: running `/iconix-upgrade` cannot corrupt your authored UCs, source code, tests, or bug reports.
