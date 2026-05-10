# Kit-Version Upgrade Report — <from>-to-<to> — <date>

> Produced by the iconix-upgrade agent. Records what was auto-applied
> and what needs human review.
>
> Saved as `upgrades/upgrade-<from>-to-<to>-<date>.md`. Preserve under
> your retention policy — alongside the metrics snapshots, this is
> audit evidence of methodology evolution.

## Summary

- **From version:** v<X.Y.Z> (detected via <kit_version field | heuristic markers>)
- **To version:** v<A.B.C>
- **Mode:** dry-run | applied
- **Result:** OK | partial (some auto-applies blocked) | failed

## 1. Auto-applied changes

### A. Folder structure
> Layer A: purely additive; safe to auto-apply.

- [x] Created `metrics/` (introduced v0.9.7)
- [x] Created `phase9-cycles/` (introduced v0.9.8)
- [ ] (none needed) `use-case-packages/` already present

### B. Config schema
> Layer B: new sections added with **conservative defaults** so existing
> project behaviour does not change. See "Suggested config flips" below.

- [x] Added `git:` section (provider: generic, pr_cli: none) — v0.9.5
- [x] Added `concurrent_check:` section (enabled: **false**) — v0.9.6
- [x] Added `metrics:` section (enabled: **false**) — v0.9.7
- [x] Added `phase9:` section (enabled: **false**) — v0.9.8
- [x] Set `kit_version: "<A.B.C>"`

### C. Reference templates in `docs/iconix/templates/`
> Layer C: reference docs only; not project artifacts. Safe to refresh.

- [x] Refreshed `bug-report-template.md` (v0.9.4)
- [x] Added `concurrent-touch-template.md` (v0.9.6)
- [x] Added `metrics-snapshot-template.md` (v0.9.7)
- [x] Added `metrics-schema.json` (v0.9.7)
- [x] Added `metrics-glossary.md` (v0.9.7)
- [x] Added `phase9-cycle-template.md` (v0.9.8)
- [x] Added `git-integration/` subtree (branch + commit conventions, generic validator)

### E. CI / git integration files
> Layer E: applied based on `git.provider` setting.

- [ ] **`git.provider` is `generic`** — only the generic validator was copied to `.ci/`. Set `git.provider` to `github` or `azure-devops` and re-run `iconix-init` to install the matching CI workflow + PR templates.
- (or:) [x] Provider `<github|azure-devops>` detected; copied workflow + PR templates.

## 2. Detected for review (Layer D — project artifacts)

> The agent does **not** modify existing UCs, RBs, SDs, source files, or
> bug reports. This section lists what differs from the current template
> format so the team can decide what to retrofit.

### Use cases (`use-cases/UC-*.md`)
- **NN UCs scanned**
- **NN UCs missing `## Traceability` block** (introduced v0.X.X)
  - List: UC-XXX, UC-YYY, ...
- **NN UCs missing M1 checklist references** (e.g., domain-model citation, package-overview citation)
  - List: ...

### Source files (`src/`)
- **NN files missing `Traceability:` comment** (CI gate would fail on these)
  - List of paths
- **NN files using older traceability format** (e.g., `// REQ-XXX` instead of `// Traceability: UC-XXX | RB-XXX | SD-XXX`)
  - List of paths

### Bug reports (`bug-reports/BUG-*.md`)
- **NN Type 2 bug reports without `## Closure` section** (introduced v0.9.8)
  - List: BUG-..., BUG-...
  - Recommended action: invoke Reviewer in Type 2 closure mode for each, OR mark as "pre-v0.9.8 — closure not retroactively required" in a note

### Milestone reports (`milestone-reports/M*-*.md`)
- **NN reports without M2 concurrent-touch summary** (introduced v0.9.6)
- **NN reports using old phase nomenclature**

## 3. Suggested config flips

> The auto-applied config sections use conservative defaults (`enabled: false`)
> so the upgrade itself doesn't change runtime behaviour. After reviewing this
> report, consider flipping these on:

- [ ] `concurrent_check.enabled: true` — surfaces M2 cross-UC conflicts. Recommended once you have ≥2 active feature branches.
- [ ] `metrics.enabled: true` — produces `/iconix-metrics` snapshots. Recommended for any project beyond proof-of-concept.
- [ ] `phase9.enabled: true` — enables the explicit Phase 9 loop semantics. Recommended for any team with >1 Implementation PR per week.
- [ ] `git.provider: <github|azure-devops>` — required to wire up CI gates and `/iconix-pr`. Set this only if you actually use one of these providers.

## 4. Recommended manual actions

> Things the agent flagged that need human follow-up.

1. <e.g., "Address the NN UCs missing `## Traceability` block — invoke `/iconix-next` to refresh M1 readiness; the Product Owner agent will surface them as gate blockers">
2. <e.g., "Run `/iconix-trace-check` against `main` to confirm source files are now passing the v0.9.5 trace gate before turning on the CI workflow">
3. <e.g., "Decide whether to retroactively close pre-v0.9.8 Type 2 bugs">

## 5. Rollback notes

If the auto-applied changes need to be undone, the agent's changes are limited to:
- Folder creation (rm if empty)
- Config-section addition (delete the added sections from `iconix.config.yaml`; the original sections were not modified)
- Template-file refresh under `docs/iconix/templates/` (only reference docs were touched; project artifacts were not)
- `kit_version` field setting

The agent **never** modified files under `requirements/`, `use-cases/`, `robustness/`, `sequence/`, `class-model/`, `test-cases/`, `bug-reports/`, `src/`, or `tests/`.

## Traceability

- Generated by: `agents/iconix-upgrade.md`
- Detected via: `kit_version` field | heuristic markers (list which features were detected)
- Kit source consulted: `<path/URL/SHA of kit source used to determine the target version>`
- Companion: `iconix.config.yaml` `kit_version` was set/updated
