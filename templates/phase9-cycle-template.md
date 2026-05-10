# Phase 9 Cycle Log — UC-XXX

> **Optional artifact.** Teams that want audit-grade evidence of the
> Phase 9 Developer ↔ Tester ↔ Reviewer loop maintain this file per UC.
> It records each iteration's verdict and exit condition. Skip it if
> your team doesn't need that level of evidence.
>
> Save as `phase9-cycles/UC-XXX-cycle.md`.

## Use case
- **ID:** UC-XXX
- **Title:** <UC title>
- **Branch:** `feature/UC-XXX-<slug>`
- **M3 pass commit:** <SHA, date>
- **Phase 9 entry:** <date>

## Iteration log

> One row per Developer ↔ Tester ↔ Reviewer cycle. Append; never edit
> historical entries. The cap is `phase9.max_iterations_per_uc`
> (default 5) — escalate to Architect/PO if you reach the cap.

| # | Date | Developer state | Tester state | Reviewer verdict | Notes |
|---|---|---|---|---|---|
| 1 | YYYY-MM-DD | initial impl complete | TCs implemented | REQUEST CHANGES — 4 drift findings | see reviews/REVIEW-...-1.md |
| 2 | YYYY-MM-DD | drift fixes applied | regression re-run | APPROVE WITH NOTES | merged via PR #NNN |

## Exit
- **Final verdict:** APPROVE | APPROVE WITH NOTES
- **Implementation merge commit:** <SHA, date>
- **Iterations used:** <N>
- **Cap hit?** No / Yes (escalated to <Architect/Product Owner>)

## Drift patterns observed (for `reviews/review-checklist.md`)
- <if any recurring patterns surfaced during this UC's Phase 9 — copy to
  the project review checklist so future UCs benefit from the lesson>

## Traceability
- UC: UC-XXX
- RB: RB-XXX
- SD: SD-XXX
- Reviewer reports: <list of REVIEW-*.md files referenced above>
- PR: <provider PR URL>
