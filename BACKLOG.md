# Backlog

Proposed enhancements to iconix-kit that are not yet scheduled for implementation.
Each entry should carry enough design context that a future session (or a different
maintainer) can pick it up without re-deriving the problem.

Status legend:
- **Proposed** — surfaced via discussion/audit; design sketch exists; not committed.
- **In design** — actively being refined; expect API/contract churn.
- **In progress** — implementation underway; tracked by version.
- **Done** — shipped; remove from backlog and reference the version that landed it.
- **Rejected** — considered and dropped; keep the rationale so it isn't re-proposed.

---

## Lightweight mode

**Status:** Proposed (2026-05-16)
**Origin:** Cross-agent logic audit follow-up — see CHANGELOG v1.0.58 through v1.0.66
for the audit chain; the lightweight-mode discussion came after D4 was closed.

### Problem

The full ICONIX pipeline (PO → Analyst → Architect → Developer → Tester through M1/M2/M3
gates) is well-calibrated for features at the use-case granularity that ICONIX
historically targets — "Place a bet", "Check out cart", "Process refund" — multi-step,
multi-screen, inherently multi-alternate-course features.

It is **not** well-calibrated for sub-day work that modern dev workflow generates
constantly: "add a date filter to the orders list", "fix a typo in a label", "tighten
input validation". For these the overhead math is:

| Feature size | Pure code work | ICONIX overhead | Ratio |
|---|---|---|---|
| <1 day (filter, single endpoint, copy change) | 20–60 min | 2–3 h | ~6:1 |
| 1–3 days (new screen + backend + DB column) | 8–24 h | 3–5 h | ~20–40 % |
| 3+ days (sub-system, new flow) | 24 h+ | 4–8 h | ~15–25 % |

For sub-day work the overhead dominates. The kit currently has no skip-path: every
feature traverses the full chain. Anti-paralysis rules cap *iteration count per artifact*
but not *artifact count per feature*.

### Why this isn't a kit defect

ICONIX (Rosenberg & Stephens, 2007) assumed quarterly-release granularity where "use case"
meant something that fits a screen-flow story. Modern hourly/daily granularity didn't
exist in the methodology's design context. The kit inherits this assumption faithfully —
that's why the reference matrix still shows ✅ across the rules. The friction is real
but it's a *methodology fit* problem, not a *kit correctness* problem.

### Proposed solution

Add a parallel **lightweight mode** that the Product Owner (or Orchestrator router)
selects when the change is judged small. Lightweight skips diagram production but
preserves the traceability data that impact/risk analysis depends on, by declaring it
inline in the UC instead of deriving it from separate RB / container-mapping / NFR
artifacts.

#### Lightweight UC schema

```markdown
**ID:** UC-017
**Mode:** lightweight        ← new field, distinguishes from "heavy" (the default)
**Title:** Filter orders by date

## Basic Course
| User Action       | System Response          |
|---                |---                       |
| Selects date range | Filters order list      |
| Applies filter    | Shows matching orders    |

## Alternate Courses
- Invalid date → show validation error
- No results → show empty state

## Traceability (lightweight — data declared, not derived)
**Class-touch:** OrderListController.applyFilter, OrderRepository.findByDateRange
**NFRs:** NFR-005-list-latency
**Containers:** Web, API
**TCs:** TC-042 (basic), TC-043 (empty), TC-044 (invalid date)
**Parent UC:** UC-009 (View orders)
**ADRs:** none
```

The `Class-touch:` field is the linchpin — it carries the class-level data that
Analyst+Developer would have produced in heavy mode.

#### What still works under lightweight mode

| Impact / risk feature | Works under lightweight? | Why |
|---|---|---|
| `/iconix-impact UC-XXX` blast radius | ✅ | Walks declared `Class-touch:` list, same as walking RB-derived list in heavy mode |
| Concurrent-touch detection (M2 gate) | ✅ | Compares declared class-touch lists across in-flight UCs |
| NFR violation prediction | ✅ | NFR refs are inline in the UC |
| TC regression scope | ✅ | TC list is inline |
| Container/architecture impact | ✅ | Container list is inline |
| Test coverage gates (M3) | ✅ | TC links resolve to actual TC files |

#### What lightweight mode genuinely loses

| Capability | Lost because |
|---|---|
| GRASP reasoning visibility | No RB diagram to inspect |
| Formal stereotype validation | No Analyst to enforce boundary↔controller↔entity rules |
| Visual debugging of design | No RB / SD diagrams |
| **Class-touch correctness guarantee** | User/agent declared, not auto-derived |

The first three are documentation losses — acceptable for small features where design
visibility wasn't the point. The fourth is the real risk and needs mitigation (below).

#### Mitigation for the class-touch honesty risk

Heavy mode derives class-touch from the RB diagram (which has stereotype rules), so the
list is mechanically correct. Lightweight mode declares it directly, with two failure
modes:

1. **Declared list incomplete** — agent forgets a transitively-called class (UC calls
   `OrderService`, which calls `EmailNotifier`; `EmailNotifier` is missing from the list).
2. **Declared list hallucinated** — class name doesn't exist in the codebase.

Two cheap CI checks bring lightweight class-touch back to verified-on-commit quality:

- **Traceability validation at commit:** for each name in `Class-touch:`, grep `src/` for
  the class. If not found → flag `[VERIFY — class not found in codebase]` before the
  UC is committed.
- **Reviewer drift check at Phase 9.2:** Reviewer compares `Class-touch:` declared against
  the classes actually modified in the PR diff. If drift > 20 % (declared classes not
  touched, or touched classes not declared), BLOCK MERGE until the UC is corrected.

Both checks are mechanical, both are cheap, both shift the risk from "process compliance"
to "declaration honesty plus mechanical verification".

### Roadmap to implementation

Estimated ~3–5 commits. Order matters because each step is independently testable:

1. **Template** — `templates/use-case-template-lightweight.md` with the schema above.
   Update `README.md` Project layout to list it. CHANGELOG only.

2. **Product Owner agent** — add a "lightweight mode triage" step at intake. Heuristics:
   - ≤ 1 page of basic course
   - ≤ 2 alternate courses
   - Touches ≤ 3 classes (per PO's initial domain-model scan)
   - No new container, no new NFR, no new ADR required
   → propose lightweight; else propose heavy. User confirms which mode applies.

3. **Traceability agent** — extend the artifact parser to accept the `Mode: lightweight`
   header and the `Class-touch:` field. Add the class-name-exists validator. Update
   `/iconix-impact` to walk class-touch from the UC when `Mode: lightweight`, and from
   the RB+container-mapping when `Mode: heavy` (the existing path).

4. **Reviewer agent** — Pre-merge drift mode (Phase 9.2) gains a "lightweight UC
   class-touch drift" check that compares declared vs actually-modified classes in the
   PR diff. Existing Bug-fix verification mode is unaffected.

5. **Orchestrator pre-flight** — extend `# Pre-flight checks` (added in v1.0.66) to
   recognize lightweight UCs so it doesn't accidentally treat them as malformed heavy UCs.
   Phase 0 skips Analyst / Architect dispatch when the UC is `Mode: lightweight`; Phase 4
   M2 gate still runs but it expects no separate `container-mapping/UC-XXX.md` for
   lightweight UCs.

Heavy mode remains the default. Lightweight is opt-in via PO's triage prompt or via
explicit `--lightweight` flag at /iconix-next.

### Open questions

- **Should lightweight UCs require a Parent UC?** The schema above shows `Parent UC: UC-009`.
  If lightweight is mostly used for incremental change ("add filter to view orders"),
  forcing a parent link gives `/iconix-impact` a clean way to walk "what depends on
  this feature".
- **Can lightweight UC be promoted to heavy later?** Sometimes a feature grows. The kit
  would need a `/iconix-promote-uc UC-XXX --to=heavy` command that retroactively runs
  Analyst + Architect to fill in RB + container-mapping. Probably defer to a v2 of
  lightweight mode.
- **What about Tester?** Lightweight TCs can stay terse (1 TC per course) but still need
  to exist — Phase 9 implementation loop won't run without TCs. No change to Tester
  agent expected.
- **Methodology audit:** Rosenberg's book doesn't have a "lightweight mode" concept.
  Adding it makes the kit a *superset* of ICONIX rather than a faithful implementation.
  The reference matrix will need a new column or footnote acknowledging this. Decision
  point for the author.

### Rejected alternatives

- **Just skip the kit for small features.** Considered. Loses traceability —
  small-feature work would not appear in `/iconix-metrics` / coverage matrices,
  creating blind spots. The kit's value is exactly that everything is in the matrix.

- **Make heavy mode faster instead.** Considered. The fixed overhead is not from agent
  speed; it's from artifact count + gate count. No amount of model speed-up changes the
  ratio for sub-day work.

- **Single-agent "feature" agent that does PO+Analyst+Architect+Dev+Tester inline.**
  Considered. Tighter than lightweight mode but breaks the agent-prompt-discipline rules
  in CLAUDE.md (one agent = one responsibility). Lightweight mode keeps separation of
  concerns but reduces the artifact count per agent.

---

## DDD (Domain-Driven Design) Support

**Status:** Proposed (2026-05-16)
**Origin:** Discussion session — gap analysis between ICONIX methodology and DDD
tactical/strategic patterns. The kit faithfully implements ICONIX but that makes it
structurally incompatible with DDD end-to-end (see conversation context for full
gap analysis).

### Problem

The iconix-kit is a faithful implementation of ICONIX (Rosenberg & Stephens, 2007).
That faithfulness is also its DDD limitation: ICONIX and DDD make **opposite design
decisions** in three load-bearing places.

**Gap 1 — Domain model role**

| | ICONIX (kit today) | DDD |
|---|---|---|
| What the domain model is | Project glossary — drawn in ~2 h | The design — Aggregates enforce invariants in code |
| Must it match final class diagrams? | No (Ch2 #2 explicitly says "don't expect this") | Yes — the model IS the code |
| Used for | Shared vocabulary | Invariant enforcement, transaction boundaries |

The kit encodes Ch2 #2 in `iconix-analyst.md` rule 6 ("domain model evolves — don't
expect it to match final class diagrams exactly"). DDD directly contradicts this. No
amount of config tuning resolves the contradiction — it is a deliberate, load-bearing
rule in both methodologies.

**Gap 2 — No Bounded Context / Strategic Design**

DDD requires Strategic Design first:
- Identify Bounded Contexts (each with its own Ubiquitous Language)
- Draw a Context Map (ACL, Shared Kernel, Open Host, Conformist relationships)
- Each context is an autonomous model boundary

The kit has no equivalent concept. `iconix-architect.md` maps use cases to containers
(deployment units), but **container ≠ bounded context**. A bounded context is a
linguistic and model boundary; a container is a runtime deployment unit. They can
coincide, but the identity condition is different. The kit has no agent that identifies
or enforces linguistic boundaries between contexts.

**Gap 3 — No DDD tactical patterns in the traceability chain**

DDD tactical design requires specific patterns to appear in the codebase:
- **Aggregate** — consistency boundary that enforces invariants; only the Aggregate Root
  is accessible from outside
- **Value Object** — immutable, identity-less; equality by value
- **Domain Service** — logic that doesn't belong to any single entity
- **Domain Event** — something that happened in the domain; emitted by Aggregates
- **Repository** — abstraction for persistence (one per Aggregate Root)
- **Factory** — creates complex Aggregates

The current traceability chain (`REQ → UC → RB → SD → CLS → TC`) has no slot for any of
these. The robustness diagram distinguishes Boundary / Controller / Entity, but Entity
on an RB is any real-world object — not an Aggregate with enforced invariants. A
developer cannot derive "which classes should be Aggregate Roots" from the kit's current
output.

### Why this isn't a kit defect

The kit correctly implements ICONIX. ICONIX was not designed to produce DDD output —
Rosenberg's book predates Evans' DDD book (2003 vs 2007) but DDD was not on the ICONIX
radar. The gap is a *methodology fit* problem, not a kit correctness problem. Running
both methodologies end-to-end on the same project is not documented anywhere in either
book; this backlog entry is proposing new intellectual territory, not a bug fix.

### Proposed solution

Add a DDD mode activated by `ddd.enabled: true` in `iconix.config.yaml`. The normal
ICONIX pipeline runs unchanged when `ddd.enabled: false` (the default). When enabled,
two new phases are inserted and three existing agents gain DDD-awareness.

The pipeline becomes:

```
REQ → Domain Model (glossary) → UCs → [M1]
  → DDD Strategic Design (BC identification + Context Map)   ← NEW Phase 2.5
  → Analysis / RBs
  → DDD Tactical Design (Aggregate design + Domain Events)   ← NEW Phase 3.5
  → Architecture fit (BC → container mapping)
  → [M2] → SDs → Code/Tests → [M3]
```

The traceability chain is extended:

```
Before DDD mode:  REQ → UC → RB → SD → CLS → TC
After DDD mode:   REQ → BC → UC → RB → AGG → SD → CLS → TC
```

---

#### Layer 1 — Config (no methodology surface change)

Add to `templates/iconix.config.yaml`:

```yaml
ddd:
  enabled: false                        # opt-in; false = ICONIX unchanged
  bounded_context_policy: strict        # strict = 1 BC = 1 service; relaxed = 1 BC = 1 module
  aggregate_root_ownership: per_context # each BC owns its own Aggregate Roots
  event_sourcing: false                 # enable Domain Event capture in AGG artifacts
```

Add to `iconix-init.ps1` / `iconix-init` installer: new folders when `ddd.enabled`
is set during install:
- `bounded-contexts/` — BC-XXX definition files
- `context-map/` — Context Map diagram
- `aggregates/` — AGG-XXX design files
- `domain-events/` — DE-XXX event definitions

---

#### Layer 2 — New agent: `iconix-ddd-strategic`

**Purpose:** Identify Bounded Contexts from REQs + UC list; produce Context Map.

**Invoked:** After M1, before Analyst (Phase 2.5). Only when `ddd.enabled: true`.

**Inputs:**
- `requirements/REQ-*.md`
- `use-cases/UC-*.md` (preliminary, may be incomplete)
- `domain-model/domain-model.puml` (initial PO draft)

**Process:**
1. **Linguistic scan** — Group domain objects by the team or actor that "owns" the
   language. Objects that mean different things to different actors are a bounded-context
   boundary signal (e.g., "Customer" means `Prospect` in Sales and `Account` in Billing).
2. **Autonomy test** — For each candidate boundary: could this group evolve independently
   without breaking other groups? If yes → separate BC.
3. **Relationship classification** — For each BC-to-BC link: is the upstream BC the
   authority (Open Host), does the downstream adapt (ACL), or do both share a model
   (Shared Kernel)? Record as Context Map relationship.
4. **Ubiquitous Language per context** — Write the canonical term list for each BC.
   Any UC that uses a term from another BC's language is flagged as a cross-context UC
   (may need to be split or routed through an ACL).

**Artifacts produced:**
- `bounded-contexts/BC-XXX-<slug>.md` — one per context:
  ```markdown
  ## BC-001: Ordering
  **Core domain:** yes / no / supporting
  **Actors:** Customer, Order Manager
  **Ubiquitous Language:** Order, LineItem, Cart, Checkout
  **REQs in scope:** REQ-001, REQ-003, REQ-007
  **UCs in scope:** UC-001, UC-003
  ## Traceability
  Parent REQs: REQ-001, REQ-003
  ```
- `context-map/context-map.puml` — PlantUML diagram of all BCs and relationships
  (ACL, Shared Kernel, Open Host, Conformist, Partnership)

**Gate rule:** Analyst cannot start until every UC is assigned to ≥1 BC. An
unassigned UC is a strategic design gap — STOP and resolve.

---

#### Layer 3 — New agent: `iconix-ddd-tactical`

**Purpose:** Derive Aggregate design, Domain Events, and Repository/Factory interfaces
from robustness diagrams and BC definitions.

**Invoked:** After Analyst (RBs complete), before Architect (Phase 3.5). Only when
`ddd.enabled: true`.

**Inputs:**
- `robustness/RB-*.puml` — Entity / Controller / Boundary nodes
- `bounded-contexts/BC-XXX-*.md` — language and scope per context
- `domain-model/domain-model.puml` — current state after Analyst refinement

**Process:**
1. **Entity classification** — For each Entity node across all RBs, classify:
   - Is it referenced from multiple Controllers as the *primary consistency unit*? → Aggregate Root candidate
   - Does it have identity but is never the root of operations? → Entity inside an Aggregate
   - Is it immutable and equality-by-value? → Value Object
   - Does it perform domain logic but doesn't map to a real-world thing? → Domain Service
2. **Invariant extraction** — For each Aggregate Root: list the invariants that must
   hold on save (derived from business rules in `docs/business-rules.md` if present,
   or from UC alternate courses that mention validation / rejection).
3. **Domain Event identification** — For each Controller that changes state on an
   Entity: identify the resulting Domain Event (e.g., "Validate Order" → `OrderPlaced`).
   Events are named in past tense.
4. **Boundary-to-Repository mapping** — Each Outbound Boundary on an RB that accesses
   persistent state maps to a Repository interface for its Aggregate Root.
5. **Factory identification** — Aggregate Roots with complex creation logic (≥3
   constructor parameters, or creation requires other Aggregates) → Factory candidate.

**Artifacts produced:**
- `aggregates/AGG-XXX-<slug>.md` — one per Aggregate Root:
  ```markdown
  ## AGG-001: Order
  **Aggregate Root:** Order
  **Bounded Context:** BC-001 (Ordering)
  **Entities inside:** OrderLineItem
  **Value Objects inside:** Money, Address
  **Invariants:**
  - Order.TotalAmount ≥ 0
  - Order cannot be Confirmed if any LineItem.Quantity = 0
  **Domain Events emitted:** OrderPlaced, OrderCancelled
  **Repository interface:** IOrderRepository (CRUD + FindByCustomer)
  **Factory:** OrderFactory (when creation requires PricingService)
  ## Traceability
  Source RBs: RB-001, RB-003
  Parent BC: BC-001
  Related UCs: UC-001, UC-003
  ```
- `domain-events/DE-XXX-<slug>.md` — one per event:
  ```markdown
  ## DE-001: OrderPlaced
  **Emitted by:** AGG-001 (Order)
  **Trigger:** "Confirm Order" Controller on RB-001
  **Payload:** OrderId, CustomerId, TotalAmount, PlacedAt
  **Consumers:** BC-002 (Inventory) via ACL, BC-003 (Notification)
  ## Traceability
  Source UC: UC-001
  Source RB: RB-001 (Controller: Confirm Order)
  ```

**Gate rule:** Every Aggregate Root must have ≥1 invariant. An Aggregate Root with
no invariants is just a data container — flag for Analyst review (may be a Value Object
or a misclassified Entity).

---

#### Layer 4 — Modified existing agents

**`iconix-analyst.md` — DDD annotation mode**

When `ddd.enabled: true`, the Analyst adds DDD stereotypes to Entity nodes on
robustness diagrams:
- `[AR]` — Aggregate Root candidate
- `[VO]` — Value Object candidate
- `[DS]` — Domain Service candidate

This does NOT change the robustness diagram rules (the four allowed connection pairs
still apply). It adds metadata for `iconix-ddd-tactical` to consume in Phase 3.5.

Critical note: This is a **conscious override of Ch2 #2** ("don't expect domain model
to match final class diagrams"). In DDD mode, the Analyst is explicitly building
toward a model that WILL match the Aggregate structure in code. The process reference
matrix must document this as an intentional deviation.

**`iconix-architect.md` — Bounded Context → container mapping**

When `ddd.enabled: true`, the Architect gains three new responsibilities:

1. **BC-to-container assignment** — Each Bounded Context maps to ≥1 container. When
   `bounded_context_policy: strict`, one BC = one service (microservice or deployable
   module). When `relaxed`, one BC = one module inside a monolith or shared service.
   Record in `docs/architecture/package-map.md` with a new "Bounded Context" column.

2. **Cross-BC communication ADR** — Every Context Map relationship that crosses a
   container boundary requires an ADR:
   - ACL → ADR: "Anti-corruption Layer between BC-001 and BC-002; Adapter class in
     Infrastructure container; maps BC-002's `Account` to BC-001's `Customer`"
   - Shared Kernel → ADR: "Shared Kernel between BC-001 and BC-003; shared types in
     `SharedKernel` package; changes require both teams to agree"
   - Open Host → ADR: "BC-002 exposes Open Host (REST API); downstream BCs must not
     reference BC-002's internal model directly"

3. **Domain Event routing** — If `event_sourcing: true`, raise an ADR for the event
   bus strategy (in-process domain events vs. message broker).

**`iconix-orchestrator.md` — DDD phase routing**

Add to `# Phase order you enforce`:

```
2.5. DDD Strategic Design (iconix-ddd-strategic) — runs after M1, before Analyst.
     SKIP when ddd.enabled: false.
     GATE: every UC assigned to ≥1 BC before Analyst can start.

3.5. DDD Tactical Design (iconix-ddd-tactical) — runs after Analyst RBs, before Architect.
     SKIP when ddd.enabled: false.
     GATE: every RB Entity node has DDD annotation; every AGG-XXX has ≥1 invariant.
```

Add to routing heuristics:
- `bounded-contexts/` empty + `ddd.enabled: true` → `iconix-ddd-strategic`
- RBs exist + `aggregates/` empty + `ddd.enabled: true` → `iconix-ddd-tactical`

**`iconix-traceability.md` — Extended chain validation**

When `ddd.enabled: true`, the traceability chain becomes:
```
REQ → BC → UC → RB → AGG → SD → CLS → TC
```

Additional validation rules:
- Every UC must link to ≥1 BC (via `Parent BC:` field in UC frontmatter)
- Every AGG-XXX must link to ≥1 RB (via `Source RBs:` in the AGG file)
- Every DE-XXX must link to the Controller node that emits it
- Orphan check: an Entity in any RB that has no corresponding AGG entry is a tactical
  design gap — flag at M2 gate when `ddd.enabled: true`

---

#### New artifact templates needed

| Template file | Used by |
|---|---|
| `templates/bounded-context-template.md` | `iconix-ddd-strategic` |
| `templates/context-map-template.puml` | `iconix-ddd-strategic` |
| `templates/aggregate-template.md` | `iconix-ddd-tactical` |
| `templates/domain-event-template.md` | `iconix-ddd-tactical` |

---

### Roadmap to implementation

Estimated ~8 commits. Order matters — each step is independently testable and
does not break the existing ICONIX pipeline.

**Commit 1 — Config + installer (no methodology surface)**
- Add `ddd:` block to `templates/iconix.config.yaml`
- Add new folders (`bounded-contexts/`, `context-map/`, `aggregates/`,
  `domain-events/`) to `iconix-init.ps1` and `iconix-init` installer
- Update `README.md` Project layout section
- Update `iconix-state-machine.puml` to show DDD phases as conditional branches
- CHANGELOG bump

**Commit 2 — Artifact templates (no methodology surface)**
- Create the four templates above
- Update `README.md` Project layout to list them
- CHANGELOG bump

**Commit 3 — `iconix-ddd-strategic` agent**
- Write the agent from scratch (linguistic scan → autonomy test → relationship
  classification → Ubiquitous Language output)
- Add `name:` and `description:` frontmatter; wire tools (`Read, Grep, Glob, Write`)
- Add to CI frontmatter lint + uniqueness check
- CHANGELOG bump + process reference matrix: add new "DDD Strategic" row

**Commit 4 — `iconix-ddd-tactical` agent**
- Write the agent from scratch (entity classification → invariant extraction →
  domain event identification → boundary-to-repository mapping → factory detection)
- Add `name:` and `description:` frontmatter; wire tools
- Add to CI frontmatter lint + uniqueness check
- CHANGELOG bump + process reference matrix: add new "DDD Tactical" row

**Commit 5 — `iconix-analyst.md` DDD annotation**
- Add DDD annotation block (gated on `ddd.enabled: true`) to the entity
  classification section
- Document Ch2 #2 override explicitly in the agent and in the process reference
  matrix (status changes from ✅ to ⚠️ with note: "overridden in DDD mode")
- Token budget check before and after
- CHANGELOG bump

**Commit 6 — `iconix-architect.md` DDD responsibilities**
- Add BC-to-container assignment rule, cross-BC ADR trigger, Domain Event routing
  rule (all gated on `ddd.enabled: true`)
- Update PDR readiness checklist to include DDD checks
- Token budget check before and after
- CHANGELOG bump

**Commit 7 — `iconix-orchestrator.md` DDD routing**
- Add Phase 2.5 and Phase 3.5 with their SKIP and GATE conditions
- Add DDD-specific routing heuristics
- Token budget check before and after
- CHANGELOG bump

**Commit 8 — `iconix-traceability.md` extended chain**
- Add DDD chain validation (BC → UC, AGG → RB, DE → Controller)
- Add orphan checks for DDD mode M2 gate
- Update M1/M2/M3 gate checklists with DDD conditions (gated on `ddd.enabled: true`)
- Token budget check before and after
- CHANGELOG bump + process reference matrix: update Summary Coverage Matrix counts

### Process reference matrix impact

Every Commit 3–8 is a methodology-surface change requiring a theory audit per the
CLAUDE.md rule. The audits should be batched per commit:

- Commit 3: no existing ICONIX rule is violated (Strategic Design is additive)
- Commit 4: no existing ICONIX rule is violated (Tactical Design is additive)
- Commit 5: **Ch2 #2 override** — must cite the rule, document the deviation, and
  change status from ✅ to ⚠️ in the matrix
- Commits 6–8: additive to existing rules; no overrides expected

### Open questions

- **Is DDD mode a superset or a fork of ICONIX?** If `ddd.enabled: true` overrides
  Ch2 #2, the kit is no longer a faithful ICONIX implementation in that mode. The
  README must clearly state this. Decision: call it "ICONIX + DDD hybrid mode" and
  document it as a deliberate extension, not a core feature.

- **Should Bounded Contexts replace or augment UC packages?** UC packages (`use-case-packages/`)
  are PO-owned groupings by actor/goal. BCs are linguistically-bounded design units.
  They often overlap but are not the same. Option A: keep both separately. Option B:
  make BCs the primary grouping and deprecate UC packages in DDD mode.

- **Event Sourcing scope.** `event_sourcing: true` in config enables Domain Event
  capture in AGG artifacts. Should the kit also generate event store schema or
  projection skeletons? That is deep implementation territory — probably a v2 of DDD
  support.

- **CQRS alignment.** Many DDD projects use CQRS (Command Query Responsibility
  Segregation). The robustness diagram's Boundary/Controller/Entity maps loosely to
  CQRS Command Side, but the Read side (Query) has no representation. This is
  likely a Phase 2 extension.

- **Methodology audit depth.** The DDD canon (Evans, 2003; Vernon, 2013) is not
  in the kit's reference set. The process reference matrix cites Rosenberg & Stephens
  only. Adding DDD support means the kit needs a second reference column in the matrix
  citing Evans for DDD rules. This is a documentation-only change but a notable one.

### Rejected alternatives

- **Map DDD patterns onto existing ICONIX artifacts without new agents.**
  Considered. The Analyst's robustness diagram could carry `[AR]` / `[VO]` annotations
  without a separate Tactical Design agent. But the invariant extraction, Domain Event
  identification, and Repository interface generation require reasoning that is distinct
  from robustness analysis — collapsing them into the Analyst agent would violate the
  single-responsibility rule in `CLAUDE.md` `## Agent prompt discipline`.

- **Replace ICONIX with DDD entirely.**
  Considered. DDD's Strategic Design is superior for microservice boundary identification.
  But ICONIX's Use Case pipeline is superior for requirements traceability and test
  derivation. The hybrid approach gets both; a full replacement loses ICONIX's
  traceability chain, which is the kit's primary value proposition.

- **Use Event Storming as the primary input instead of robustness diagrams.**
  Considered. Event Storming is a discovery workshop technique — it requires a live
  facilitated session with domain experts. It cannot be mechanized into an agent without
  reducing it to a checklist that misses the point. The kit can use Event Storming
  output as input (a transcript or sticky-note dump), but it cannot replace the session
  itself. Deferred to future work.
