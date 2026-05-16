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
