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

### Why full automation is impractical

Before describing the proposed solution, three reasons the originally designed 8-commit
full-integration plan (two new agents + three modified agents + extended traceability
chain) is unlikely to deliver value proportional to its cost:

**1. DDD value lives in conversations, not artifacts**

Bounded Context identification and Aggregate design emerge from intensive, iterative
workshops (Event Storming, domain modeling sessions) with domain experts. The raw
material those workshops produce — which terms mean different things to different teams,
which invariants are non-negotiable, which state transitions are the core of the domain —
is not present in REQs and UCs. An agent deriving Aggregate Roots from robustness
diagram Entity nodes will produce artifacts that are syntactically correct DDD but
semantically shallow. A team reading `AGG-001: Order` with auto-derived invariants may
trust the artifact and skip the workshop that would have revealed the real complexity.
This is worse than having no DDD artifact at all.

Concrete example: REQs and UCs say "Customer places order". An agent assigns `Order`
as Aggregate Root. But in the real domain, `Cart` is the Aggregate Root that enforces
pricing invariants, and `Order` is just a point-in-time snapshot after checkout. The
agent cannot know this from the written artifacts — only domain expert discussion reveals
it.

**2. ICONIX pipeline gates conflict with DDD's iterative discovery**

The pipeline enforces: "every UC must be assigned to ≥1 BC before Analyst starts."
But BC boundaries often only become clear *during* robustness analysis — when you draw
the RB for UC-003 and discover that `Account` (owned by Billing) and `Customer` (owned
by Ordering) are actually the same object, and that resolving the ambiguity forces a BC
boundary decision. Making BC assignment a gate *before* RBs means the gate fires at
the worst moment: before the information needed to answer it exists. Forcing an answer
early produces premature, brittle BC boundaries that need to be revisited after M2.

**3. The complexity-to-target-audience mismatch**

Teams that truly need DDD typically already have DDD practitioners who would not trust
auto-derived Aggregates. Teams without DDD experience would be handed a new layer of
concepts (Aggregate Root, Value Object, Domain Event, Context Map) on top of an already
novel methodology (ICONIX). The cognitive load doubles while the guidance on *how to do
DDD correctly* is absent — the agent produces artifacts but cannot teach the team why
Aggregate boundaries matter.

### Revised proposed solution

The real gap in the current kit is narrower and more tractable: **`iconix-architect.md`
maps UCs to containers but gives no guidance on where container boundaries should be.**
Teams using the kit can produce technically correct container mappings that cut across
natural domain boundaries — splitting what should be one service, or merging what should
be two. A team walking away from Phase 4 without thinking about linguistic boundaries
has missed the most important architectural decision.

The fix is a **guided strategic design checklist embedded in `iconix-architect.md`**,
not a new agent. When the Architect is about to draw `docs/architecture/package-map.md`,
surface three DDD-derived questions:

> **Before assigning UCs to containers, answer these questions for each candidate
> service boundary:**
>
> 1. **Linguistic test** — Does any domain term in this container mean something
>    different to a different actor or team? If yes, that difference signals a boundary.
>    (e.g., "Customer" = Prospect in Sales, Account in Billing → boundary exists)
>
> 2. **Autonomy test** — Could this group of UCs be deployed or changed independently
>    without coordinating with the team that owns adjacent UCs? If yes → strong
>    candidate for a separate container.
>
> 3. **Invariant ownership test** — Which container is the authoritative enforcer of
>    the most critical business rules? That container is your core domain service.
>    Other containers that call into it are downstream — model their relationship
>    explicitly (ACL, Open Host, Shared Kernel) rather than letting it be implicit.
>
> Record the answers in the "Bounded Context reasoning" field of
> `docs/architecture/package-map.md`. An empty field is a signal that the boundary
> was not consciously chosen.

This approach:
- Adds zero new agents and zero new artifact types
- Does not touch the traceability chain
- Does not require a Ch2 #2 override (no change to domain model philosophy)
- Surfaces the right DDD questions at the right moment (when container boundaries
  are being decided, not before RBs exist)
- Teams with DDD practitioners can go deeper using the vocabulary the checklist
  introduces; teams without them get the minimum they need to avoid the worst mistakes

#### What changes

**`iconix-architect.md`** — add a `# Bounded Context reasoning` section before
`# Decision rules`. The section contains the three-question checklist above and
mandates a "Bounded Context reasoning" column in `docs/architecture/package-map.md`.

**`templates/architecture-package-map-template.md`** — add the new column.

**`docs/architecture/package-map.md` PDR readiness checklist** — add one entry:
`[ ] Every internal package row has a non-empty "Bounded Context reasoning" field
    (per Architect # Bounded Context reasoning)`.

No new folders, no installer changes, no config flag, no new agent names to register
in CI.

### Roadmap to implementation

Estimated ~2 commits. Both are tooling-adjacent, not methodology-surface.

**Commit 1 — `iconix-architect.md` + template**
- Add `# Bounded Context reasoning` section to `iconix-architect.md` with the
  three-question checklist (linguistic / autonomy / invariant ownership)
- Add "Bounded Context reasoning" column to
  `templates/architecture-package-map-template.md`
- Add PDR readiness checklist item for the new column
- Token budget check before and after
- CHANGELOG bump

**Commit 2 — Process reference matrix**
- Add row for "Bounded Context / Strategic Design guidance" in the Chapter 2 table
  of `docs/iconix/iconix-process-reference.md`
- Status: ⚠️ Partial — questions are surfaced but BC identification is not enforced
  as a gate condition (deliberate; see "Why full automation is impractical" above)
- CHANGELOG bump

### Open questions

- **Should the checklist become a soft gate at M2?** The PDR readiness checklist
  currently requires non-empty "Bounded Context reasoning" fields but does not block
  M2 if a team consciously leaves them empty with a note. A stricter version would
  make empty fields a hard M2 blocker. Risk: adds friction for small projects where
  one service makes the question moot.

- **Should teams that already did Event Storming be able to import results?**
  The checklist as designed is for teams that have not done Event Storming. Teams
  that have could provide a summary of their BC decisions and the Architect would
  simply record them. No change needed — the checklist is additive either way.

- **Methodology audit depth.** The DDD canon (Evans, 2003; Vernon, 2013) is not in
  the kit's reference set. The process reference matrix cites Rosenberg & Stephens
  only. The new matrix row should note "guided by DDD Strategic Design vocabulary
  (Evans, 2003)" without claiming full DDD compliance.

### Rejected alternatives

- **Full 8-commit integration: two new agents (`iconix-ddd-strategic` +
  `iconix-ddd-tactical`) + three modified agents + extended traceability chain.**
  Considered and rejected. The tactical agent auto-derives Aggregates from robustness
  diagram Entity nodes — a mapping that is too shallow to produce trustworthy DDD
  artifacts (see "Why full automation is impractical" above). The strategic agent fires
  a BC-assignment gate before RBs exist, which is the wrong moment: BC boundaries often
  only become clear *during* robustness analysis. The complexity cost (~8 commits,
  2 new agent files, 3 modified agents, 4 new templates, extended traceability chain)
  is not justified when the practical benefit is a checklist-level prompt, not genuine
  DDD enforcement. The full design is preserved in the v1.0.70 version of this entry
  for reference if future requirements change this assessment.

- **Replace ICONIX with DDD entirely.**
  Considered. DDD's Strategic Design is superior for microservice boundary
  identification. But ICONIX's Use Case pipeline is superior for requirements
  traceability and test derivation. The hybrid approach described above gets the
  most value from each; a full replacement loses ICONIX's traceability chain, which
  is the kit's primary value proposition.

- **Use Event Storming as the primary input instead of robustness diagrams.**
  Considered. Event Storming is a discovery workshop technique requiring live
  facilitation with domain experts. It cannot be mechanized into an agent. The kit
  can accept Event Storming *output* as input to the Architect's BC reasoning, but
  cannot replace the session itself.
