# Changelog

All notable changes to the ICONIX Claude Kit.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.9.9] — 2026-05-10

Closes the kit-version-evolution loop that v0.9.5–v0.9.8 implicitly
opened: every minor version added new templates, folders, or config
sections, but existing projects had no way to pick those up without
re-running `iconix-init --force` (which works for templates and
config but doesn't surface what's *different* about authored
artifacts). v0.9.9 adds `/iconix-upgrade` — a kit-version migration
agent that auto-applies safe additive changes and produces a
detect-and-report for project artifacts.

Three-layer migration model:

  Layer A (folders)     — auto-apply via mkdir -p
  Layer B (config)      — auto-apply with conservative defaults
                          (every new boolean toggle = false on upgrade,
                          even if the kit's seeded template has true)
  Layer C (templates)   — auto-apply, refresh reference docs
  Layer D (artifacts)   — DETECT ONLY. Never touch UCs / source /
                          tests / bug reports. Report what differs.
  Layer E (CI / git)    — auto-apply based on git.provider

The "conservative defaults during upgrade" rule is deliberate: the
upgrade itself must not change runtime behaviour. The user opts in
by editing iconix.config.yaml after reading the report.

Distinct from iconix-migration (which retrofits ICONIX onto legacy
CODE). Upgrade migrates the kit VERSION. Same word, different
problems; intentionally separate agents.

This is a **tooling-only** change per CLAUDE.md (no ICONIX rules
introduced; no methodology shifts). Theory audit consciously skipped
and noted here for clarity.

### Added
- `agents/iconix-upgrade.md` — new agent. Detects current installed
  version (from `kit_version` field, or heuristic feature-presence),
  computes the diff, applies layers A/B/C/E, produces a
  detect-and-report for layer D, updates `kit_version`. Read-only on
  project artifacts. Idempotent. Refuses if detected version < 0.9.0
  (recommends fresh install instead).
- `commands/iconix-upgrade.md` — new slash command. Supports
  `--dry-run` for preview-only, `--from <version>` to override
  detection, `--source <path>` to specify a kit-source path
  different from the original install.
- `templates/upgrade-report-template.md` — report format. Sections:
  Summary, Auto-applied (per layer), Detected for review (per
  artifact category), Suggested config flips, Recommended manual
  actions, Rollback notes, Traceability footer.
- `templates/iconix.config.yaml` — new `kit_version: "0.9.9"` field
  at the top of the config. Set automatically by `iconix-init` on
  fresh install; bumped by `/iconix-upgrade` after a successful
  migration. Used by `iconix-upgrade` for version detection (with
  heuristic fallback for pre-v0.9.9 projects).
- New folder seed: `upgrades/` — where upgrade reports are written.

### Changed
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers now create `upgrades/` folder, copy
  `upgrade-report-template.md` to `docs/iconix/templates/`, and
  list the new agent + command in the Next-steps output.
- `agents/iconix-orchestrator.md` — routing heuristic for "we're on
  an older kit version" / "how do I upgrade" → Upgrade agent
  (`/iconix-upgrade` or `/iconix-upgrade --dry-run`).
- `README.md` — `iconix-upgrade.md` in agents and commands listings;
  `upgrade-report-template.md` in templates listing; new full
  **Upgrading an existing installation** section explaining the
  three-layer model, what's auto-applied, what's never touched,
  what gets detected-and-reported, version detection logic, and
  the distinction from `iconix-migration`.
- `.github/workflows/validate.yml` — smoke test asserts
  `kit_version` field present in seeded `iconix.config.yaml`,
  `upgrade-report-template.md` installed, `upgrades/` folder exists.

### Methodology audit (per CLAUDE.md `# Auditing kit changes against ICONIX Theory`)
- **Tooling-only change.** `/iconix-upgrade` is kit-version
  maintenance — it does not introduce ICONIX rules, does not change
  any phase semantics, does not modify the matrix's coverage.
  Theory audit consciously skipped per CLAUDE.md's guidance: *"Tooling-
  only changes (installer scripts, CI workflow, version bumps, typo
  fixes, methodology-neutral bug fixes, formatting) do not require
  a theory audit."*
- The agent's "detect-and-report" of artifacts that don't match
  current template format is methodology-aware (it knows what
  current templates require) but doesn't change the rules — it
  surfaces drift between authored artifacts and the kit's evolved
  templates, leaving remediation to the user.

## [0.9.8] — 2026-05-10

Closes the largest remaining behavioural gap from the v0.9.4 kit
assessment: **Phase 9 — the implementation loop**. Until now, the
post-CDR phase was a one-line placeholder in the orchestrator
("Developer + Tester iterate") with no specification of who owns
which iteration, when the Reviewer kicks in, or what triggers
"done." v0.9.8 expands Phase 9 into 4 explicit sub-states
(9.1 kickoff → 9.2 pre-merge drift → 9.3 fix loop → 9.4 merge)
with handoff conditions, an iteration cap, and escalation paths.

Bundles backlog item #2 — **Reviewer Type 2 closure**. After a Type 2
bug's REQ change flow completes, the Reviewer now re-confirms the
*original* bug report against the *new* SD, appending a `## Closure`
section to the bug report. Without this, a Type 2 fix could merge
without anyone re-checking it actually solved the reported problem.
Both changes ship together because Phase 9 is the natural home for
the bug-fix paths.

Methodology audit: operationalizes existing Ch10 rules (#10, #9, #8,
#5, #4, #3, #1) — no new rules introduced. Verified via PDF read of
the Ch10 Top 10 list. Type 2 closure is a small refinement of Ch10
#9 ("review the process") — closing a missing step in the kit's
prior bug flow rather than inventing a new methodology.

### Added
- `templates/phase9-cycle-template.md` — optional per-UC cycle log.
  Records each Developer ↔ Tester ↔ Reviewer iteration's verdict and
  the final exit state. For teams wanting audit-grade evidence of
  the loop history (lives in `phase9-cycles/UC-XXX-cycle.md`).
- `agents/iconix-reviewer.md` — three new mode sections:
  - **Pre-merge drift mode (Phase 9.2)** — the canonical Phase 9
    review. Aggregates code↔SD, code↔class-model, robustness, NFR,
    framework/business-logic checks into one verdict (APPROVE /
    APPROVE WITH NOTES / REQUEST CHANGES / BLOCK MERGE). Drives 9.4
    or 9.3 routing.
  - **Bug-fix verification mode (post-Type 1)** — focused re-check
    that the *specific drift the original triage flagged* is closed.
    Not a full pre-merge review; just verification.
  - **Type 2 closure mode (post-REQ-change-flow)** — re-confirms the
    *original bug report* against the *new* SD. Appends a `## Closure`
    section to the bug report on success; recommends `REOPEN` if the
    new design or implementation doesn't address the reported issue.
- `agents/iconix-developer.md` — new **Implementation mode (Phase 9)**
  section with two sub-modes: initial implementation (9.1) and drift
  fix iteration (9.3). Cites Ch10 #1 explicitly for alternate-course
  coverage.
- `agents/iconix-tester.md` — new **Test implementation mode (Phase 9)**
  section with two sub-modes: initial test implementation (9.1) and
  test re-run after drift fix (9.3). Tester runs in parallel with
  Developer on the same `feature/UC-XXX-<slug>` branch.
- `templates/iconix.config.yaml` — new `phase9:` section with
  `enabled` (default true), `max_iterations_per_uc` (default 5 — the
  9.2↔9.3 cap), `reviewer_required_for_merge` (default true).

### Changed
- `agents/iconix-orchestrator.md`:
  - Phase 9 in the phase-order list expanded from one-line placeholder
    to a pointer to the new `# Phase 9 routing` section.
  - New section **Phase 9 routing — the implementation loop** with
    explicit 9.1 / 9.2 / 9.3 / 9.4 sub-state semantics, exit conditions,
    and the iteration-cap escalation logic (architectural drift →
    Architect; requirements-shaped → PO; either path effectively bumps
    a stuck Type 1 to Type 2).
  - Type 1 bug flow now ends with **Reviewer bug-fix verification mode**
    (the missing closure step the prior version skipped).
  - Type 2 bug flow now ends with **Reviewer Type 2 closure mode**.
- `iconix-state-machine.puml`:
  - `Implementation` state expanded to a composite state with
    sub-states 9.1 / 9.2 / 9.3 / 9.4 and an `Escalate` change-state.
    Loop transition 9.3 → 9.2; cap-hit transition 9.3 → escalate;
    merge transition 9.4 → done.
  - **Removed standalone `BugFix` and `BugVerify` states** — they
    redundantly modelled the same loop as Phase 9.3 → 9.2. The
    Type 1 bug flow now re-enters the Implementation Loop at 9.3
    on a `bugfix/T1-*` branch (book Ch10 #9 treats fix-and-verify
    as one process; the kit shouldn't draw two loops). Reviewer
    mode selection (Pre-merge drift mode vs Bug-fix verification
    mode) is an internal detail of the agent at 9.2 — not a
    separate state-machine flow. `Done` now has an outbound
    `--> BugTriage` transition for "bug reported on shipped feature."
- `agents/iconix-orchestrator.md` — `# Bug flow` Type 1 narrative
  rewritten to acknowledge it's the same loop as Phase 9.3 → 9.2,
  with the only differences being the branch name and the Reviewer's
  mode at 9.2. No new behaviour; just stops drawing the loop twice.
- `README.md`:
  - `phase9-cycle-template.md` added to the templates listing.
  - Pipeline diagram now shows `Implementation loop` with the four
    sub-states inline.
  - New full **Phase 9 — the implementation loop** section explaining
    the 4-sub-state flow, configuration, three new Reviewer modes,
    optional cycle log, and the methodology mapping to Ch10.
- `docs/iconix/iconix-process-reference.md`:
  - Ch10 row citations refreshed (#10, #9, #8, #5, #4, #3, #1) to
    point at the new Phase 9 sub-states and Reviewer modes. Status
    unchanged on every row (already ✅).
  - "Last reviewed" bumped to v0.9.8 with rationale citing PDF read
    of book p. 259.
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell):
  - Both create `phase9-cycles/` folder during folder-structure
    seeding.
  - Both copy `phase9-cycle-template.md` to `docs/iconix/templates/`.
- `.github/workflows/validate.yml` — smoke test asserts
  `phase9-cycle-template.md`, `phase9-cycles/` folder, and the
  `phase9:` section in seeded `iconix.config.yaml`.

### Methodology audit (per CLAUDE.md `# Auditing kit changes against ICONIX Theory`)
- **Cited rules:** Ch10 #10 (drive code from design), #9 (if coding
  reveals design wrong, change it AND review the process), #8 (regular
  code inspections), #5 (if code gets out of control, revisit the
  design), #4 (keep design and code in sync), #3 (focus on unit
  testing while implementing), #1 (implement alternate courses too).
- **Book verification:** PDF read of Ch10 Top 10 list (book p. 259).
  Confirmed Phase 9's sub-state design maps cleanly to Ch10's
  guidelines without inventing new ones.
- **Status shifts:** none. Every Ch10 ✅ row gets a richer kit-location
  citation pointing at the new Phase 9 sub-states / Reviewer modes.
- **Type 2 closure framing:** small refinement of Ch10 #9's "AND
  review the process" — closing a missing step in the prior bug flow.
  Not classified as a new methodology rule.
- **No contradictions found.**

## [0.9.7] — 2026-05-10

Closes the #1 gap from the v0.9.6 backlog: **metrics & audit evidence**.
The kit produces well-structured artifacts at every phase, but until
now there was no aggregation showing teams whether the process was
actually paying off — and no single artifact a regulated-environment
auditor could point at and say "this is your ICONIX evidence." v0.9.7
adds an `iconix-metrics` agent that scans the project's current state
+ git history at run-time and produces audit-friendly snapshots
(markdown for humans + JSON for dashboards).

Snapshot-based, not event-based. The agent reads everything that
already exists (artifacts, milestone reports, reviews, change-impact
reports, bug reports, git log) and computes ~15 metrics across 5
categories. No external state, no new infrastructure — fits the kit's
"all artifacts are files" principle.

Provider-neutral on visualization: the JSON conforms to a stable
schema (v1.0); teams build their own dashboards in Power BI, Grafana,
Azure Workbooks, GitHub Insights, or anything else that reads JSON.
The kit ships no vendor templates — same provider-neutrality stance
as v0.9.5 git integration.

Honestly marked as a kit extension. The book has only incidental
mentions of metrics (per-review data on Ch11 line 12405; the Code-
Inspection-vs-Code-Review sidebar acknowledging that formal
inspections gather metrics). v0.9.7 extends these to project-wide
aggregation, justified by Ch11 #6 and SME / regulated-environment
audit needs (ISO 27001 + 9001).

### Added
- `agents/iconix-metrics.md` — new read-only agent. Produces
  `metrics/snapshot-<date>.md` (audit-friendly markdown) and
  `metrics/snapshot-<date>.json` (validates against schema v1.0). On
  `/iconix-metrics trend`, also produces `metrics/trend-<date>.md`
  with deltas vs the prior snapshot. Read-only on everything except
  `metrics/`. Eight-step computation algorithm specified in the agent
  prompt: read config → throughput → cycle time (from
  `[<UC>] <phase>: ...` commits) → quality → process compliance →
  trends → blockers → render. Retention enforced: prunes old
  snapshots beyond `metrics.retention` (default 12).
- `commands/iconix-metrics.md` — new slash command.
  `/iconix-metrics` produces a snapshot; `/iconix-metrics trend`
  also produces the trend report.
- `templates/metrics-snapshot-template.md` — markdown format. Six
  numbered sections: throughput, cycle time, quality, process
  compliance, trend (when applicable), blockers and stale state.
  Includes ISO-audit framing.
- `templates/metrics-schema.json` — formal JSON schema (Draft
  2020-12, schema version 1.0). Stable contract for downstream
  dashboards. Required and optional fields explicitly documented.
- `docs/iconix/metrics-glossary.md` — authoritative definitions for
  every metric. Lists what's intentionally **not** a metric (no
  per-developer attribution, no LOC, no story-point velocity, no
  cost estimates — Ch13 #3 stays 🚫).

### Changed
- `templates/iconix.config.yaml` — new `metrics:` section with
  `enabled` (default true), `output_dir` (default `metrics`),
  `ci_snapshot` (default false), `retention` (default 12),
  `git_history_window` (default 12 months).
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell):
  - Both create `metrics/` folder during folder-structure seeding
  - Both copy `metrics-snapshot-template.md` and
    `metrics-schema.json` to `docs/iconix/templates/`
  - Both copy `metrics-glossary.md` to `docs/iconix/`
  - Bash "Next steps" lists `/iconix-metrics`
- `agents/iconix-orchestrator.md` — routing heuristic for "how is
  the project doing?" / "ISO audit evidence" → Metrics agent.
- `README.md` — `iconix-metrics.md` in agents listing;
  `iconix-metrics.md` command listing; `metrics-snapshot-template.md`
  and `metrics-schema.json` in templates listing; new full **Metrics
  & audit evidence** section explaining the 5 metric categories,
  output layout, configuration, and ISO-audit framing.
- `docs/iconix/iconix-process-reference.md`:
  - Drift-detection sub-table gains a "Project-wide metrics + audit
    evidence (kit extension)" row marked ✅, explicitly framed as
    not-in-book.
  - Ch11 #6 kit-location updated to cite the project-wide extension.
  - "Last reviewed" bumped to v0.9.7 with rationale (PDF grep
    confirms only incidental coverage of "metric/dashboard/measure/kpi").
- `.github/workflows/validate.yml` — smoke test asserts
  `metrics-snapshot-template.md`, `metrics-schema.json`,
  `metrics-glossary.md`, `metrics/` folder, and `metrics:` section
  in the seeded `iconix.config.yaml`.

### Methodology audit (per CLAUDE.md `# Auditing kit changes against ICONIX Theory`)
- **Cited rules:** Ch11 #6 (Gather data during the review) — kit
  location updated to add project-wide extension. Ch11
  Code-Inspection-vs-Code-Review sidebar — explicitly acknowledges
  formal code inspections gather metrics.
- **Book verification:** PDF grep for `metric|dashboard|measure|
  gate-failure|drift rate|kpi|throughput` returned only incidental
  hits (class-count metrics on line 648; the per-review note on
  line 12405). Confirmed: project-wide metrics is a kit extension.
- **Status shifts:** new ✅ row added to the Drift-detection
  sub-table for "Project-wide metrics + audit evidence", explicitly
  marked as kit extension. Ch11 #6 status unchanged (already ✅;
  citation extended).
- **No contradictions found.** The book's bias toward small co-
  located teams doesn't conflict with project-wide metrics — it just
  doesn't address them. Adding metrics doesn't violate any canonical
  principle.

## [0.9.6] — 2026-05-09

Closes the second-largest gap from the v0.9.4 kit assessment: **multi-
developer concurrency upfront detection**. Until now, two devs working
on UCs that quietly converged on the same domain class (or controller,
or DB table) only discovered the conflict when the Reviewer ran post-
implementation drift detection. v0.9.6 shifts that detection left to
**M2 / PDR**, when the robustness diagrams already make class
references explicit. Advisory by default — teams enable CI blocking
after they trust the detector.

This is honestly a **kit extension** over the canonical ICONIX text.
The book assumes a small co-located team sharing one whiteboard model;
it doesn't address cross-UC conflict detection (verified via grep of
the PDF: "concurrent" appears only in unrelated contexts). v0.9.6 fills
that gap, justified by Ch11 #1 (Model Update at every gate) extended
to the multi-dev reality. The matrix marks this clearly as a kit
extension rather than misclaiming book coverage.

### Added
- `commands/iconix-concurrent.md` — new slash command. Standalone
  invocation of the concurrent-touch detection (the same routine also
  runs automatically at M2 gate). Accepts an optional UC-ID to filter
  the report to conflicts involving that UC.
- `templates/concurrent-touch-template.md` — report format. Sections:
  detection scope, in-flight UCs, class-touch matrix, per-conflict
  detail with severity (HIGH / MEDIUM / LOW) and recommended
  resolutions, configuration echo, traceability footer. Installer
  copies it to `docs/iconix/templates/`; CI smoke test asserts it
  exists.
- `templates/iconix.config.yaml` — new `concurrent_check:` section:
  `enabled` (default true), `block_on_high_conflict` (default false —
  advisory), `detect_boundaries` (default true), `detect_db_containers`
  (default true).

### Changed
- `agents/iconix-traceability.md` — new section **Concurrent touch
  detection**. Six-step routine: read config → identify in-flight UCs
  via `git branch -r --list 'origin/feature/UC-*'` (or DRAFT artifacts
  as fallback) → build class-touch maps from RBs and class model →
  detect conflicts pairwise → recommend resolutions → render report.
  Integrated into the M2 gate report.
- `agents/iconix-architect.md` — new section **Resolving concurrent
  touches**. Architect is the canonical resolver for HIGH conflicts,
  proposing options (extract shared service, rename controllers, share
  migration, etc.) but never unilaterally rewriting UCs/RBs. PDR
  readiness checklist gains a concurrent-touch review item.
- `agents/iconix-orchestrator.md` — phase 5 (M2 gate) now explicitly
  includes concurrent-touch detection; HIGH conflicts route back to
  Architect before M2 promotion. New routing heuristic for
  `/iconix-concurrent`.
- `agents/iconix-git.md` — new section **In-flight UC detection** as a
  helper for Traceability's concurrent-touch check. Returns the list
  of `(UC-ID, phase, branch-age)` tuples from open feature branches.
  Falls back to empty list when no git context is available.
- `iconix-state-machine.puml` — M2 gate now branches to a new
  `Concurrent-touch resolution (Architect)` state on HIGH conflicts;
  loops back to the gate after resolution.
- `templates/git-integration/github/PULL_REQUEST_TEMPLATE/m2.md` and
  `templates/git-integration/azure-devops/pull_request_templates/m2.md`
  — both M2 PR templates gain a checklist item for concurrent-touch
  review with `[CT-ACCEPT-XXX]` markers for explicitly-accepted
  conflicts.
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers copy `concurrent-touch-template.md` to
  `docs/iconix/templates/`. Bash "Next steps" output mentions
  `/iconix-concurrent`.
- `README.md` — `iconix-concurrent.md` added to the commands listing;
  `concurrent-touch-template.md` added to the templates listing; new
  full **Multi-developer concurrency** section explaining detection
  scope, the M2 → Traceability → Architect flow, and configuration.
- `docs/iconix/iconix-process-reference.md` — new row in the Drift-
  detection sub-table for "Concurrent class touches across in-flight
  UCs" marked ✅ with explicit "kit extension" framing. "Last reviewed"
  bumped to v0.9.6 with rationale citing the book grep that confirmed
  no canonical coverage.
- `.github/workflows/validate.yml` — smoke test asserts
  `concurrent-touch-template.md` exists and the seeded
  `iconix.config.yaml` contains the `concurrent_check:` section.

### Methodology audit (per CLAUDE.md `# Auditing kit changes against ICONIX Theory`)
- **Cited rules:** Ch11 #1 (Model Update at every gate) — concurrent-
  touch detection extends the model-update concept across UCs at M2.
  Ch6 PDR readiness — gains a new technical check, no shift to
  existing rule statuses.
- **Book verification:** grep of the PDF for "concurrent / parallel
  develop / multi-dev / merge conflict / shared class" returned only
  unrelated hits (transaction throughput in REQ wording, concurrent
  activities in activity diagrams). Confirmed: this is a kit
  extension, not a re-derivation of an existing rule.
- **Status shifts:** new row added to the Drift-detection sub-table.
  Marked ✅ for the new check itself, with explicit "kit extension"
  framing in the kit-location cell so future audits aren't misled
  about book coverage.
- **No contradictions found.**

## [0.9.5] — 2026-05-09

Closes the largest gap identified in the v0.9.4-session kit assessment:
**git integration**. Until now only the Reviewer was git-aware (it read
`git diff`); no agent created branches, opened PRs, or enforced commit
hygiene. The kit's careful artifact discipline could be undone at the
merge stage by inconsistent git history. v0.9.5 adds a provider-agnostic
core (branch + commit conventions + a shell-script merge-gate) plus
first-class adapters for **GitHub** and **Azure DevOps** — chosen because
they cover the vast majority of regulated/enterprise iGaming
environments. GitLab and Bitbucket are deferred to a later version; the
generic adapter (any CI that can run a shell script) keeps them usable
in the meantime.

### Added
- `agents/iconix-git.md` — new agent. Owns branch creation/validation,
  PR opening, commit-message format checking, posting Reviewer findings
  as PR comments. Reads `git.provider` from `iconix.config.yaml`.
  Read-only on ICONIX artifacts; never force-pushes; never bypasses
  branch protection or required CI checks.
- `commands/iconix-pr.md` — opens a phase-appropriate draft PR (M1 / M2
  / M3 / Implementation) using the matching template. Detects phase
  from the diff; refuses on mixed-phase commits. Routes through `gh`
  (GitHub) or `az` (Azure DevOps) when configured; prints the suggested
  URL when `pr_cli: none`.
- `commands/iconix-trace-check.md` — runs the traceability validator
  locally with the same checks the CI merge-gate runs. Pre-push guard.
- `templates/git-integration/` — new top-level templates folder:
  - `branch-conventions.md` — `feature/UC-XXX-<slug>`, `arch/<scope>`,
    `bugfix/T1-<slug>`, `bugfix/T2-UC-XXX-<slug>`, `hotfix/T1-<slug>`,
    `release/<version>`. Trunk vs. GitFlow strategies.
  - `commit-conventions.md` — `[<artifact-id>] <phase>: <summary>`
    format. Phases: M1 / M2 / M3 / Impl / Fix / Doc / Refactor / Chore.
    Mixed-phase commits flagged. Optional work-item ref footer.
  - `generic/validate-traceability.sh` — provider-agnostic merge-gate.
    Checks every changed file under `src/` and `tests/` for a
    `Traceability:` comment; checks every cited ID points to an
    existing artifact. Self-contained POSIX shell; runs identically in
    CI containers and on developer laptops.
  - `generic/README.md` — how to wire the script into any CI provider
    not covered by a first-class adapter.
  - `github/workflows/iconix-validate.yml` — GitHub Actions workflow
    that runs the validator on every PR and pushes comment with fix
    instructions on failure.
  - `github/pull_request_template.md` + `PULL_REQUEST_TEMPLATE/{m1,m2,m3,implementation}.md`
    — default + phase-specific PR templates.
  - `azure-devops/azure-pipelines-iconix-validate.yml` — Azure
    Pipelines equivalent. Uses `SYSTEM_PULLREQUEST_TARGETBRANCH` for
    base-ref detection; posts a PR comment via REST on failure.
  - `azure-devops/pull_request_templates/{default,m1,m2,m3,implementation}.md`
    — Azure DevOps PR templates (loaded from
    `.azuredevops/pull_request_templates/`).
- `templates/iconix.config.yaml` — new `git:` section: `provider`
  (github / azure-devops / generic), `default_branch`,
  `branch_strategy` (trunk / gitflow), `work_item_prefix` (optional;
  `AB#` for Azure Boards, `#` for GitHub Issues, empty to disable),
  `pr_cli` (gh / az / none), `impl_squash`. Default `provider:
  generic`, `pr_cli: none` — the kit doesn't assume a provider until
  configured.

### Changed
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers now read `git.provider` from the just-seeded
  `iconix.config.yaml` and copy the matching subtree:
  - Always: `validate-traceability.sh` to `.ci/`; conventions docs to
    `docs/iconix/templates/git-integration/`.
  - `github`: workflow to `.github/workflows/`, PR templates to
    `.github/` and `.github/PULL_REQUEST_TEMPLATE/`.
  - `azure-devops`: pipeline to repo root, PR templates to
    `.azuredevops/pull_request_templates/`.
  - `generic`: just the script + a README explaining manual wiring.
  - "Next steps" output now lists the new agents and commands.
- `agents/iconix-orchestrator.md` — routing heuristics gain an entry
  for the Git agent (`/iconix-pr`, `/iconix-trace-check`).
- `agents/iconix-reviewer.md` — new section "Posting reviews on PRs"
  explaining that when git integration is configured, the Git agent
  posts the review report as a structured PR comment. Reviewer doesn't
  post directly — produces the report; Git agent handles delivery.
  When recommendation is BLOCK MERGE / REQUEST CHANGES, the Git agent
  also sets the PR to draft (when supported).
- `agents/iconix-traceability.md` — new section "CI counterpart"
  acknowledging that `.ci/validate-traceability.sh` runs a subset of
  the agent's validation as a fast pre-merge gate. The agent remains
  the canonical auditor for the full chain.
- `README.md` — `iconix-git.md` added to the agents listing;
  `iconix-pr.md`, `iconix-trace-check.md` added to the commands
  listing; `templates/git-integration/` added to the templates
  listing; new full **Git integration** section explaining
  configuration, conventions, what the installer drops in per
  provider, the merge-gate, and the Reviewer-as-PR-bot flow.
- `docs/iconix/iconix-process-reference.md` — Ch11 #5 row gains a
  citation for Reviewer-as-PR-bot (already ✅; kit-location updated
  only). "Last reviewed" bumped to v0.9.5.
- `.github/workflows/validate.yml` — smoke test now asserts
  `branch-conventions.md`, `commit-conventions.md`, and a working
  executable `validate-traceability.sh` are installed.

### Methodology audit (per CLAUDE.md `# Auditing kit changes against ICONIX Theory`)
- Cited rules: **Ch11 #5** (Follow up review with action points) — kit
  location updated; **Ch11 #2** (Just formal enough) — PR templates
  and check runs are "structured but lightweight"; **Ch11 #6** (Gather
  data; build boilerplate checklists) — already ✅, no shift; **Ch1
  milestones** — gates as PR boundaries doesn't change the methodology,
  it just expresses it through git.
- Status shifts: none. Git/PR is a tooling integration over existing
  rules.
- Out-of-scope unchanged: "Human review meeting" remains 🚫 — a PR
  comment thread is async/asynchronous, not the in-person whiteboard
  session the book describes.
- No contradictions found.

## [0.9.4] — 2026-05-08

Two changes that travel together: (1) a procedural rule in `CLAUDE.md`
forcing Claude to audit every methodology-surface kit change against the
process-reference matrix and the book before treating it complete — this
is the upstream check that prevents kit drift from accumulating one
well-intentioned edit at a time. (2) `/iconix-bug` exposes the Reviewer's
existing bug-triage workflow as a first-class slash command. The
workflow itself was already in `iconix-reviewer.md` `# Bug triage` and
already credited ✅ in the matrix (Ch10 #9, Ch10 #5, Ch11 #1,
Drift-detection sub-table); previously users had to invoke it
conversationally or wait for the Orchestrator to detect the input. Now
they can route directly. This v0.9.4 work was itself the first
methodology-surface change to follow the new audit rule from (1) — book
Ch11 cited inline in the new command for traceability.

### Added
- `commands/iconix-bug.md` — new slash command. Direct entry point to the
  Reviewer's `# Bug triage` workflow. Accepts a bug description, source
  path, or UC-ID; produces the standard `## Bug triage` block (Type 1
  implementation defect vs Type 2 design defect) and recommends the next
  step (Developer bug-fix mode for Type 1; `/iconix-impact` → REQ change
  flow for Type 2). Reviewer-only — no fixes made by this command.
- `templates/bug-report-template.md` — optional structured input for
  `/iconix-bug`, mirroring the existing intake-template pattern for the
  Product Owner. Sections: affected artifact, observed behaviour,
  **exception / stack trace** (top application frame is the Reviewer's
  direct anchor against SD methods; exception type often pre-classifies
  Type 1 vs Type 2), expected behaviour, reproduction, optional triage
  hint, Reviewer-filled traceability block. Installer (bash + PowerShell)
  copies it to `docs/iconix/templates/` alongside the intake templates;
  CI smoke test asserts it exists.
- `CLAUDE.md` — new section **Auditing kit changes against ICONIX
  Theory**. Defines what counts as a methodology-surface change (agent
  rules, templates, gates, pipeline order, the matrix itself,
  methodology-bearing commands) and what does not (installer scripts,
  CI, version bumps, typos, methodology-neutral bug fixes). Specifies a
  4-step audit procedure: cite the matrix row → verify against the book
  PDF when the matrix doesn't resolve the question → update the matrix
  in the same change if coverage shifted → surface contradictions
  rather than silently introducing them. Requires Claude to state in
  the response which rules were audited and what was cited.

### Changed
- `README.md` — `/iconix-bug` added to the directory listing and the
  command-routing table; the bug-flow narrative (Step 1 — Always triage
  first) gains a three-row **Input form** table (UC-ID / Source path /
  Free-text) showing example invocations and what the Reviewer does
  first for each; mentions both entry points (`/iconix-bug` direct and
  `/iconix-next` via Orchestrator); points users at the new template
  for larger bugs with stack traces. Templates listing in the directory
  layout adds `bug-report-template.md`.
- `iconix-state-machine.puml` — `BugTriage` state's note reframed from
  single-trigger ("Triggered at any time by the Orchestrator") to
  two-entry-point ("/iconix-bug" direct, "/iconix-next" via Orchestrator).
- `agents/iconix-orchestrator.md` — `# Bug flow` Step 1 now acknowledges
  the `/iconix-bug` direct entry point for users who already know it's
  a bug (the Orchestrator's input-detection is bypassed in that case;
  same triage workflow either way).
- `docs/iconix/iconix-process-reference.md`:
  - Drift-detection sub-table row "Bug type classification (Type 1 vs
    Type 2)" kit-location cell now cites both `iconix-reviewer.md`
    `# Bug triage` and `/iconix-bug <ref>`. Status unchanged (already ✅).
  - **Ch11 #10** ("Prepare for review; participants read material in
    advance") flips from ❌ to ⚠️ — `bug-report-template.md` forces the
    bug reporter to surface affected artifact, observed-vs-expected,
    exception trace, and reproduction *before* the Reviewer is invoked,
    which partially covers "prepare review material in advance"; full
    guideline still includes a human meeting the kit does not convene.
  - Summary Coverage Matrix: Ch11 chapter row updated from `8|0|2|0`
    (80%) to `8|1|1|0` (85%). "Last reviewed" bumped to v0.9.4 with
    inline rationale.
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers now copy `bug-report-template.md` to
  `docs/iconix/templates/` alongside the intake templates.
- `.github/workflows/validate.yml` — smoke test asserts
  `docs/iconix/templates/bug-report-template.md` exists after install,
  mirroring the assertions for the four intake templates.

## [0.9.3] — 2026-05-08

Two themes: (1) corrects a misattribution of book Ch2 rule #3 ("Draw the
domain model before writing use cases") — the matrix marked it ✅ because
the Orchestrator forced PO → Analyst order, but in practice neither agent
drew an initial domain model from REQs; the Analyst drew the only one
*after* UC text was already written. v0.9.3 reassigns initial domain-model
authorship to the Product Owner, as the book intends, and reframes the
Analyst's role as "refine, not create." (2) post-v0.9.0 audit of the
process-reference matrix introduces a 🚫 (Out of scope) marker so
deliberate boundaries (persona research, TDD red-green, storyboards,
human review meetings, code-header generation, UC-point estimation) stop
appearing as ❌ gaps and inflating the apparent missing-coverage count.

### Changed
- `agents/iconix-product-owner.md` — role expanded to own the **initial
  domain model**; new rule 9 mandates drawing it after REQs and before UC
  flows (book Ch2 guideline #3); adds `domain-model/domain-model.puml` to
  the artifact list; adds matching M1 checklist item.
- `agents/iconix-analyst.md` — role reframed: Analyst now **refines** the
  domain model started by the PO rather than creating it; step 7 and the
  artifact-list comment updated accordingly.
- `agents/iconix-orchestrator.md` — phase 1 description now states the
  Product Owner produces "REQs, **initial domain model**, UCs, glossary".
- `iconix-state-machine.puml` — Product Owner state machine now has an
  explicit `DraftDomainModel` substate between `DraftREQs` and `DraftUCs`,
  matching the new rule 9 ordering.
- `examples/write-customer-review/README.md` — project-wide artifacts
  callout corrected: domain model is "Product Owner drafts; Analyst
  refines as entities are discovered" (was: "Analyst owns").
- `README.md` — pipeline diagram adds the **Implementation** phase
  (Developer + Tester iterate after M3); PO bullet mentions "initial
  domain model"; templates listing adds `use-case-diagram-template.puml`
  (already present in `templates/`, was missing from the doc).
- `CLAUDE.md` — pipeline diagram adds **Implementation** as phase 9,
  matching the orchestrator and state machine.
- `docs/iconix/iconix-process-reference.md` — Ch2 rule #3 row rewritten
  to credit the PO and note the v0.9.3 correction.

### Added
- `docs/iconix/iconix-process-reference.md` — new `🚫 Out of scope`
  status marker. Six items reclassified from ❌ to 🚫 because they are
  deliberate kit boundaries, not gaps:
  - Ch1: Persona analysis (requires primary user research)
  - Ch1: TDD red-green-refactor cycle (kit derives TCs from RBs;
    "test-first thinking" is separately ⚠️ in scope per Ch12 #7)
  - Ch3 #6 / Ch4 #3: UI storyboards (external tools — Figma, Balsamiq)
  - Ch4 #2 / Ch6 #4: Human review meetings (kit produces artifacts
    *for* meetings; doesn't convene them)
  - Ch9 #2: Generate code headers (IDE/toolchain concern)
  - Ch13 #3: Estimates from UC scenarios (UC-point estimation needs
    team calibration data)
- `docs/iconix/iconix-process-reference.md` — Summary Coverage Matrix
  now shows a 🚫 column; coverage formula updated to exclude 🚫 from
  the denominator (out-of-scope items don't penalize coverage).
- `CLAUDE.md` — new **ICONIX Theory References** section pointing
  Claude at `docs/iconix/iconix-process-reference.md` (committed) and
  the gitignored `Use Case Driven Object Modeling with UML.pdf` for
  resolving methodology questions, with guidance to always read the
  PDF with the `pages` parameter.
- `CLAUDE.md` — new **Keeping README and state machine in sync**
  section instructing Claude to review `README.md` and
  `iconix-state-machine.puml` whenever a change touches the kit's
  user-facing surface.

### Fixed
- `docs/iconix/iconix-process-reference.md` — Summary Coverage Matrix
  count errors corrected: Ch4 was listed `7|2|1`, actual was `7|1|2`
  (one ⚠️, two ❌); Ch7 was listed `7|1|2`, actual was `7|0|3`. Ch7
  coverage corrects from 75% to 70%; remaining ❌ items (#10 hardware
  cost, #9 legacy default, #6 unproven tech) are genuine gaps, not
  out-of-scope.

## [0.9.2] — 2026-05-07

Closes a gap left in v0.9.0: the migration agent now reverse-engineers all
project-wide ICONIX artifacts, not just the per-feature ones. Without this,
human reviewers had to author the domain model and UC package overviews on
a second pass — even though the migration agent already had the information
needed.

### Changed
- `agents/iconix-migration.md` — two new phases added to both workflows
  (graph-assisted and code-walking fallback):
  - **Phase 4b — Domain model synthesis.** Filters the Phase 2 class model
    down to entity classes (drops Boundary / Controller classes from RBs,
    drops framework-typed fields, drops methods); maps inheritance and
    field references to is-a / has-a relationships; emits
    `domain-model/domain-model-DRAFT.puml` with provenance per class.
  - **Phase 5b — Use case package overview synthesis.** Clusters UC drafts
    by source directory / namespace (or graph community-detection in
    graph-assisted mode); emits one
    `use-case-packages/<package-slug>-DRAFT.puml` per cluster; flags any
    UC that does not fit a cluster as an orphan in the handoff report.
- `agents/iconix-migration.md` — pre-run idempotency check (Step 3) now
  detects human-edited DRAFTs of the two new artifacts; agent description
  in YAML frontmatter mentions them.
- `agents/iconix-migration.md` — *Output structure* section updated.
- `agents/iconix-migration.md` — non-HTTP entry points are now recognised
  as first-class boundaries: `BackgroundService` / `IHostedService`,
  message-bus consumers (`IConsumer<T>`, MassTransit / Azure Service Bus
  handlers), Azure Functions, AWS Lambda handlers. Phase 1 entry-point
  detection (graph-assisted + code-walking) and Phase 4 boundary mapping
  both updated. New mixed-responsibility check in Phase 4: when a
  background-service node also has direct outbound edges to entity / DB
  nodes, the agent flags the class `[VERIFY]` and recommends extracting
  a controller so the boundary stays thin.

### Fixed
- `agents/iconix-migration.md` — Phase 3 (sequence diagram extraction)
  was overpromising in graph-assisted mode. The previous wording told
  the agent to use `shortest_path` and treat the result as a sequence
  diagram, but `shortest_path` returns *one* topological route and is
  blind to branching, loops, async semantics (`await` vs
  `Task.WhenAll`), exception flow, fire-and-forget patterns, and
  polymorphic dispatch — all of which a sequence diagram must capture.
  Phase 3 now mandates a two-step extraction in both modes:
  (a) bound the call graph by enumerating **all simple paths** to leaf
  operations; (b) recover behaviour by reading the source at each
  visited node (the graph already gives `file_path` + `line_range`),
  mapping `if` / `try-catch` / loops / `await` / `Task.WhenAll` to
  PlantUML `alt` / `loop` / `par` groups. Provenance discipline
  extended: every group is marked `INFERRED (control-flow: <kw>)`
  with the source file:line cited. The agent now states the
  topology-vs-behaviour disclaimer to the user at the start of Phase 3.
- `agents/iconix-migration.md` — entry-point detection (Phase 1, both
  modes) and stereotype mapping (Phase 4 graph-assisted) were leaning
  on .NET-flavoured class-name lists. Restructured to be tech-stack
  neutral: detection is now by **responsibility shape** (universal
  signals: inbound dispatch, outbound infrastructure imports,
  conditional logic over domain values), with cross-stack reference
  tables covering C#/.NET, Java, Python, Node.js/TypeScript, Go, and
  Ruby. The agent reads `iconix.config.yaml` `stack.language` to
  weight the most likely patterns first.
- `agents/iconix-migration.md` — added explicit **Outbound Boundary**
  classification for repositories, SDK / API clients, message
  publishers, file/blob writers, and email/SMS senders. Previously
  the Phase 4 mapping recognised only inbound boundaries (controllers
  / hubs / consumers / hosted services); outbound adapters were
  silently miscategorised as Controllers because of their
  `*Service` / `*Repository` names. Outbound boundaries now render
  on the right side of their controller on the SD and carry an
  `<<outbound>>` stereotype on the RB.
- `agents/iconix-migration.md` — added a **disambiguation rule**:
  when a node's name suggests one stereotype but its imports suggest
  another, trust the imports. (A class named `OrderService` that
  imports a Stripe SDK and a DbContext is an outbound boundary's
  worth of work, not a controller.)
- `agents/iconix-migration.md` — broadened the Phase 4
  mixed-responsibility check beyond background-service-with-DB-edges:
  it now triggers on **any** boundary node (inbound or outbound) that
  carries domain conditionals in its body, recommending a Controller
  extraction so the boundary stays thin.

## [0.9.1] — 2026-05-07

### Added
- `examples/write-customer-review/` — end-to-end worked example replaying
  the canonical *Internet Bookstore / Write Customer Review* use case from
  Rosenberg & Stephens (2007), adapted to this kit's templates and the
  C# / ASP.NET Core 9 / EF Core 9 / xUnit + NSubstitute stack. 21 files
  threading one feature through every ICONIX phase:
  - 3 intake artifacts (email, transcript, feature request)
  - 1 requirement (BS-REQ-001)
  - 1 use case (BS-UC-001) with basic + 5 alternate courses
  - 1 domain model (project-wide, continuously updated)
  - 1 UC package overview (Reviews & Ratings package)
  - 1 robustness diagram (BS-RB-001)
  - 1 ADR (BS-ADR-001 — IValidatableObject vs FluentValidation vs service-layer)
  - 1 sequence diagram (BS-SD-001) with full class model
  - 1 test plan + 7 test cases covering all five V-model levels:
    - unit (BS-TC-002 rating, BS-TC-003 review length)
    - system (BS-TC-001 basic course via WebApplicationFactory, BS-TC-004 not-logged-in)
    - integration (BS-TC-007 — Testcontainers SQL Server + Service Bus emulator)
    - acceptance (BS-TC-101 — Reqnroll Gherkin, stakeholder-signed by Doug, Sarah, Linda)
    - regression (BS-TC-021 — supersedes BS-TC-003 after BS-CI-001 lands)
  - 1 change-impact report (BS-CI-001 — adding a title-length rule)
  - 1 project config (`iconix.config.example.yaml`)
- Worked-example `README.md` documents the thread map, file index, and
  traceability chain (`grep -r BS-REQ-001 examples/write-customer-review/`
  recovers the full chain).
- Demonstrates the v0.9.0 UC-package-overview methodology in context, plus
  the test-case template's `Type` field (unit | integration | system |
  acceptance | regression) and `Supersedes TC` field for regression tests.

## [0.9.0] — 2026-05-07

Closes the methodology gaps tracked in `iconix-process-reference.md` as
Ch3 #9 (use cases organised with actors and use case diagrams / packages)
and Ch4 #6 (use cases organised into packages with at least one UC diagram
per package).

### Added
- `templates/use-case-diagram-template.puml` — PlantUML template for the
  per-package UC overview diagram. Actors, package boundary as a labelled
  rectangle, in-package use cases, cross-package use cases shown outside,
  `<<include>>` / `<<extend>>` arrow guidance, and a maintenance reminder
  note
- `use-case-packages/` — new ICONIX folder seeded by both installers; one
  `<package-slug>.puml` file per UC package
- `agents/iconix-product-owner.md` — new section `# Use case packaging rules`
  with five rules covering one-package-per-UC, one-overview-per-package, how
  to draw cross-package invocations, when to update the diagram, and the
  exact-title-match rule
- `agents/iconix-product-owner.md` — three new M1 checklist items: every UC
  belongs to one package and appears on its overview, every overview entry
  has a matching UC file, no dangling cross-package `<<include>>` /
  `<<extend>>` links
- `agents/iconix-traceability.md` — four new validation checks (#10–13):
  orphan UCs (file with no package entry), ghost UCs (overview entry with
  no file), title drift (overview label mismatched against UC heading),
  dangling cross-package links

### Changed
- `iconix-init` and `iconix-init.ps1` — both create `use-case-packages/`
  during folder seeding and copy `use-case-diagram-template.puml` into
  `docs/iconix/templates/`
- `.github/workflows/validate.yml` — smoke test now asserts the new
  template and folder are present after install
- `.gitignore` — adds `/use-case-packages/` so installed projects don't
  ship their UC packages back into the kit
- `agents/iconix-traceability.md` — orphan report scope expanded to cover
  the four new UC-overview check types
- `docs/iconix/iconix-process-reference.md` — Ch3 #9 (UC packages) moved
  ⚠️ → ✅; Ch4 #6 (one UC diagram per package) moved ❌ → ✅; Ch3 coverage
  85% → 90%, Ch4 coverage 70% → 80%; "Closed in v0.9.0" entry added

## [0.8.11] — 2026-05-07

### Added
- `README.md` — `## AI agent patterns` section documenting the four Anthropic
  agent design patterns the kit applies: orchestrator → subagents, prompt
  chaining, parallelization, and evaluator / gate

## [0.8.10] — 2026-05-05

### Changed
- `.github/workflows/validate.yml` — smoke test now asserts all four intake
  templates (`intake-transcript-template.md`, `intake-brd-template.md`,
  `intake-email-template.md`, `intake-feature-request-template.md`) are
  present in `docs/iconix/templates/` after installation

## [0.8.9] — 2026-05-05

### Added
- `templates/intake-transcript-template.md` — structured template for stakeholder
  interviews and meeting notes: metadata, stakeholder profile, current-state narrative,
  pain points, desired future state, scenario walkthrough table (Who/Action/Response),
  what-if-fails probes, NFR seeds, open questions, and analyst summary with candidate
  actors, UC stubs, and REQ stubs
- `templates/intake-brd-template.md` — 13-section Business Requirements Document template:
  executive summary, business objectives, explicit scope (in/out), stakeholders/actors,
  current state, future state, functional requirements table (observable behaviour, no tech
  names), NFR table (5 categories with measurable targets), business rules, assumptions /
  constraints / dependencies, glossary, per-requirement acceptance criteria, and approvals
- `templates/intake-email-template.md` — email/written-request intake template: source
  metadata, verbatim text block, PO restatement layer (stated request, inferred goal
  `[VERIFY]`, inferred actors, scope, NFR seeds, ambiguity questions), candidate artifacts
  section, and Blocked / Ready status
- `templates/intake-feature-request-template.md` — Connextra story + Gherkin acceptance
  criteria template with inline comments mapping Given/When/Then to two-column UC format;
  includes out-of-scope section, NFR notes table (separate from Gherkin), UI/screens,
  INVEST self-check, priority, and linked artifacts
- `agents/iconix-product-owner.md` — `# Intake checklist` section: maps each input type
  to its template, defines six cross-cutting quality checks (named actor, goal vs solution,
  alternate path, quantified constraints, named screens/domain objects, scope boundary),
  enforces `[VERIFY]` for all inferences, and requires multi-UC decomposition before
  drafting any artifacts
- `iconix-init` / `iconix-init.ps1` — both installers updated to copy the four new intake
  templates into `docs/iconix/templates/` during project-scope installation

## [0.8.8] — 2026-05-05

### Changed
- `README.md` — updated to reflect all changes since v0.7.2:
  - Added `iconix-state-machine.puml` to the kit tree listing
  - `/iconix-status` description updated to reflect 6-section output (artifact inventory,
    NFR coverage, test matrix, open CI reports, milestone readiness, next action)
  - Pipeline diagram: Architect now shows "testability seams"; M2 gate notes NFR→ADR
    validation; M3 gate notes test plan existence and completeness check
  - Bug triage section: added note on `reviews/review-checklist.md` accumulation
  - Philosophy footer: corrected "six primary agents" → "ten agents, seven commands"

## [0.8.7] — 2026-05-05

### Added
- `agents/iconix-product-owner.md` — `# When to split a use case` section: five split
  signals (basic course >~6 rows, >~4 alternate courses, alternate courses cover different
  goals, "and" in UC title, unreadable RB), step-by-step split procedure with invoked UC
  reference guidance, and three "do NOT split" counter-examples; rule 3 updated to
  reference the new section

## [0.8.6] — 2026-05-05

### Added
- `agents/iconix-developer.md` — rule 8: show design patterns on the SD as lifelines;
  a pattern hidden in code but absent from SD is flagged as drift (Ch9 #6 ❌→✅)
- `agents/iconix-reviewer.md` — check #2: untyped attributes in class model flagged as
  "attribute untyped" (Ch9 #3 ❌→✅)
- `agents/iconix-tester.md` — ICONIX rules: TCs are authored before code skeletons;
  deferring TC authoring until after implementation defeats design-first intent (Ch12 #7 ❌→⚠️)

### Fixed
- `docs/iconix/iconix-process-reference.md` — Ch4 Eight-steps #8 corrected ⚠️→✅; rule was
  already implemented in v0.6.0 M1 checklist item 8 but matrix was not updated

### Changed
- `docs/iconix/iconix-process-reference.md` — Ch9 60%→80%, Ch12 80%→85%; added "Closed in
  v0.8.6"; last-reviewed bumped to v0.8.6

## [0.8.5] — 2026-05-05

### Added
- `agents/iconix-reviewer.md` — check #6: Framework vs. business logic — flags framework
  concerns mixed into business classes, boilerplate-only methods, and framework trade-offs
  without an ADR (Ch10 #7 ❌→✅, Ch10 #6 ❌→✅); `Framework/business issues` count added
  to review report summary
- `agents/iconix-reviewer.md` — Rules: Reviewer accumulates recurring defect patterns into
  `reviews/review-checklist.md` after each review (Ch11 #6 ❌→✅)
- `agents/iconix-product-owner.md` — rule 8: requirements must describe observable
  behaviour, not implementation technology; REQs naming frameworks/libraries rejected and
  rewritten as constraints (Ch13 #1 ❌→✅)
- `agents/iconix-product-owner.md` — M1 checklist: two new items — domain model abstraction
  coverage (UC nouns with no model counterpart flagged, Ch4 #10 ❌→✅) and domain model
  relationship coverage (isolated entities with real-world relationships flagged, Ch4 #9 ❌→✅)

### Changed
- `docs/iconix/iconix-process-reference.md` — Ch4 50%→70%, Ch10 70%→90%, Ch11 70%→80%,
  Ch13 80%→90%; added "Closed in v0.8.5"; last-reviewed bumped to v0.8.5

## [0.8.4] — 2026-05-05

### Added
- `agents/iconix-analyst.md` — PDR readiness check: two new gate items: data flow
  documentation (Boundary↔Entity paths must have named data in UC text or analysis notes,
  Ch6 #8 ⚠️→✅) and no-detailed-design guard (method signatures/types on RB are a blocker,
  Ch6 #2 ⚠️→✅)
- `agents/iconix-reviewer.md` — check #2 attribute completeness: entity classes with ≥2
  operations and 0 attributes flagged as "attribute-sparse" (Ch9 #7 ⚠️→✅)

### Changed
- `docs/iconix/iconix-process-reference.md` — Ch6 75%→85%, Ch9 55%→60%; added "Closed in
  v0.8.4"; last-reviewed bumped to v0.8.4

## [0.8.3] — 2026-05-05

### Added
- `agents/iconix-developer.md` — rule 6: prefactor on SD before writing code; SD is
  complete when every RB controller has a message and every message has an allocated
  operation (Ch8 #2 ⚠️→✅)
- `agents/iconix-developer.md` — rule 7: don't worry about focus of control; activation
  bars are optional detail; SD purpose is operation allocation (Ch8 #5 ❌→✅)
- `agents/iconix-tester.md` — ICONIX rules expanded: explicit fine-grained unit test rule
  (one controller operation per TC, Ch12 #1 ⚠️→✅) and caller-POV unit test rule (test the
  contract the controller exposes to its caller, Ch12 unit test sub-table ⚠️→✅)
- `templates/req-template.md` — `## Examples` section: optional but encouraged; concrete
  example + counter-example per requirement (Ch13 #2 ❌→✅)

### Changed
- `docs/iconix/iconix-process-reference.md` — Ch8 85%→100%, Ch12 75%→80%, Ch13 70%→80%;
  added "Closed in v0.8.3" section; last-reviewed bumped to v0.8.3

## [0.8.2] — 2026-05-05

### Changed
- `commands/iconix-status.md` — expanded from a 4-line stub to a structured 6-section
  report template: artifact inventory (REQ/UC/RB/SD/CLS/TC/ADR + test plan + open CI
  reports), NFR coverage from `nfr_catalog`, test coverage summary from `test-matrix.md`
  (automated vs manual, UC coverage gaps), open change impact reports with blast-radius
  and pipeline re-run status, milestone readiness (M1/PDR/CDR), and next recommended action

## [0.8.1] — 2026-05-05

### Added
- `agents/iconix-analyst.md` — `# Robustness diagram principles` section with three explicit rules:
  arrow direction is irrelevant (Ch5 #5 ❌→✅); RB is conceptual design only — no method names
  or types (Ch5 #3 ⚠️→✅); controllers are logical functions, not control classes — map to
  messages on SD, not instantiated classes (Ch5 #6 ⚠️→✅)
- `agents/iconix-product-owner.md` — rule 7: noun-verb-noun sentence structure with rewrite
  instruction (Ch3 #3 ⚠️→✅)

### Changed
- `docs/iconix/iconix-process-reference.md` — Ch3 80%→85%, Ch5 75%→100%; added "Closed in
  v0.8.1" section; last-reviewed bumped to v0.8.1

## [0.8.0] — 2026-05-05

### Added
- `agents/iconix-architect.md` — rule 5: time-box architecture work; unresolved decisions
  become `Proposed` ADRs so the pipeline is not blocked (guards against architectural
  paralysis, Ch7 #4)
- `agents/iconix-architect.md` — rule 6: every ADR must cite ≥1 REQ-ID, NFR ID, or UC-ID
  in its Context section; uncited ADRs are flagged (requirement-driven TA validation, Ch7 #5)
- `agents/iconix-architect.md` — `# Testability annotations` section: every container with
  significant business logic must have ≥1 test seam (unit / integration / system) noted in
  the container mapping; no-seam containers flagged as testability risks at M2 gate (Ch7 #3)
- `agents/iconix-architect.md` — PDR readiness checklist expanded with two new items:
  ADR upstream traceability check and container testability seam check

### Changed
- `docs/iconix/iconix-process-reference.md` — Ch7 coverage updated: #3 ⚠️→✅, #4 ❌→✅,
  #5 ❌→✅; summary table Ch7 45%→75%; added "Closed in v0.8.0" section to gap list;
  last-reviewed version bumped to v0.8.0

## [0.7.6] — 2026-05-05

### Changed
- `docs/iconix/iconix-process-reference.md` — coverage matrix updated to v0.7.5:
  - Added `_Last reviewed: v0.7.5_` to summary table
  - Replaced "Priority 2 — Out of kit scope" list with a structured
    "Documented as intentionally out-of-scope in v0.7.2" table (6 items with
    rationale column: UI storyboards, stakeholder reviews, persona analysis,
    effort estimation, code headers, TDD red-green cycle)
  - Added "Added in v0.7.3/v0.7.4/v0.7.5" sections documenting
    `test-plan-template.md`, TC `## Type` field, and state machine diagram

## [0.7.5] — 2026-05-04

### Added
- `iconix-state-machine.puml` — PlantUML state machine diagram of the full ICONIX kit
  workflow: Idle → Requirements (M1 gate) → Preliminary Design (M2 gate) → CDR Phase
  (M3 gate) → Implementation → Done; includes bug triage flow (CDRPhase / Implementation /
  Done → BugTriage → BugFix → BugVerify) and REQ change flow (any active phase →
  REQChange → Requirements); states colour-coded by stereotype: `<<agent>>` blue,
  `<<gate>>` yellow, `<<bug>>` red, `<<change>>` green

## [0.7.4] — 2026-05-04

### Changed
- `templates/test-case-template.md` — added `## Type` field
  (unit | integration | system | acceptance | regression) with inline
  guidance on which traceability fields apply per type: `Robustness
  controller` for unit only; `Sequence diagram` for unit/integration only;
  `Supersedes TC` for regression only; angle-bracket placeholders wrapped
  in backticks for correct VS Code preview rendering
- `agents/iconix-tester.md` — test case template reference now instructs
  agent to set `## Type` and omit non-applicable traceability fields

## [0.7.3] — 2026-05-04

### Added
- `templates/test-plan-template.md` — pre-CDR test plan template with five sections:
  release scope (UC table), TC inventory by type, automation status, coverage status
  (blocker check), and outstanding risks
- `agents/iconix-tester.md` — `# Pre-CDR test plan summary` now references
  `templates/test-plan-template.md` as the authoritative format
- `agents/iconix-tester.md` — `test-plan/test-plan-<date>.md` added to
  `# Artifacts you produce` with downstream consumers noted (Traceability M3 gate, Docs)
- `agents/iconix-docs.md` — `test-plan/test-plan-<date>.md` added to `# Inputs you use`;
  release notes section now includes a test coverage summary from the test plan
- `iconix-init` + `iconix-init.ps1` — both installers now copy `test-plan-template.md`
  to `docs/iconix/templates/`

## [0.7.2] — 2026-05-04

### Added
- `README.md` — `## What the kit intentionally does not cover` section: six
  documented gaps (UI storyboards, stakeholder review meetings, persona analysis,
  effort estimation, code header generation, TDD red-green cycle) each with a
  brief rationale and recommended practice for teams

## [0.7.1] — 2026-05-04

### Added
- `agents/iconix-analyst.md` — `# Invoked use cases on robustness diagrams`: when a UC
  step invokes another UC, drag the invoked UC onto the diagram as a use case node (not a
  plain controller); it connects to the triggering controller following normal connection rules

## [0.7.0] — 2026-05-04

### Added
- `agents/iconix-tester.md` — `# Test types (V-model)` table: maps each test type
  (unit / integration / system / acceptance / regression) to the ICONIX phase that
  triggers it, its primary inputs, and its scope
- `agents/iconix-tester.md` — `# Pre-CDR test plan summary` section: Tester must
  produce `test-plan/test-plan-<date>.md` before the M3 gate, covering release scope,
  TC inventory by type, automation status, coverage status, and outstanding risks
- `agents/iconix-traceability.md` — NFR validation check (#9): every NFR in
  `iconix.config.yaml` `nfr_catalog` must be cited by ≥1 ADR or container-mapping
  annotation; uncovered NFRs are flagged as orphans
- `agents/iconix-traceability.md` — NFR added to the traceability chain diagram
  (`NFR-XXX → ADR-XXX / container-mapping`)
- `agents/iconix-traceability.md` — milestone gate report now includes NFR coverage
  row and test plan existence/completeness check

## [0.6.0] — 2026-05-04

### Added
- `agents/iconix-analyst.md` — `# Domain model rules` section: six explicit constraints
  (real-world objects only, not a data model, domain model = project glossary, only real-world
  relationships, time-box to ~2 hours, domain model will not match final class diagram)
- `agents/iconix-analyst.md` — `# Boundary object naming` rule: every distinct UI screen,
  page, dialog, or API surface must appear as a **named** boundary object; generic labels
  like "web page" are rejected; vague UC text must be rewritten before diagramming

### Changed
- `agents/iconix-product-owner.md` — added rule #6: "shall" statements belong in
  `requirements/REQ-XXX.md`, not in UC text; passive-voice statements found in UC flows
  must be moved to a REQ file and replaced with the active-voice behavior they imply
- `agents/iconix-product-owner.md` — M1 checklist expanded from 5 → 8 items, aligned to the
  book's eight-step Requirements Review: fixed "per course" wording (rule is two paragraphs
  **total**, not per course); added passive-voice/shall check; added abstraction-level check
  (no "the system", "a page", "the data"); added goal-oriented framing check
- `docs/iconix/iconix-process-reference.md` — coverage matrix updated: all five
  "Not fully extracted" placeholder rows filled in (Ch5 #5, Ch6 #1, Ch7 #4/#5, Ch8 #9,
  Ch12 #7); summary table percentages recalculated with consistent formula
  (✅×1 + ⚠️×0.5) ÷ total

## [0.5.3] — 2026-05-04

### Added
- `templates/adr-template.md` — Architecture Decision Record template with Status,
  Context (REQ/NFR/UC refs), Options considered, Decision with rationale, Consequences
  table (positive/negative/risks/follow-ups), and Traceability block

### Changed
- `agents/iconix-architect.md` — replaced inline ADR template block with reference to
  `templates/adr-template.md`; artifact declaration updated to reference the file
- `iconix-init` + `iconix-init.ps1` — both installers now copy `adr-template.md`
  to `docs/iconix/templates/`

## [0.5.2] — 2026-05-04

### Added
- `templates/sequence-template.puml` — PlantUML sequence diagram template with UC step
  text embedded as `group` blocks (basic course + alternate courses shaded `#Pink`)
- `templates/req-template.md` — atomic requirement template with statement, rationale,
  acceptance criteria, priority, and traceability block
- `templates/test-case-template.md` — test case template extracted from Tester agent
  inline format; mirrors UC two-column steps and expected results exactly
- `templates/change-impact-template.md` — CI report template with blast radius tree,
  flat affected artifact table, and recommended dispatch order

### Changed
- `templates/robustness-template.puml` — now embeds full UC scenario text (basic +
  alternate courses) as a numbered comment block at the top of the file
- `agents/iconix-analyst.md` — workflow step 4 now requires UC scenario text to be
  embedded in the RB `.puml` header comment block (references robustness-template.puml)
- `agents/iconix-developer.md` — workflow step 2 now requires each UC step to be wrapped
  in a PlantUML `group` block in the SD `.puml` (references sequence-template.puml)
- `agents/iconix-product-owner.md` — artifact declarations now reference
  `req-template.md` and `use-case-template.md` explicitly
- `agents/iconix-tester.md` — replaced inline test case template block with reference
  to `templates/test-case-template.md`; file template is the authoritative format
- `agents/iconix-traceability.md` — CI report artifact declaration now references
  `templates/change-impact-template.md`
- `iconix-init` + `iconix-init.ps1` — both installers now copy all 7 templates to
  `docs/iconix/templates/` (previously only 3 were copied)

## [0.5.1] — 2026-05-04

### Fixed
- **Product Owner change mode — brand new REQ detection**: when a new REQ has no
  existing UC citations, Traceability's CI report is empty and the change mode previously
  skipped straight to editing with no affected UCs identified. Added Step 0 (check CI
  report content) and Step 1 (manual candidate identification with human confirmation)
  before any UC edits are made. Uncertain candidates are flagged with `[VERIFY]` and
  require explicit user approval before proceeding.

## [0.5.0] — 2026-05-03

### Added
- **Bug flow in Orchestrator**: new `# Bug flow` section routes bug reports through a
  mandatory triage step before dispatching to Developer:
  - Type 1 (implementation bug — code diverges from correct design): Reviewer → Developer
    bug fix mode → Tester bug verification mode; no artifacts change
  - Type 2 (design bug — design is wrong): Reviewer → Traceability impact → full REQ
    change flow
- **Bug triage in Reviewer**: new `# Bug triage` section classifies bugs as Type 1 or
  Type 2 and appends a `## Bug triage` block to the review report with root artifact,
  affected UC, rationale, and recommended next step
- **Bug fix mode in Developer**: new `# Bug fix mode` section — fixes only the code
  identified in the Reviewer's drift-report; explicitly forbids modifying SDs, class
  model, or UCs; re-runs drift detection after fix to confirm the gap is closed
- **Bug verification mode in Tester**: new `# Bug verification mode` section — re-runs
  failing TCs for Type 1 fixes; follows Change mode for Type 2 fixes; includes a
  regression check for UCs sharing classes touched by the fix
- README: documented the bug triage flow with Type 1 / Type 2 decision table and agent
  dispatch diagrams

## [0.4.1] — 2026-05-03

### Fixed
- **Migration idempotency guard**: `iconix-migration` now runs a `# Pre-run idempotency
  check` before any Phase 1 work in both modes, preventing silent overwrites on repeated
  `/iconix-migrate` runs:
  - Detects artifacts already promoted to permanent IDs (via `ids.registry.md`) and skips them
  - Detects DRAFT files modified by humans since the last run and skips them by default
  - Outputs a pre-run summary before proceeding so the user knows exactly what will be (re)generated
  - Aborts cleanly if everything is already promoted or human-edited
  - Two new rules added to `# What you never do` to reinforce the constraints

## [0.4.0] — 2026-05-03

### Added
- **Change mode for artifact-producing agents**: Product Owner, Analyst, and Tester
  each have a new `# Change mode` section. When given a `change-impact/CI-<date>.md`
  report, each agent self-scopes to the blast radius only:
  - Product Owner: updates only the affected UCs and re-runs M1 checklist scoped to those UCs
  - Analyst: updates only the affected RBs in place; updates domain model only if new entities appear
  - Tester: revises only the affected TCs and `test-matrix.md` rows; re-runs coverage gates scoped to changed UCs
- **REQ change flow in Orchestrator**: new `# REQ change flow` section drives the full
  scoped pipeline automatically via `/iconix-next` when a REQ change is detected —
  Traceability → Product Owner → M1 → Analyst → M2 → Developer+Tester (parallel) → M3

### Changed
- Orchestrator passes the CI report path in its dispatch plan so downstream agents
  can self-scope without manual instruction
- README: documented the REQ change flow, plan mode behaviour per agent,
  migration→pipeline handoff, and added a Notation & abbreviations glossary

## [0.3.0] — 2026-04-19

### Added
- **Graphify integration (Phase 1, migration agent only)**: `iconix-migration`
  now runs in graph-assisted mode when `iconix.config.yaml` enables Graphify.
  In graph-assisted mode:
  - Phase 1 (code survey) uses graph queries instead of code walking
  - Phases 2-3 (class model, sequence diagrams) seed from graph nodes/edges
  - Every artifact carries a `## Provenance` footer showing
    EXTRACTED / INFERRED / AMBIGUOUS edge counts
  - Stale graphs (>30 days) block migration; >7 days warns
- `knowledge_graph:` section in `iconix.config.yaml` template
  (disabled by default; portability preserved)
- `/iconix-graphify` slash command — bootstraps Graphify in a project
- `templates/graphify-setup.md` — full setup guide with confidence tuning,
  MCP server config, troubleshooting

### Changed
- `iconix-migration` agent now declares "operating mode" at start of every
  run (graph-assisted | code-walking)
- Orchestrator routing recognizes graph-assisted vs code-walking flow
- Installer copies Graphify setup guide into project templates

### Notes
- Other 9 agents (orchestrator, product-owner, analyst, architect,
  developer, tester, traceability, reviewer, docs) are **unchanged** in this
  release. Phase 2 will extend graph integration to architect/reviewer/
  traceability/docs once Phase 1 is validated in real use.
- This is an additive change. Existing projects on v0.2.0 continue to work
  identically without enabling `knowledge_graph`.

## [0.2.0] — 2026-04-19

### Added
- `iconix-reviewer` agent — detects drift between code and design artifacts
  (sequence diagram, class model, NFRs); produces review reports with
  BLOCK / CHANGES / APPROVE recommendations
- `iconix-docs` agent — generates user guides, developer onboarding, API
  reference, release notes, and SRE runbooks from ICONIX artifacts
- `iconix-migration` agent — reverse-engineers draft ICONIX artifacts from
  existing legacy codebases in a 7-phase workflow
- `/iconix-review`, `/iconix-docs`, `/iconix-migrate` slash commands
- PowerShell installer (`iconix-init.ps1`) for Windows users
- GitHub Actions validation workflow
- `CONTRIBUTING.md`, `LICENSE` (MIT), `CHANGELOG.md`

### Changed
- Orchestrator routing heuristics extended to cover review, docs, and
  migration flows
- Installer success message now lists all 10 agents and 6 commands

## [0.1.0] — 2026-04-19

### Added
- Initial kit with 7 agents: orchestrator, product-owner, analyst, architect,
  developer, tester, traceability
- 3 slash commands: `/iconix-next`, `/iconix-status`, `/iconix-impact`
- Bash installer (`iconix-init`) with project-scope and user-scope modes
- `iconix.config.yaml` template with prefix, stack, containers, NFRs
- Use case and robustness diagram templates
- README with install recipe and portability matrix
