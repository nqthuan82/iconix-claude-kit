# Phase 9 Cycle Log — UC-XXX

> Created at **9.1 kickoff** by the Orchestrator (one file per UC, when `phase9.enabled: true`).
> Iteration rows are appended by the Orchestrator after each **9.2 Reviewer verdict**.
> The Exit section is filled at **9.4 merge**.
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
>
> **`Reviewer verdict` column** — use ONE of the four discrete tokens
> exactly (machine-readable for `iconix-metrics` to compute Phase 9
> iteration-count distributions per UC). Optional context after a
> dash, no other prefix:
>
> - `APPROVE` — clean review; proceed to 9.4
> - `APPROVE WITH NOTES` — approved with non-blocking [INFO] findings
> - `REQUEST CHANGES` — drift findings; back to 9.3 (Developer + Tester)
> - `BLOCK MERGE` — multiple findings or NFR violations; back to 9.3
>
> Token must appear at the start of the cell. Free-text-only verdicts
> (e.g., "looks good") are an audit-trail smell and break metrics.

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
