# Changelog

All notable changes to the ICONIX Claude Kit.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

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
