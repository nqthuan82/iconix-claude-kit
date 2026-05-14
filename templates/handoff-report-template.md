# Migration Handoff Report — `<YYYY-MM-DD>`

> Produced by the `iconix-migration` agent at the end of every migration run.
> Save as `migration/handoff-<YYYY-MM-DD>.md`.
>
> Purpose: give the human reviewer a single document that describes what was
> reverse-engineered, what confidence to place in each artifact, what gaps
> require business input, and what to do next. Read this before touching any DRAFT.

## Migration run

- **Project:** `<project name from iconix.config.yaml>`
- **Date:** `<YYYY-MM-DD>`
- **Mode:** Graph-assisted (Graphify v`<version>`, graph built `<date>`) | Code-walking
- **Phases completed:** `<list, e.g. 1, 2, 3, 4, 4b, 5, 5b, 6, 7>`
- **Scope:** Full repository | `<module or path scoped>`
- **Previous run:** `<date of prior survey, or "none">`

---

## Artifact inventory

| Artifact | Path | Status | Phase |
|---|---|---|---|
| Survey | `migration/survey-<date>.md` | Generated | 1 |
| System architecture | `docs/architecture/system-architecture.md` | Generated DRAFT \| Skipped (exists) | 1 |
| Class model | `class-model/class-model.puml` | Generated DRAFT \| Skipped | 2 |
| Sequence diagrams | `sequence/SD-DRAFT-*.puml` | `<N>` generated | 3 |
| Robustness diagrams | `robustness/RB-DRAFT-*.puml` | `<N>` generated | 4 |
| Domain model | `domain-model/domain-model-DRAFT.puml` | Generated DRAFT \| Skipped | 4b |
| Package map | `docs/architecture/package-map.md` | Generated DRAFT \| Skipped (exists) | 4b+5b |
| Use case drafts | `use-cases/UC-DRAFT-*.md` | `<N>` generated | 5 |
| UC package overviews | `use-case-packages/*-DRAFT.puml` | `<N>` generated | 5b |
| Domain glossary | `migration/domain-glossary.md` | Generated \| Skipped (no schema source) | 5c Steps 1–3 |
| BDD-DRAFT files | `features/BDD-DRAFT-*.feature` | `<N>` generated \| Skipped — `stack.bdd: false` \| Skipped — no UC-DRAFTs | 5c Steps 4–6 |
| Business rules | `docs/business-rules.md` | Generated — `<N>` rules \| Skipped — `business_rules.enabled: false` | 5d |
| Coverage gaps | `migration/coverage-gaps.md` | Generated | 6 |

**Skipped artifacts** (human-edited since last run or already promoted):
- `<path>` — `<reason: human-edited | already promoted as UC-XXX>`
- (none)

---

## Confidence summary

> **Graph-assisted mode:** edges come from Graphify's analysis of your source.
> **Code-walking mode:** all output is INFERRED — no graph edges to mark EXTRACTED against.

| Artifact type | EXTRACTED | INFERRED | AMBIGUOUS | Notes |
|---|---|---|---|---|
| Class model entries | `<N>` | `<N>` | `<N>` | |
| Sequence diagram messages | `<N>` | `<N>` | `<N>` | |
| Robustness diagram nodes | `<N>` | `<N>` | `<N>` | |
| Domain model relationships | `<N>` | `<N>` | `<N>` | |
| Use case flows | — | `<N>` | `<N>` | UC flows are always INFERRED |

**Overall confidence:** `<% of artifacts derived from EXTRACTED edges only>` EXTRACTED-only
`<% containing any INFERRED material>` contain INFERRED material
`<% containing AMBIGUOUS>` contain AMBIGUOUS items requiring `[VERIFY]`

> Code-walking mode: confidence is uniformly lower. Every artifact is flagged `[VERIFY]`.
> Treat all outputs as hypotheses until a human confirms the business intent.

### [VERIFY] item breakdown

> Count of `[VERIFY]` markers per artifact group. These are the items the human reviewer
> must confirm before running `/iconix-promote`. High counts in UC-DRAFTs or RB-DRAFTs
> are the most critical — they block promotion directly.

| Artifact group | Files | [VERIFY] count |
|---|---|---|
| UC-DRAFTs | `use-cases/UC-DRAFT-*.md` | `<N>` |
| RB-DRAFTs | `robustness/RB-DRAFT-*.puml` | `<N>` |
| Domain glossary | `migration/domain-glossary.md` | `<N>` |
| BDD-DRAFTs | `features/BDD-DRAFT-*.feature` | `<N>` (omit row if none generated) |
| Business rules | `docs/business-rules.md` | `<N>` (omit row if Phase 5d skipped) |
| **Total** | | **`<N>`** |

> Zero `[VERIFY]` items on a DRAFT does not mean it is correct — it means the agent had
> high confidence. Human review is still required before promotion.

---

## Successfully reverse-engineered

> What can be used as a starting point without immediate rework.

- **Entry points:** `<N>` identified — `<brief description, e.g., "8 HTTP controllers, 2 background services">`
- **Architectural layers:** `<N>` container clusters identified — `<brief description>`
- **Class model:** `<N>` classes extracted with attributes and operations
- **Sequence diagrams:** `<N>` diagrams drafted covering the happy-path flows
- **Domain entities:** `<N>` entities identified; `<N>` relationships mapped
- **Use cases:** `<N>` UC-DRAFTs produced; `<N>` UC packages drafted
- **Per-container stack overrides:** suggested YAML snippet in `migration/survey-<date>.md` (Section: Suggested per-container stack overrides)

---

## Phase 5c — BDD scenario synthesis

| Item | Result |
|---|---|
| **Schema source** | `<SQL (.sqlproj / .sql) \| ORM (<framework>) \| schema.prisma \| db/schema.rb \| ent/schema \| migration DSL \| none>` |
| **Tracks active** | `<e.g., Track A + Track B (EF Core) + Track B5 (app enum) \| Track C1 (schema.prisma)>` |
| **Entities in glossary** | `<N>` — `<N>` with state machines, `<N>` with [VERIFY] |
| **Integer status columns resolved** | `<N High (EXTRACTED) \| N Medium (INFERRED) \| N Ambiguous \| N not found>` |
| **Domain glossary** | Generated at `migration/domain-glossary.md` \| Skipped — no schema source detected |
| **BDD-DRAFTs** | `<N>` files generated in `features/` \| Skipped — `stack.bdd: false` \| Skipped — no UC-DRAFTs found |

> When BDD-DRAFTs were generated: every scenario is marked `[VERIFY]` — confirm actor
> identity, operation triggers, and state-transition sequence before promoting to TC-XXX.
> Lifecycle: human review → `/iconix-promote` → Tester at M3.

> When Steps 4–6 were skipped: the domain glossary at `migration/domain-glossary.md` is
> still valid for use by the Analyst (UC vocabulary), Architect (entity naming), and Tester
> (state machine reference). Enable BDD generation by setting `stack.bdd: true` in
> `iconix.config.yaml` and re-running Phase 5c.

---

## Phase 5d — Business rules trigger scan

> Pre-computed by `iconix-migration` from `docs/business-rules.md`.
> This is a preliminary view — the Architect performs the definitive cross-container analysis at M2.
> Omit this section when `business_rules.enabled: false` or when no rules were extracted.

| Rule ID | Category | Rule summary | Provenance | ADR signal |
|---|---|---|---|---|
| BR-001 | Invariant | `<rule summary>` | EXTRACTED \| INFERRED [VERIFY] | ⚠ Investigate |
| BR-002 | Authorization | `<rule summary>` | EXTRACTED \| INFERRED [VERIFY] | ⚠ Investigate |
| BR-003 | Transition guard | `<rule summary>` | EXTRACTED \| INFERRED [VERIFY] | ⚠ Investigate |
| BR-004 | Precondition | `<rule summary>` | INFERRED [VERIFY] | ✓ No ADR likely |
| (none) | | | | |

**ADR signal key:**
- ⚠ **Investigate** — category (Invariant / Authorization / Transition guard / Workflow / Calculation) may require an ADR if enforcement spans containers. Architect confirms at M2.
- ✓ **No ADR likely** — category (Precondition / Postcondition) typically enforced within a single layer.

**Summary:**
- Total rules: `<N>` (`<N>` EXTRACTED, `<N>` INFERRED [VERIFY])
- ⚠ Investigate: `<N>` rules — `<list BR-IDs>`
- ✓ No ADR likely: `<N>` rules — `<list BR-IDs>`

---

## Requires human input

### Business intent gaps
> The agent recovered what the code *does*. These items need a human to supply what users *need*.

- `UC-DRAFT-XXX` (`<slug>`) — `<one-line gap, e.g., "alternate course for payment timeout not clear from error handling">`
- `UC-DRAFT-YYY` — `<gap>`
- (none)

### NFR gaps
> NFRs cannot be reliably recovered from code. Every item below needs a Product Owner or Architect decision.

- `<container or class>` — `<observed signal, e.g., "retry loop in PaymentClient suggests availability NFR; threshold not codified">`
- (none)

### Alternate course gaps
> Error handling was found in `try/catch` or early-return blocks, but whether these represent
> real user journeys vs defensive programming is a business question, not a code question.

- `UC-DRAFT-XXX` Step `<N>` — `<e.g., "catch(TimeoutException) maps to alternate course A2 — confirm with PO">`
- (none)

### Architecture decisions needed
> Items the Architect must confirm before M2 can proceed.

- `<package or class>` — `<e.g., "OrderService imports both DbContext and StripeClient — mixed-responsibility; recommend extract PaymentGateway as outbound boundary">`
- `[VERIFY]` items in `docs/architecture/system-architecture.md`: `<N>`
- `[VERIFY]` items in `docs/architecture/package-map.md`: `<N>`

---

## AMBIGUOUS findings (graph-assisted only)

> Items where Graphify could not resolve to a single implementation. Each requires human confirmation.
> Omit this section in code-walking mode.

| Finding | Location | Candidates | Risk |
|---|---|---|---|
| Polymorphic dispatch | `<class>.<method>` | `<ImplA>`, `<ImplB>` | `<HIGH / MEDIUM>` |
| Deep call chain (>8) | `<entry point>` | — | Review for refactoring |
| (none) | | | |

---

## Test coverage gaps

> From `migration/coverage-gaps.md`. UC-DRAFTs with no existing test coverage need tests written at M3.

- UCs with no test coverage: `<N>` (`<list UC-DRAFT IDs>`)
- UCs with partial coverage: `<N>` (`<list>`)
- UCs with full coverage: `<N>`

---

## Recommended next steps

> Ordered by risk / coverage impact. Complete in this order before opening M1/M2 PRs.

1. **Review `[VERIFY]` items in system-architecture.md and package-map.md** — the Architect must confirm container boundaries before any M2 work proceeds. Unconfirmed boundaries lead to wrong robustness diagrams.
2. **PO reviews UC-DRAFTs for business intent** — pay special attention to alternate courses and actor descriptions. The code knows the happy path; only the PO knows the full user journey.
3. **Resolve NFR gaps** — at least one NFR per observable quality constraint (performance, security, compliance) should be added to `docs/nfr-catalog.md` before M2.
4. **Resolve AMBIGUOUS polymorphic dispatch items** — these are the most error-prone inferences; confirm the correct implementation before M2 robustness work.
5. **Promote reviewed DRAFTs** — once a DRAFT is human-confirmed, run the Traceability agent to allocate permanent IDs (`UC-DRAFT-XXX` → `UC-XXX`). Then the normal M1/M2/M3 pipeline applies.
6. **Address test coverage gaps** — plan test-case authoring at M3 for UCs in `migration/coverage-gaps.md`.

---

## Traceability

- **Generated by:** `iconix-migration` agent (`<kit version>`)
- **Mode:** Graph-assisted | Code-walking
- **Source artifacts read:**
  - `iconix.config.yaml`
  - All source files under `src/` (or configured source root)
  - `graphify-out/graph.json` + `GRAPH_REPORT.md` (graph-assisted only)
- **Outputs written:** see Artifact inventory above
- **Next action:** human review → Traceability agent DRAFT promotion → M1 gate
