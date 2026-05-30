# Changelog

All notable changes to the ICONIX Claude Kit.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.79] — 2026-05-29

**BACKLOG.md: add SDK Hybrid Option B entry (Claude Code-compatible); fix 4 gaps.**

New backlog entry for Python-scripts approach keeping full Claude Code UX while
moving deterministic work to `.claude/scripts/`. Eight-commit roadmap: general
pipeline (router, validate, ids, checkpoint, promote) + migration-specific
(preflight, promoted-check, params normalizer).

Entry revised to fix 4 gaps: (1) validate.py savings corrected to ~9,000 tokens
per full pipeline run (3 gates × ~3,000), not per gate call; (2) token savings
split into greenfield (40–50%) vs migration (higher, ~2,290 additional per run);
(3) infra.md budget relief quantified (~1,140 tokens removed, ~8,992 → ~7,852);
(4) migration_params.py scope clarified — NL detection stays in prompt, Python
handles normalize + checkpoint write only. migration_promoted.py noted as shared
utility with promote.py.

- `BACKLOG.md` — new "SDK Hybrid — Python scripts for deterministic parts" entry

## [1.0.78] — 2026-05-29

**migration: add `--entry-point` parameter to target a specific entry point by name.**

Teams doing selective migration had no way to specify which UC to draft — `--max-uc 1`
always picked by confidence order (EXTRACTED first), not by user intent. The new
`--entry-point <name>` filter lets you name an exact entry point from
`survey-phase1-<date>.md` and draft only that UC, regardless of its confidence tier.

Two name formats accepted (case-insensitive): `<class.method>` (e.g.,
`OrderController.PlaceOrder`) and `<HTTP-method /path>` (e.g., `POST /orders`).
Multiple targets via comma-separation. Takes precedence over `--max-uc`. Hard STOP
with valid-names list if the name is not found in the survey; silent skip if already
promoted.

Implemented as a semantic-only filter — structural still surveys all entry points in
scope; only Phase 5 drafting is filtered. Consistent with how `--max-uc` works.

- `agents/iconix-migration-infra.md` — parameter table, acknowledgement block, behavior description, checkpoint field `entry_point_filter`
- `agents/iconix-migration-semantic.md` — entry-point filter block in Phase 5 (graph-assisted + code-walking)
- `BACKLOG.md` — entry marked Done (v1.0.78)

## [1.0.77] — 2026-05-17

**BACKLOG.md: add SDK-based architecture entry.**

New backlog entry documenting the case for rewriting iconix-kit on the Anthropic
Python SDK. Covers token savings (60–70% at scale from routing elimination, fresh
context per call, selective prompt loading, and prompt caching), hard enforcement
gains (programmatic gates vs. advisory prompts), and a lower-risk hybrid alternative
(Python for orchestration/validation, agents for content generation). Includes
trade-off analysis, 6-step hybrid roadmap, and rejected alternatives.

- `BACKLOG.md` — new "SDK-based architecture" entry

## [1.0.76] — 2026-05-16

**README: fix incorrect paths for migration reference files in project layout.**

`migration-schema-detection-reference.md` and `migration-stack-patterns-reference.md`
were listed under `templates/` in the source kit layout section, but they actually
live under `docs/iconix/templates/`. Removed the two entries from `templates/` and
added a `docs/iconix/templates/` section with the correct paths and descriptions.
The installed-files layout section was already correct — no change needed there.

- `README.md` — source kit layout section fixed

## [1.0.75] — 2026-05-16

**Orchestrator Case A: offer choice instead of hard-stop when migration DRAFTs are pending.**

Previously, if a user ran `/iconix-next` with unpromoted migration DRAFTs present
(Case A: migration complete, DRAFTs awaiting promotion), the orchestrator hard-stopped
with no way to proceed except promoting first. This blocked users who wanted to start
a new unrelated feature while leaving DRAFTs for later review.

Case A now prints two options and waits for user reply:
- **Option 1** (recommended): promote DRAFTs first via `/iconix-promote`, then re-run.
- **Option 2**: reply `"new feature"` to skip the check and route to the normal ICONIX
  pipeline immediately. Includes a warning that permanent IDs assigned to the new
  feature will be numbered before the promoted DRAFTs (non-sequential, but no data
  loss — `/iconix-promote` always uses `highest existing ID + 1`).

- `agents/iconix-orchestrator.md` — Case A block replaced

## [1.0.74] — 2026-05-16

**Migration semantic: fix batch-2 re-draft bug when using `--max-uc` batching.**

When a user ran migration with `--max-uc 10` for batch 1, promoted the DRAFTs, then
ran migration again for batch 2 (same scope), the semantic agent had no mechanism to
skip already-promoted entry points. Since `--max-uc` orders by confidence and takes
the top N, batch 2 would select the same top-10 entry points as batch 1 and re-draft
them — the user never advanced to entry points 11–20.

Root cause: Phase 5 max-uc cap logic had no "skip already-promoted" step. The
idempotency check in infra marks promoted artifacts but does not pass that information
to semantic.

Fix: added a "remove already-promoted entry points" step as the first bullet in the
max-uc cap block. Before ordering by confidence, semantic now reads
`robustness/<PREFIX>-RB-*.puml` (permanent files — no `DRAFT` in filename), extracts
the inbound boundary node name from each (the entry point covered by that promoted UC),
and removes matching entry points from the candidate list. Applies to both graph-assisted
and code-walking modes (code-walking Phase 5 references "same max-uc cap logic").

- `agents/iconix-migration-semantic.md` — Phase 5 max-uc cap: new first bullet

## [1.0.73] — 2026-05-16

**Controller-to-container classification heuristic added to Architect agent.**

Closes the gap in Decision rule 2 ("Controllers should map to services/components
already in the architecture") which stated the outcome but not the method. Changes:

- `agents/iconix-architect.md` — new `# Controller-to-container classification`
  section (inserted before `# ADR format`) with a four-row classification table
  keyed on what each RB Controller connects to (Inbound Boundary / Entity /
  Outbound Boundary combinations → Application Service / Domain / Web/API), direct
  mappings for Boundary and Entity stereotypes, four edge-case rules, and a
  step-by-step procedure for producing container-mapping rows from an RB.
- `templates/container-mapping-template.md` — new "Source RB nodes" column in the
  "Containers traversed" table; updated header note to reference the classification
  heuristic; updated example rows with realistic RB node names.
- `agents/iconix-analyst.md` — `Store` and `Provider` added to Outbound Boundary
  valid suffix list.
- `agents/iconix-architect.md` — same two suffixes added to the classification
  table's Outbound Boundary example list.
- `docs/iconix/templates/migration-stack-patterns-reference.md` — `*Store` added
  to the adapter-pattern suffix list (`*Provider` was already present there).

Token budget: `iconix-architect.md` ~5,686 tokens (under 10,000 soft ceiling).
Methodology audit: no ICONIX rule overridden — heuristic is additive guidance not
present in Rosenberg & Stephens; no process reference matrix update required.

## [1.0.72] — 2026-05-16

**DDD Strategic Design guidance added to Architect agent and package-map template.**

Implements the revised DDD backlog proposal (v1.0.71): no new agents, no new folders,
no config flag. Changes are confined to three files:

- `agents/iconix-architect.md` — new `# Bounded Context reasoning` section (three
  questions: linguistic test, autonomy test, invariant ownership test) inserted before
  `# Decision rules`; new PDR readiness checklist item requiring non-empty "Bounded
  Context reasoning" column in every internal package row.
- `templates/architecture-package-map-template.md` — new "Bounded Context reasoning"
  column added to the Package list table with example answers; new Quality check item.
- `docs/iconix/iconix-process-reference.md` — new "DDD Strategic Design guidance"
  section (additive, citing Evans 2003 not Rosenberg & Stephens) with ⚠️ coverage for
  linguistic/autonomy/invariant-ownership signals and 🚫 for DDD tactical patterns.

Token budget: `iconix-architect.md` ~4,938 tokens (well under 10,000 soft ceiling).

## [1.0.71] — 2026-05-16

**Backlog: DDD entry revised — narrow scope, reject full automation.**

Revised the DDD support backlog entry (added in v1.0.70) after assessing the practical
limits of full ICONIX+DDD integration. The original 8-commit plan (two new agents,
three modified agents, extended traceability chain) is moved to "Rejected alternatives"
with three documented reasons: DDD value lives in conversations not artifacts; pipeline
gates conflict with DDD's iterative discovery; complexity-to-audience mismatch. The
revised proposed solution is a focused 2-commit change: a Bounded Context reasoning
checklist added to `iconix-architect.md` and a new column in the package-map template.
No agent or code files changed.

## [1.0.70] — 2026-05-16

**Backlog: DDD (Domain-Driven Design) support entry added.**

Added a detailed backlog entry for DDD hybrid mode to `BACKLOG.md`. The entry
documents the three structural incompatibilities between ICONIX and DDD (domain model
role, absence of Bounded Context / Strategic Design, no DDD tactical patterns in the
traceability chain), proposes a four-layer solution (config flag, two new agents, three
modified agents), and lays out an 8-commit implementation roadmap with explicit gate
conditions, artifact templates, and process reference matrix impact. No code or agent
files changed.

## [1.0.69] — 2026-05-16

**Fix: CI step `Agent tool consistency check` aborting under `set -e`.**

The v1.0.68 implementation passed local testing but failed on the first CI run
([run 25959417113](https://github.com/nqthuan82/iconix-claude-kit/actions/runs/25959417113)).
Root cause: `grep -c` returns **exit code 1** when the match count is zero. Under
`set -e`, the very first agent with zero matches (alphabetically: `iconix-git.md`,
which legitimately has zero file-write signals) aborts the loop before any check
can run.

Local Git Bash testing during development used the loop *without* `set -e`, so
the divergence wasn't visible until the workflow ran on Ubuntu CI.

**Fix:** append `|| true` to every `grep -c` and `grep -oE | head -1` invocation
in the new step. `grep -c` still prints "0" to stdout when there are zero matches,
so the captured variable is correct; only the non-zero exit code is swallowed.

Re-tested locally with `set -e` enabled — all 16 agents pass with the same signal
counts as before. No semantic change; pure CI compatibility fix.

## [1.0.68] — 2026-05-16

**CI: per-agent dry-run consistency check (Tier 1, static analysis).**

Tier 1 of the "per-agent dry-run tests" idea floated during the design discussion
that produced BACKLOG.md (v1.0.67). Static-analysis tier — no LLM invocation, no
API cost, runs in ~1 second alongside the existing frontmatter / token-budget /
uniqueness checks.

**Bug class targeted:** tool-list vs body inconsistency. Two real bugs from
earlier this session both fell in this class:
- v1.0.58 — `iconix-reviewer` body said "Produce `reviews/REVIEW-*.md`" but
  the `tools:` field declared only `Read, Grep, Glob, Bash`. Every invocation
  would have failed at the first Write attempt. Caught by audit, not CI.
- v1.0.62 — same pattern in `iconix-metrics`: body wrote
  `metrics/snapshot-<today>.md` but `tools:` omitted `Write`. Also caught by
  audit, not CI.

This step would have failed both PRs at CI time before they merged.

**New step `Agent tool consistency check`** in
`.github/workflows/validate.yml` `validate-agents` job. For each `agents/*.md`:

1. Count file-writing action verbs paired with backticked paths ending in
   `.md` / `.puml` / `.json` / `.yaml` / `.sh`. Verbs covered: `Produce`,
   `Save`, `Create`, `Write`, `Refine`, `Append`, `Update`, `Aggregate`, `Emit`.
   Allows leading bullet markers (`-`, `*`) and bold (`**Create ...**`) for
   the orchestrator's phase9-cycle write pattern.

2. Detect the `# Artifacts you produce` / `# What you produce` / `# What you write`
   / `# Artifacts produced` section header.

3. Sum the two signals. If signal > 0 AND `tools:` field lacks BOTH `Write`
   AND `Edit`, the build fails with a pointer to past examples in CHANGELOG.

Tested locally against all 16 agents in current main: 0 failures. If either
v1.0.58 or v1.0.62 were reverted, the check would fire (Reviewer signal=3,
Metrics signal=2 — both well above the 0 threshold).

**Advisory check (warn, no fail):** descriptions containing version tags like
`v0.9.7+`. Frontmatter `description:` is a routing signal; version-tagged
descriptions age badly. None of the 16 agents currently has this issue
(cleaned in v1.0.61), so this is forward-only protection.

**CLAUDE.md updated:** new "Tool-list discipline" paragraph in the
`## Adding or Modifying Agents/Commands` section explains the gate, its
heuristic, and the two past bugs it would have caught. Future maintainers
adding or modifying agents will see the discipline requirement next to the
frontmatter rules.

**Token / cost impact:** zero — no LLM calls, no extra dependencies. The
check runs grep + shell arithmetic, completes in well under a second.

**Tier 2 (LLM stub invocation) remains in BACKLOG.md** territory — deferred
unless Tier 1 proves insufficient. Tier 1 closes the specific bug class that
has actually occurred twice.

## [1.0.67] — 2026-05-16

**Add `BACKLOG.md` — living doc for proposed enhancements; first entry: Lightweight mode.**

New top-level file `BACKLOG.md` captures enhancement proposals that have a design
sketch but aren't scheduled for implementation. Each entry carries enough context
(problem statement, design, trade-offs, mitigation, roadmap, open questions, rejected
alternatives) that a future session can pick it up without re-deriving the problem.

Status legend: Proposed / In design / In progress / Done / Rejected. Entries that
ship migrate from the backlog into a versioned CHANGELOG entry; rejected proposals
stay in BACKLOG.md with the rationale so they aren't re-proposed.

**First entry — Lightweight mode** (Proposed):
A parallel pipeline path for sub-day features (filter additions, copy changes, single
endpoints) where the full PO → Analyst → Architect → Developer → Tester chain has a
6:1 overhead ratio. Lightweight UCs skip diagram production but preserve traceability
data inline (`Class-touch:`, `NFRs:`, `Containers:`, `TCs:`) so impact/risk analysis
still works. Two CI sanity checks (Traceability validates declared class names exist;
Reviewer compares declared vs actually-modified classes at Phase 9.2) mitigate the
class-touch honesty risk that comes from declaring data rather than deriving it from
RB diagrams.

`README.md` Project layout updated to list BACKLOG.md at the top level.

No agent / template / methodology / CI changes — this commit only adds documentation.

## [1.0.66] — 2026-05-16

**Orchestrator: pre-flight check for unpromoted migration DRAFTs.**

Closes D4 from the cross-agent logic audit. After `iconix-migration-semantic`
finishes, users had to remember to run `/iconix-promote` before invoking
`/iconix-next` to convert DRAFT slugs (e.g., `UC-DRAFT-001`) into permanent
ICONIX IDs (e.g., `UC-017`). If they forgot and ran `/iconix-next` directly,
the orchestrator would route work as if DRAFTs were first-class artifacts —
but the Traceability chain expects permanent IDs and DRAFTs cannot pass
M1/M2/M3 gates properly. Result: silent confusion and gate-failure spam.

The previous nudge was a single text line in the `iconix-migration` router's
Case D output ("When DRAFTs are ready: run /iconix-promote"). Easy to miss.

**New: Orchestrator `# Pre-flight checks` section (before `# Phase order`)**

Runs before any routing decision. The first check (`Check 1 — Unpromoted
migration DRAFTs`) greps for DRAFT artifacts across all migration output
paths:
- `use-cases/UC-DRAFT-*.md`
- `robustness/RB-DRAFT-*.puml`
- `sequence/SD-DRAFT-*.puml`
- `domain-model/domain-model-DRAFT.puml`
- `class-model/class-model-DRAFT.puml` (greenfield-coexistence mode from v1.0.64)
  OR `class-model/class-model.puml` with a DRAFT stamp in its header (standard mode)
- `use-case-packages/*-DRAFT.puml`

If any are found, the orchestrator reads `migration/checkpoint-*.json` to
classify the situation:

- **Case A — migration complete, DRAFTs awaiting promotion**
  (`phases_completed` includes `"semantic"`): stop and tell the user to
  run `/iconix-promote all` or `/iconix-promote UC-DRAFT-<slug>`, then
  re-run `/iconix-next`.
- **Case B — migration mid-pipeline** (checkpoint missing or
  `phases_completed` does not include `"semantic"`): stop and tell the
  user to continue migration first via `iconix-migration` router.
- **Case C — no DRAFTs found**: proceed to normal Phase-order routing.

**No methodology surface changes.** ICONIX phase order, gate criteria,
and traceability chain unchanged. The fix is a guard on the orchestrator's
entry point — it can't route through invalid state, and the user gets a
specific command to run instead of a vague gate failure later.

**No changes to `iconix-migration` router or `iconix-promote` command** —
the Case D message in the router and the promotion command itself are
correct as-is. The orchestrator is the new safety net on the receiving
end of `/iconix-next`.

**Token impact:** orchestrator ~4,333 → ~4,860 tokens (still 51% under
the 10K soft ceiling). No other agent touched.

## [1.0.65] — 2026-05-16

**Orchestrator: docs-sync nudges in Phase 9.4 exit and REQ change flow.**

Closes D3 risk from the cross-agent logic audit. `iconix-docs` is the only
artifact-writing agent that the Orchestrator does not route to — public
docs (`docs/user-guide/`, `docs/dev-guide/`, `docs/api/`, `docs/ops/`) are
generated only when the user explicitly invokes `/iconix-docs`. The audit
flagged that nothing in the pipeline reminds the user to refresh these
docs after a UC text or design change, so they silently go stale.

**New: Phase 9.4 Step 6 — Docs sync check (non-blocking)**
Runs after Phase 9 Exit bookkeeping (Step 5), before the UC moves to
"Done". The Orchestrator greps `docs/user-guide/`, `docs/dev-guide/`,
`docs/api/`, and `docs/ops/` for the traceability footer pattern
`Generated from UC-XXX` (the footer `iconix-docs` writes per its
`# Rules` section). For each match, prints a non-blocking suggestion
naming the exact `/iconix-docs <type> UC-XXX` command to refresh. If
no pages reference the UC, the check is silent. Cannot block Phase 9 exit
— this is a follow-up the user decides.

**New: REQ change flow Step 9 — Docs sync check (non-blocking)**
Same check after the scoped M3 gate re-run completes, applied to every
UC in the change-impact (CI) report's blast radius. A REQ change typically
shifts UC text and post-conditions, so any existing user-facing page for
those UCs is likely stale. Same silent-skip semantics for UCs without
public docs.

**No `iconix-docs` agent changes** — the agent already accepts a UC-ID
scope (`/iconix-docs user UC-017`), and its `# Rules` already emit the
`Generated from UC-XXX` footer. The fix is purely Orchestrator-side: it
now points users at the existing capability at the right moment.

**No methodology surface changes.** Phase 9 sub-state semantics, REQ
change flow phase order, gate criteria, and the traceability chain are
all unchanged. ICONIX reference matrix (`docs/iconix/iconix-process-reference.md`)
doesn't need an update.

**Token impact:** orchestrator ~3,831 → ~4,333 tokens (still 60% under
the 10K soft ceiling). No other agent touched.

## [1.0.64] — 2026-05-16

**Migration: greenfield artifact collision guard (`--allow-greenfield` flag).**

Closes the D2 risk surfaced by the cross-agent logic audit. Migration is for
retrofitting ICONIX onto code with NO existing artifacts; without a guard, a
user who accidentally runs `/iconix-migrate` on a project that already has
greenfield UCs / RBs / SDs / class model would:

1. **Silently overwrite `class-model/class-model.puml`** — the only true
   filename collision between greenfield Developer output and migration
   structural output. Both write to the same canonical path.
2. **Pollute target folders** with a confusing mix of greenfield `UC-*.md`
   and migration `UC-DRAFT-*.md` (different filename patterns but
   coexistence in `use-cases/` confuses Analyst and Tester downstream).

**New: `iconix-migration-infra` Step 0 — Greenfield artifact collision check**
Runs before the existing idempotency check (Step 1). Detects any non-DRAFT
artifact in `use-cases/`, `robustness/`, `sequence/`, `use-case-packages/`,
plus the canonical `class-model/class-model.puml`. If found AND
`--allow-greenfield` not in `$ARGUMENTS`, prints the detected file list
and aborts with options for the user. Default behavior is safe-by-refuse.

**New: `--allow-greenfield` flag** (declared in `iconix-migration-infra`
and surfaced in the `iconix-migration` router's Case A guidance). When
passed:
- Migration proceeds despite greenfield detection.
- Checkpoint records `greenfield_coexistence: true` and the
  `greenfield_files` list.
- `iconix-migration-structural` Phase 2 (both graph-assisted and
  code-walking variants) reads the flag and writes to
  `class-model/class-model-DRAFT.puml` instead of overwriting the
  greenfield `class-model.puml`. The greenfield file becomes a read-only
  input.
- `domain-model`, `UC`, `RB`, `SD`, `use-case-packages` already use
  `-DRAFT` filename suffixes, so no further filename routing needed —
  they coexist with greenfield names cleanly under the flag.

**Files touched:**
- `agents/iconix-migration-infra.md` — new Step 0 section (~40 lines),
  `--allow-greenfield` row in the scope/run-parameters table, checkpoint
  schema gains `greenfield_coexistence` and `greenfield_files` fields.
- `agents/iconix-migration-structural.md` — Phase 2 (graph-assisted +
  code-walking) reads `greenfield_coexistence` and resolves the output
  filename; final output-structure block and structural-complete gate
  reflect both possible filenames.
- `agents/iconix-migration.md` — router Case A surfaces the new flag
  in the parameter list with a one-line description.

**No methodology surface changes** — this is a tooling guard. ICONIX
phase order, gate criteria, stereotype rules, and traceability chain are
all unchanged. Reference matrix (`docs/iconix/iconix-process-reference.md`)
doesn't need an update.

**Token impact:** migration-infra ~7.9K → ~8.7K, migration-structural
~8.0K → ~8.2K, router ~1.2K → ~1.2K. All under the 10K soft ceiling;
semantic remains the only WARN-tier agent at 10.65K.

## [1.0.63] — 2026-05-16

**Consistency: Plan mode block for 6 artifact-writing agents + orchestrator role wording.**

Follow-up to v1.0.62. The re-audit flagged that 6 agents have `Write` in their
tools list and write files in their body, but lack the `# Plan mode` section
that 8 other artifact-writing agents already have (analyst, architect, developer,
docs, migration-semantic, migration-structural, product-owner, tester).

Without the block, these agents would error out in plan mode (Write blocked by
harness) instead of emitting their content inline as a fenced code block — the
canonical fallback that v1.0.50 established as kit-wide convention.

**Agents that gained `# Plan mode`:**
- `iconix-reviewer` — writes `reviews/REVIEW-*.md` (had no plan-mode fallback since Write was added in v1.0.58)
- `iconix-metrics` — writes `metrics/snapshot-*.{md,json}` and `metrics/trend-*.md` (Write was added in v1.0.62; this completes the gap)
- `iconix-migration-infra` — writes `migration/checkpoint-*.json` and `migration/dependency-registry-*.md`
- `iconix-traceability` — writes orphan reports, traceability matrices, milestone-gate reports, change-impact reports, ID registry
- `iconix-upgrade` — writes `upgrades/upgrade-<from>-to-<to>-*.md`, modified `iconix.config.yaml`
- `iconix-orchestrator` — writes `phase9-cycles/UC-XXX-cycle.md`

The block is the canonical 8-line version copied verbatim from the kit's other
artifact-writing agents (no per-agent customization needed — the wording works
generically for any "the artifact you would have written").

**Orchestrator role wording fix:**
Line 9 said "You do not produce artifacts yourself — you dispatch." This was
accurate when written but became overstated when Phase 9 added the cycle log
(`phase9-cycles/UC-XXX-cycle.md`), which the orchestrator does create and
append to during Phase 9.1/9.2/9.4. Reworded to: "You do not produce ICONIX
artifacts (UCs, RBs, SDs, code, tests, ADRs) yourself — you dispatch. The only
file you write directly is `phase9-cycles/UC-XXX-cycle.md`, which is an
iteration journal, not a methodology artifact." This matches the existing
`# What you never do` list, which already correctly excludes the cycle log.

No methodology surface changes — Plan mode is a harness-fallback convention,
not an ICONIX rule. No pipeline / gate / agent label changes; state machine
unchanged.

## [1.0.62] — 2026-05-16

**Fix: `iconix-metrics` missing `Write` tool (runtime bug).**

Same class of bug as the `iconix-reviewer` Write tool gap fixed in v1.0.58.

`agents/iconix-metrics.md` line 5 declared `tools: Read, Grep, Glob, Bash` —
no `Write`. But the body requires the agent to produce three files on every
invocation:

- line 22: `metrics/snapshot-<YYYY-MM-DD>.md` (markdown snapshot)
- line 23: `metrics/snapshot-<YYYY-MM-DD>.json` (machine-readable snapshot)
- line 24: `metrics/trend-<YYYY-MM-DD>.md` (trend mode only)

And line 120 says explicitly: "Write the markdown to `metrics/snapshot-<today>.md`...
and the JSON to `metrics/snapshot-<today>.json`."

Without `Write` in the tools list, every `/iconix-metrics` invocation would
fail the first time the agent tried to produce a snapshot file. Fix: add
`Write` to the tools declaration. One-line change.

This is an isolated bug-fix commit (no other agent / config / methodology
changes) so it can be reverted cleanly if anything downstream depends on
the old declaration. The Plan-mode and orchestrator-wording consistency
items surfaced in the same re-audit will ship in a separate commit.

## [1.0.61] — 2026-05-15

**Frontmatter polish + iconix-docs structure normalization.**

Closes the remaining "quality" items from the v1.0.58 audit. No methodology or
behavior changes — purely frontmatter trimming and section-header consistency.

**Description rewrites** (frontmatter `description:` is a routing signal; shorter +
evergreen helps Claude pick the right agent faster):
- `iconix-migration`: 700 → 336 chars. Was 5 sentences mixing role, capabilities,
  Graphify caveat, and implementation detail. Now 3 short sentences focused on
  routing identity + dispatch targets.
- `iconix-upgrade`: 340 → 291 chars. Folded the read-only artifact list into a
  parenthetical inside the detect-and-report sentence; dropped the redundant
  "Use to" opener.
- `iconix-metrics`: dropped the trailing `v0.9.7+.` version tag. Frontmatter
  descriptions should be evergreen — agent versioning lives in CHANGELOG, not in
  the routing description that Claude reads on every dispatch.

**`iconix-docs.md` section normalization:**
- Renamed `# Translation rules` → `# Rules` to match the standard header used by
  6 other agents (git, metrics, migration-{infra,semantic,structural}, upgrade).
  Content unchanged — translation IS this agent's rule set, so the original name
  was just a less-discoverable synonym.
- Added `# Plan mode` block (8 lines, copy of the standard incantation used by
  analyst, architect, developer, tester, product-owner, and the migration
  sub-agents). The docs agent writes to `docs/user-guide/`, `docs/dev-guide/`,
  etc. — it needed the standard plan-mode fallback so a blocked Write surfaces
  inline content instead of an error.

Section order for `iconix-docs.md` is now: Role → Inputs → Documentation types →
Rules → Workflow → Plan mode → What you never do → Quality checks — matches the
canonical pattern across the kit.

## [1.0.60] — 2026-05-15

**Guardrails: CI token-budget check + in-session sync-reminder hook.**

Two complementary guardrails that close gaps surfaced by the v1.0.58 audit. Both are
self-policing — neither requires a maintainer to remember a rule.

**CI — Agent token budget step (`.github/workflows/validate.yml`):**
- Loops every `agents/*.md`, measures chars/4 as a portable token estimate.
- **Soft warn:** > 10,000 tokens — prints `WARN` next to the row but does not fail the
  build. Matches the CLAUDE.md soft ceiling.
- **Hard fail:** > 12,000 tokens — fails the job with a pointer to CLAUDE.md
  `## Agent token budget` for the extraction technique.
- Prints a full size table on every PR so reviewers see at a glance which agents are
  approaching the budget. Drift past the soft ceiling used to be invisible
  (`migration-structural` silently grew from 7.1K to 9.75K between v1.0.40 and v1.0.58);
  now any PR that bumps an agent past 10K shows the WARN inline.

**In-session — PostToolUse sync reminder (`.claude/settings.json` + `.claude/hooks/check-iconix-surface.sh`):**
- Project-scoped Claude Code hook (checked in; team-wide). Fires after every Write/Edit.
- Inspects `tool_input.file_path`; if the path touches the kit's user-facing surface
  (`agents/*.md`, `commands/*.md`, `templates/`, `iconix-init`, `iconix-init.ps1`,
  `iconix-state-machine.puml`), prints a stderr reminder pointing at the CLAUDE.md
  "Keeping README and state machine in sync" checklist.
- Handles both POSIX and Windows-backslash paths (normalises `\` → `/` before pattern
  matching).
- Always exits 0 — non-blocking. CI is the gate; the hook is a per-edit reminder.
- Uses bash (`shell: bash` in settings.json). On Windows the hook needs Git Bash on
  PATH; without it the hook silently no-ops, which is fine for a reminder.

**CLAUDE.md updated:**
- `## Agent token budget` section adds a note about the new CI enforcement.
- `## Keeping README and state machine in sync` section removes the "would be needed"
  language about a hook — the hook now exists and is described alongside the
  in-prompt rule.

## [1.0.59] — 2026-05-15

**Token budget: extract cross-stack patterns out of `iconix-migration-structural` (~1.7K tokens saved).**

Background: the audit in v1.0.58 surfaced that `iconix-migration-structural.md` had
grown from ~7,100 tokens (registered in CLAUDE.md) to ~9,750 tokens (37% drift),
approaching the 10K soft ceiling. This release applies the same extraction technique
v1.0.52 used on the semantic agent.

**New reference file `docs/iconix/templates/migration-stack-patterns-reference.md`:**
- **Block A** — Entry-point taxonomy (Phase 1, both modes): cross-stack pattern matrix
  for inbound HTTP / async / CLI across C# / Java / Python / Node.js / Go / Ruby; graph
  node-type strings; actor identification rules.
- **Block B** — Cross-container boundary correlation (Phase 1b): inbound boundary table
  per protocol (B.1), outbound call collection (B.2), match conditions and confidence
  tiers (B.3).
- **Block C** — Source-construct → PlantUML mapping (Phase 3 Step 3): the if/else,
  try/catch, loops, `Task.WhenAll`, fire-and-forget, polymorphic-dispatch mapping rows.
- **Block D** — Outbound boundary cross-stack patterns (Phase 4): universal signals,
  cross-stack illustration (Outbound HTTP / DB / message publisher / vendor SDK / file-blob
  across 6 stacks), Entity/Controller companion classifications, disambiguation rule
  (trust imports over class names).

**Changes to `iconix-migration-structural.md`:**
- Phase 1 (graph-assisted): inline cross-stack table → `Read Block A` pointer.
- Phase 1 (code-walking): inline framework-marker bullet list → `Read Block A` pointer
  (eliminates the duplicate-vs-graph-assisted maintenance burden).
- Phase 1b Steps 1–3: three inline tables → `Read Block B` pointer (Step 4 onward unchanged).
- Phase 3 Step 3: inline PlantUML mapping table → `Read Block C` pointer.
- Phase 4 Step 1: inline cross-stack illustration + Entity/Controller stack examples +
  disambiguation rule → `Read Block D` pointer. Three classification signals
  (inbound dispatch / outbound infra imports / pure data) and the [VERIFY] discipline
  remain inline — these are ICONIX methodology, not stack-specific detection.

**Methodology surface unchanged.** The extraction is pure relocation of stack-specific
detection aids. ICONIX rules (boundary/entity/controller stereotypes, noun-verb-noun,
mixed-responsibility check, alternate course discipline, traceability) all remain in
the agent body. Per CLAUDE.md `## Methodology-in-Config Split`: stack-specific patterns
were never supposed to live in the agent prompt anyway.

**File size:** `iconix-migration-structural.md` 39,048 → 32,107 chars (~9,750 → ~8,030 tokens).
Back under the 10K soft ceiling and below the v1.0.58 highest-risk flag.

**Installer + CI:**
- `iconix-init` and `iconix-init.ps1` now copy the new reference file to the project's
  `docs/iconix/templates/` (same pattern as the v1.0.47 schema-detection reference).
- `.github/workflows/validate.yml` Linux + Windows smoke tests now assert the new
  reference file is present after install.

**README + CLAUDE.md updates:**
- `README.md` `## Project layout` section adds the new reference file in both the
  installed-layout and templates-tree blocks.
- `CLAUDE.md` `## Agent token budget` table reflects new sizes; "Reference files
  extracted" section now lists both reference files and their consumers; the
  highest-risk flag drops away (no agent currently above 10K).

## [1.0.58] — 2026-05-15

**Agent prompt audit fixes — runtime bug, frontmatter completeness, dedupe, doc drift.**

Four targeted fixes surfaced by an audit of all 16 agent prompts:

1. **`iconix-reviewer` — added `Write` to tools (runtime bug).** The agent body
   instructs it to produce `reviews/REVIEW-<date>-<scope>.md` at four places
   (lines 75, 141, 161, 234), but the tools list omitted `Write`. Any review
   invocation would have failed at the first write attempt. `Write` now added.

2. **`iconix-docs` and `iconix-upgrade` — added `model:` field.** v1.0.53
   established 3-tier model assignment across all agent frontmatter; these two
   were missed. Both assigned to `claude-sonnet-4-6` (balanced tier: docs does
   prose transformation, upgrade does detection + diff computation — neither
   needs Opus reasoning, neither is purely mechanical).

3. **Deduped `# Honest limitations` section.** The block existed in both
   `iconix-migration.md` (router) and `iconix-migration-infra.md` (Phase 0
   sub-agent), violating the "Grep before writing" rule in CLAUDE.md
   `## Agent prompt discipline`. Router is the user's first contact with the
   migration pipeline, so the canonical copy stays there; infra now carries a
   single-line pointer back to the router. The router-side copy also picked up
   the bullet about traceability recovery that previously only lived in infra,
   so no information is lost.

4. **CLAUDE.md doc drift — counts and token budget table refreshed.**
   - `## What This Repo Is`: agent count 10 → 16, command count 7 → 14
     (actual counts from `agents/*.md` and `commands/*.md`).
   - `## Agent token budget`: numbers re-measured (chars/4). Highest-risk flag
     moved from `migration-semantic` (now ~10,650 tokens after v1.0.52's BDD
     table extract) to `migration-structural` (now ~9,750 tokens, grown 37%
     from its registered ~7,100 baseline and approaching the 10K soft ceiling).

No methodology surface changes; no template, command, or pipeline-order changes.
README.md agent/command counts were already correct (line 165 says "16 agent
definitions") — only CLAUDE.md was stale.

## [1.0.57] — 2026-05-15

**CI: Windows smoke test for PowerShell installer (`iconix-init.ps1`).**

Added `smoke-test-installer-windows` job to `.github/workflows/validate.yml` running on
`windows-latest` with `shell: powershell` (Windows PowerShell 5.1 — the shell Windows
users actually run, not PowerShell Core 7).

The job mirrors every check in the existing Linux `smoke-test-installer` job:
agent count (≥10), config patching (prefix + language), knowledge_graph defaults,
graphify integration, intake templates, migration sub-agents (v1.0.47+), schema detection
reference file, git integration files, concurrent_check/metrics/phase9/kit_version config
sections, all architect/developer/tester templates, use-case-packages folder.

Previously, a regression in `iconix-init.ps1` (e.g. missing a new agent in the copy list)
would pass CI silently and only surface when a Windows user reported the issue.

## [1.0.56] — 2026-05-15

**Feature: `[VERIFY]` severity tiers (HIGH / MEDIUM / LOW) in migration artifacts and handoff report.**

On large systems (15–20 containers), handoff reports can contain 200–400 `[VERIFY]` markers
all appearing at equal weight. Reviewers cannot identify what to resolve first.

**Semantic agent — `# [VERIFY] severity classification` section (new):**
Every `[VERIFY]` marker now carries a tier suffix: `[VERIFY:HIGH]`, `[VERIFY:MEDIUM]`, or `[VERIFY:LOW]`.
Classification rules applied throughout all phases:

- **HIGH** — blocks promotion; resolve before `/iconix-promote`: cross-container UC grouping (MEDIUM confidence), AMBIGUOUS graph edges, SQL-only state machine sequences, INFERRED Invariant/Transition-guard business rules, unknown actor identity, unclear try/catch alternate courses.
- **MEDIUM** — resolve before M1/M2 gate: specific-but-unconfirmed actor role names, try/catch alternate courses with plausible intent, INFERRED Precondition/Authorization/Workflow rules, ORM enum state machine sequences (order reliable, meaning needs PO sign-off).
- **LOW** — cosmetic; review last: FK-derived preconditions, stored procedure verb mappings, EXTRACTED attribute names, Track V validator rules, UC package cluster groupings.

**Semantic agent — Phase 7 instruction updated:**
Populate both `### [VERIFY] priority summary` and `### [VERIFY] breakdown by artifact group` tables with HIGH/MEDIUM/LOW counts per artifact group.

**`templates/handoff-report-template.md` updated:**
Replaced the single-count `### [VERIFY] item breakdown` table with:
- `### [VERIFY] priority summary` — cross-tab (tier × artifact group) showing total per tier at a glance
- `### [VERIFY] breakdown by artifact group` — per-artifact-group HIGH/MEDIUM/LOW columns

## [1.0.55] — 2026-05-15

**Fix: BDD generation in reverse-order workflow (application scope before DB scope).**

When a user runs `--scope ServiceA` first (producing UC-DRAFTs) and then runs `--scope DatabaseContainer` (producing domain-glossary.md), the semantic agent now correctly generates BDD for ServiceA's UC-DRAFTs during the DB container run — without requiring a third run.

Two targeted fixes in `iconix-migration-semantic.md`:

**1. Phase 5c Gate (Steps 4–6) — project-wide UC-DRAFT scan:**
Clarified that the gate scans ALL `use-cases/UC-DRAFT-*.md` project-wide (including those from previous scope runs), not just UC-DRAFTs produced in the current run. Added explicit database-container note: when schema sources exist but zero entry points are found in scope, the project-wide scan is the primary mechanism for finding UC-DRAFTs to generate BDD for. Added duplicate guard: skip UC-DRAFTs that already have a corresponding `BDD-DRAFT-*.feature` file.

**2. Phase 5c Step 4 — explicit scope:**
Added leading instruction: process ALL UC-DRAFTs that passed the gate (current run + previous runs); skip those already having BDD-DRAFT files.

**3. `semantic-complete` gate — condition 2 loosened:**
Zero UC-DRAFTs is now acceptable when the current scope is a database container (schema found, zero entry points). Previously this would fail the completion check even though it's expected behavior for a DB-scoped run.

Correct incremental workflows now supported in both orders:
```
Order 1 (recommended): --scope DB → glossary  →  --scope App → BDD via Case B
Order 2 (also works):  --scope App → UC-DRAFTs  →  --scope DB → glossary + BDD for App's UCs
```

## [1.0.54] — 2026-05-15

**Fix: Database container readiness warning for scoped runs.**

When running `--scope <AppContainer>` and database-like containers exist but no `domain-glossary.md` has been built yet, the migration infra agent now stops and warns the user before proceeding:

- Detects containers with SQL schema files and zero application entry points
- Warns that Phase 5c BDD generation will be silently skipped without a glossary
- Presents two options: cancel (run DB container first) or continue (get UC-DRAFTs now, BDD later)
- Waits for user reply before writing the checkpoint
- Skip condition: if `domain-glossary.md` already exists (DB run already done), warning is suppressed — Phase 5c Case B will fire and BDD will be generated normally

This prevents the "why didn't I get BDD?" confusion that occurs when a user runs an application container before the database container in a `.sqlproj` / SqlClient architecture.

## [1.0.53] — 2026-05-15

**Feature: `model:` field in all agent frontmatter — 3-tier model assignment.**

Pins each agent to the optimal Claude model so kit quality and cost are consistent regardless of the user's session model. Three tiers:

- **Opus (`claude-opus-4-7`)** — heavy reasoning / artifact generation from code: `iconix-analyst`, `iconix-architect`, `iconix-migration-structural`, `iconix-migration-semantic`
- **Sonnet (`claude-sonnet-4-6`)** — structured rules + good judgment: `iconix-orchestrator`, `iconix-developer`, `iconix-tester`, `iconix-product-owner`, `iconix-reviewer`, `iconix-migration`, `iconix-migration-infra`
- **Haiku (`claude-haiku-4-5-20251001`)** — pattern matching / counting / validation: `iconix-traceability`, `iconix-git`, `iconix-metrics`

Before this change, all agents ran on the user's session model — a user on a Haiku session for cost reasons would unknowingly run Analyst and Architect on Haiku, producing lower-quality design artifacts. Now the kit "just works" regardless of session model.

## [1.0.52] — 2026-05-15

**Fix: Phase 5c BDD generation with dedicated database containers and incremental scoped runs.**

Three targeted fixes for the case where SQL schema lives in a dedicated container (e.g. `Migrations`, `Database`) separate from application containers:

**1. Two-tier skip condition (semantic agent Phase 5c):**
The original single skip condition bypassed both Steps 1–3 (schema detection) AND Steps 4–6 (BDD generation) whenever the current scope had no schema sources — even when `domain-glossary.md` already existed from a previous run. Split into two independent tiers:
- Case A (no schema AND no existing glossary): skip Steps 1–3 and Steps 4–6; move to Phase 6.
- Case B (no schema BUT existing glossary): skip Steps 1–3 only; proceed to Step 4 gate so BDD-DRAFTs are generated from existing glossary + current run's UC-DRAFTs.

**2. domain-glossary.md append/merge mode (semantic agent Phase 5c Step 3):**
When `migration/domain-glossary.md` already exists (from a previous `--scope` run), merge new entities rather than overwrite. Existing entity content is preserved; new entities are appended; new attributes on existing entities are annotated `[VERIFY — updated by run <date>]`.

**3. Database container workflow guidance (infra agent `# Scope and run parameters`):**
Added explicit note: if SQL schema lives in a dedicated container, include it in an early `--scope` run to build the glossary first. Clarifies that the container name is irrelevant — detection is functional (schema files present, zero entry points).

This enables the correct incremental workflow:
```
Run 1: --scope Migrations   → domain-glossary.md produced; no UC-DRAFTs
Run 2: --scope OrderService → UC-DRAFTs produced; Phase 5c Case B fires;
                              BDD-DRAFTs generated from existing glossary
```

## [1.0.51] — 2026-05-15

**Feature: Migration scoped execution — `--scope` and `--max-uc` parameters.**

Large systems (500+ entry points) previously required a full single-run migration. Added two optional parameters for incremental, prioritized migration:

- **`--scope <ContainerName>`** — survey only entry points from the named container in Phase 1. Other containers are skipped this run. Combine with subsequent runs (`--scope PaymentService`, `--scope UserService`) to process containers incrementally.
- **`--max-uc N`** — cap UC-DRAFT production at N in Phase 5 (semantic), ordered by confidence (EXTRACTED first). Remaining entry points are listed at the end with a re-run suggestion.

**Cross-container UC handling:** `--scope` does not filter Phase 1b cross-container correlation. Phase 1b always loads all `migration/survey-phase1-*.md` files from previous runs to detect UCs spanning multiple containers. A UC-DRAFT created for OrderService in Run 1 will be proposed as an amendment (not duplicated) when PaymentService is scoped in Run 2 and the pairing is detected.

Files changed:
- `agents/iconix-migration-infra.md` — `# Scope and run parameters` section added; checkpoint template gains `max_uc` field; `scope` and `max_uc` populated from user message.
- `agents/iconix-migration-structural.md` — scope filter gate added after entry gate; Phase 1b Step 0 (both modes) gains explicit note: load all surveys regardless of scope.
- `agents/iconix-migration-semantic.md` — Phase 5 (both modes) gains max-uc cap logic with remaining-entry-points log.
- `agents/iconix-migration.md` (thin router) — Case A shows optional parameters and example.

## [1.0.50] — 2026-05-15

**Fix: Plan mode support for all artifact-writing agents.**

When Claude Code runs in plan mode, the Write tool is blocked pending user approval. Previously, all artifact-writing agents would stall silently at the first blocked Write call — producing no useful output. Added a `# Plan mode` section to 7 agents:

- `iconix-product-owner.md`
- `iconix-analyst.md`
- `iconix-architect.md`
- `iconix-developer.md`
- `iconix-tester.md`
- `iconix-migration-structural.md`
- `iconix-migration-semantic.md`

Each agent now: (1) detects a blocked Write as plan mode, (2) emits all artifact content inline as labeled fenced code blocks, (3) continues through all remaining artifacts without stopping, (4) tells the user to approve Write calls or exit plan mode to write to disk.

## [1.0.49] — 2026-05-15

**Fix: Migration survey file self-choking — `survey-phase3-<date>.md` compact hand-off.**

`migration/survey-phase1-<date>.md` accumulates the full Phase 1 output (raw entry-point inventory, graph stats, per-container stack override YAML, cross-container correlation). On large systems (20 containers × 50 entry points) this file can reach 50,000+ words. `iconix-migration-semantic` was reading the full file at Phase 5 (cross-container correlation) and Phase 6 Step 0 (amendment proposals) — each read consuming unnecessary context budget.

Fix: structural agent now produces a second, compact file **`migration/survey-phase3-<date>.md`** (new Phase 4c step) containing only what semantic needs:
- **Run metadata** — mode, container count, entry point total, SD/RB-DRAFT counts
- **`## Cross-container boundary correlation`** — copied from `survey-phase1`; semantic reads this at Phase 5 to group multi-container entry points into single UC-DRAFTs
- **`## Amendment proposals (incremental run)`** — copied from `survey-phase1`; semantic reads this at Phase 6 Step 0 to sync amended UC-DRAFTs
- **Sequence diagram index** — one row per SD-DRAFT (filename, entry point, type)

Raw entry-point inventory, graph stats, and per-container YAML remain in `survey-phase1-<date>.md` only.

Files changed:
- `agents/iconix-migration-structural.md` — Phase 4c section added; completion gate adds verification item 3 (`survey-phase3` exists); output structure updated.
- `agents/iconix-migration-semantic.md` — entry gate reads `survey-phase3` after checkpoint; Phase 5 (both modes) and Phase 6 Step 0 (both modes) reference `survey-phase3` instead of `survey-phase1`.
- `agents/iconix-migration.md` (thin router) — Case B "Writes" and Case C "Reads" updated.

## [1.0.48] — 2026-05-15

**Fix: State machine — migration flow added as retrofit entry point.**

`iconix-state-machine.puml` updated to show migration as a first-class entry path alongside the greenfield flow, bug flow, and REQ change flow:

- New `<<migration>>` stereotype (lavender `#D7BDE2`) distinguishes migration from agent (blue), gate (yellow), bug (red), and change (green) states.
- `Idle → MigrationFlow` transition: "existing codebase (retrofit migration)".
- `MigrationFlow` state shows the 3-sub-agent sequence (`infra → structural → semantic`) and lists produced artifacts (UC-DRAFTs, class model, RB-DRAFTs, sequence diagrams, domain model, business-rules.md, handoff report).
- `MigrationFlow → M1Gate` transition: "DRAFTs promoted — handoff reviewed; REQs seeded (re-enters pipeline at M1)".
- Note block documents both entry commands (`/iconix-migration` thin router and individual sub-agents).

Migration was absent from the diagram despite being added in v1.0.0. The split in v1.0.47 (3 sub-agents) made this gap visible: the diagram had Bug flow and REQ Change flow as retrofit entry points but no equivalent for the migration path.

## [1.0.47] — 2026-05-15

**Feature: Migration agent split into 3 phase-based sub-agents with checkpoint protocol and prompt optimization.**

The monolithic `iconix-migration.md` (32,515 tokens) has been split into three phase-based sub-agents to solve context window exhaustion on large systems (50+ entry points, 20+ containers):

- **`agents/iconix-migration-infra.md`** (~10K tokens) — pre-flight checks: mode detection, per-container graph resolution, multi-repo source resolution, pre-run idempotency check, dependency source reconnaissance (Step 0b), cross-container boundary correlation (Phase 1b). Writes `migration/checkpoint-<date>.json` and `migration/dependency-registry-<date>.md`.
- **`agents/iconix-migration-structural.md`** (~7K tokens) — structural phases: code survey (Phase 0/1), class model (Phase 2), sequence diagrams (Phase 3), robustness diagrams (Phase 4), domain model (Phase 4b). Both graph-assisted and code-walking modes. Writes `migration/survey-phase1-<date>.md`.
- **`agents/iconix-migration-semantic.md`** (~8K tokens) — semantic phases: use case drafts (Phase 5), UC packages (Phase 5b), BDD scenarios (Phase 5c), business rules (Phase 5d), test coverage map (Phase 6), handoff report (Phase 7). Both modes.
- **`agents/iconix-migration.md`** — reduced to a thin router (~300 tokens): reads checkpoint and tells the user which sub-agent to invoke next.
- **`docs/iconix/templates/migration-schema-detection-reference.md`** — Phase 5c B1–B5 language-detection tables and Track C signals extracted from the semantic agent to an on-demand reference file. Reduces semantic agent token cost by ~6K tokens; loaded by semantic agent at Phase 5c Step 1 only.

Prompt optimizations implemented simultaneously:
- **Technique 1** (reference file): Phase 5c lookup tables → `migration-schema-detection-reference.md`
- **Technique 2** (XML gates): all pre-phase and completion gates wrapped in `<gate id="..." mandatory="true">` blocks for reliable instruction following across long contexts
- **Techniques 3+4** (prompt caching + extended thinking): documented as `# Future optimization` notes in each sub-agent's frontmatter — implement when Claude Code exposes `cache_control` and `thinking:` frontmatter

Checkpoint protocol: `migration/checkpoint-<date>.json` tracks `phases_completed` with 3-case fallback (valid → proceed, missing → re-run infra, corrupt → report path). Sub-agents verify the checkpoint before doing any work.

**Scalability gate** added to structural Phase 3: caps paths per entry point at 20 when `entry_point_count > 50` to prevent `all_simple_paths` timeout on large systems.

Installer (`iconix-init`, `iconix-init.ps1`) updated to copy the reference file. CI smoke test updated to assert all 4 new/changed files exist. README updated: agent count 13→16.

## [1.0.46] — 2026-05-14

**Feature: CI validator — BR-NNN citation integrity (Traceability check #17).**

`templates/git-integration/generic/validate-traceability.sh` extended with a new check:

- **Check 5 (header) / Check 5 (code):** when `docs/business-rules.md` exists, scan every
  changed ADR file (`adrs/*.md`) for `BR-NNN` patterns and verify each cited ID appears as
  an entry in `docs/business-rules.md`. Emits `BROKEN_BR_CITE: <adr-file> cites <BR-NNN>
  but no matching entry found` to stderr; increments the violation counter (M2 blocker).
  Skipped silently when `docs/business-rules.md` is absent (non-migration projects or
  projects that haven't authored business rules yet).
- In `--full-scan` mode: scans all tracked `adrs/*.md` (not just PR-changed files).
- Also fixes internal numbering mismatch: container-mapping check comment label was
  "Check 3" in the code body but "Check 4" in the header — corrected to "Check 4" throughout.

`agents/iconix-traceability.md` CI counterpart note updated: removed the now-stale
"does not validate BR-NNN citations" caveat; replaced with accurate description of Check 5.

## [1.0.45] — 2026-05-14

**Feature: `iconix-upgrade` — migration awareness for `migration/business-rules.md` → `docs/business-rules.md`.**

Projects that ran the migration agent before v1.0.44 will have `business-rules.md` at the old
`migration/` path; all agents now look for it at `docs/business-rules.md`. The upgrade agent
handles the transition automatically:

- **Step 1b heuristic table**: new row — `docs/business-rules.md` at canonical path → ≥ v1.0.44.
  Absence of the canonical file while `migration/business-rules.md` exists → predates v1.0.44.
- **Layer C auto-copy**: when target ≥ 1.0.44 AND `migration/business-rules.md` exists AND
  `docs/business-rules.md` does not yet exist → copy to canonical path (additive, idempotent;
  original left intact). Logged in the upgrade report.
- **Layer D check #9**: detects stale-path state and flags severity:
  - MEDIUM — old path only (auto-copied by Layer C; verify + delete `migration/` copy).
  - LOW — both paths exist (old is stale; delete `migration/business-rules.md`).
  - Both cases scan `adrs/*.md` for literal `migration/business-rules.md` path citations and
    flag any found as stale citations needing manual update.

## [1.0.44] — 2026-05-14

**Refactor: `docs/business-rules.md` canonical path + greenfield PO authoring + new template.**

Unifies the business rules file location (`docs/business-rules.md`) across all agents and templates,
matching the pattern of `docs/architecture/system-architecture.md` and `docs/nfr-catalog.md`.
Adds PO-authored business rules for greenfield projects and a new scaffold template.

Changes across 11 files:

1. **`templates/business-rules-template.md`** — NEW. Scaffold for both modes:
   - Greenfield (PO-authored): all 7 categories with DEFINED provenance, usage guidance.
   - Migration (Phase 5d extracted): EXTRACTED / INFERRED [VERIFY] provenance reminder.
   - Save path: `docs/business-rules.md`.

2. **`agents/iconix-product-owner.md`** — new `# Business rules authoring` section:
   when to produce `docs/business-rules.md` (greenfield), DEFINED provenance, format
   conventions, incremental update guidance. M1 checklist: `docs/business-rules.md` exists.

3. **Path refactor — `migration/business-rules.md` → `docs/business-rules.md`** in:
   - `agents/iconix-architect.md` — inputs + section title ("migration mode only" removed)
   - `agents/iconix-tester.md` — inputs + section title updated
   - `agents/iconix-traceability.md` — chain diagram, check #17, matrix population guide
   - `agents/iconix-migration.md` — Phase 5d output path
   - `commands/iconix-status.md` — section 2b title and path
   - `templates/handoff-report-template.md` — artifact inventory row
   - `templates/traceability-matrix-template.md` — business rules coverage section
   - `templates/milestone-report-template.md` — ADR health line
   - `templates/iconix.config.yaml` — `business_rules:` comment

4. **Installers** — `iconix-init` (bash) and `iconix-init.ps1` (PowerShell): copy
   `business-rules-template.md` to `docs/iconix/templates/`.

5. **`README.md`** — template listings + project layout updated.

## [1.0.43] — 2026-05-14

**Feature: `/iconix-status` — `[VERIFY]` total row in artifact inventory.**

`commands/iconix-status.md`: new `[VERIFY]` row added to the artifact inventory table,
directly after the BR row. Shows total `[VERIFY]` marker count across all DRAFT files
(UC-DRAFTs, RB-DRAFTs, domain-glossary.md, BDD-DRAFTs, business-rules.md) with the
highest-count file called out in the Orphans/gaps column. Row omitted when no DRAFT files
exist. Read-only — no files written.

## [1.0.42] — 2026-05-14

**Feature: Migration handoff report — auto-count `[VERIFY]` items per artifact group.**

The Confidence summary section of the handoff report now includes a `### [VERIFY] item breakdown`
table showing how many `[VERIFY]` markers exist in each artifact group. Two changes:

1. **`templates/handoff-report-template.md`** — new `### [VERIFY] item breakdown` sub-section
   added inside `## Confidence summary`:
   - Table rows: UC-DRAFTs, RB-DRAFTs, domain glossary, BDD-DRAFTs (omitted when not
     generated), business rules (omitted when Phase 5d skipped), Total.
   - Note: zero `[VERIFY]` on a DRAFT means high agent confidence, not correctness —
     human review still required.
2. **`agents/iconix-migration.md` Phase 7 (graph-assisted)** — Confidence summary bullet
   extended: count literal `[VERIFY]` occurrences across the matching file globs for each
   artifact group; omit rows for skipped groups; sum to Total.

Manual Phase 7 inherits automatically via "Same template and sections as graph-assisted Phase 7."

## [1.0.41] — 2026-05-14

**Feature: `/iconix-status` — BR-NNN stats (migration mode, read-only).**

`commands/iconix-status.md` extended with three additions. No files are written — status
remains a read-only conversation report.

1. **Section 1 — Artifact inventory**: new `BR` row showing EXTRACTED/INFERRED counts and
   broken ADR citation count. Row is omitted when `migration/business-rules.md` is absent.
2. **New section 2b — Business rules coverage** (between NFR coverage and test coverage):
   - Total rules with EXTRACTED / INFERRED / AMBIGUOUS split.
   - ⚠ Investigate categories (Invariant / Authorization / Transition guard / Workflow /
     Calculation) with no covering ADR — lists BR-IDs as ADR candidates for Architect.
   - Broken ADR citations (Traceability check #17): scans `adrs/*.md` Context sections for
     `BR-\d+` patterns and verifies each against `business-rules.md` — lists broken pairs.
   - Unlinked rules: BR-IDs that no UC file references in `## Business rules cross-reference`.
   - Section skipped entirely when `migration/business-rules.md` is absent.
3. **Section 5 — Milestone readiness**: BR-NNN check #17 added to M2 blocker list with
   per-broken-citation detail.

## [1.0.40] — 2026-05-14

**Feature: Traceability matrix — BR-NNN column + Phase 5d rule IDs.**

Closes the gap that BR-NNN IDs were referenced in check #17, trigger scan, and ADR Context
but never actually assigned during Phase 5d extraction. Seven changes across six files:

1. **`agents/iconix-migration.md` Phase 5d Step 3** — rules now carry sequential `BR-NNN`
   IDs (BR-001, BR-002 …) assigned as they are written. ID counter is sequential across all
   categories; IDs are stable across incremental runs. Format change:
   `- <description>` → `- **BR-NNN** | <description>`.
2. **`agents/iconix-migration.md` Phase 5d Step 4** — UC annotation updated:
   - Preconditions use `[BR-NNN]` (exact ID) instead of generic `[BR]`.
   - `## Business rules cross-reference` table gains a `BR-ID` column so Traceability can
     scan UC files and collect which BR-IDs are linked to each UC.
3. **`templates/traceability-matrix-template.md`** — new template. UC-centric table with
   columns: UC-ID, Title, REQ-IDs, RB-ID, SD-IDs, CLS names, TC-IDs, ADR-IDs, NFR-IDs,
   BR-NNN (migration mode only — omit when no business rules). Includes:
   - Population guide (how to derive each column from artifact files)
   - Chain integrity summary table
   - `## Business rules coverage` section: BR-ID → Linked UCs + Linked ADRs; flags unlinked
     rules and uncovered ⚠ Investigate category rules (no ADR).
4. **`agents/iconix-traceability.md`** — two additions:
   - Artifacts section: reference `templates/traceability-matrix-template.md`.
   - New `# Traceability matrix population` section: per-column derivation guide including
     BR-NNN column; business rules coverage population steps (unlinked + uncovered flag).
5. **`templates/milestone-report-template.md`** — two additions:
   - ADR health line: `with no upstream REQ/NFR/UC/BR ref` + `broken BR-NNN citations: <n>`.
   - M2-only check: BR-NNN citation integrity (Traceability check #17) as M2 blocker.
6. **`README.md`** — `traceability-matrix-template.md` added to both template listings.
7. **`iconix-init.ps1` + `iconix-init`** — installer copies new template to
   `docs/iconix/templates/`.

## [1.0.39] — 2026-05-14

**Feature: Traceability agent — BR-NNN citation validation (migration mode).**

The Traceability agent now validates that business rule IDs cited in ADR Context sections
resolve to actual entries in `migration/business-rules.md`. Three additions to
`agents/iconix-traceability.md`:

1. **Traceability chain diagram** — `BR-NNN` added as a second upstream source into
   `ADR-XXX / container-mapping`, alongside `NFR-XXX`:
   ```
   ADR-XXX / container-mapping
       ↑         ↑
    NFR-XXX    BR-NNN  (from migration/business-rules.md — migration mode only)
   ```
2. **Validation check #17 — BR-NNN citation integrity** (M2 check, migration mode only):
   - Scans every `adrs/<PREFIX>-ADR-XXX-*.md` for `BR-\d+` patterns in `## Context`.
   - **Broken citation:** BR-NNN cited but not found in `business-rules.md` →
     **ADR citation drift** (M2 blocker).
   - **Missing source:** BR-NNN cited but `business-rules.md` absent →
     **missing business rules source** (M2 blocker — run Migration Phase 5d first).
   - When `business-rules.md` absent and no ADR cites BR-NNN: skip silently.
3. **CI counterpart note** — clarified that the shell script does NOT validate BR-NNN
   citations (business rule IDs are markdown entries, not standalone artifact files);
   check #17 is the Traceability agent's exclusive responsibility.

## [1.0.38] — 2026-05-14

**Feature: Migration handoff report — Phase 5d business rules trigger scan section.**

The Migration agent's handoff report now includes a pre-computed business rules trigger scan
so the human reviewer can anticipate which rules are likely to require Architect ADRs before
handing off to M2. Three changes:

1. **`templates/handoff-report-template.md`** — new `## Phase 5d — Business rules trigger scan`
   section (inserted between Phase 5c and "Requires human input"):
   - One row per rule: Rule ID, Category, one-line summary, Provenance, ADR signal
     (⚠ Investigate = Invariant/Authorization/Transition guard/Workflow/Calculation;
     ✓ No ADR likely = Precondition/Postcondition).
   - Summary block: total rule count, EXTRACTED vs INFERRED split, ⚠/✓ counts.
   - Omitted when `business_rules.enabled: false` or no rules extracted.
2. **`agents/iconix-migration.md` Phase 5d step e)** — extended handoff report entry:
   after logging UC annotation counts, also populate the trigger scan section using the
   same category classification as the Architect's trigger table. Explicitly does NOT
   perform cross-container analysis — flags that as Architect's job at M2.
3. **`agents/iconix-migration.md` Phase 7 (graph-assisted)** — added `Phase 5d trigger scan`
   bullet to the fill-in list, with the same skip condition.

The manual Phase 7 (code-walking) inherits automatically via "Same template and sections as
graph-assisted Phase 7."

## [1.0.37] — 2026-05-14

**Feature: Architect agent — business rules feed into ADRs (migration mode).**

When `migration/business-rules.md` exists (produced by Migration Phase 5d), the Architect agent
now reads it before drafting ADRs and uses extracted business rules to drive architectural
decisions. Four additions to `agents/iconix-architect.md`:

1. **`# Inputs`** — `migration/business-rules.md` listed as optional input with a one-line
   summary of its purpose.
2. **Decision rule 6** — extended to allow `BR-NNN` citations (business rule IDs from
   `migration/business-rules.md`) in ADR Context sections when no formal REQ-ID exists yet
   in migration mode.
3. **`# Business rules integration (migration mode)`** — new section with three steps:
   - **Step 1 — Trigger scan:** read `business-rules.md` once before any ADR work; evaluate
     each rule against a trigger table (Invariant, Authorization, Transition guard, Workflow,
     Calculation → ADR when cross-container; Precondition/Postcondition → no ADR unless at
     infrastructure layer). Produce a markdown trigger scan table.
   - **Step 2 — Populate ADR Context:** cite BR-NNN, category, provenance (EXTRACTED → no
     [VERIFY]; INFERRED → [VERIFY — confirm enforcement point]). Merge related rules into one
     ADR when they concern the same decision.
   - **Step 3 — Close audit trail:** for non-trigger rules, add a one-line "no ADR — single-
     container enforcement" note in the relevant `container-mapping/*.md` file. Every rule in
     `business-rules.md` must be either ADR-covered or explicitly acknowledged.
4. **PDR readiness check** — new item: when `migration/business-rules.md` exists, every
   cross-container Invariant/Authorization/Transition guard/Workflow/Calculation rule either
   has a covering ADR or an explicit single-container acknowledgment. Unacknowledged rules
   are M2 PDR blockers.

## [1.0.36] — 2026-05-14

**Feature: Analyst agent — domain glossary integration (migration mode).**

When `migration/domain-glossary.md` exists (produced by Migration Phase 5c), the Analyst agent
now reads it before extracting nouns and uses glossary canonical names throughout all M2 work.
Four additions to `agents/iconix-analyst.md`:

1. **Workflow step 2** — pointer: read `migration/domain-glossary.md` first and resolve each
   noun candidate against glossary canonical names before proceeding.
2. **Domain model rule 3** — extended: when `migration/domain-glossary.md` exists, the glossary
   is the authoritative source of canonical entity names; name drift between UC text, domain model,
   and glossary is resolved using the glossary — not by choosing arbitrarily between UC and model.
3. **`# Domain glossary integration (migration mode)`** — new section specifying:
   - Step 0: build a lookup map (canonical name, plural, snake_case table name, aliases).
   - Noun resolution: exact/synonym match → use glossary name; partial match → use glossary name
     + `[VERIFY]` in analysis notes; no match → use noun as-is + `[VERIFY — not in domain glossary]`.
   - Domain model refinement: class names match glossary; `States:` and `Invariants:` copied
     verbatim; renaming a glossary entity requires `[VERIFY]` justification.
   - Drift detection: every discrepancy recorded in `analysis-notes/UC-XXX-notes.md` under
     `## Glossary drift` heading — human reviewer must confirm which side is authoritative.
4. **PDR readiness check** — new item: when `migration/domain-glossary.md` exists, every RB entity
   node and every domain model class either matches a glossary canonical name or is flagged
   `[VERIFY — not in domain glossary]`. Silent deviations are M2 PDR blockers.

Theory audit: Ch2 #4 (domain model as project glossary) already ✅ — change strengthens
existing enforcement without shifting coverage status. Matrix unchanged.

## [1.0.35] — 2026-05-14

**Feature: Tester agent — business rules enrichment from `migration/business-rules.md`.**

When `migration/business-rules.md` exists (produced by Migration Phase 5d), the Tester agent
now uses it to generate more concrete, less generic test cases. Three additions to
`agents/iconix-tester.md`:

1. **`# Inputs` section** — `migration/business-rules.md` listed as optional input with a
   one-line summary of its purpose.
2. **`# Edge case generation rules`** — pointer added: when the file exists, use it to supply
   concrete values for edge-case families 1 (Boundary values ← Invariants), 3 (Authorization
   ← Authorization rules), and 6 (State violations ← Transition guards).
3. **`# Business rules enrichment (migration mode)`** — new section specifying exactly how each
   rule category maps to TC families:
   - **Invariants → boundary/negative TCs:** numeric constraint gives -1/-0.01; required field
     gives absent-field test; format constraint gives invalid-format test; uniqueness gives
     duplicate-submission test.
   - **Transition guards → state violation TCs:** wrong starting state is set up in TC
     Preconditions; operation called; response asserted as rejection.
   - **Calculations → value verification TCs:** assert computed value equals formula for
     known inputs.
   - **Authorization → unauthorized-access TCs:** EXTRACTED rules generate tests without
     [VERIFY]; INFERRED rules add [VERIFY — confirm enforcement point].
   - Provenance labeling in `## Implementation note`: EXTRACTED = confirmed, INFERRED = [VERIFY].
   - Fallback when file absent: generate generic placeholder test data as before.

## [1.0.34] — 2026-05-14

**Docs: process reference matrix — update Last reviewed to v1.0.33 for Phase 5c/5d.**

Prepended new "Last reviewed: v1.0.33" entry to the Summary Coverage Matrix in
`docs/iconix/iconix-process-reference.md`. Covers methodology audit for:

- **Phase 5c extensions (v1.0.24–v1.0.29):** cross-stack detection (7 language families),
  Track C (SoT files + migration DSL), Track B5 (integer status columns), skip logic
  decoupled from `stack.bdd`, config naming fix.
- **Phase 5d (v1.0.32–v1.0.33):** business rule extraction (4 tracks, 7 categories),
  Step 4 UC-DRAFT precondition annotation.

Theory audit results (no status shifts):
- Ch2 #4 (domain model as glossary ✅) — `domain-glossary.md` + `business-rules.md`
  together serve as reverse-engineered domain vocabulary.
- Ch12 #4 (scenario-level acceptance ✅) — Phase 5c/5d feed into Tester's UC coverage.
- Ch13 #9 (link requirements to UCs ✅) — Phase 5d Step 4 strengthens REQ→UC chain.

Coverage table unchanged — all changes are Migration agent kit extensions reinforcing
existing ✅ rows, not closing ❌ gaps in ICONIX book rules.

## [1.0.33] — 2026-05-14

**Feature: Migration Phase 5d Step 4 — auto-annotate UC-DRAFT preconditions from business rules.**

Phase 5d now has a Step 4 that runs after producing `migration/business-rules.md`. For each
`UC-DRAFT-*.md` found, it:

1. Builds an entity + operation set from the UC's actor, main course, alt courses, and the
   associated `RB-DRAFT-XXX.puml` entity nodes. Resolves canonical names via domain glossary.
2. Matches rules from `business-rules.md` by entity name, action verb, and actor/role:
   - **Precondition / Transition guard / Authorization / Workflow** → appended to the UC's
     `## Preconditions` section as `[BR] <description> [VERIFY — Phase 5d]`.
   - **Invariant / Calculation** → cross-reference table only (not Preconditions).
   - **AMBIGUOUS** rules → cross-reference table only with `[VERIFY — multiple candidates]`.
3. Adds `## Business rules cross-reference (Phase 5d)` section at bottom of each UC-DRAFT
   (table of all matched rules by category; removed by reviewer after promotion).
4. Never overwrites or reorders existing UC-DRAFT content; skips duplicate preconditions.
5. Appends annotation summary to handoff report (N UC-DRAFTs annotated, N rules linked,
   UC-DRAFTs with no match listed for investigation).

Manual mode note updated: Step 4 uses class-model.puml and RB-DRAFT entity nodes instead
of graph node IDs for entity matching.

No theory audit required — capability extension within the Migration agent role.

## [1.0.32] — 2026-05-14

**Feature: Migration Phase 5d — business rule extraction.**

New phase added to `agents/iconix-migration.md` (both graph-assisted and manual modes).
Produces `migration/business-rules.md` from four detection tracks:

- **Track S (Schema):** pulls invariants, transition guards, and operation preconditions
  directly from `migration/domain-glossary.md` (Phase 5c output) — no extra scanning.
- **Track V (Validators):** language-aware grep for validator classes and annotations across
  7 stacks (FluentValidation, Bean Validation, Django clean(), Laravel rules(), Rails validates,
  class-validator, go-playground/validator). Labels: `EXTRACTED`.
- **Track D (Domain logic):** guard clauses and throw/raise patterns in domain/service layer
  paths; specification/policy classes (`ISpecification<T>`, `is_satisfied_by`); `Calculate*`
  / `Compute*` methods. Labels: `INFERRED [VERIFY]`.
- **Track T (SQL Triggers):** `RAISERROR`/`THROW` → Invariant/Precondition; `SET` formulas
  → Calculation; audit inserts skipped. Labels: `INFERRED [VERIFY]`.

Seven rule categories: Invariant, Precondition, Postcondition, Transition guard,
Calculation, Authorization, Workflow. Classification heuristics with priority order
(Transition guard > Precondition > Invariant) prevent double-counting.

Manual mode note: Track D uses directory-convention layer detection instead of graph
classification; all Track D/T results are `INFERRED`; adds confidence caveat to file header.

Controlled by new `business_rules.enabled` key in `iconix.config.yaml` (default `true`).
Templates updated: `iconix.config.yaml` (new section), `handoff-report-template.md`
(new artifact row), `README.md` (project layout + flow diagram).

No theory audit required — capability extension within the Migration agent role.

## [1.0.31] — 2026-05-14

**Docs: README — update `features/` directory entry and migration flow diagram for Phase 5c.**

Three changes to `README.md`:

1. **`## Project layout` — Phase 3 `features/` entry:** added note that Migration Phase 5c
   also writes `BDD-DRAFT-*.feature` here (when `stack.bdd: true`); these are promoted to
   TC-XXX by the Tester at M3.

2. **`## Project layout` — Migration section:** updated `domain-glossary.md` description
   to "Phase 5c Steps 1–3 — always generated when any schema source detected, regardless
   of `stack.bdd`"; updated `features/` line to "Phase 5c Steps 4–6 — written when
   `stack.bdd: true` and UC-DRAFTs exist". Removed outdated "when SQL schema found" wording.

3. **Migration flow diagram:** added two new output lines inside the `}` DRAFT block:
   `migration/domain-glossary.md` (Phase 5c Steps 1–3) and `features/BDD-DRAFT-*.feature`
   (Phase 5c Steps 4–6).

No theory audit required — documentation sync.

## [1.0.30] — 2026-05-14

**Feature: Handoff report template — add Phase 5c section and artifact inventory rows.**

`templates/handoff-report-template.md` updated in two places:

1. **Artifact inventory table** — two new rows for Phase 5c outputs:
   - `migration/domain-glossary.md` (Steps 1–3) — shows Generated or Skipped (no schema source).
   - `features/BDD-DRAFT-*.feature` (Steps 4–6) — shows N generated, or which skip reason
     applied (`stack.bdd: false` vs no UC-DRAFTs found).

2. **New `## Phase 5c — BDD scenario synthesis` section** (after "Successfully reverse-engineered"):
   - Summary table: schema source, active tracks, entity count, integer status resolution
     breakdown (High/Medium/Ambiguous/not found), glossary status, BDD-DRAFT status.
   - Two contextual notes: one for when BDD-DRAFTs were generated (review guidance),
     one for when Steps 4–6 were skipped (explains glossary is still usable; how to enable).

No theory audit required — template documentation update.

## [1.0.29] — 2026-05-14

**Fix: Phase 5c — add `stack.bdd` comment to config template; fix `bdd.enabled` naming mismatch.**

Two changes bundled:

1. **`templates/iconix.config.yaml`** — expanded `stack.bdd` with a multi-line comment
   explaining the two-part behaviour: `false` skips only BDD-DRAFT file generation
   (Steps 4–6); schema analysis and domain glossary (Steps 1–3) still run. Also added
   `jasmine` to `bdd_framework` comment.

2. **`agents/iconix-migration.md`** — corrected all four references from `bdd.enabled`
   to `stack.bdd` to match the actual key name in `iconix.config.yaml`. The agent was
   using a non-existent top-level key; the template has always used `stack.bdd`.

No theory audit required — config documentation and naming consistency fix.

## [1.0.28] — 2026-05-14

**Fix: Migration Phase 5c (manual mode) — propagate two-part skip logic and Step 4 gate.**

The manual Phase 5c section previously said "All other rules apply unchanged" without
explicitly calling out the gate added in v1.0.27. Added an explicit bullet to make it
unambiguous that the same two-part logic applies in code-walking mode:
- Steps 1–3 (domain glossary) always run when schema sources are found.
- The Step 4 gate checks `bdd.enabled` and UC-DRAFT existence before generating
  BDD-DRAFT files; log messages and handoff report entries are identical to graph-assisted.

No theory audit required — parity fix between the two execution modes.

## [1.0.27] — 2026-05-14

**Fix: Migration Phase 5c — decouple domain glossary generation from `bdd.enabled` flag.**

Previously, setting `bdd.enabled: false` skipped the entire Phase 5c including the domain
glossary (`migration/domain-glossary.md`). The glossary is independently valuable — Analyst,
Architect, and Tester all use it regardless of BDD output — so skipping it under `bdd.enabled:
false` was incorrect.

Phase 5c now has two independent parts with separate skip conditions:

- **Steps 1–3 (schema analysis → domain glossary):** always run when any SQL, ORM, or
  migration DSL source is detected. Skip only when Tracks A, B, and C all yield zero
  entity definitions.
- **Steps 4–6 (glossary → BDD-DRAFT feature files):** controlled by a new gate inserted
  before Step 4. The gate stops here (logs to handoff report, moves to Phase 6) when:
  - `bdd.enabled: false` or absent in `iconix.config.yaml`, OR
  - No `docs/use-cases/UC-DRAFT-*.md` files found.

The Phase 5c header updated to describe both parts and their independent skip conditions.
The single skip condition at the end of Step 1 updated to scope it to Steps 1–3 only.

No theory audit required — this is a skip-logic correction within the Migration agent.

## [1.0.26] — 2026-05-14

**Feature: Migration Phase 5c — Track B5 (application-layer enum lookup for integer status columns).**

Addresses the gap where SQL `CHECK (col IN (1,2,3,...))` columns carry integer values with
no semantic names. Track B5 searches the full application codebase (outside ORM entity classes)
to find an enum or constant declaration that maps those integers to domain names.

Track B5 runs only when Track A finds an integer CHECK constraint **and** Track B4 finds no
ORM enum type for the same column. Per-language search patterns:
- **C# / .NET** — `enum *<ColName>*` with `= N` members; `const int` blocks inside classes
  named after the column.
- **Java** — standalone `enum *<ColName>*` with constructor values or ordinal order;
  excludes classes already covered by `@Enumerated` in B4.
- **Python** — `IntEnum` / `int`-base subclasses; integer-keyed dict literals; `CHOICES` tuples.
- **PHP** — constants classes (`const PENDING = 1`) named after the column.
- **Ruby** — hash constants (`STATUSES = { pending: 1, ... }`) outside a model's `enum` call.
- **TypeScript / JS** — `enum` with `= N` members; `as const` objects with integer values.
- **Go** — typed int with `const` block using `= N` or `iota`.

Column-to-enum matching uses a three-tier heuristic (exact → suffix → substring) with
corresponding confidence tiers:
- **High (exact match + full coverage)** → `EXTRACTED (B5-enum)`; no `[VERIFY]` on sequence.
- **Medium (fuzzy match or partial coverage)** → `INFERRED (B5-enum)`; `[VERIFY]` on match.
- **Ambiguous (multiple candidates)** → `AMBIGUOUS (B5-enum)`; list all, do not auto-select.
- **Not found** → fall back to view/SP-name SQL heuristic or `State_N` placeholders with
  `[VERIFY — integer status, semantic names unknown]`.

Step 2A-c updated to route integer CHECK constraints through B5 before SQL secondary signals.
Step 2B-g added to apply the B5 result during entity glossary construction.
Four new rows added to the 2C merge table covering all B5 confidence tiers.
Report block updated: `Track B5 (app enum)` line added.
`Source` field in glossary extended with `B5-enum (<file>)` value.

No theory audit required — capability extension within the Migration agent; no ICONIX
methodology surface affected.

## [1.0.25] — 2026-05-14

**Feature: Migration Phase 5c — full cross-stack schema detection (7 language families, Track C).**

Phase 5c Step 1 extended from C# Entity Framework only to all major ORM stacks and adds
Track C (schema/migration DSL files). Detection now covers three tracks:

- **Track A (SQL):** unchanged — `.sqlproj` and `**/*.sql` glob.
- **Track B (ORM model classes):** language-aware detection across 7 families:
  - **C# EF Core** — DbContext/DbSet<T>, entity annotations, IEntityTypeConfiguration<T>
  - **Java JPA/Hibernate** — `@Entity`, `@Table`, `@Enumerated`, `@Embedded`, `@ManyToOne`/`@OneToMany`
  - **Python Django/SQLAlchemy** — `models.py` subclasses, `Column()`, `relationship()`, `__tablename__`
  - **PHP Doctrine/Eloquent** — `@ORM\Entity`, `#[ORM\Entity]`, `$fillable`/`$table`, `belongsTo()`
  - **Ruby ActiveRecord** — `ApplicationRecord` subclasses, `belongs_to`, `has_many`, `enum` declarations
  - **TypeScript TypeORM/Prisma** — `@Entity()`, `@Column()`, `@ManyToOne()`
  - **Go GORM/Ent** — `gorm.Model` embeds, `ent/schema/*.go` struct definitions
  - Four cross-stack signal tables (B1 entity registry, B2 field signals, B3 relationship signals,
    B4 enum/status signals) cover all stacks in a uniform structure.
- **Track C:**
  - **C1 (single source of truth):** `schema.prisma`, `db/schema.rb`, `ent/schema/*.go` — when
    present, supersede Tracks A and B entirely.
  - **C2 (migration DSL fallback):** Alembic `.py`, Liquibase XML/YAML, Laravel `.php`,
    Rails migrations `.rb`, Flyway `.sql`.
  - Priority: `C1 > B > C2 > A`.

Step 2B generalized from EF-specific to cross-stack ORM analysis with language-aware rules for:
entity name normalization, required attribute detection, relationships → Given preconditions,
enum state machines (all ORM stacks: declaration order authoritative — no `[VERIFY]` on
sequence), value objects / embedded types, and skip markers.

Step 2C merge table updated from EF-centric to ORM-centric; C1 conflict rule added (C1 wins
over Track B when both are present).

Three remaining wording fixes:
- Step 2A-c `[VERIFY]` drop condition: "EF enum in Track B" → "ORM enum in Track B or C"
- Phase 5c header: "SQL schema analysis" → "schema analysis (SQL, ORM, or migration DSL)"
- Code-walking manual Phase 5c note: expanded to mention all three tracks (A, B, C).

No theory audit required — capability extension within the Migration agent; no ICONIX
methodology surface affected.

## [1.0.24] — 2026-05-14

**Feature: Migration Phase 5c — extend schema detection to Entity Framework (DbContext, annotations, enums).**

Phase 5c Step 1 now runs two detection tracks in parallel instead of SQL-only:

- **Track A (SQL):** unchanged — `.sqlproj` and `**/*.sql` glob.
- **Track B (EF):** grep for `DbContext` subclasses → read `DbSet<T>` entity list →
  read entity class annotations (`[Required]`, `[ForeignKey]`, `[Owned]`, `[Range]`,
  `[NotMapped]`) and navigation properties → discover `IEntityTypeConfiguration<T>`
  for fluent rules → read enum declarations for status properties → migration fallback
  when no DbContext is found but `Migrations/` folder exists.

Step 2 restructured into three subsections: **2A (SQL analysis)**, **2B (EF analysis)**,
and **2C (merge rules)**. Key improvements from EF:
- Entity class names are already PascalCase singular — no normalization needed.
- Enum-typed status properties give state sequences in declaration order (authoritative
  — no `[VERIFY]` on sequence, only on individual UC transitions).
- `[Owned]` / `.OwnsOne` / `.OwnsMany` → value objects nested under owning entity,
  not listed as standalone domain entities.
- When both tracks present: EF enum wins over SQL `CHECK IN` for state ordering; EF
  property name wins over SQL column name for domain vocabulary.

Skip condition updated: "no SQL or EF schema source detected" (was SQL-only).
Phase 5c report block added at detection start.
Code-walking manual Phase 5c note updated — both tracks are schema-driven in both modes.

No theory audit required — this is a schema-parsing capability extension within the
Migration agent; no ICONIX rules or methodology surface affected.

## [1.0.23] — 2026-05-14

**Feature: Migration agent Phase 5c — BDD Gherkin scenario synthesis from SQL schema.**

Migration agent now parses Microsoft SQL Server Database Project (`.sqlproj`) and
plain `.sql` files to build a domain vocabulary glossary, then uses it alongside
UC-DRAFTs to produce `BDD-DRAFT-XXX-<slug>.feature` files — one per UC-DRAFT.

What Phase 5c does:
- **SQL schema parsing:** reads `CREATE TABLE` statements to extract entity names,
  attributes, FK relationships, `CHECK IN` status enums (state machines), and
  stored procedure verbs from `sp_<Verb><Entity>` naming.
- **Domain glossary:** produces `migration/domain-glossary.md` with normalized entity
  names, states, invariants, and relationships derived from the schema.
- **BDD-DRAFTs:** produces `features/BDD-DRAFT-XXX-<slug>.feature` using the existing
  `feature-template.feature`. Each file has a happy-path Scenario from the UC main
  course, one Scenario per alternate course, and a Scenario Outline for entity state
  transitions when a status column with `CHECK IN` is found.
- Both graph-assisted and code-walking modes support Phase 5c (SQL parsing is
  schema-driven in both modes; only entity-to-UC cross-reference differs).
- Phase is skipped gracefully when no SQL schema source is found; logged in survey
  and handoff report.

Entities not matched in any UC-DRAFT are surfaced as "possible missing use cases"
for PO review — the unmatched-entity signal is a practical byproduct of schema coverage.

Theory audit: Ch12 #4 (scenario-level acceptance testing ✅) — BDD-DRAFTs are
reverse-engineered drafts that feed the Tester's formal TC-XXX generation at M3;
Ch2 #4 (domain model as project glossary ✅) — `migration/domain-glossary.md` is
the reverse-engineered equivalent, built from SQL table definitions rather than PO
modeling. No rule status shifts. Summary Coverage Matrix unchanged.

## [1.0.22] — 2026-05-14

**Fix: PO agent rule 9 — remove duplicated domain model heuristics and VERIFY convention.**

PO rule 9 had a "Critical heuristics (inline so you don't have to bounce to the Analyst
file)" block with 6 entity/attribute rules, followed by a pointer to `iconix-analyst.md
# Domain model rules`. This was deliberate duplication — but it means two agents maintain
overlapping domain model guidance that can drift independently. The `' VERIFY:` annotation
convention was also defined in PO, while the Analyst owns the `' VERIFY:` lifecycle
(resolution at M2, PDR blocker if unresolved).

Both removed. Rule 9 now reads: "Apply the entity/attribute rules in
`iconix-analyst.md # Domain model rules` when classifying nouns. Flag uncertain entities
with `' VERIFY:` for the Analyst to resolve at M2 — do not silently choose when a noun's
classification is ambiguous."

## [1.0.21] — 2026-05-14

**Fix: Traceability agent concurrent-touch Step 6 — remove duplicated Architect resolution options.**

Step 6 "Recommend resolutions" encoded concrete architectural options (service extraction,
class splitting, migration coordination, ADR guidance) that are duplicated from
`iconix-architect.md # Resolving concurrent touches`. Two agents maintaining the same
resolution list is a drift risk. The Traceability agent is an auditor; its job ends at
detection and classification. Resolution belongs to the Architect.

Step 6 replaced with "Escalate active HIGH conflicts to Architect" — flags conflicts for
Architect resolution and defers all options to `iconix-architect.md`.

## [1.0.20] — 2026-05-14

**Fix: remove stale `# Drift detection` section from Developer agent.**

The Developer agent had a `# Drift detection (when re-invoked on existing code)` section
that instructed it to parse source, diff against class-model.puml, and produce
`drift-report.md`. This is the Reviewer's job (Phase 9.2, checks #1–#2). The section was
a pre-v0.9.8 artifact predating the full Phase 9 loop with a dedicated Reviewer mode.
Having both agents run drift detection created two competing sources of truth. Removed.
Developer reads drift findings from `reviews/REVIEW-*.md` as already documented in 9.3.

## [1.0.19] — 2026-05-14

**Tooling: CLAUDE.md — agent prompt discipline rule.**

Added `## Agent prompt discipline` section to `CLAUDE.md` to prevent instructions
meant for one agent from being written into another agent's prompt across sessions.

Three rules:
1. State ownership explicitly before writing — ownership table maps each responsibility
   (drift detection, ID assignment, routing, code generation, test plan, etc.) to its
   owning agent.
2. Grep before writing — check other agent files for the same concept to avoid
   duplication.
3. Cross-agent instructions go in the receiving agent — Agent A may reference that
   Agent B handles X, but must not encode B's logic.

Motivated by a session error where drift-check logic was written into the Developer
agent (Phase 9.1 migration mode) before the user correctly identified it as the
Reviewer's responsibility.

## [1.0.18] — 2026-05-14

**Fix: Developer agent Phase 9.1 — migration-originated UCs must not be re-implemented from scratch.**

When Phase 9 starts on a UC that was reverse-engineered by the migration agent, the code
already exists. The SD was derived FROM that code. Running Phase 9.1 in greenfield mode
would overwrite working code with skeleton implementations.

New mode-detection step in Phase 9.1: check whether the UC is migration-originated
(has a `Source-container:` annotation **or** its ID appears in `migration/survey-*.md`).

Two explicit sub-modes now documented under Phase 9.1:

**Greenfield implement mode** (unchanged behavior):
Write code from SD. Implement all SD messages, alternate courses, unit test bodies.
Commit format: `[UC-XXX] Impl: <summary>`.

**Migration annotate + gap-fill mode** (new):
Code already exists — do NOT rewrite or drift-check it (drift is the Reviewer's job
at 9.2). Instead:
1. Add `Traceability:` comments to existing source and test files.
2. Unit test gap-fill — fill stub bodies where missing; skip files that already have bodies.
3. Do not touch business logic — record anything suspicious in the commit message for
   the Reviewer; do not silently fix it.
Commit format: `[UC-XXX] Migrate: <summary>` (distinguishable in git log from Impl: commits).

## [1.0.17] — 2026-05-14

**Feature: Source-container routing for multi-container UCs through promotion and Phase 9.**

When a UC-DRAFT spans multiple containers (produced by Phase 1b cross-container
correlation), neither the Traceability agent nor the Developer agent had instructions
for handling the multi-value `Source-container:` annotation after promotion.

Two gaps closed:

**Traceability agent (`agents/iconix-traceability.md`):**
- DRAFT promotion Step 4: explicit instruction to preserve `Source-container:` annotation
  as-is during ID replacement — it is the Developer's routing signal for multi-repo
  code placement and must not be removed or modified.
- DRAFT promotion Step 5: after the main summary, check each promoted UC for a
  multi-value `Source-container:` annotation (contains `,`). If any exist, append a
  "Multi-container UCs promoted" section listing the repos and instructing the Developer
  to create feature branches in each before coding.

**Developer agent (`agents/iconix-developer.md`):**
- Phase 9.1 gains a **Pre-step — Multi-repo branch setup**: read `Source-container:` from
  the UC file; if one container or no annotation → standard flow; if multiple containers →
  create `feature/UC-XXX-<slug>` in each container repo before coding, write code under
  each container's resolved source root, commit with the same `[UC-XXX] Impl:` format
  in each repo.

## [1.0.16] — 2026-05-14

**Fix: Phase 6 coverage-gaps.md stale after Phase 1b Case 2 amendment (incremental run).**

When a UC-DRAFT is amended in Phase 1b Case 2 (new container added to an existing DRAFT),
Phase 6 would still evaluate coverage against the old single-container entry point only.
A test covering Frontend → Backend was downgraded to Partial because the Frontend entry
point was not in the original coverage-gaps.md row — leading to false coverage gaps.

New `### Step 0 — Sync amended UC-DRAFTs from Phase 1b` added to both Phase 6 modes
(graph-assisted and code-walking):
- Reads `### Amendment proposals (incremental run)` from the survey
- Builds the full entry-point set for each amended UC-DRAFT (old + new containers)
- Carries this full set into Steps 2–3 so coverage is evaluated across all containers
- If coverage-gaps.md already exists and was not human-edited: updates only the amended
  rows in-place. If it was human-edited: flags MANUAL MERGE REQUIRED in handoff report.

Step 3 updated in both modes: UC-DRAFTs with amendments are evaluated against the full
entry-point set — a test covering only the old container's entry point downgrades to
Partial until the new container's entry point is also covered.

## [1.0.15] — 2026-05-14

**Fix: Phase 1b Case 2 — clarify amendment proposals are human-applied, not auto-written.**

The term "auto-apply" in Phase 1b Step 4 and the survey template implied the migration
agent would directly edit existing DRAFT files. The agent's role is to propose — humans
apply changes by hand (consistent with migration being a read/propose workflow, not a
write-to-existing-artifacts workflow).

Changes in `agents/iconix-migration.md`:
- Step 4 Case 2: replaced "flag it as MANUAL MERGE REQUIRED instead of auto-applying"
  with explicit wording that the agent *proposes* changes and a human applies them; the
  MANUAL MERGE REQUIRED flag now explains it means conflicts may exist with human edits.
- Step 5 survey template: replaced `Status: READY — auto-apply` with
  `Status: READY — apply changes above by hand (DRAFT unmodified; no conflicts expected)`;
  the MANUAL MERGE REQUIRED variant updated to say "reconcile conflicts before applying".

## [1.0.14] — 2026-05-14

**Feature: Incremental migration — Phase 1b handles containers added across separate runs.**

When a project migrates Container 1 in one run and adds Container 2 in a later run,
Phase 1b previously had no mechanism to correlate the new container's boundaries against
the old one's existing UC-DRAFTs or promoted IDs. A cross-container match would either
silently create a duplicate UC-DRAFT or be missed entirely.

Three new cases in Phase 1b cover all incremental scenarios:

- **Case 1 (all current-run):** both containers are in the current run → standard unified
  UC-DRAFT, same as before.
- **Case 2 (mix of current-run + previous-run with existing DRAFT):** propose an
  **amendment** to the existing UC-DRAFT — append the new container's entry point to
  `Source-container:`, extend the RB-DRAFT and SD-DRAFT. If the DRAFT was human-edited
  since the last run, flag as MANUAL MERGE REQUIRED instead of auto-applying.
- **Case 3 (previous-run UC already promoted to permanent ID):** do NOT modify the
  promoted UC directly — flag as a **change flow candidate** and recommend
  `/iconix-impact <UC-ID>` to trigger a REQ change flow for the extended scope.

Concrete changes in `agents/iconix-migration.md`:
- **Phase 1b Step 0** (new): detect incremental run, load previous surveys, identify
  previous-run containers with their boundary data, existing DRAFTs, and promoted IDs.
  Build two sets: current-run containers and previous-run containers.
- **Phase 1b Step 1**: updated header — collects from both current-run (Phase 1 survey)
  and previous-run (Step 0 loaded data) containers.
- **Phase 1b Step 3**: updated — for each matched pair, record which run each container
  belongs to (current-run / previous-run); this classification feeds Step 4.
- **Phase 1b Step 4**: replaced single-case logic with explicit three-case dispatch
  (Case 1 / Case 2 / Case 3) as described above.
- **Phase 1b Step 5**: survey template updated — Mode line shows current-run vs
  previous-run count; Matched pairs table gains a "Run" column; Proposed UC groupings
  labelled with their Case number; two new conditional sections added:
  `### Amendment proposals (incremental run)` and `### Change flow candidates (promoted UCs)`.

## [1.0.13] — 2026-05-14

**Feature: Phase 1b — cross-container boundary correlation in migration agent.**

In multi-repo mode the migration agent surveyed each container independently and produced
separate UC-DRAFTs per entry point. A user action that flows Frontend → Backend API →
Database would become three separate drafts instead of one unified UC — a significant gap
for multi-container architectures.

New `# Phase 1b — Cross-container boundary correlation` section (runs in both modes,
skipped in single-repo). After Phase 1 completes for all containers, Phase 1b:

1. Collects inbound boundaries per container (HTTP routes, gRPC methods, message topics)
2. Collects outbound cross-container calls per container (HTTP client calls, gRPC stubs,
   message publishes) — graph-assisted uses graph outbound nodes; code-walking greps for
   HTTP client patterns
3. Matches inbound ↔ outbound pairs with confidence levels (HIGH = exact URL+method/topic,
   MEDIUM = pattern/prefix match); records unmatched boundaries (external actors/services)
4. Proposes UC groupings: HIGH-confidence → recommend merge to one UC-DRAFT; MEDIUM →
   flag `[VERIFY]` for human review
5. Appends `## Cross-container boundary correlation` section to `migration/survey-<date>.md`
   with matched pairs table, unmatched lists, and proposed grouping narrative

Phase 5 (both modes) updated: check Phase 1b results before drafting — entry points in
the same group produce one UC-DRAFT covering the full multi-container flow with
`Source-container:` annotation listing all containers.

Phase 7 handoff report updated: new "Cross-container UC groupings" section listing all
proposed groups; human must confirm before `/iconix-promote`.

## [1.0.12] — 2026-05-13

**Feature: Tester and Reviewer dependency_sources awareness.**

Completes the `dependency_sources` propagation across the full agent pipeline. Two
remaining agents had gaps:

- **Tester** had no way to determine isolation strategy for plugin/contract dependencies
  when writing integration tests and test plans — the test plan would be silent on whether
  to load the real plugin or use a test double.
- **Reviewer** would produce false-positive `[TRACEABILITY]` findings when code extended
  or implemented a type from `dependency_sources` (a legitimate external type not in the
  container's own source root), because check #2 had no external-type lookup step.

Changes:
- **`agents/iconix-tester.md`**: New `# Dependency isolation strategy` section — before
  writing the test plan, read `dependency_sources:` (with `containers:` scope filter);
  `role: contracts` → mock in unit tests, decide real vs. test double in integration;
  `role: plugin` → mock contract in unit tests, document real-vs-stub decision in test
  plan. Pre-CDR test plan gains point 6: dependency isolation strategy (required when
  any `contracts`/`plugin` entries are in scope).
- **`agents/iconix-reviewer.md`**: Check #2 (Code ↔ Class Model) gains an external type
  lookup step — when a class inherits from a type not in the source root or class model,
  look it up in `dependency_sources:` before flagging. Found → `[INFO]` advisory (not
  blocking); not found → `[TRACEABILITY]` as before.

## [1.0.11] — 2026-05-13

**Fix: clarify unit test ownership — Developer writes unit tests, not Tester.**

The kit had an internal inconsistency: the process reference matrix (Ch10 #3) stated
"Developer is expected to write unit tests," but the Tester agent's Phase 9.1 translated
ALL TC types (including unit) into runnable test code. The Developer agent only emitted
empty stubs. This contradicted ICONIX Ch10 #3: "Focus on unit testing *while* implementing
code" — an activity that belongs to the Developer.

- **`agents/iconix-developer.md`**: Phase 9.1 now includes an explicit step to implement
  unit test bodies from unit-level TC specifications (`## Type: unit`) alongside the
  corresponding production method (arrange/act/assert from TC Steps/Expected results).
  Traceability comment added to unit test files. Signal-ready condition updated to require
  unit test bodies complete.
- **`agents/iconix-tester.md`**: Phase 9.1 scoped to integration, system, and acceptance
  TCs only. Unit TCs are Developer's responsibility. Tester verifies unit test coverage
  by checking `test-matrix.md` for test file paths before signaling ready.
- **`docs/iconix/iconix-process-reference.md`**: Ch10 #3 row updated to accurately
  describe the split: Developer writes unit test bodies at Phase 9.1; Tester writes
  integration/system/acceptance code in parallel.

## [1.0.10] — 2026-05-13

**Feature: Architect agent dependency source awareness.**

The Architect produces `package-map.md` and container-mapping files that define
architectural boundaries. Without knowledge of `dependency_sources:`, the "Allowed
dependencies" column in the package map would silently omit in-house packages and plugin
contracts — making the map incomplete and causing false drift findings downstream.

- **`agents/iconix-architect.md`**: New `# Dependency source awareness` section. Before
  producing `package-map.md` and container-mapping files, the Architect reads
  `dependency_sources:` from `iconix.config.yaml` (applying the same `containers:` scope
  filter as Migration and Developer agents) and takes role-specific actions: `domain /
  infrastructure / utility` entries are added to "Allowed dependencies"; `contracts /
  plugin` entries additionally trigger an ADR for the plugin loading strategy and require
  the plugin's outbound boundaries in `integration-surface.md`. New PDR readiness
  checklist item enforces this.

## [1.0.9] — 2026-05-13

**Feature: Developer agent dependency source lookup.**

The Developer agent implements code based on sequence diagrams and class models. When a
class extends or implements a type from an in-house package or plugin contract, the agent
had no way to locate the type's source — leading to invented APIs or `[VERIFY]` gaps in
generated code.

- **`agents/iconix-developer.md`**: New `# Dependency source lookup` section. When a type
  is not found in the container's own source root, the Developer now looks it up in
  `dependency_sources:` from `iconix.config.yaml`, applying the same `containers:` scope
  filter as the Migration agent. `role: contracts` entries guide plugin implementation;
  `role: domain/infrastructure/utility` entries expose base class APIs. Types still not
  found are annotated `// [VERIFY — type source unknown]` rather than silently invented.

## [1.0.8] — 2026-05-13

**Feature: per-container scoping for `dependency_sources`.**

`dependency_sources` entries are defined at the project level but some sources — plugins
especially — are only loaded by one specific container. Without scoping, the migration
agent would include every plugin in every container's known-types registry, polluting
registries with types that can never appear in that container's code.

New optional `containers:` list field on each `dependency_sources` entry. If present,
the entry is only included in the known-types registry when the migration agent is
processing a container whose name is in the list. If absent, the entry applies to all
containers (existing behaviour unchanged).

- **`agents/iconix-migration.md`**: Sub-step B now starts by determining the current
  container name (multi-repo: the container being processed; single-repo: first
  container in config). Each `dependency_sources` entry is checked for `containers:`
  before loading — entries not in scope are skipped and shown in the Sub-step C registry
  report as `skipped (containers: [...] — current: <name>)`.
- **`templates/iconix.config.yaml`**: Added `containers:` field documentation to the
  `dependency_sources` section with examples and the "omit = all containers" rule.

## [1.0.7] — 2026-05-13

**Feature: dependency source reconnaissance for the migration agent.**

When the migration agent walks a container's code it encounters types defined in
dependencies — not in the container's own source root. Without access to those type
definitions the agent falls back to name-based heuristics and emits `[VERIFY]` on
every unrecognised base class or interface. Two categories of dependency were unhandled:

1. **In-house packages** (NuGet, npm, pip, Maven, etc.) whose source is cloned on the
   same machine but whose manifest entry is a package name + version — not a resolvable
   path the agent can follow automatically.
2. **Plugins** loaded at runtime via reflection / MEF / plugin-framework — the main
   container has no compile-time reference to the plugin implementation at all.

- **`agents/iconix-migration.md`**: New `# Step 0b — Dependency source reconnaissance`
  section, running in both graph-assisted and code-walking modes before Phase 0/1.
  Three sub-steps: (A) auto-detect project references from manifest (`<ProjectReference>`,
  `workspaces`, `go.work`, etc.) and classify their public types; (B) read explicit
  `dependency_sources:` entries from config for packages and plugins the manifest cannot
  describe; (C) report the known-types registry before proceeding. Types not in the
  registry fall back to name-based heuristics + `[VERIFY]`, unchanged from before.
- **`templates/iconix.config.yaml`**: New `dependency_sources:` section (commented out,
  with `role:` enum documented: `domain | infrastructure | utility | contracts | plugin`).
  Distinction between project-reference (auto-detected, no entry needed) and
  package/plugin (must be declared) is explained in the comment block.
- **`agents/iconix-upgrade.md`**: Layer D check #8 — verifies each `dependency_sources`
  `path:` exists on disk; flags missing role as informational.

CLAUDE.md audit: tooling-only (migration agent reconnaissance step + config extension);
no ICONIX methodology rules changed; theory audit not required; state machine unchanged;
README and project layout unchanged.

## [1.0.6] — 2026-05-13

**Gap fix: Phase 9 loop metrics — phase9-cycles/ was not read by the metrics agent.**

`phase9-cycles/` existed since v0.9.8 and the orchestrator writes `UC-XXX-cycle.md` files
there, but the metrics agent, JSON schema, glossary, and snapshot template had zero phase9
content. Per-iteration statistics (`iterations_per_uc`, `cap_hit_pct`,
`first_pass_approve_pct`) could never be computed.

- **`agents/iconix-metrics.md`**: Added `phase9-cycles/` to Inputs list. Added new
  `## Step 3b — Phase 9 loop health` computation step with rules for `uc_total`,
  `uc_active`, `uc_done`, `iterations_per_uc` (from `Iterations used: N` in Exit section),
  `cap_hit_count`, `cap_hit_pct`, `first_pass_approve_pct`. Active UCs in loop > 21 days
  emit as `stale_branch` blockers.
- **`templates/metrics-schema.json`**: Added optional top-level `phase9` object with 7
  fields matching the new step. `null` when `phase9.enabled: false`.
- **`docs/iconix/metrics-glossary.md`**: Added new section 3.5 defining all 7 phase9
  fields with healthy ranges (median ≤ 2 iterations; cap hit < 10%;
  first-pass approve > 70%).
- **`templates/metrics-snapshot-template.md`**: Added `## 3.5. Phase 9 loop health`
  section with interpretation guidance; added `phase9-cycles/` to the Traceability
  source-artifacts list.

CLAUDE.md audit: tooling-only (metrics extension — no ICONIX methodology rules changed);
theory audit not required; state machine unchanged; README and project layout unchanged
(phase9-cycles/ folder already listed, introduced in v0.9.8).

## [1.0.5] — 2026-05-13

**Gap fix: validate-traceability.sh --full-scan mode for metrics snapshots.**

`trace_comment_coverage_pct` in the metrics agent called `validate-traceability.sh main HEAD~0`
intending a full scan, but the script only operates on `git diff` output. When `HEAD~0 == main`
the diff is empty and the script exits with "skipping" — producing no parseable output. The
`trace_comment_coverage_pct` field could never be computed.

- **`templates/git-integration/generic/validate-traceability.sh`**: Added `--full-scan` flag.
  When set, uses `git ls-files -- 'src/**' 'tests/**'` instead of `git diff` to enumerate files.
  Check 3 (container-mapping Effective stack) is skipped in full-scan mode — it is PR-specific.
  Output format (`"OK (N files checked)"` / `"MISSING_TRACE: ..."`) is unchanged so the metrics
  agent can parse it without modification. Updated header comment to document the flag.
- **`agents/iconix-metrics.md`**: `trace_comment_coverage_pct` updated to call
  `validate-traceability.sh --full-scan` instead of `main HEAD~0`. Note clarified: the script
  validates source-file → artifact ID links (not REQ → UC → RB artifact chains, which is the
  orphan report's job).

CLAUDE.md audit: tooling-only (CI script + metrics agent invocation); no ICONIX methodology
rules changed; theory audit not required; state machine unchanged; README and project layout
unchanged.

## [1.0.4] — 2026-05-12

**Gap fix: upgrade agent heuristic detection gap for v1.0.1 and v1.0.2.**

The version-detection heuristic table in `iconix-upgrade.md` jumped from v1.0.0 directly to
v1.0.3 with no entries for v1.0.1 or v1.0.2. A project at v1.0.1 would be mis-detected as
v1.0.0, producing an inaccurate "upgrading from v1.0.0" report and potentially missing
version-specific Layer D checks.

- **`agents/iconix-upgrade.md`** Step 1b — Pass 1 heuristic table: added v1.0.1 detection
  signal (`graph_path:` field present on any container in `iconix.config.yaml`).
- **`agents/iconix-upgrade.md`** Step 1b — added v1.0.2 note after the Pass 1 table: v1.0.2
  is pure agent-prompt fixes with no structural signals; cannot be auto-detected; users on
  v1.0.2 should use `--from 1.0.2` to override.
- **`agents/iconix-upgrade.md`** Layer D step 6: added `graph_path:` broken-path check —
  if a container defines `graph_path:` but the file doesn't exist locally, flag it; the
  Migration agent will silently fall back to code-walking without this check.

CLAUDE.md audit: tooling-only (upgrade agent heuristic and detection check); no ICONIX
methodology rules changed; theory audit not required; state machine unchanged; README
and project layout unchanged.

## [1.0.3] — 2026-05-12

**Backlog #1 — Branch protection config generation: enforce ICONIX CI gates on merge.**

Prior to this version, the ICONIX CI gate (`iconix-validate.yml` / `azure-pipelines-iconix-validate.yml`)
was advisory — it ran on every PR but nothing prevented a user from merging a failing PR. This
change closes that gap by shipping one-time branch protection setup scripts that make the CI
check required.

- **`templates/git-integration/github/scripts/setup-branch-protection.sh`** (new): uses
  `gh api` to enable GitHub branch protection on `main` (and `develop` for gitflow). Sets
  "Traceability gate" as a required status check; requires ≥1 PR review; blocks force pushes
  and direct pushes. Auto-detects gitflow from `iconix.config.yaml`. Supports `--dry-run`,
  `--min-reviewers`, `--enforce-admins`, `--also-branch`, `--check-name` flags. Idempotent.
- **`templates/git-integration/azure-devops/scripts/setup-branch-policies.sh`** (new): uses
  `az repos policy` to create a build validation policy (ICONIX pipeline required) and an
  approver-count policy on `main`. Auto-discovers pipeline ID by name. Supports `--dry-run`,
  `--min-reviewers`, `--branch`, `--pipeline-name` flags.
- **`agents/iconix-git.md`**: New `## 7. Branch protection setup` section — pre-flight check
  to detect if protection is already configured; step-by-step run instructions for both
  providers; post-setup verification pointers.
- **`iconix-init`** (bash) + **`iconix-init.ps1`** (PowerShell): both installers now copy the
  matching setup script to `.ci/scripts/` when `git.provider` is `github` or `azure-devops`;
  print a reminder to run it once to activate enforcement.
- **`agents/iconix-upgrade.md`**: Layer A gains `.ci/scripts/` folder (v1.0.3+, provider-
  conditional); Layer E gains setup-script copy for both providers; version-detection heuristic
  table gains v1.0.3 entry.
- **`templates/git-integration/README.md`**: Layout diagram updated with `scripts/` subtrees;
  new `## Enforcing CI gates` section with quickstart commands.
- **`README.md`**: Project layout updated (`.ci/scripts/` with both script names); provider
  table updated; new "Enforcing the gate" block in the git integration section.

CLAUDE.md audit: tooling-only (new shell scripts + installer copy logic); no ICONIX methodology
rules changed; theory audit not required; state machine unchanged; README and project layout
updated in this same change.

## [1.0.2] — 2026-05-12

**Gap fix: remaining multi-repo gaps in reviewer, metrics, trace-check, and upgrade agents.**

Comprehensive scan of all agents and commands for backlog item #8 residual gaps. Five gaps
found and fixed; four agents (Architect, Docs, Analyst, PO) confirmed clean.

- **`agents/iconix-reviewer.md`**: Check #4 updated — "source files under `src/`" replaced with
  "resolved source root" covering both single-repo (`src/<container-name>/`) and multi-repo
  (`<path>/<src_dir>/` per container with `path:`). Check #7 restructured into single-repo mode
  (first-path-segment-after-`src/` logic) and multi-repo mode (identify container by matching
  resolved source/test root prefix). Stack-alignment checks consolidated as a shared section
  applying to both modes.
- **`commands/iconix-trace-check.md`**: Step 4 now detects execution context before running the
  shell script: meta-project context (has `iconix.config.yaml` → no env var needed); service-repo
  context (no `iconix.config.yaml` → reads `ICONIX_CONFIG_PATH` from environment, prompts if
  unset). Mirrors the `ARTIFACT_ROOT` logic implemented in Phase D.
- **`agents/iconix-metrics.md`**: Multi-repo awareness added in three places: (1) `bugs.*` branch
  count now unions `git -C <path> branch -r` results from all external repos; (2) `trace_comment_coverage_pct`
  clarified — script covers meta-project artifact links only, not service-repo source-file
  `Traceability:` comments (those checked in each service repo's own CI); (3) Step 6 stale-branch
  detection now checks `feature/UC-*` across all external repos with `git -C <path> branch -r`.
- **`agents/iconix-upgrade.md`**: Layer D step 3 (source-file spot-check) now includes
  multi-repo containers: scans `<path>/<src_dir>/` when `path:` is defined, verifying the path
  exists locally before reading; skips with broken-path finding if unavailable.

CLAUDE.md audit: tooling-only (path resolution and context detection); no ICONIX methodology
rules changed; theory audit not required; README agent count, command list, and project layout
unchanged; state machine unchanged.

## [1.0.1] — 2026-05-12

**Gap fix: multi-repo + graph-assisted mode — per-container Graphify graph support.**

Discovered during post-v1.0.0 review of backlog item #8. The migration agent previously
assumed a single unified Graphify graph for all containers (global `knowledge_graph.graph_path`).
In practice, each container repo may have its own graph. Three scenarios now handled:

- Container has `graph_path:` → uses its own graph (Phase 0 checks it independently)
- Container has no `graph_path:`, global graph is set → uses global graph, queries scoped to that container's source root (existing behaviour, now explicit)
- Container has no graph at all → falls back to code-walking for that container only (new)

Mixed-mode (some containers graph-assisted, others code-walking) is supported within a single
migration run; results are merged into one unified survey.

- **`templates/iconix.config.yaml`**: Added optional `graph_path:` per container (commented out) with explanation of the three-way fallback.
- **`agents/iconix-migration.md`**: New `# Per-container graph resolution` section (4 steps: detect, report, Phase 0 per-container check, mixed-mode execution); Phase 0 updated to delegate multi-repo resolution to the new section; Phase 1 multi-repo pre-step updated to reference per-container graph resolution and merge mixed-mode results.

CLAUDE.md audit: tooling-only (graph detection infrastructure); no ICONIX rules changed; theory audit not required; state machine and README project layout unaffected.

## [1.0.0] — 2026-05-12

**Multi-repo / microservices support — final release.**

Completes the four-phase arc started in alpha.1. One iconix meta-project can now orchestrate
multiple microservice repos cloned locally: config, migration, git sync, PRs, code generation,
testing, and CI traceability all understand the multi-repo topology.

### Phase D — Developer/Tester write to the correct repo; cross-repo CI

- **`agents/iconix-developer.md`**: New `# Container path resolution` section defines the
  source/test root lookup table per container (has `path:` + `src_dir:` → `<path>/<src_dir>/`;
  single-repo fallback → `./src/<container-name>/`). `# Stack resolution` step 3 updated.
  `# Artifacts you produce` now references resolved paths instead of `src/<lang>/`.
  `# Code skeleton paths` section updated: "resolved source root" instead of `src/`; examples
  labelled "single-repo layout"; tests rule updated to `<resolved-test-root>/<package>.Tests/`.
- **`agents/iconix-tester.md`**: New `# Container path resolution` section adds a two-level
  distribution table — unit/integration tests go to `<path>/<test_dir>/` in the container repo;
  system tests go to `meta.system_tests_dir`; acceptance BDD step definitions go to
  `meta.acceptance_tests_dir`; `.feature` files always stay in the meta-project.
  `# Stack resolution` step 4 updated. Phase 9 test implementation step 1 updated to use
  resolved test root and note system/acceptance test destinations.
- **`templates/git-integration/generic/validate-traceability.sh`**: New `ARTIFACT_ROOT`
  variable from `ICONIX_CONFIG_PATH` env var (default `.`). Config reading and artifact folder
  lookups (`use-cases/`, `robustness/`, `sequence/`, etc.) now use `${ARTIFACT_ROOT}/...`.
  Usage comment updated with service-repo CI example.
- **`agents/iconix-traceability.md`**: `# CI counterpart` section updated with multi-repo CI
  guidance — `ICONIX_CONFIG_PATH` usage, worked GitHub Actions example, and clarification
  that the source diff is still computed in the service repo's git history.

### Summary — all four phases

| Phase | Ships | What it adds |
|---|---|---|
| A | alpha.1 | Per-container `path:` / `src_dir:` / `test_dir:` / `git_url:` / `reviewers:` in config; `meta:` system/acceptance test dirs; upgrade detection |
| B | alpha.1 | Migration agent walks each container's source root independently; `Source-container:` annotation on DRAFTs |
| C | alpha.3 | Git agent multi-repo sync (plan → confirm → branch all repos); multi-repo Implementation PRs; Orchestrator Phase entry routing |
| D | 1.0.0 | Developer/Tester resolve `<path>/<src_dir|test_dir>/` per container; test distribution (unit → container repo, system/acceptance → meta-project); `ICONIX_CONFIG_PATH` for service-repo CI |

## [1.0.0-alpha.3] — 2026-05-12

**Multi-repo support — Phase C: git sync, multi-repo PRs, Orchestrator branch protocol.**

Completes the git-surface side of multi-repo support. Agents now create feature branches
across all repos simultaneously, open one PR per external repo at Implementation phase,
and detect in-flight UCs from external repo branches as well as the meta-project.

### Phase C — Git multi-repo sync + PR support

- **`agents/iconix-git.md`**:
  - `# Before you do anything` now also reads `architecture.containers` to detect multi-repo mode.
  - New `# Multi-repo sync` section: deduplicates containers by unique `path:` value, resolves
    `base_branch:` per repo (container override > global `git.default_branch`), shows a
    per-repo sync plan and **waits for user confirmation** before touching any repo,
    then runs `fetch → checkout base → pull → checkout -b` (or `checkout` for existing
    branches) in each repo. Halts the entire sync if any repo is dirty or fails.
    Single-repo fallback applies when no container has `path:` defined.
  - `## 3. Pull request opening` — new `### Multi-repo Implementation PRs` sub-section:
    for Implementation-phase diffs in multi-repo mode, opens one PR per unique `path:`
    (for containers touched by the UC) plus one meta-project PR; PR body lists all
    containers at that path; reviewers are the union of all container `reviewers:` lists.
    M1/M2/M3 phases always use the single meta-project PR path.
  - `## 6. In-flight UC detection` — new step 1b: in multi-repo mode, also checks
    `git -C <path> branch -r --list 'origin/feature/UC-*'` for each external repo;
    deduplicates by UC-ID before returning the list to Traceability.
- **`commands/iconix-pr.md`**: Step 4 updated — when phase is Implementation and any
  container has `path:`, delegates to the Git agent's multi-repo PR algorithm.
  M1/M2/M3 are unchanged (single meta-project PR).
- **`agents/iconix-orchestrator.md`**: `# Phase entry — branch creation protocol` step 3
  updated — single-repo mode uses `git checkout -b` as before; multi-repo mode calls
  the Git agent's `# Multi-repo sync` algorithm (shows plan, waits for confirmation,
  syncs all repos atomically).
- **`templates/git-integration/branch-conventions.md`**: New `## Multi-repo mode` section
  documents that the same branch name is created in all repos simultaneously, that
  containers sharing a `path:` are one git repo, and that `base_branch:` can differ
  per repo.

## [1.0.0-alpha.2] — 2026-05-12

**Mixed-topology clarification: multiple containers sharing one git repo.**

Discovered via design Q&A: when multiple containers live in the same git repo
(e.g., Backend + WebAPI both in `../shared-platform/`), the Phase A config and
Phase B migration agent needed explicit support for nested `src_dir:` paths and
a "deduplicate by `path:`" rule for Phase C git operations.

- **`templates/iconix.config.yaml`**: Expanded multi-repo comment block — `src_dir:`
  now documented as accepting nested paths (e.g., `"src/Backend"`). Added inline
  mixed-topology example showing two containers sharing the same `path:` with
  different `src_dir:` subdirectories. Added note that same `path:` = same git repo.
- **`agents/iconix-migration.md`**: Updated container source root resolution table to
  document nested `src_dir:` support with a concrete example. Disk-existence check
  now deduplicates by unique `path:` value before verifying.
- **Memory (backlog #8)**: Phase A updated with mixed-topology rule. Phase C updated
  with "deduplicate by `path:`" rule — one branch and one PR per unique `path:` value,
  not per container.

## [1.0.0-alpha.1] — 2026-05-12

**Multi-repo / microservices support — Phase A (config) + Phase B (migration).**

Enables one iconix meta-project to orchestrate multiple microservice repos cloned
locally. Phases C (git multi-repo sync + Phase 9 write-to-correct-repo) and D
(traceability cross-repo CI) are deferred to v1.0.0 final.

### Phase A — Config foundation

- **`templates/iconix.config.yaml`**: Added optional multi-repo fields per container:
  `path:` (local clone path), `git_url:` (for PR creation), `src_dir:` (default `"src"`),
  `test_dir:` (default `"tests"`), `reviewers:`. All fields are commented-out by default —
  single-repo projects are unaffected. Added commented-out `meta:` section for
  `system_tests_dir` / `acceptance_tests_dir` (cross-container tests in the meta-project).
- **`agents/iconix-upgrade.md`**: v1.0.0 heuristic detection (presence of `meta:` section
  or any container `path:` field). Layer B auto-adds commented-out `meta:` section.
  Layer D detects containers with `path:` but no `git_url:` (oversight that breaks
  `/iconix-pr`), missing/broken local path, and absent `src_dir:` for non-standard layouts.

### Phase B — Migration agent multi-repo

- **`agents/iconix-migration.md`**: New `# Multi-repo source resolution` section defines:
  container source root resolution table (`path:` + `src_dir:` → resolved path, with
  single-repo fallback), multi-repo detection and announcement format, disk-existence
  check per container path, unified survey **Containers surveyed** table, and
  `Source-container:` annotation required on every DRAFT artifact in multi-repo mode
  (enables Phase C to write code back to the correct repo).
  Phase 1 (both graph-assisted and code-walking) modified with a **Multi-repo pre-step**
  that scopes the walk to each container's resolved source root.
  Phase 6 (test coverage) modified to search each container's resolved test root.

### What's NOT in this alpha (deferred to v1.0.0 final)

- Phase C: `iconix-git` multi-repo branch sync; Developer/Tester writing to `<path>/src/`
- Phase D: `ICONIX_CONFIG_PATH` env var for service-repo CI; `traceability.mode: cross-repo`

**Versioning note:** v1.0.0 marks the first breaking change to `iconix.config.yaml` schema
(new container fields + `meta:` section). Single-repo projects are fully backward compatible —
no config changes required.

## [0.9.48] — 2026-05-12

**Add `feature-template.feature` — Gherkin BDD feature file scaffold.**

The Tester agent already produced `features/UC-XXX.feature` files for acceptance-bdd TCs,
but there was no template to scaffold from. This adds it.

- **`templates/feature-template.feature`**: Gherkin scaffold covering the mandatory header
  comment block (Traceability, Generated-by, TCs covered), Feature user-story block, optional
  Background, one Scenario per UC course with TC-ID comment, and a commented-out Scenario
  Outline pattern for data-driven alternates.
- **`agents/iconix-tester.md`**: updated artifact line and added `# Feature file template`
  section with authoring rules (one file per UC, filename convention, TC-ID comments,
  Background usage, Scenario Outline guidance, step definition location, grep-able
  Traceability header).
- **`README.md`**: `feature-template.feature` added to both the `## What's inside` and
  `## Project layout` template lists.

ICONIX theory: kit extension. The canonical text does not cover BDD/Gherkin; this scaffolds
the existing acceptance-testing obligation (Ch12 #4, already ✅). No matrix update required.

## [0.9.47] — 2026-05-12

**Kit extension: legacy-code integration guidance in greenfield agents.**

Discovered via Q&A: when a new feature uses existing legacy code that violates ICONIX
rules, the three greenfield agents (Analyst, Architect, Developer) had no guidance on
how to handle it. The "Outbound Boundary as Adapter" pattern existed only in
`iconix-migration.md`; the greenfield pipeline was silent.

Three targeted additions:

- **`agents/iconix-analyst.md`**: Boundary stereotype split into Inbound / Outbound
  sub-categories. New `# Outbound Boundary — legacy code and external systems` section:
  draw an Outbound Boundary node for the adapter wrapping the legacy class; name after
  responsibility (not the legacy class); mark `[LEGACY]` in a PlantUML note; let the
  Architect raise the ADR. Connection rules unchanged — Outbound Boundary still connects
  only via Controller. PDR checklist updated to distinguish inbound from outbound.

- **`agents/iconix-architect.md`**: Decision rule 7 added — when a new UC touches a
  legacy class that violates ICONIX rules, treat it as an external dependency; raise an
  ADR citing the UC-ID, the violation, and the technical debt; map the adapter to the
  Infrastructure container. Legacy class does not appear in container-mapping.

- **`agents/iconix-developer.md`**: Rule 9 added — when an RB Outbound Boundary wraps
  a legacy class, the SD lifeline is the Adapter interface (e.g. `IOrderReadRepository`),
  not the legacy class; the legacy class appears only in a `note over` block.

- **`docs/iconix/iconix-process-reference.md`**: Last-reviewed line bumped to v0.9.24.
  No matrix status shifts — these are clarifications/extensions within existing ✅
  coverage (Ch5 #7, Ch7 #5, Ch8 Four Essential Steps #2).

The terminology (Inbound / Outbound Boundary) now matches `iconix-migration.md`'s Phase 4
classification, making the kit internally consistent across migration and greenfield flows.

Changes:
- **`agents/iconix-analyst.md`**: Boundary stereotype, new Outbound Boundary section, PDR checklist
- **`agents/iconix-architect.md`**: Decision rule 7
- **`agents/iconix-developer.md`**: Rule 9
- **`docs/iconix/iconix-process-reference.md`**: Last-reviewed version bumped

## [0.9.46] — 2026-05-12

**Fix: document and implement DRAFT promotion process for iconix-migration.**

After `iconix-migration` runs, the path from DRAFT artifacts to permanent ICONIX IDs
was undocumented. The migration agent said "the traceability agent re-allocates
permanent IDs" with no further guidance. Users had no command to trigger this, no
algorithm to follow, and no explanation of what to do between migration output and the
normal M1/M2/M3 pipeline.

Three additions close this gap:

- **New command `/iconix-promote`** — triggers DRAFT promotion via the Traceability
  agent. Accepts an optional slug or `all`. Handles safety checks, ID assignment,
  file rename, cross-reference updates, and `ids.registry.md` registration.

- **New `# DRAFT promotion` section in `agents/iconix-traceability.md`** — 5-step
  algorithm: identify candidates, safety checks (unresolved `[VERIFY]` → skip),
  assign permanent IDs (highest existing + 1 per type), rename/update/register,
  print summary.

- **Expanded `# Naming conventions for drafts` in `agents/iconix-migration.md`** —
  replaces the vague one-liner with a full 3-step lifecycle (human review → promote
  → continue pipeline) including a diagram showing DRAFT filenames → permanent IDs.

Changes:
- **`commands/iconix-promote.md`**: new command
- **`agents/iconix-traceability.md`**: `# DRAFT promotion` section added before CI counterpart section
- **`agents/iconix-migration.md`**: naming conventions section expanded with DRAFT lifecycle
- **`iconix-init`** + **`iconix-init.ps1`**: `/iconix-promote` added to printed command list
- **`README.md`**: `/iconix-promote` added to command table and Project layout commands tree

## [0.9.45] — 2026-05-12

**Fix: flesh out Phase 6 (test coverage mapping) in iconix-migration.**

Phase 6 in both modes was a stub with no actionable logic. Graph-assisted had
4 vague bullet points; code-walking had a single sentence.

Both modes now have concrete 4-step workflows:

**Graph-assisted:** (1) locate test nodes via language-specific file patterns and
class/function signals (table covering C#, Java, Python, TypeScript/JS, Go, Ruby);
(2) trace graph `calls` edges to build a test→production map, classifying tests as
integration (calls entry-point boundary) vs unit (calls controller/entity only);
(3) map tests to UC-DRAFTs by cross-referencing RB-DRAFT class lists — Full / Partial
/ No coverage; (4) produce `migration/coverage-gaps.md` with a defined format
(summary counts + per-UC table + recommended M3 actions).

**Code-walking:** same 4-step structure; replaces graph queries with Glob + import-
statement reading; conservative coverage classification (unknown → Partial with
`[VERIFY]`); coverage-gaps.md notes code-walking mode in header.

Changes:
- **`agents/iconix-migration.md`**: Phase 6 graph-assisted expanded to 4 concrete steps; Phase 6 code-walking expanded from one sentence to 4 concrete steps

## [0.9.44] — 2026-05-12

**Fix: add missing handoff-report-template.md for iconix-migration Phase 7.**

The migration agent's Phase 7 (Handoff report) instructed the agent to produce
`migration/handoff-<date>.md` but provided no template — unlike every other agent
in the kit which references a specific template file. This meant the agent had to
improvise the structure each run, producing inconsistent handoff reports.

New `templates/handoff-report-template.md` covers: migration run metadata, artifact
inventory with skip reasons, confidence summary (EXTRACTED/INFERRED/AMBIGUOUS per
artifact type), successfully reverse-engineered summary, four human-input gap
categories (business intent, NFRs, alternate courses, architecture decisions),
AMBIGUOUS findings table (graph-assisted only), test coverage gaps, and recommended
next steps ordered by risk. Phase 7 in both workflows (graph-assisted and
code-walking) now reference the template with per-section filling instructions.

Changes:
- **`templates/handoff-report-template.md`**: new template
- **`agents/iconix-migration.md`**: Phase 7 (graph-assisted + code-walking) reference template and list required sections
- **`iconix-init`**: copy handoff-report-template.md to `docs/iconix/templates/`
- **`iconix-init.ps1`**: same
- **`README.md`**: handoff-report-template.md added to Project layout (both kit machinery and artifact directories sections)

## [0.9.43] — 2026-05-11

**Enhancement: hot-spot ranking in concurrent-touch detection.**

After building the per-UC class-touch map, a new Step 3 aggregates across all in-flight UCs to identify architectural hot spots — classes touched by ≥3 UCs simultaneously. Results are ranked by write count and classified HIGH (≥3 writers), MEDIUM (≥1 writer, ≥3 touchers), or LOW (all readers). The hot-class table appears in the CT report before the pair-based conflict list, giving the Architect an immediate view of structural bottlenecks rather than having to infer them from individual conflict pairs.

Hot spots are advisory: they do not block M2 on their own, but HIGH hot spots trigger a recommendation to review extraction or decomposition before Implementation. The M2 gate report now includes hot-spot counts alongside the conflict summary. Hot-spot ranking is always global (not filtered by `$ARGUMENTS` UC-ID focus).

Changes:
- **`agents/iconix-traceability.md`**: new Step 3 (hot-spot ranking); existing Steps 3–7 renumbered to 4–8; Step 7 note about global hot-spot scope; M2 gate section includes hot-spot counts and Architect advisory
- **`commands/iconix-concurrent.md`**: Step 3 references hot-spot aggregation; Step 8 summary includes hot-spot counts
- **`templates/concurrent-touch-template.md`**: new "Hot classes" section with ranked table, risk legend, and Architect recommendation; Summary section includes hot-spot HIGH/MEDIUM counts

## [0.9.42] — 2026-05-11

**Enhancement: operation-name collision detection and CT-ACCEPT suppression in concurrent-touch check.**

Two improvements to the `/iconix-concurrent` detection logic:

**Operation-name collision detection.** The previous W/W rule classified any two UCs both writing to the same class as HIGH. This was too coarse: UC-A adding `save()` and UC-B adding `delete()` to the same class is a coordination concern (MEDIUM), not a true collision. The new rule resolves to operation/attribute names: if the same name is being added by both UCs, it escalates to HIGH (operation-name collision); if the names are distinct, it stays MEDIUM (parallel writes, coupling risk). The class-touch map now records specific operation/attribute names per UC, and the conflict classification uses them.

**CT-ACCEPT suppression.** When a HIGH conflict was previously reviewed and deliberately accepted (documented as `[CT-ACCEPT-XXX]` in a prior CT report or merged PR commit message), subsequent `/iconix-concurrent` runs re-flagged it as active HIGH — noise for the team. A new Step 3 now loads the accepted set from `change-impact/CT-*.md` files (last 90 days) and `git log --grep="CT-ACCEPT"`. Accepted conflicts appear in the report tagged `[ACCEPTED — CT-<date>]` for transparency but are excluded from the active HIGH count, `block_on_high_conflict` exit semantics, and M2 gate readiness.

Changes:
- **`agents/iconix-traceability.md`**: Step 2 records operation/attribute names; new Step 3 loads accepted conflicts; Step 4 uses operation-name collision rules and accepted-set check; Step 5 adds operation-name resolution options; Step 7 exit semantics exclude accepted; M2 gate section updated
- **`commands/iconix-concurrent.md`**: steps updated to reflect new classification and accepted-set logic
- **`templates/concurrent-touch-template.md`**: class-touch map shows named operations; detection scope documents collision and ACCEPTED rules; ACCEPTED conflict example added; Summary section with active/accepted counts added; Recommendations updated with CT-ACCEPT instructions; Configuration note on `block_on_high_conflict` scope

## [0.9.41] — 2026-05-11

**Fix: sync Azure DevOps PR templates to parity with GitHub templates.**

ADO templates had the same sections and checklist structure as their GitHub counterparts
but were missing parenthetical explanations, examples, and minor wording improvements
that make the templates self-contained for new team members:

- `default.md`: phase checkboxes now include artifact descriptions (REQs/UCs/glossary for M1, etc.); reviewer checklist items include examples; work item field updated to reference `iconix.config.yaml`; CI reference changed from "build" to "CI"
- `m1.md`: REQ rule now includes "those belong in ADRs"; removed "in Claude Code" from `/iconix-status` call; work item field updated
- `m2.md`: robustness rules checklist item now lists all four constraints explicitly; container-mapping path added; traceability example added; work item field updated
- `m3.md`: class model item clarified "not domain-model-only"; TC path added to test case item; typed attribute note expanded; "fix before merging" added; traceability example added; work item field updated
- `implementation.md`: affected UCs note added; "Reviewer will verify" added to SD call-order item; reviewer notes expanded; traceability note clarified; work item field updated

Changes:
- **`templates/git-integration/azure-devops/pull_request_templates/default.md`**
- **`templates/git-integration/azure-devops/pull_request_templates/m1.md`**
- **`templates/git-integration/azure-devops/pull_request_templates/m2.md`**
- **`templates/git-integration/azure-devops/pull_request_templates/m3.md`**
- **`templates/git-integration/azure-devops/pull_request_templates/implementation.md`**

## [0.9.40] — 2026-05-11

**Fix: four mismatches between README Project layout and actual kit.**

Audit of README.md against the actual kit revealed four discrepancies introduced when the
Project layout section was added in v0.9.39:

1. **`test-matrices/` removed** — the installer created this folder, the upgrade agent
   protected it, but no agent writes there. The Tester writes `test-matrix.md` at the
   project root, not inside this subfolder. Removed from `iconix-init`, `iconix-init.ps1`,
   and `iconix-upgrade.md`'s never-touch list.
2. **Artifact-directory labels corrected** — the subtitle "created empty at install" was
   wrong for eight directories (`reviews/`, `change-impact/`, `bug-reports/`,
   `edge-case-reports/`, `test-plan/`, `migration/`, `src/`, `tests/`) that are created
   on-demand by agents, not by the installer. Every directory now carries an `[install]`
   or `[agent]` label.
3. **`.github/pull_request_template.md` added** — the GitHub default PR template is
   installed by `iconix-init` (for `git.provider = github`) but was missing from the
   README layout tree.
4. **README's `.github/` comment text** was also missing the `pull_request_template.md`
   file reference, which is now corrected.

Changes:
- **`iconix-init`**: removed `test-matrices` from `mkdir -p`
- **`iconix-init.ps1`**: removed `"test-matrices"` from `$folders` array
- **`agents/iconix-upgrade.md`**: removed `test-matrices/` from "What you NEVER touch" list
- **`README.md`**: `[install]`/`[agent]` labels on all artifact directories; `pull_request_template.md` added to `.github/` tree

## [0.9.39] — 2026-05-11

**Docs: add full project layout section to README; add layout-maintenance rule to CLAUDE.md.**

New `## Project layout` section in README.md documents the complete directory structure
of a project after `iconix-init`: kit machinery (agents, commands, templates, CI scripts,
provider-specific git integration) and artifact directories organized by pipeline phase
(M1 requirements → M2 analysis → M3 detailed design → Phase 9 implementation → audit
trail, traceability, metrics, migration). CLAUDE.md sync rule extended from 2 to 3 items;
item 3 requires the Project layout section to be updated in the same change whenever
installer folders, agent output directories, template destinations, or git-integration
paths change.

Changes:
- **`README.md`**: new `## Project layout` section between Per-project configuration and Usage
- **`CLAUDE.md`**: sync rule extended to item 3 — Project layout maintenance triggers documented

## [0.9.38] — 2026-05-11

**Fix: four follow-on gaps in per-container stack support.**

- **Architect** Stack resolution section extended to cover `package-map.md` alongside `container-mapping` files; PDR checklist gains a package-map Effective stack gate; consistency between both files is now a stated requirement
- **Reviewer** check #7 test-framework extension mapping is now explicit (`xunit`/`nunit` → `.cs`, `junit` → `.java`, `pytest` → `.py`, `jest`/`vitest` → `.ts`/`.tsx`/`.js`/`.jsx`, `rspec` → `.rb`, `gotest` → `.go`); Gherkin and config files explicitly excluded
- **Traceability agent + concurrent-touch template**: fix stale filename `container-mapping/<UC>-mapping.md` → correct pattern `container-mapping/<PREFIX>-UC-XXX-containers.md` (pre-existing bug; would have caused concurrent-touch DB detection to silently find no files)
- **CI script** (`validate-traceability.sh`): new check 4 — changed `container-mapping/*.md` files must have a non-empty "Effective stack" column on every data row; emits `MISSING_STACK_COL` or `BLANK_STACK` violations

Changes:
- **`agents/iconix-architect.md`**: Stack resolution covers both container-mapping and package-map; PDR checklist item added for package-map Effective stack consistency
- **`agents/iconix-reviewer.md`**: check #7 test-framework → extension mapping table; `.feature`/`.json`/`.xml` excluded
- **`agents/iconix-traceability.md`**: filename pattern corrected
- **`templates/concurrent-touch-template.md`**: filename pattern corrected
- **`templates/git-integration/generic/validate-traceability.sh`**: check 4 added; header comment updated

## [0.9.37] — 2026-05-11

**Enhancement: complete per-container stack support across Reviewer, Traceability, Migration, and package-map template.**

Follow-on to v0.9.36. Closes the remaining gaps in polyglot stack support:

- **Reviewer** gains check #7 — flags `[DRIFT]` when source files are placed in a directory that doesn't match their container, or whose language extension mismatches the container's "Effective stack"
- **Traceability** gains validation check #16 — blank "Effective stack" cells in any `container-mapping/*` file are an M2 blocker
- **Migration** emits a "Suggested per-container stack overrides" YAML snippet in the survey report (both modes), so the Architect can paste detected per-container languages straight into `iconix.config.yaml` without re-deriving them
- **Package-map template** gains an "Effective stack" column and a matching quality check, keeping stack context consistent between the package map and container-mapping files

Changes:
- **`agents/iconix-reviewer.md`**: new check #7 — container placement and stack alignment
- **`agents/iconix-traceability.md`**: new validation check #16 — "Effective stack" completeness (M2 blocker)
- **`agents/iconix-migration.md`**: Phase 1 (both modes) now produces "Suggested per-container stack overrides" YAML snippet in the survey
- **`templates/architecture-package-map-template.md`**: "Effective stack" column added to Package list table; matching quality check added

## [0.9.36] — 2026-05-11

**Enhancement: per-container `stack.language` / `stack.test_framework` overrides in `iconix.config.yaml`.**

Polyglot projects (e.g., C# backend + TypeScript frontend) can now declare a `stack:`
sub-key on any container entry to override the top-level language and test framework for
that container. Developer and Tester agents resolve stack settings via two-level lookup:
container-level first, global fallback. The container-mapping template gains an
"Effective stack" column so the Architect documents the resolved stack per container,
giving Developer and Tester a single authoritative source.

Changes:
- **`templates/iconix.config.yaml`**: optional `stack:` sub-key on container entries; example on the `Frontend` container
- **`agents/iconix-architect.md`**: new `# Stack resolution` section; Architect resolves and writes the "Effective stack" column when producing container-mapping files; PDR checklist gains a non-empty "Effective stack" gate
- **`agents/iconix-developer.md`**: new `# Stack resolution` section; artifact lines updated to reference container-level resolution
- **`agents/iconix-tester.md`**: new `# Stack resolution` section; `bdd`/`bdd_framework` remain global; test plan automation-status line updated
- **`templates/container-mapping-template.md`**: "Effective stack" column added to Containers traversed table

## [0.9.35] — 2026-05-11

**Add `docs/iconix-simulation.html` — interactive pipeline state machine simulation.**

Self-contained HTML file (no dependencies) that animates all 22 steps of the ICONIX
pipeline: happy path, M1/M2/M3 gates, concurrent-touch conflict resolution, Phase 9
implementation loop with drift-check alternates, escalation, bug triage, and REQ change
flow. Each step highlights the active state(s), shows a description and artifact list,
and marks previously-visited states. Includes Play/Pause auto-advance and Prev/Next
step controls. Open directly in any browser — no server or build step required.

Changes:
- **`docs/iconix-simulation.html`**: new file

## [0.9.34] — 2026-05-11

**Fix: sequence-template.puml rewritten as a minimal renderable scaffold.**

Previous attempts at incremental fixes still hit version-specific PlantUML edge
cases. Rewrote the template following the same approach as robustness-template.puml:
minimal working diagram with advanced patterns (invoked UC, UI dependency, downstream
handoff) as commented-out blocks. All guidance moved to comments.

Changes:
- **`templates/sequence-template.puml`**: full rewrite — clean scaffold, advanced patterns commented out, traceability block in comments

## [0.9.33] — 2026-05-11

**Fix: sequence-template.puml still fails to preview — two remaining causes.**

(1) `note over` block contained `<<controller>>` etc. which PlantUML misparsed even
inside a note. Moved the class-model reference block to `'` comments instead.
(2) Unused `MVC` lifeline declaration commented out; some PlantUML versions reject
declared-but-never-messaged lifelines.

Changes:
- **`templates/sequence-template.puml`**: `note over` replaced with comment block; unused MVC lifeline commented out

## [0.9.32] — 2026-05-11

**Fix: sequence-template.puml fails to preview in VS Code.**

Three causes: (1) angle brackets `<...>` in group labels — PlantUML interprets these
as HTML markup and fails to parse; (2) em dashes `—` in message labels; (3) stereotype
with spaces `<<from PREFIX-UC-XXX Other-UC-Title>>`. All replaced with safe equivalents.

Changes:
- **`templates/sequence-template.puml`**: replace `<...>` in group labels with `[...]`, em dashes with `-`, and stereotype `<<from PREFIX-UC-XXX Other-UC-Title>>` with `<<from_PREFIX-UC-XXX>>`

## [0.9.31] — 2026-05-11

**Enhancement: iconix-migration now drafts `docs/architecture/package-map.md` during Phase 4b/5b.**

For migration (legacy code), the package structure already exists — the migration agent
now documents it rather than leaving it for the Architect to design from scratch. Phase 4b
drafts the package list, layers, responsibilities, and cross-package rules using robustness
classification; Phase 5b fills in the UC → package allocation table once UC-DRAFTs exist.
Both modes (graph-assisted and code-walking) produce the draft. File is skipped if it
already exists. Also added a C4 Level 3 cross-reference section to the architecture
template pointing at `package-map.md`.

Changes:
- **`agents/iconix-migration.md`**: Phase 4b (both modes) drafts `docs/architecture/package-map.md`; Phase 5b (both modes) fills in UC → package allocation; file added to idempotency check; output structure updated
- **`templates/system-architecture-template.md`**: added C4 Level 3 section cross-referencing `package-map.md`

No ICONIX methodology rule affected — tooling enhancement only.

## [0.9.30] — 2026-05-11

**Enhancement: iconix-migration now drafts `docs/architecture/system-architecture.md` during Phase 1.**

The migration agent already observes the information needed for the architecture doc
(entry points, layer clusters, outbound infrastructure, external systems) but
previously discarded it. It now writes a DRAFT `system-architecture.md` at the end
of Phase 1 in both graph-assisted and code-walking modes, using the new template
structure. The file is skipped if it already exists (human-authored docs are never
overwritten). Added to the idempotency check so re-runs respect human edits.

Changes:
- **`agents/iconix-migration.md`**: Phase 1 (both modes) produces draft `docs/architecture/system-architecture.md`; file added to idempotency check Step 3; output structure updated

No ICONIX methodology rule affected — tooling enhancement only.

## [0.9.29] — 2026-05-11

**Add `system-architecture-template.md` — scaffold for the canonical architecture doc.**

The `architecture.canonical_doc` path in `iconix.config.yaml` had no template,
leaving users without guidance on what to write. Added a C4-flavoured template
covering Context, Containers table, Container interactions, External systems,
Architectural constraints, Scalability/deployment notes, and Open questions.

Changes:
- **`templates/system-architecture-template.md`**: new template
- **`iconix-init`** / **`iconix-init.ps1`**: template copied to `docs/iconix/templates/`; also seeded to `docs/architecture/system-architecture.md` on fresh install (guarded — skipped if file already exists)
- **`templates/iconix.config.yaml`**: added comment on `canonical_doc` pointing to the template
- **`agents/iconix-architect.md`**: agent now tells the user to copy the template if the file is missing
- **`README.md`**: added the new template to the directory listing

No ICONIX methodology rule affected — tooling/documentation gap closure only.

## [0.9.28] — 2026-05-11

**Enhancement: three-stage confirmation wizard with navigation and final submit.**

Extended the confirmation protocol with two new capabilities: the user can
navigate between items at any point using `edit N` / `back` to change a previous
answer, and after all items are confirmed a final summary is shown requiring an
explicit `submit` before anything is executed.

Changes:
- **`agents/iconix-orchestrator.md`**: Rewrote `# Confirmation protocol` as a
  three-stage wizard. Stage 1: overview list + item 1. Stage 2: sequential
  confirmation with navigation table (`yes`, `<edit>`, `edit N`, `back`). Stage 3:
  final summary block, waits for `submit`; `edit N` loops back to Stage 2.
  Rule added: nothing executes until `submit`.
- **`commands/iconix-next.md`**: Updated confirmation UX rule to reference the
  three-stage wizard and the `submit` requirement.

No ICONIX methodology rule affected — UX/interaction protocol only.

## [0.9.27] — 2026-05-11

**Fix: confirmation stops bundled into one response — user could not confirm each item separately.**

The orchestrator had multiple STOP points but no rule to prevent Claude from
grouping all confirmations into a single "yes/no for everything" message.

The correct UX: show all pending confirmations as a numbered list upfront so
the user has the full picture, then confirm each item individually in separate
replies — one item per response, one reply per item.

Changes:
- **`agents/iconix-orchestrator.md`**: Added `# Confirmation protocol` section.
  Two-part pattern: Part A shows all items as a numbered overview list; Part B
  confirms each item one at a time, ending the response after each until the
  user replies. Rules: always show all items upfront, one confirmation per
  response, each item requires its own reply, edits applied before proceeding.
- **`commands/iconix-next.md`**: Replaced one-question-at-a-time rule with the
  matching "show full list, confirm each separately" rule.

No ICONIX methodology rule affected — UX/interaction protocol only.

## [0.9.26] — 2026-05-11

**Fix: Phase 9.4 auto-opened PR and listed "Merge to main" with no confirmation.**

Both are consequential, externally visible actions. PR creation is visible to
teammates and triggers CI; merge to main is irreversible.

Changes:
- **`agents/iconix-orchestrator.md`**: Rewrote Phase 9.4 as 5 explicit steps:
  (1) STOP — Git agent prints PR details, waits for user confirmation;
  (2) open draft PR after approval;
  (3) STOP — wait for user to confirm CI green + PR approved;
  (4) print merge command for user to run manually — never auto-merge;
  (5) exit bookkeeping after user confirms merge done.
- **`iconix-state-machine.puml`**: Updated Phase9_4 label to show the two STOP points.
- **`README.md`**: Updated Phase 9.4 description in the implementation loop diagram.

No Rosenberg rule affected — kit infrastructure extension.

## [0.9.25] — 2026-05-11

**Fix: feature branch never created in the pipeline — added branch creation as Phase 0.**

`branch-conventions.md` stated "Created at M1 entry" but the orchestrator never
dispatched the Git agent to do it. Phase 9.1 assumed the branch existed but nothing
created it. All phases ran on whatever branch was currently active.

Changes:
- **`agents/iconix-orchestrator.md`**: Added step 0 to the phase order list; added new
  `# Phase entry — branch creation protocol` section (Git agent suggests
  `feature/UC-XXX-<slug>` → STOP for user confirmation → `git checkout -b`); updated
  Phase 9.1 to reference the already-existing branch and add a Git agent branch
  validation check before dispatching Developer + Tester.
- **`iconix-state-machine.puml`**: Added `BranchCreate` state between `Idle` and
  `Requirements`.
- **`README.md`**: Added Git Agent step to the `/iconix-next` pipeline diagram.

No Rosenberg rule affected — kit infrastructure extension.

## [0.9.24] — 2026-05-11

**Fix: /iconix-next missing confirmation stops at M1 and M2.**

The command said "stop before any milestone gate" but that was vague enough
that M1 and M2 were being auto-passed. Only the M3→Phase 9 transition
reliably paused because dispatching developers and creating branches gave
Claude a natural signal to confirm.

Changes:
- **`commands/iconix-next.md`**: Replaced the vague gate instruction with an
  explicit 4-step gate protocol: run Traceability → STOP → print gate name
  with `## Milestone N — waiting for approval` header → wait for explicit
  user approval. Protocol applies equally to M1, M2, and M3.

No ICONIX methodology rule affected — behavioral enforcement fix only.

## [0.9.23] — 2026-05-10

**Fix: phase9-cycles/UC-XXX-cycle.md never created in normal pipeline flow.**

`iconix-orchestrator.md` Phase 9 routing had the cycle log referenced only
as `Optional: append final entry … if the team uses cycle logs` at 9.4. No
sub-state created the file, no sub-state appended iteration rows.

Changes:
- **9.1**: Orchestrator now creates `phase9-cycles/UC-XXX-cycle.md` from
  `templates/phase9-cycle-template.md` with UC metadata pre-populated.
- **9.2**: Orchestrator appends one iteration-log row after each Reviewer
  verdict before routing to 9.3 or 9.4.
- **9.4**: Replaced `Optional: append final entry` with an explicit step to
  fill the `## Exit` section (final verdict, merge commit, iteration count,
  cap flag, drift patterns).
- **Template header**: Replaced "Optional artifact — skip if not needed"
  with a description of the automatic lifecycle (created at 9.1, rows at
  9.2, Exit at 9.4).

No Rosenberg rule row affected — kit extension artifact.

## [0.9.22] — 2026-05-10

**Fix: test-matrix.md never created in normal pipeline flow.**

`iconix-tester.md` listed `test-matrix.md` as an artifact it produces and
referenced it in Phase 9 update paths and coverage gates — but contained no
instruction to *create* the file during Phase 7 (after first TC batch). The
coverage-gates checklist said "run before release", not "before M3 gate",
so agents treated it as a final validation rather than a production trigger.

Changes:
- Added `# Test matrix lifecycle` section to `iconix-tester.md` with explicit
  **create** (Phase 7, first UC batch), **extend** (each additional UC), and
  **update** (Phase 9 / bug-fix) steps.
- Renamed coverage-gates heading to "run before M3 gate".
- Updated Ch12 #5 row in `docs/iconix/iconix-process-reference.md` noting the
  fix and clarifying creation ownership. No status shift (✅ was aspirational;
  now correctly enforced).

Theory audit: Ch12 #5 "Use a traceability matrix". PDF not read (gitignored);
matrix row is authoritative for this correction.

## [0.9.21] — 2026-05-10

Round 8 — first **real Phase 9** forcing-function walkthrough across
all three new Reviewer modes introduced in v0.9.8 (Pre-merge drift,
Bug-fix verification, Type 2 closure). Walked through the modes end-
to-end on hypothetical PR + bug-flow scenarios for BS-UC-001:
- Sub-round 8a — Greenfield Phase 9 (9.1 → 9.2 → 9.4) exercising
  Pre-merge drift mode
- Sub-round 8b — Type 1 bug flow (triage → fix → Bug-fix verification)
- Sub-round 8c — Type 2 bug flow (triage → REQ change flow → Type 2
  closure)

**Nine issues** found across the three modes. Slightly fewer than
M3 Tester (10) because the Reviewer's existing `# What you check`
infrastructure (6 categories) absorbed some surface that would
otherwise have been finding territory. Confirms the v0.9.20 pattern:
shipped infrastructure correlates inversely with finding count.

Pattern continues:
  - M1 PO:        prompt 13 + real 7  (v0.9.10/11 + v0.9.15)
  - M2 Analyst:   prompt 8  + real 6  (v0.9.13 + v0.9.17)
  - M2 Architect: prompt 10 + real 10 (v0.9.14 + v0.9.18)
  - M3 Developer: prompt 0  + real 12 (v0.9.19)
  - M3 Tester:    prompt 0  + real 10 (v0.9.20)
  - Phase 9:      prompt 0  + real 9  (v0.9.21) <-- this round

Nine fixes, three groups + one cross-cutting:

### Group A — Pre-merge drift mode (3 fixes)

  M3-Phase9-#1 `[INFO]` finding tag had no documentation; producing
        the 8a review I had to invent it. Fix: added formal severity
        table — `[DRIFT]` / `[TRACEABILITY]` / `[NFR]` are blocking;
        `[INFO]` is advisory and can produce APPROVE / APPROVE WITH
        NOTES.

  M3-Phase9-#2 `## Bug triage` section appeared awkwardly in non-bug
        Pre-merge reviews. Fix: section now explicitly conditional
        — included only when invoked via `/iconix-bug` (Bug triage
        mode); omitted in Pre-merge drift / Bug-fix verification /
        Type 2 closure modes. Disambiguation table added.

  M3-Phase9-#3 phase9-cycle template's "Reviewer verdict" column
        accepted free text. Fix: standardized to the four discrete
        tokens (APPROVE / APPROVE WITH NOTES / REQUEST CHANGES /
        BLOCK MERGE) at start of cell — machine-readable for
        iconix-metrics to compute Phase 9 iteration-count
        distributions per UC.

### Group B — Bug-fix verification mode (2 fixes)

  M3-Phase9-#4 The mode didn't say WHO populates the bug report's
        `## Closure` section. The bug-report template's wording
        ("Filled in by the Reviewer after triage") predates v0.9.8
        and was wrong post-v0.9.8. Fix: bug-report template now
        explicitly distinguishes Traceability (filled at triage) vs
        Closure (filled at verification/closure); Bug-fix
        verification mode step 5 now mandates populating the bug
        report's Closure section, not just the verification report.

  M3-Phase9-#5 Mode lacked regression-sweep guidance. Fix: new
        step 3 requires confirming the Tester's regression sweep
        result; if no shared classes (single-UC fix), state that
        explicitly. Silent skipping no longer allowed.

### Group C — Type 2 closure mode (3 fixes)

  M3-Phase9-#6 (combined with #4) Bug-report template's Traceability
        and Closure sections didn't distinguish triage-time vs
        verification/closure-time ownership. Fix: explicit "Filled
        by..." annotations on each section; empty Closure is now an
        auditable signal ("bug filed but not yet verified closed");
        section heading must NOT be deleted.

  M3-Phase9-#7 Closure schema missing `Driven by CI report:` field.
        Fix: added to the closure schema in Type 2 closure mode AND
        in the bug-report template — preserves the audit chain
        "what triggered this REQ change" on the closed bug report.

  M3-Phase9-#8 Where to post the closure verdict was unspecified.
        Fix: new "Where to post the closure verdict" sub-section —
        Type 2 closure runs AFTER the Implementation PR has merged;
        the verdict is posted as a comment on THAT SAME PR (not a
        separate PR). The bug-report file's updated Closure section
        is the durable record.

### Group D — Cross-cutting (1 fix)

  M3-Phase9-#9 Phase 9 routing had no escalation path for "Type 1
        fix attempt reveals it's actually Type 2." Naïve handling
        forced the Reviewer to either approve a still-broken fix
        or REQUEST CHANGES forever (looping inside the cap). Fix:
        new `RE-TRIAGE` recommendation token in Bug-fix
        verification mode (alongside APPROVE / REQUEST CHANGES) —
        Orchestrator routes back to Bug triage with the failed
        Type 1 fix attempt as new triage evidence. The in-the-wild
        case where a bug looks like code but turns out to be design.

Methodology audit per CLAUDE.md: methodology-surface change
(Reviewer rules + bug-report template + phase9-cycle template).
All cited rules already approved; v0.9.21 enriches kit-location
citations and closes the audit-trail gap on the bug-report's
Closure ownership. No status shifts. Cited Ch11 #1 (Model Update
at every gate), Ch10 #9 (if coding reveals design wrong, change
it AND review the process — Type 2 closure is the "review the
process" half), Ch11 #5 (follow up review with action points).

Cumulative: 11 forcing-function rounds, 91 issues fixed
(13+8+10+5+7+6+1[v0.9.16]+10+12+10+9). Phase 9 (the post-CDR
implementation loop) is now real-run-tested. Remaining real-run
rounds: `/iconix-metrics` real run (Round 9), real
`/iconix-upgrade` end-to-end (Round 10).

### Changed
- `agents/iconix-reviewer.md`:
  - `# Output format` adds an `[INFO]` example finding,
    finding-tag severity table, conditional bug-triage rule
    (M3-Phase9-#1, #2)
  - `# Bug-fix verification mode` adds regression-sweep step
    (M3-Phase9-#5), Closure-population step (M3-Phase9-#4),
    `RE-TRIAGE` recommendation (M3-Phase9-#9)
  - `# Type 2 closure mode` adds `Driven by CI report:` field
    (M3-Phase9-#7) and "Where to post the closure verdict"
    sub-section (M3-Phase9-#8)
- `templates/bug-report-template.md` — Traceability vs Closure
  ownership distinguished; explicit "Filled by..." annotations;
  Closure schema expanded with `Driven by CI report:` and
  `Drift closed:` fields (M3-Phase9-#4, #6, #7)
- `templates/phase9-cycle-template.md` — Reviewer-verdict column
  standardized to discrete tokens with format rule (M3-Phase9-#3)
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.21 with the Round-8-Phase-9 audit summary

## [0.9.20] — 2026-05-10

Round 7 — first **real M3 Tester** forcing-function run.
Followed the v0.9.13 Tester prompt against BS-UC-001 + BS-RB-001
+ my fresh BS-SD-001 + class model + container-mapping +
nfr-annotations to produce fresh test plan + per-course TCs +
per-controller unit TCs. Diffed against the example's 7 TCs +
test plan + sampled BS-TC-001 (system, basic) and BS-TC-002
(unit, alt-D) for code-level structure.

**Ten issues** found. Slightly less than M3 Developer (12)
because the Tester had two existing templates (`test-case-template`,
`test-plan-template`) absorbing some surface; Developer had only
one (`sequence-template`). **Confirms: shipped templates correlate
inversely with finding count.** Pattern continues:

  - M1 PO:        prompt 13 + real 7  (v0.9.10/11 + v0.9.15)
  - M2 Analyst:   prompt 8  + real 6  (v0.9.13 + v0.9.17)
  - M2 Architect: prompt 10 + real 10 (v0.9.14 + v0.9.18)
  - M3 Developer: prompt 0  + real 12 (v0.9.19)
  - M3 Tester:    prompt 0  + real 10 (v0.9.20) <-- this round

Ten fixes, three groups:

### Group A — Coverage strategy / rule contradicts example (2 fixes)

  M3T-R-#1 "One test per controller" was a mandatory rule but the
        example BS-UC-001 has 11 controllers and only 7 TCs total
        — many controllers have NO dedicated unit TC. Fix:
        reworded to "every controller exercised by ≥1 TC (unit OR
        system); unit preferred for non-trivial logic, system-
        transitive acceptable for orchestration steps." The
        example's strategy is now the documented strategy.

  M3T-R-#2 TC template's `Robustness controller:` field was
        SINGULAR; example uses `Robustness controllers exercised:`
        (plural, comma-separated). Fix: template renamed and
        reformatted; one TC may exercise multiple controllers.

### Group B — Implementation surface missing from templates (4 fixes)

  M3T-R-#3 TC template had NO `## Implementation note` section,
        but every example TC has runnable code (60+ lines of C#
        per TC). The biggest gap of this round. Fix: new
        `## Implementation note (<stack> + <test framework>, per
        <ADR>)` section in the TC template with explicit guidance:
        cite stack, test framework, ADRs, infrastructure
        dependencies. The example's runnable code blocks finally
        have a home in the kit. Closes the gap between TC-as-spec
        and TC-as-runnable-test.

  M3T-R-#4 Test-plan template had no Test-framework / dependencies
        section. Example's tests reference WebApplicationFactory,
        Testcontainers, NSubstitute, Reqnroll — none documented.
        Fix: new §6 "Test framework / dependencies" with rows for
        primary framework, mocking lib, integration infra, BDD
        framework (when applicable), test data builders, DB test
        doubles, HTTP/browser automation. Includes guidance for
        the per-TC BDD convention (BDD scoped to acceptance tests
        only).

  M3T-R-#6 `edge-case-reports/UC-XXX-edge-cases.md` declared as
        Tester output; no template. Fix: new
        `templates/edge-case-report-template.md` covering all 7
        edge-case families with one row per family — covering TC
        OR documented waiver. Silent omission no longer possible.

  M3T-R-#7 `test-matrix.md` declared as Tester output; no template.
        Fix: new `templates/test-matrix-template.md` with REQ↔UC↔TC
        coverage table, superseded-TC ledger, orphan/gap audit.
        `iconix-metrics` will parse Pass/Fail/Skip from this
        matrix.

### Group C — Convention / lifecycle ambiguities (4 fixes)

  M3T-R-#5 Per-TC BDD when project default is non-BDD was
        undocumented. Example has `bdd: false` in config but
        BS-TC-101 uses Reqnroll. Fix: new TC `## Type` value
        `acceptance-bdd` for stakeholder-signed acceptance TCs
        using Gherkin even when project default is xUnit. Tester
        agent prompt now formalizes the convention; test-plan §6
        documents the framework scope; `features/UC-XXX.feature`
        artifact rule updated.

  M3T-R-#9 Acceptance TCs in Gherkin format don't fit the
        template's two-column Steps/Expected mirror. Fix:
        template's Steps section now allows Given/When/Then prose
        when `## Type: acceptance-bdd`; Expected may be empty
        (Then clauses live inside Steps).

  M3T-R-#10 Regression TC's `Supersedes TC:` lifecycle was
        unspecified. Example BS-TC-021 supersedes BS-TC-003 but
        TC-003's file is still present and unmarked. Fix: new
        `## Status` field on TC template (`active` /
        `superseded by TC-XXX` / `retired`); Tester agent's new
        `# Superseded TC lifecycle` section formalizes the
        keep-and-mark convention; test-matrix template includes a
        "Superseded TC ledger" section.

  M3T-R-#12 `## Edge case family` was mandatory but always `n/a`
        for basic-course TCs. Fix: section made conditional —
        include only if the TC tests one of the edge-case
        families; omit entirely otherwise.

Methodology audit per CLAUDE.md: methodology-surface change. All
cited rules already approved; v0.9.20 enriches kit-location
citations and closes a major template-coverage gap. No status
shifts. Cited Ch12 Top 10 (test-design rules), Ch12 #7
(test-first thinking), Ch11 #6 (gather data; build boilerplate
checklists — extended to the test-matrix template's superseded-TC
ledger and orphan/gap audit).

Cumulative: 10 forcing-function rounds, 82 issues fixed
(13+8+10+5+7+6+1[v0.9.16]+10+12+10).

### Added
- `templates/edge-case-report-template.md` — per-UC edge-case
  enumeration with one row per of the 7 families; covering TC
  OR documented waiver. Includes coverage summary at the bottom.
- `templates/test-matrix-template.md` — living REQ↔UC↔TC matrix
  with status legend (Pass / Fail / Skip / Pending / Superseded),
  superseded-TC ledger, and orphan / gap audit (orphan TCs,
  uncovered UCs, stale automation entries).

### Changed
- `templates/test-case-template.md` — substantial rewrite:
  - New `## Type` value `acceptance-bdd` (M3T-R-#5)
  - New `## Status` field for superseded TCs (M3T-R-#10)
  - `Robustness controller:` → `Robustness controllers exercised:`
    (plural list) (M3T-R-#2)
  - Steps section accepts Given/When/Then for acceptance-bdd
    (M3T-R-#9)
  - `## Edge case family` made conditional (M3T-R-#12)
  - New `## Implementation note (<stack> + <test framework>, per
    <ADR>)` section with code block (M3T-R-#3)
- `templates/test-plan-template.md` — new §6 "Test framework /
  dependencies" with 7 layer rows (M3T-R-#4)
- `agents/iconix-tester.md`:
  - ICONIX rules reworded — controller-coverage rule now describes
    the two-path strategy (unit-preferred vs system-transitive)
    (M3T-R-#1)
  - New `# Per-TC BDD convention` section (M3T-R-#5)
  - New `# Superseded TC lifecycle` section (M3T-R-#10)
  - `# Artifacts you produce` updated with template references
    for all 5 outputs
  - `# Test case template` section expanded with field-by-field
    guidance keyed to the new template structure
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers copy the 2 new templates to `docs/iconix/templates/`.
- `.github/workflows/validate.yml` — smoke test asserts the 2 new
  templates are installed.
- `README.md` — 2 new templates added to the directory listing.
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.20 with the Round-7-real audit summary.

## [0.9.19] — 2026-05-10

Round 6 — first **real M3 Developer** forcing-function run.
Followed the v0.9.13 Developer prompt against my v0.9.17 fresh
BS-RB-001 + the example's analyst-refined domain model + my
v0.9.18 fresh container-mapping + BS-ADR-001. Mentally produced
fresh BS-SD-001 + class model + code skeleton structure; diffed
against `08-BS-SD-001-...example.puml`.

**Twelve issues — largest finding count of any round.** Two
reasons: (1) the Developer agent had **zero prior prompt review**,
so every issue is net-new; (2) the Developer integrates heavily
with v0.9.10–v0.9.18 upstream changes, surfacing many integration
gaps the upstream-only prompt review couldn't see.

Pattern continues:
  - M1 PO:        prompt 13 + real 7  (v0.9.10/11 + v0.9.15)
  - M2 Analyst:   prompt 8  + real 6  (v0.9.13 + v0.9.17)
  - M2 Architect: prompt 10 + real 10 (v0.9.14 + v0.9.18)
  - M3 Developer: prompt 0  + real 12 (v0.9.19) <-- this round

Twelve fixes, three groups:

### Group A — SD-rendering rules (3 fixes)

  M3D-R-#1 No rule for representing invoked UCs on the SD. The
        RB has `usecase` nodes (v0.9.13); the SD didn't have an
        equivalent. Fix: new SD-rendering rule — render as
        synthetic boundary lifeline + explanatory note describing
        the framework mechanism (e.g., cookie auth challenge,
        OAuth consent screen). Fallback: `note over` block when
        framework hides the invocation.

  M3D-R-#3 No rule for framework-helper lifelines. The example
        introduces `MVC ModelBinder + ModelState` as a lifeline;
        kit didn't say when. Fix: new heuristic — include when
        the framework's behavior maps to ≥1 RB controller; omit
        for trivial forwarding (DI resolution, routing).

  M3D-R-#4 v0.9.15's three Invokes sub-categories had no SD-level
        rendering rules. Fix: dedicated section mirroring the RB
        rules at SD level. UI dependencies → `<<from PREFIX-UC-
        XXX>>` stereotype on lifeline; downstream consumers →
        lifeline at right edge with dashed `..>` from producing
        entity. The example's BS-SD-001 is missing the Moderator
        downstream-consumer rendering — that's now flagged as
        SD-RB drift.

### Group B — Template / convention gaps (4 fixes)

  M3D-R-#6 Sequence template used generic `User` actor + bare
        `ScreenName` placeholders, violating PO actor rules and
        unrepresentative of real SDs. Fix: complete rewrite with
        stack-anchored multi-line labels (`\n` syntax),
        Razor-View paths, EF Core annotations, repository-pattern
        lifelines. Demonstrates rule 8 (design patterns visible
        on SD) instead of leaving it to readers.

  M3D-R-#7 No template for `class-model.puml`. Developer declared
        it as output; nothing existed. Same gap pattern as
        Architect pre-v0.9.14 (4 of 5 outputs untemplated). Fix:
        new `templates/class-model-template.puml` — distinct
        from `domain-model.puml` (entities only, attributes only)
        because the class model is the DETAILED static model
        (entities + DI interfaces + repositories + orchestrators
        with attributes AND operations). Six rules in the header,
        stack stereotypes (`<<entity>>`, `<<controller>>`,
        `<<repository>>`, `<<service>>`, `<<value>>`,
        `<<external>>`), interface↔implementation pairs.

  M3D-R-#8 No template for `cdr-report.md`. Same gap as v0.9.18
        milestone-report. Fix: new `templates/cdr-report-template.md`
        — per-UC M3 readiness report with SD↔RB-controller coverage
        table, lifelines-introduced-beyond-domain-model
        justification table, SD-rendering-rule mirror checks,
        cross-cutting allocation summary, code skeleton paths
        table, full CDR readiness checklist, open questions for
        the Tester running in parallel.

  M3D-R-#11 Sequence template didn't demonstrate design-pattern
        rendering. Rule 8 says "show patterns"; template didn't
        show how. Fix: rewrite (combined with M3D-R-#6) includes
        Repository (`IBookRepository` + `EfBookRepository`), DI
        interface (`ICurrentUserService`), framework controller
        as orchestrator lifeline.

### Group C — Allocation / structure rules (5 fixes)

  M3D-R-#2 "Controller" name collision (ICONIX RB controller vs
        framework controller class). Fix: rule 2 expanded with
        explicit name-collision warning. RB controllers become
        messages (logical actions); framework controllers
        (MVC controller, Spring controller, etc.) become
        orchestrator lifelines. The framework controller
        receives or initiates many RB-controller-derived
        messages.

  M3D-R-#5 Rule for DI interfaces vs domain classes was unclear.
        Architectural / DI interfaces (e.g., `ICurrentUserService`)
        are NOT domain classes; they appear as lifelines when
        the container-mapping allocates behavior to them. Fix:
        rule 4 expanded — DI interfaces don't violate the
        no-invent-classes rule but DO require justification (in
        class-model annotation, SD note, or cdr-report).

  M3D-R-#9 Code skeleton paths didn't align with v0.9.14
        package-map. Naive run produces `src/csharp/Class.cs`;
        real .NET solutions need `src/Bookstore.Web/Controllers/Class.cs`.
        Fix: new section "Code skeleton paths align with the
        architecture package map" — every source file's directory
        name MUST match a package row in `docs/architecture/
        package-map.md`. Files placed under non-package-map
        directories are flagged as architectural drift by the
        Reviewer.

  M3D-R-#10 Behavior allocation heuristic didn't address
        cross-cutting concerns. "Information expert" works for
        domain ops; auth lives elsewhere (controller `[Authorize]`,
        not on `CustomerSession`). Fix: explicit override —
        cross-cutting concerns listed in container-mapping's
        "Cross-cutting concerns" section override the
        information-expert default. Connects v0.9.14's
        cross-cutting section to the Developer's allocation rule.

  M3D-R-#12 Rule 6 "stable SD" was vague — no concrete signal.
        Fix: 6 explicit signals required — every RB controller
        has ≥1 message; every message has an allocated class;
        every UC course has its own group block; class-model
        annotation block filled in; `class-model.puml` exists;
        no Phase-9 commits yet.

CDR readiness checklist expanded to enforce all new rules
(11 items, up from 6).

Methodology audit per CLAUDE.md: methodology-surface change.
All cited rules already approved; v0.9.19 enriches kit-location
citations and closes a major template-coverage gap. No status
shifts. Cited Ch8 Top 10 (sequence diagrams and behavior
allocation), Ch9 CDR, Ch10 Implementation #1 (alternate courses),
Ch11 #6 (cross-cutting concerns).

Cumulative: 9 forcing-function rounds, 72 issues fixed
(13+8+10+5+7+6+1[v0.9.16]+10+12).

### Added
- `templates/class-model-template.puml` — detailed static model
  template; entity / controller / repository / service / value /
  external stereotypes; interface↔implementation pairs; six
  inline rules. Distinct from `domain-model-initial-template.puml`
  (which has attributes only and is the project glossary).
- `templates/cdr-report-template.md` — per-UC M3 readiness
  report. SD↔RB-controller coverage table, lifeline
  justifications, SD-rendering-rule mirror checks, cross-cutting
  allocation summary, code skeleton paths, full CDR checklist,
  Tester awareness section.

### Changed
- `agents/iconix-developer.md` — substantial overhaul:
  - Rule 2 expanded with controller name-collision warning
    (M3D-R-#2)
  - Rule 4 expanded for DI interfaces / Application-layer types
    (M3D-R-#5)
  - Rule 6 "stable SD" criteria made concrete (M3D-R-#12)
  - Behavior allocation heuristics include cross-cutting override
    (M3D-R-#10)
  - New section `# SD-level rendering rules` (M3D-R-#1, #3, #4)
  - New section `# Code skeleton paths align with the
    architecture package map` (M3D-R-#9)
  - CDR readiness checklist expanded from 6 to 11 items
- `templates/sequence-template.puml` — full rewrite with
  stack-anchored multi-line lifelines, repository pattern, DI
  interface, framework-controller orchestrator, downstream
  consumer dashed-arrow demonstration, UI-dependency
  stereotype demonstration, invoked-UC synthetic-boundary +
  note pattern (M3D-R-#6, M3D-R-#11)
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers copy the 2 new templates to `docs/iconix/templates/`.
- `.github/workflows/validate.yml` — smoke test asserts the
  2 new templates are installed.
- `README.md` — 2 new templates added to the directory listing.
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.19 with the Round-6-real audit summary.

## [0.9.18] — 2026-05-10

Round 5 — first **real M2 Architect** forcing-function run.
Followed the v0.9.14 Architect prompt to actually produce all 5
Architect artifact categories for BS-UC-001 (container-mapping,
nfr-annotations, NFR catalog, package-map, integration-surface),
then diffed against the example's BS-ADR-001 (the only Architect
artifact the example ships) plus the stack info in
`iconix.config.example.yaml`.

**Ten issues** only visible by producing artifacts — the largest
real-run finding count yet, matching v0.9.14's prompt-review count.
Architect templates were brand-new in v0.9.14 and untested under
real input; this run exercises all 5 of them at once.

Pattern continues:
  - M1 PO: prompt review 13 + real run 7 (v0.9.10/11 + v0.9.15)
  - M2 Analyst: prompt review 8 + real run 6 (v0.9.13 + v0.9.17)
  - M2 Architect: prompt review 10 + real run 10 (v0.9.14 + v0.9.18)

Ten fixes:

  M2A-R-#1 Example pre-dates v0.9.14 catalog template (NFRs are in
        config comments instead of `docs/nfr-catalog.md`). Known
        retrofit gap; deferred to example refresh.

  M2A-R-#2 Container-mapping testability column doesn't model
        "indirect seam via upstream container" (e.g., Database
        tested through Infrastructure adapter). Fix: explicit
        `(out of scope — covered via <upstream-container>'s seam)`
        convention added to template's testability values list.

  M2A-R-#3 NFR applicability duplicated across catalog ↔
        container-mapping ↔ nfr-annotations with no consistency
        check. Fix: new Traceability check #15 — per-UC NFR-list
        match between container-mapping and nfr-annotations is an
        M2 blocker. Closes the duplication trap.

  M2A-R-#4 nfr-annotations "Out-of-scope NFRs" framing biased
        toward expecting exclusions. For small catalogs, all NFRs
        usually apply; for large regulatory/security suites,
        explicit out-of-scope is the common case. Reworded to be
        size-aware.

  M2A-R-#5 package-map template has no convention for cross-team /
        infra-owned containers (e.g., PendingReviewsQueue owned by
        INFRA-88). Fix: new `Infrastructure (external)` layer
        marker; external packages exempt from cross-package /
        architecture-test rules.

  M2A-R-#6 integration-surface "Bidirectional integrations"
        section almost always empty for typical UCs. Fix: moved to
        commented-out optional block; uncomment-and-fill only if
        actually needed. Same pattern as v0.9.13's Alternate Course
        handling.

  M2A-R-#7 container-mapping "Open architectural questions"
        section had unclear format. Fix: standardized to
        `<question>. [Proposed ADR-XXX]` so future Traceability
        checks can mechanically validate the link.

  M2A-R-#8 nfr-catalog `Owner:` field couldn't model split
        ownership (PO defines target, Architect enforces). Common
        in regulated environments. Fix: split into `Defined by:`
        and `Enforced by:` fields.

  M2A-R-#9 integration-surface had a redundant `Failure handling`
        column AND a per-touchpoint failure-modes sub-section.
        Fix: dropped the column; kept the prose-friendly
        sub-sections. Failure handling needs prose, not keywords.

  M2A-R-#10 No template for the M2 milestone report (Traceability
        produces these but format was inline-prompt-only — same
        gap Architect had pre-v0.9.14). Fix: new
        `templates/milestone-report-template.md` formalizing
        gate-specific checks (M1/M2/M3 sub-sections), the
        machine-readable `Recommendation` token (`READY` /
        `NOT READY` — parsed by `iconix-metrics` for
        `gate_failure_rate`), and concurrent-touch summary
        section. Traceability agent's inline format pointer now
        delegates to this template.

Methodology audit per CLAUDE.md: methodology-surface change
(template + Traceability validation rule additions). All cited
rules already approved; v0.9.18 enriches kit-location citations
and closes the per-UC NFR-consistency gap. No status shifts.
Cited Ch7 Top 10 (architecture decisions, cross-cutting concerns,
testability seams), Ch6 PDR, Ch4 #5 (REQ traceability — extended
via NFR-list check #15).

Cumulative: 8 forcing-function rounds, 60 issues fixed
(13+8+10+5+7+6+1[v0.9.16]+10). Real-run methodology continues to
match or exceed prompt-review counts.

### Added
- `templates/milestone-report-template.md` — M1/M2/M3 readiness
  format. Machine-readable Recommendation token; gate-specific
  check sub-sections; M2 concurrent-touch summary. Subsumes the
  inline format previously in `iconix-traceability.md`.

### Changed
- `templates/container-mapping-template.md`:
  - Testability seam values list adds `(out of scope — covered
    via <upstream-container>'s seam)` for indirect seams (M2A-R-#2)
  - Open architectural questions section formalized to
    `<question>. [Proposed ADR-XXX]` format with usage example
    (M2A-R-#7)
- `templates/nfr-annotations-template.md` — Out-of-scope NFRs
  section reworded to be size-aware (M2A-R-#4)
- `templates/nfr-catalog-template.md` — `Owner:` field split into
  `Defined by:` + `Enforced by:` for split-ownership NFRs
  (M2A-R-#8)
- `templates/architecture-package-map-template.md`:
  - Package list table gains `Infrastructure (external)` example
    row + Layer-column note explaining the convention (M2A-R-#5)
  - Quality checks add the external-package coverage check and
    the architecture-test exclusion check
- `templates/integration-surface-template.md`:
  - Outbound integrations table drops the `Failure handling`
    column (M2A-R-#9)
  - Bidirectional integrations section moved to a commented
    optional block (M2A-R-#6)
- `agents/iconix-traceability.md`:
  - New validation check #15 — per-UC NFR-list consistency
    between container-mapping and nfr-annotations is an M2 blocker
    (M2A-R-#3)
  - `# Milestone gate report format` section now delegates to
    `templates/milestone-report-template.md` instead of carrying
    the inline format (M2A-R-#10)
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers copy `milestone-report-template.md` to
  `docs/iconix/templates/`.
- `.github/workflows/validate.yml` — smoke test asserts the new
  template is installed.
- `README.md` — `milestone-report-template.md` added to the
  templates listing.
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.18 with the Round-5-real audit summary.

## [0.9.17] — 2026-05-10

Round 4 — first **real M2 Analyst** forcing-function run. Followed
the v0.9.13 Analyst prompt to actually produce a fresh BS-RB-001
robustness diagram from BS-UC-001 + the PO-only initial domain
model, then diffed against the example's RB-001. **Six issues**
only visible by producing the diagram — net-new findings prompt
review couldn't catch.

The pattern from v0.9.15 holds: prompt-review of M2 Analyst
(v0.9.13) found 8 issues; real run added 6 more. Real production
keeps surfacing things prompt review missed.

Six fixes:

  R4-#1 Example RB violates v0.9.13's verb-led controller rule —
        uses question-form names like `Is user logged in?`, `Is
        Book Review length OK?`. Methodologically wrong (the
        v0.9.13 rule says controllers are *actions*, not
        *predicates*). Known limitation: example refresh deferred;
        v0.9.17 keeps the rule and notes the example needs retrofit.

  R4-#2 Analyst rules silent on rendering v0.9.15's `UI
        dependencies (page/component reuse)` sub-field. Both my
        run and the example drew reused pages identically to
        UC-owned pages — visually indistinguishable. Fix: new
        Analyst section `# Rendering UI dependencies and
        downstream consumers on the RB` — UI-reused boundaries get
        a `<<from PREFIX-UC-XXX Title>>` stereotype.

  R4-#3 Same gap for v0.9.15's `Downstream consumers` sub-field.
        Same fix: dashed arrow (`..>`) from produced entity to
        consumer actor distinguishes async handoff from
        synchronous flow.

  R4-#4 Analyst lacked a controller-granularity rule equivalent
        to PO rule 13. New section `# Controller granularity` —
        consolidate similar error paths producing the same
        response (alt B "too short" + alt C "too long" → one
        controller); split paths producing different responses.
        Default to consolidation; don't pre-fragment for testability.

  R4-#5 Workflow step 6 was unconditionally imperative ("Rewrite
        UC text"). Reworded to "Verify mapping; rewrite ONLY if
        mismatches surface." On real runs UC text often already
        maps cleanly — the prior wording read as "always rewrite."

  R4-#6 Analyst rules didn't say what to do with PO's `' VERIFY:`
        notes (v0.9.15 R3-#3 introduced them on the PO side
        without specifying Analyst-side processing). Asymmetric:
        PO wrote, Analyst silently improvised. Fix: Domain model
        rule 5 now mandates `' RESOLVED at M2:` reword OR class
        removal; unresolved VERIFY notes are an M2 PDR blocker.

Methodology audit per CLAUDE.md: methodology-surface change. All
cited rules already approved; v0.9.17 enriches kit-location
citations and resolves the PO↔Analyst handoff asymmetry from v0.9.15.
No status shifts. Cited Ch5 Top 10 #5 (RB syntax), Ch5
controller-as-action principle, Ch6 PDR.

Cumulative: 7 forcing-function rounds, 50 issues fixed
(7+6+5+8+10+7+6+1[v0.9.16]). Real-run methodology continues to
outpace prompt review by ~3-7 net-new findings per agent. M2
Architect (real run), M3, Phase 9 still ahead.

### Changed
- `agents/iconix-analyst.md`:
  - Workflow step 6 reworded from imperative-rewrite to verify-
    then-rewrite-only-if (R4-#5)
  - Workflow step 7 now references "Resolve every PO `' VERIFY:`
    note" (R4-#6)
  - New section `# Controller granularity (when to consolidate
    vs split)` — mirrors PO rule 13 at the controller level
    (R4-#4)
  - New section `# Rendering UI dependencies and downstream
    consumers on the RB` — formalizes the rendering rules for
    v0.9.15's three Invokes sub-categories (R4-#2, R4-#3)
  - Domain model rule 5 gains explicit `' VERIFY:` → `' RESOLVED at
    M2:` resolution procedure (R4-#6)
  - PDR readiness checklist gains four mirror checks: Invokes /
    UI dependencies / Downstream consumers / VERIFY-resolved
    (R4-#2, R4-#3, R4-#6)
- `templates/robustness-template.puml`:
  - Adds commented examples for UI-dependency boundary syntax
    (`<<from ...>>` stereotype) (R4-#2)
  - Adds commented examples for downstream-consumer dashed-arrow
    syntax (R4-#3)
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.17 with the Round-4-real audit summary

## [0.9.16] — 2026-05-10

PlantUML validation in CI. The forcing-function-within-forcing-
function pattern hit twice — v0.9.13 caught a robustness-template
bug at preview time (bare `<...>` in arrow labels), and v0.9.15
caught a domain-model-template bug (every line commented out;
PlantUML rendered nothing). Both were invisible to prompt review;
both got past every CI check we had until a human opened the file
in a previewer. v0.9.16 adds the missing CI step.

The new `validate-plantuml` job runs on every push and PR. It:

  1. Installs PlantUML on the runner (`apt-get install plantuml`).
  2. For every `.puml` file in the repo (templates/, examples/,
     root): runs `plantuml -checkonly` for syntax, AND counts
     diagram declarations + arrows for content.
  3. Fails the build with file-pinned errors if either check fails.

The content check specifically catches the v0.9.15 class of bug
(empty-but-syntactically-valid diagrams). Some PlantUML versions
return exit 0 even on parse warnings, so the syntax check also
greps output for known error markers as a safety net.

This is a tooling-only commit. No methodology changes, no
template additions, no new agents. Theory audit consciously
skipped per CLAUDE.md (same convention as v0.9.9 and v0.9.12).

### Added
- `.github/workflows/validate.yml` — new `validate-plantuml` job
  parallel to `validate-agents` and `smoke-test-installer`.
  Catches the two classes of rendering bug we hit in v0.9.13
  and v0.9.15.

### Carry-forward note
This was carried over as a robustness item across multiple
recent commits (v0.9.13, v0.9.15). Closing it now means future
PlantUML template work doesn't need preview-by-human as the
last line of defense.

## [0.9.15] — 2026-05-10

Round 3 — the **first real forcing-function run**. v0.9.10–v0.9.14
called themselves "forcing-function rounds" but were actually prompt
review: read the agent prompt, read the example, find gaps, fix.
v0.9.15 went further — produced fresh REQ + initial domain model +
UC by following the v0.9.14 PO prompt as if running it for the first
time, then diffed the fresh artifacts against the example's. Seven
issues that prompt review couldn't have caught surfaced — they only
became visible when actually producing artifacts and comparing.

The methodology shift matters: prompt review catches *prompt clarity*
problems; only artifact production catches *agent-execution* problems
(places where the prompt is clear but executing it on real input
reveals format gaps, missing fields, or arbitrary-judgment
requirements). v0.9.15 closes seven such gaps.

Seven fixes:

  R3-#1 REQ template gains `Related NFRs:` and `Related BRs:`
        fields. The example uses both; the kit had never
        standardized them. NFR linkage at REQ time means the
        Architect doesn't have to re-derive applicable NFRs at M2.
        BR linkage anticipates the deferred BR-NNN feature with
        a clean migration path ("(none — Business Rules not yet
        adopted)" until BR-NNN ships).

  R3-#2 Domain model template gains an "ownership over time"
        header (PO drafts initial at M1; Analyst refines at M2;
        both gates re-validate). The example's domain-model.example.puml
        has a similar header but with stale (pre-v0.9.3) "PO +
        Analyst joint initial pass" wording. The kit's template now
        ships the correct version.

  R3-#3 PO rule 9 + domain model template now formalize a
        `' VERIFY:` convention for PO-introduced ambiguities.
        When the PO is unsure whether a noun is a real entity or
        a state/value (e.g., "PendingQueue" in the WCR example),
        the PO marks the class with a `' VERIFY:` comment block
        for the Analyst to resolve at M2. Mirrors intake `[VERIFY]`.

  R3-#4 UC template's `Invokes:` field SPLIT into three sub-fields
        (`Invokes (UC calls)`, `UI dependencies (page/component
        reuse)`, `Downstream consumers`). The fresh-run UC for
        WCR exposed three meaningfully different cross-UC
        dependencies that v0.9.11's single `Invokes:` field
        conflated: alt A invokes Login (true call); alt E reuses
        the Book Not Found page (UI reuse, no flow invocation);
        Moderate Customer Reviews consumes the queue this UC
        writes to (downstream handoff, not invocation). PO rule 12
        rewritten with the three categories and the mirror rule
        per sub-field.

  R3-#5 PO rule 13 added: row granularity for the Basic Course
        table. One row per (a) user action + immediate system
        response, OR (b) system-only step that the Analyst would
        model as a separate controller at M2. Multiple system
        steps mapping to ONE controller collapse; multiple
        steps mapping to DIFFERENT controllers stay separate.
        "When in doubt, expand" — the Analyst can collapse but
        splitting later is harder.

  R3-#6 UC template's `Domain entities introduced or used:` field
        SPLIT into `introduced` (net-new on the domain model) and
        `used` (already on the model). The Analyst at M2 needs to
        know which entities are new vs reused; the prior single
        list didn't say.

  R3-#7 REQ acceptance criteria checkbox lifecycle documented
        (deferred from v0.9.11 / R2-#7). Tester ticks per TC pass
        (M3 / Phase 9); PO confirms at M3→Implementation merge
        during PR review; an unticked criterion at merge time is a
        Reviewer finding / blocker on the Implementation PR.

Methodology audit per CLAUDE.md: methodology-surface change. All
cited rules already approved; v0.9.15 enriches kit-location
citations. No status shifts. Cited rules: Ch3 #4 (UC in context
of object model), Ch3 #7 (event/response flow), Ch4 #5 (REQ
traced to UCs), Ch5 #1 (no GUI on domain model).

Cumulative: forcing-function arc has now produced 6 rounds
(prompt review v0.9.10/0.9.11/0.9.13/0.9.14, dogfood v0.9.12, real
run v0.9.15) and 43 issues fixed (7+6+5+8+10+7). v0.9.15 marks the
methodology shift to actual artifact production going forward.

### Changed
- `templates/req-template.md`:
  - `## Acceptance criteria` gets a checkbox-lifecycle note (R3-#7)
  - `## Traceability` gains `Related NFRs:` and `Related BRs:`
    fields (R3-#1)
- `templates/domain-model-initial-template.puml`:
  - New "Ownership over time" header explaining the v0.9.3+
    PO/Analyst split (R3-#2)
  - New rule 8 in the rules block: `' VERIFY:` convention for
    PO-introduced ambiguities (R3-#3); the rule places VERIFY
    comments IMMEDIATELY ABOVE the ambiguous class declaration
    (PlantUML treats `'` lines mid-class-block inconsistently)
  - **PlantUML rendering hardening** (caught at preview time —
    same forcing-function-within-forcing-function as v0.9.13's
    robustness template): the v0.9.10 file shipped with
    everything between `@startuml` and `@enduml` commented out,
    so PlantUML had no diagram content to render. v0.9.15 ships
    a worked example (Customer / Book / CustomerReview / status
    enum + PendingReviewsQueue with VERIFY example) that
    actually renders, with a loud "DELETE AND REPLACE" header
    instructing users to substitute their own domain entities.
    Lesson: kit-shipped PlantUML files must *render* on first
    open — empty-but-syntactically-valid `@startuml/@enduml`
    blocks aren't actually valid for users.
- `templates/use-case-template.md`:
  - `Invokes:` field replaced by three sub-fields:
    `Invokes (UC calls):`, `UI dependencies (page/component reuse):`,
    `Downstream consumers:` (R3-#4)
  - `Domain entities introduced or used:` split into
    `Domain entities introduced (new on domain model):` and
    `Domain entities used (already on domain model):` (R3-#6)
- `agents/iconix-product-owner.md`:
  - Rule 9 gains "Mark your ambiguities for the Analyst" sub-section
    on the `' VERIFY:` convention (R3-#3)
  - Rule 12 rewritten — now distinguishes three sub-categories
    of cross-UC dependency (Invokes/UI dependencies/Downstream
    consumers) with mirror rule per sub-field (R3-#4)
  - New rule 13: "Basic course row granularity" (R3-#5)
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.15 with the Round-3-real audit summary

### Note on the WCR example
The fresh-run M1 artifacts produced during this round were used as
diff input only; they were not committed. The example's existing
artifacts remain in their pre-v0.9.10 state and will surface as
Layer-D findings when `/iconix-upgrade` is run on the example.
Example refresh remains a deferred task.

## [0.9.14] — 2026-05-10

Round 2 forcing-function fixes (M2 Architect phase). We continued
the WCR run from v0.9.13 into M2 Architect. **Ten issues** found —
the largest single-agent finding count of any forcing-function
round. Why so many? The Architect was the most under-templated
agent in the kit: it produces 5 artifact categories but only ADRs
had a template, and the worked example only demonstrates 1 of the
5. Fresh users had no format guidance for 4 of the 5 outputs.

This commit ships 5 new templates and a substantial overhaul of
the Architect agent prompt to close the gap.

Ten fixes:

  M2A-#1 4 of 5 Architect artifacts had no template. Added
         container-mapping, nfr-annotations, nfr-catalog,
         architecture-package-map, integration-surface templates.
  M2A-#2 WCR example only demonstrates ADR. (Example expansion
         deferred to a future refresh; v0.9.14 ships the templates
         so future projects have format guidance.)
  M2A-#3 Folder mismatch — installer didn't create `packages/`
         or `integration-points/`. Resolved by relocating these
         project-wide artifacts to `docs/architecture/` (already
         created by installer).
  M2A-#4 "package-map" was semantically ambiguous (UC packages vs
         code packages). Renamed agent's output to
         `docs/architecture/package-map.md` and clarified in the
         prompt + template that this is CODE/deployment-level
         packaging, distinct from PO-owned `use-case-packages/`.
  M2A-#5 No template for `nfr-catalog.md`. Added.
  M2A-#6 Architect's input list named `nfr-catalog.md` (bare); the
         actual configured path is `docs/nfr-catalog.md`. Updated
         the agent prompt to read from the configured path.
  M2A-#7 Container-mapping format unspecified. Template added
         (containers + role + testability seam + NFR refs +
         cross-cutting concerns + open architectural questions).
  M2A-#8 NFR-annotations format unspecified. Template added
         (NFR ID + target + where enforced + Reviewer-checkable
         signal + test-design hints for Tester).
  M2A-#9 PDR readiness checklist had no item for "open
         architectural questions" per Decision rule 5. Added: "No
         blocking architectural questions remain open without a
         Proposed ADR."
  M2A-#10 Concurrent-touch resolver scope vs "never rewrite UCs"
         was ambiguous. Clarified routing: UC splits, entity-name
         changes in UC text, and RB updates are dispatched via
         /iconix-next to PO/Analyst respectively; the Architect
         never edits those files even when its decision drove the
         change.

Methodology audit per CLAUDE.md: methodology-surface change. All
cited rules already approved; v0.9.14 enriches kit-location
citations and closes a major template-coverage gap. No status
shifts. Cited Ch7 Top 10 (architecture decisions documented;
testability seams; cross-cutting concerns) and Ch6 PDR.

### Added
- `templates/container-mapping-template.md` — per-UC container
  mapping with role, testability seams, NFR refs, cross-cutting
  concerns, open architectural questions, traceability footer.
- `templates/nfr-annotations-template.md` — per-UC NFR
  enforcement detail with target, where-enforced, Reviewer-
  checkable signal, test-design hints for the Tester.
- `templates/nfr-catalog-template.md` — project-wide NFR catalog
  with stable IDs, categories, measurable targets, ownership,
  UC-applicability, covering-ADR references.
- `templates/architecture-package-map-template.md` — code /
  deployment package decomposition with allowed-dependencies
  matrix, UC→package allocation, architecture-test enforcement
  guidance.
- `templates/integration-surface-template.md` — inbound /
  outbound / bidirectional integration touchpoints with auth,
  rate limits, failure modes, ADR refs.

### Changed
- `agents/iconix-architect.md`:
  - `# Inputs you rely on` — NFR catalog path now references
    `iconix.config.yaml` `nfr_catalog` configuration; mentions
    template for first-time setup (M2A-#5, M2A-#6)
  - `# Artifacts you produce` — restructured into per-UC,
    project-wide, and ADR groups; each artifact references its
    template; project-wide artifacts relocated to
    `docs/architecture/` (M2A-#1, M2A-#2, M2A-#3, M2A-#4,
    M2A-#7, M2A-#8)
  - `# Resolving concurrent touches` — added explicit routing for
    UC splits, entity-name changes, RB updates (M2A-#10)
  - `# PDR readiness check` — expanded to enforce all 5 Architect
    artifacts; new "no blocking architectural questions without a
    Proposed ADR" item (M2A-#9)
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers copy the 5 new templates to `docs/iconix/templates/`.
- `.github/workflows/validate.yml` — smoke test asserts all 5 new
  templates are installed.
- `README.md` — 5 new templates added to the directory listing.
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.14 with the M2-Architect audit summary.

## [0.9.13] — 2026-05-10

Round 2 forcing-function fixes (M2 Analyst phase). We continued
the WCR run from v0.9.10/v0.9.11 into M2, walking the Analyst
agent prompt mentally against the example RB-001. Eight gaps
surfaced, all in the Analyst's prompt and the robustness template.

Eight fixes:

  M2-#1 UI sub-elements (buttons, fields, dropdowns) are NOT
        boundaries. The agent's `# Boundary object naming` rule now
        says so explicitly. Naive runs would have produced
        `boundary "Send button"` for every UI control mentioned.

  M2-#2 `Display X page` and `Load X entity` are SEPARATE
        controllers. The prior `# Display controllers` section
        conflated them. Renamed to `# Display vs data-fetch
        controllers` with explicit guidance: when the UC has "load
        then display", produce two controllers, connected.

  M2-#3 Robustness template's comment-block format mismatched the
        canonical example. Template had `User: <action>` /
        `System: <response>` literal labels; example uses concrete
        actor names. Aligned template to the example pattern.

  M2-#4 Robustness template shipped with `actor User as U`
        (generic). The kit's PO rule explicitly forbids generic
        actor names. Replaced with `actor "<Actor name from UC>"
        as Actor` placeholder.

  M2-#5 Robustness template used !define BOUNDARY()/ENTITY()/
        CONTROLLER() macros; example uses native PlantUML keywords
        (`boundary`, `entity`, `control`). Templates and examples
        now match — both use native keywords. Cleaner, more
        idiomatic, easier to read raw.

  M2-#6 Agent prompt and example disagreed on invoked-UC
        representation. Prompt: "use a usecase node, not a
        controller." Example: `control "Invoke Login"`. **Example
        violates the rule.** v0.9.13 keeps the rule (methodology-
        correct: use cases at this level are the thing being
        invoked, not implementation controllers) and adds rationale
        + a concrete PlantUML snippet. The example will surface as
        a Layer-D finding when /iconix-upgrade is run on it; an
        example refresh is deferred.

  M2-#7 Analyst's domain-model rule 5 said "Time-box the INITIAL
        domain model to ~2 hours." But since v0.9.3, the PO owns
        the initial draft. The Analyst REFINES. Reworded to
        "refinement at M2" with explicit reference to PO rule 9.

  M2-#8 Analyst's PDR readiness checklist had no item to validate
        v0.9.11's PO rule 12 mirror (Invokes: Traceability field
        ↔ usecase nodes on the RB). Added the mirror check; cited
        Traceability check #14 as the gate enforcer.

Methodology audit per CLAUDE.md: methodology-surface change
(Analyst rules + RB template). All cited rules already ✅;
v0.9.13 enriches kit-location citations. No status shifts.
Cited Ch5 #5 (RB syntax), Ch5 #1 (no GUI on domain model),
Ch6 #2 (no detailed design on RB).

### Changed
- `agents/iconix-analyst.md`:
  - `# Boundary object naming` adds the UI-sub-element exclusion
    rule (M2-#1)
  - `# Display controllers` renamed to `# Display vs data-fetch
    controllers` with the separate-controllers rule (M2-#2)
  - `# Invoked use cases on robustness diagrams` rewritten with
    a "why not a controller" rationale + native PlantUML example
    snippet (M2-#6)
  - `# Domain model rules` rule 5 reworded — "initial" → "refinement
    at M2"; references PO rule 9 explicitly (M2-#7)
  - `# PDR readiness check` gains three items: UI-sub-element
    check (M2-#1), human-verification note on the every-sentence-
    maps-to-element check, and Invokes-mirror check (M2-#8)
- `templates/robustness-template.puml` — full rewrite:
  - Comment block format aligned to example (no User:/System:
    label prefix; concrete actor names) (M2-#3)
  - `actor User as U` replaced by `<Actor name from UC>` placeholder
    (M2-#4)
  - !define macros removed; native `boundary`, `entity`, `control`,
    `usecase` keywords used throughout (M2-#5)
  - Header comment block adds notes referencing the agent's three
    new rules (UI sub-elements, invoked-UC representation, Display
    vs Load)
  - Example wiring shows the `usecase` node pattern for invoked UCs
    (M2-#6)
  - Layout defaults (`left to right direction`, `skinparam
    shadowing false`, `skinparam ArrowColor`) added — match the
    example's defaults
  - **PlantUML rendering hardening** (caught at preview time):
    arrow labels use `[bracket]` placeholders instead of
    `<angle-bracket>` (PlantUML interprets unquoted `<...>` in
    arrow labels as HTML/creole markup, which broke preview);
    `note bottom` block uses literal `PREFIX-UC-XXX` instead of
    `<PREFIX>-UC-XXX` (notes accept HTML markup, so unclosed
    `<PREFIX>` tags broke rendering); inline `' comment` after
    `as ALIAS` declarations moved to separate lines (mid-line
    comments were unreliable). Template header now documents the
    placeholder conventions explicitly so future template
    additions don't repeat the mistake.
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.13 with the M2-Analyst audit summary

## [0.9.12] — 2026-05-10

The v0.9.9 dogfood test we owed. We pointed `/iconix-upgrade
--dry-run` at the Write Customer Review example to exercise the
upgrade agent for the first time on a real-world target. The
forcing function found bugs in `/iconix-upgrade` itself — the
upgrade was designed for "freshly iconix-init'd standard project"
and didn't account for either tutorial structures (the example) or
projects with custom layouts (renamed config, custom doc paths,
flat directories). v0.9.12 closes all five issues found.

Issues #U-#1 through #U-#5:

  U-#1 Agent assumed config file is `iconix.config.yaml`. Wouldn't
       find `iconix.config.example.yaml` (the example) or any
       project-specific variant. Fix: explicit Step 1a config
       resolution with refusal messages — refuses on example-only
       configs ("this looks like a kit demo, not an installed
       project"); refuses on no-config-at-all; asks for choice on
       multiple variants.

  U-#2 Heuristic detection was path-exact, brittle to renames.
       The example has `domain-model.example.puml` (equivalent to
       v0.9.x's `domain-model/domain-model.puml`); heuristic only
       saw the latter and detected v0.3.0 even though the example
       was authored in v0.9.1+. Fix: two-pass detection — Pass 1
       canonical paths (existing), Pass 2 content-based search
       (UCs by `## Basic Course` content; REQs by `## Statement`
       content; source by `Traceability:` comment). When Pass 2
       finds higher version evidence, it's used AND recorded as a
       layout discrepancy in the report.

  U-#3 Layer C (template refresh) didn't handle missing parent
       directory. If `docs/iconix/templates/` doesn't exist, the
       agent's prompt was silent on what to do. Fix: explicit
       create-the-directory rule (it's harmless reference docs);
       opt-out via `--layers` for projects deliberately not using
       the docs/ pattern. Hand-edited templates now preserved with
       `.backup` suffix instead of overwritten.

  U-#4 Layer D (artifact detection) scanned canonical paths only.
       A project with flat or renamed structure returned "0
       artifacts found" even when artifacts clearly existed. Fix:
       same two-pass approach as U-#2 — Pass 1 canonical paths,
       Pass 2 content-based fallback. Layer D additionally now
       checks for v0.9.10+ and v0.9.11+ field gaps (Intakes, Invokes,
       Domain entities, Postconditions multi-state, alt-course
       preamble) which were missing from the agent's check list
       even though Layer-D's purpose was exactly this.

  U-#5 No per-layer opt-in. The upgrade was "all layers or
       dry-run" — no way to run "just the detection report." Fix:
       new `--layers <A,B,C,D,E>` flag (any subset). Combinable
       with `--dry-run`. Layers run is now surfaced in the
       report's Summary so reviewers know the scope.

Methodology audit: tooling-only change per CLAUDE.md (same as
v0.9.9). `/iconix-upgrade` is kit-version maintenance, not
methodology. Theory audit consciously skipped.

### Changed
- `agents/iconix-upgrade.md`:
  - Step 1 split into Step 1a (config-file resolution with refusal
    rules) and Step 1b (two-pass version detection) (U-#1, U-#2)
  - New Step 1.5 — `--layers <list>` filter handling (U-#5)
  - Layer C now handles missing `docs/iconix/templates/` parent;
    .backup suffix policy for hand-edited templates (U-#3)
  - Layer D now has Pass 1 canonical + Pass 2 content-based
    detection; expanded check list to include v0.9.10+ and v0.9.11+
    field gaps (Intakes, Invokes, Domain entities, multi-state
    Postconditions, alt-course preamble) (U-#4)
- `commands/iconix-upgrade.md`:
  - `argument-hint` advertises `--layers <A,B,C,D,E>` flag
  - Body explains useful `--dry-run --layers D` and similar combos
  - Explicit refusal-on-missing-config rule referenced (U-#1)
- `templates/upgrade-report-template.md` — Summary section
  expanded to surface: detection method (Pass 1 / Pass 2 / override),
  layers run, config-file used, layout (canonical / non-canonical).

### Note on the WCR example test run
This commit also serves as a record that `/iconix-upgrade --dry-run`
was first exercised on `examples/write-customer-review/` and that
the example deliberately remains a tutorial layout (flat numbered
files; `iconix.config.example.yaml` not `iconix.config.yaml`). With
v0.9.12 fixes, future upgrade attempts on similar non-canonical
projects will refuse cleanly (example case) or fall back to content-
based detection (real projects with custom layouts).

## [0.9.11] — 2026-05-10

Round 2 forcing-function fixes. We continued the real-world test
run from v0.9.10 (Write Customer Review example, M1 gate review).
Six more issues surfaced — gaps in template fields, the cross-UC
invocation citation rule, and the Traceability gate's coverage of
in-text UC references. v0.9.11 closes them.

Issues #R2-#1, #R2-#2, #R2-#3 — template gaps:

  R2-#1: UC template missing `Invokes:` and `Domain entities` fields
         that the example uses but the template doesn't ship. These
         carry real traceability value: Domain entities tells the
         Analyst which entities to expect on the robustness diagram;
         Invokes tells everyone downstream which UCs this one depends
         on.

  R2-#2: UC template's Postconditions field was a single string;
         real UCs split outcomes (Success vs Rejection vs ...). The
         example used `Success:` / `Rejection:` sub-headings; the
         template now formalizes that pattern.

  R2-#3: REQ template used `Source:` (free text); UC template uses
         `Intakes:` (structured list). Same concept, different field
         names — inconsistent. v0.9.11 aligns REQ to `Intakes:`.

Issues #R2-#4, #R2-#5, #R2-#6 — cross-UC invocation handling:

  R2-#4: The "cite invoked UCs with explicit IDs" rule lived only
         in the Analyst agent (M2) — but the PO drafts UC text at
         M1, before the Analyst sees it. So the Analyst had to
         retrofit invocation citations during M2 instead of finding
         them already correct. v0.9.11 adds rule 12 to the PO so
         the citation convention ships from M1.

  R2-#5: PO M1 checklist had no item for "UC-text invocations match
         the Traceability Invokes: block." Drift between the two
         was easy and undetected.

  R2-#6: Traceability agent had 13 validation checks; none covered
         in-text UC invocations. A UC saying "system invokes
         BS-UC-999" with no `BS-UC-999.md` file would slide past
         the M1 gate. v0.9.11 adds check #14 (invocation drift).

### Methodology audit (per CLAUDE.md)
- **Cited rules:** Ch3 #7 (two-column UC format), Ch4 #1 (8 easy
  steps to better use case), Ch3 #2 (UCs in context of object
  model — Domain entities field strengthens UC↔domain-model
  tracing). All already ✅.
- **Status shifts:** none. Citations get richer.
- **No contradictions found.** v0.9.11 unifies a citation
  convention that had been split across PO and Analyst agents.

### Changed
- `templates/use-case-template.md`:
  - Postconditions structured as Success/Rejection sub-bullets with
    a comment about additional states (R2-#2)
  - Traceability block adds `Invokes:` and `Domain entities
    introduced or used:` fields with example syntax (R2-#1)
- `templates/req-template.md` — `Source:` field replaced by
  `Intakes:` with same structure as UC template (R2-#3)
- `agents/iconix-product-owner.md`:
  - New rule 12 "Cross-UC invocations cite explicit IDs" with
    format spec `<PREFIX>-UC-XXX | <Title> | <Package>`, mirror
    rule between UC text and Traceability block, and
    `(downstream — not yet drafted)` escape for forward references
    (R2-#4)
  - M1 checklist gains an item enforcing the mirror rule (R2-#5)
- `agents/iconix-traceability.md` — new check #14 "invocation
  drift" added to the validation suite (R2-#6); broken / unmatched
  invocations are M1 blockers
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.11 with the Round-2 audit summary

### Note on the example
The Write Customer Review example was authored before v0.9.11 and
will not match the new template fields. This is intentional —
running `/iconix-upgrade --dry-run examples/write-customer-review/`
should now flag the example's UC as needing retrofit (missing
`Intakes:` field per v0.9.10, alt course A's preamble per v0.9.10,
plus the new v0.9.11 gaps). That's the v0.9.9 dogfood test we owe;
the example refresh itself is intentionally deferred until the
Round-2-and-beyond fixes are done.

## [0.9.10] — 2026-05-10

Forcing-function fixes. We started a real-world test run of the kit
on the Write Customer Review example (driving its 3 intakes through
the PO agent's intake checklist + REQ/UC drafting). Seven concrete
issues surfaced before reaching M1 gate — issues that no amount of
agent-prompt review could have caught. v0.9.10 fixes all seven.

This is exactly the kind of feedback that confirms the v0.9.5–v0.9.9
agent prompts need real-world exercise, not just internal logic
review. Future versions should keep running real examples through
the kit and folding back the findings.

### Issues found and fixed

1. **Multi-input intake convergence was unspecified.** Real projects
   often deliver several intakes (email + transcript + ticket) for
   the same feature. The PO agent told you what to do with one input,
   not several. Fix: new `## When multiple intakes describe the same
   goal` section in `agents/iconix-product-owner.md` with a 4-step
   consolidation rule. UC's Traceability block now lists ALL source
   intakes, not just the most recent one.

2. **REQ atomicity criteria not defined.** The kit said "atomic
   functional requirements" without telling you what *atomic* meant.
   You could plausibly produce 1, 2, or 3 REQs from the same intake.
   Fix: new rule 10 in PO agent — "one REQ per testable observable
   behaviour; alternates extending the same goal stay in the parent
   REQ unless they introduce a distinct measurable target, distinct
   user goal, or pass an orthogonality test." Bias toward fewer REQs
   with richer alternate-course coverage.

3. **Initial domain model lacked a template + inline guidance.** PO
   rule 9 said "draw an attribute-only class diagram" but shipped no
   PUML template, no concrete heuristic for "is this noun an entity
   or a state on another entity?", and forced you to bounce to the
   Analyst agent file for the rules. Fix: new
   `templates/domain-model-initial-template.puml` with inline rule
   comments AND the most critical heuristics inlined into PO rule 9
   (real-world only; attributes-only; type everything; skip state-
   machine entities; show relationships; domain model = glossary).

4. **Two-column UC format had no convention for runtime forks.**
   Some user actions branch on a runtime precondition (logged in
   yes/no). The format has no inline conditional. Fix: new rule 11
   in PO agent + comment in `templates/use-case-template.md` —
   "basic course is the happy path with preconditions met; runtime
   forks become alternate courses with `At step N, if <condition>:`
   preamble." Static preconditions go in the Preconditions metadata,
   not in alternates.

5. **"Two paragraphs total" prompt rule contradicted the UC template
   structure.** The PO agent's rule said "no UC exceeds two
   paragraphs total: paragraph 1 = basic course, paragraph 2 = all
   alternate courses" — but `templates/use-case-template.md` has
   separate `## Alternate Course A: <name>` H2 sections (one per
   alternate). A UC with 5 alternates (like Write Customer Review)
   has 5 H2 sections — clearly not "two paragraphs." Fix: rule 3
   restated as "fits on one page when rendered" (preserves the
   book's brevity intent without the literal-paragraph-count
   contradiction); template comment clarifies that the structured
   H2 alternates are correct format but total length stays
   page-length. M1 checklist item updated; feature-request
   template's INVEST line updated.

6. **Intake templates blurred raw input and PO output.** The email
   template had `## Verbatim text` (input) and `## PO restatement`
   (output) in the same file separated only by a `---`. A fresh
   reader couldn't tell at a glance what the email *was* vs what
   the PO *added*. Fix: explicit ⚠️ banner separator in
   `intake-email-template.md` and `intake-transcript-template.md`
   making input/output ownership unmistakable. (BRD and
   feature-request templates are single-author; no banner needed.)

7. **Intake `## Status` Ready/Blocked checkbox was never enforced.**
   The PO agent could happily extract REQs from an intake whose
   Status was still `Blocked` or unchecked, since nothing in the
   prompt told it to verify. Fix: new "Status-Ready check" paragraph
   in PO intake-checklist section — "before any REQ/UC drafting,
   verify the intake's `## Status` block is `Ready` and all
   `[VERIFY]` items resolved. If `Blocked`, refuse and surface the
   open items."

### Added
- `templates/domain-model-initial-template.puml` — new (issue #3).
  PUML skeleton with all six initial-domain-model rules as inline
  comments. Replaces the implicit "go read the analyst's rules"
  pointer.

### Changed
- `agents/iconix-product-owner.md`:
  - Rule 3 restated (issue #5 — "two-paragraph" → "one-page" + UC-template alignment)
  - Rule 9 expanded with inline critical heuristics + reference to
    new template (issue #3)
  - New rules 10 and 11 (issues #2 and #4 — REQ atomicity, conditional path forks)
  - New Status-Ready check paragraph in `# Intake checklist` (issue #7)
  - New `## When multiple intakes describe the same goal` section
    in `# Intake checklist` (issue #1)
  - M1 checklist item updated for one-page rule (issue #5)
  - Split-signals list adds "rendered UC overflows one page" (issue #5)
- `templates/intake-email-template.md` — ⚠️ banner between Verbatim
  text and PO restatement (issue #6)
- `templates/intake-transcript-template.md` — ⚠️ banner between
  interview content and Analyst summary (issue #6)
- `templates/intake-feature-request-template.md` — INVEST line
  updated from "two-paragraph rule" to "one page when rendered"
  (issue #5)
- `templates/use-case-template.md`:
  - Header comment block explaining the brevity rule + when to use
    Alternate Courses vs Preconditions vs basic-course path (issues #4 and #5)
  - Alternate course tables now have a leading "At step N, if
    `<condition>`:" example row (issue #4)
  - Traceability block adds an `Intakes:` field for multi-intake
    consolidation (issue #1)
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers copy `domain-model-initial-template.puml` to
  `docs/iconix/templates/`.
- `.github/workflows/validate.yml` — smoke test asserts
  `domain-model-initial-template.puml` is installed.
- `README.md` — `domain-model-initial-template.puml` in templates
  listing.
- `docs/iconix/iconix-process-reference.md` — "Last reviewed" bumped
  to v0.9.10. No status shifts (all fixes clarify existing ✅ rules);
  rationale notes the cited Ch3, Ch2, Ch4 rules.

### Methodology audit (per CLAUDE.md `# Auditing kit changes against ICONIX Theory`)
- **Cited rules:** Ch3 #7 (two-column UC format) — already ✅, fixes
  #4 and #5 strengthen citations. Ch3 #1 (UC brevity — "typically
  two paragraphs", but a *typical*, not *maximum*) — fix #5 restates
  the kit's hardened "no UC exceeds two paragraphs" to align with the
  book's softer intent. Ch2 #3 (initial domain model before UCs) —
  already ✅, fix #3 adds the missing template. Ch4 #1 (8 easy steps
  to better use case) — already ⚠️, no change to status.
- **Status shifts:** none. All seven fixes clarify or refine existing
  ✅ rows; the cited fixes don't move any cell from one status to
  another. Citations get more specific.
- **No contradictions found.** Fix #5 actually *resolved* a
  contradiction the kit had been shipping for several versions
  (agent prompt vs UC template).

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
