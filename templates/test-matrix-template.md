# Test Matrix — `<Project Name>`

> Living matrix: REQ-ID ↔ UC-ID ↔ TC-ID ↔ automated-test-file ↔
> last-run-status. Maintained by the Tester; updated whenever a TC is
> added, modified, run, or superseded.
>
> Save at the project root as `test-matrix.md`.
>
> Read by:
> - Tester: per `# Coverage gates (run before release)` — "test-matrix.md
>   is current (no orphan TCs, no uncovered UCs)"
> - Traceability: at the M3 gate, validates the matrix's TC↔UC links
>   match the TC files' Traceability blocks
> - Reviewer: at Phase 9 PRs, checks the `Last run` column to confirm
>   tests have actually been executed (not just authored)
> - `iconix-metrics`: parses `Pass / Fail / Skip` counts to compute test-
>   pass-rate metrics over time

## How to read this file

- **REQ → UC → TC chain** is the canonical traceability per kit
  `Traceability:` rules. Each row may list multiple TCs per UC.
- **Last run** captures `<status> @ <YYYY-MM-DD HH:MM>` from the most
  recent CI run. `(never)` for unrun TCs.
- **Status** values:
  - `Pass` — most recent run green
  - `Fail` — most recent run red (action required; cite the failing
    assertion in the row's Notes)
  - `Skip` — explicitly skipped (waiver required in Notes)
  - `Pending` — TC authored but no implementation yet (Phase 9.1 in
    flight)
  - `Superseded` — replaced by another TC; cite supersedor in Notes

## Coverage table

> One row per (REQ, UC) pair. Add rows for new UCs as they're authored.

| REQ | UC | TCs (active) | Type breakdown | Automated test files | Last run | Status | Notes |
|---|---|---|---|---|---|---|---|
| `<PREFIX>-REQ-001` | `<PREFIX>-UC-001` | `TC-001, TC-002, TC-003` | 1 system / 2 unit | `tests/Bookstore.SystemTests/WriteCustomerReviewSystemTests.cs`<br>`tests/Bookstore.Domain.UnitTests/CustomerReviewValidationTests.cs` | `Pass @ 2026-05-09 14:23` | All passing | — |
| `<PREFIX>-REQ-001` | `<PREFIX>-UC-001` | `TC-021` | 1 regression | `tests/Bookstore.Domain.UnitTests/CustomerReviewValidationTests.cs` (test name: `Title_Must_Be_5_To_120_Characters`) | `Pass @ 2026-05-09 14:23` | All passing | Supersedes TC-003 after BS-CI-001 (2026-05-04) |

## Superseded TC ledger

> When a TC is superseded by a regression TC (per change-impact event),
> record the supersession here. Do NOT delete the superseded TC's file —
> keep it for audit and git-log clarity.

| Superseded TC | Superseded by | Triggered by | Date | Reason |
|---|---|---|---|---|
| `<PREFIX>-TC-003` | `<PREFIX>-TC-021` | `change-impact/BS-CI-001-...md` | 2026-05-04 | Title-length validation rule added; original TC's expected results no longer match the corrected UC. |

## Orphan / gap audit

> Run this audit at every M3 gate and before every release. The Tester's
> coverage gate fails if any of these tables has rows.

### Orphan TCs (TCs whose UC has been removed or renamed)
| TC | Cited UC | Issue |
|---|---|---|
| (none) | | |

### Uncovered UCs (UCs in scope with zero active TCs)
| UC | Phase | Reason |
|---|---|---|
| (none) | | |

### Stale automation entries (matrix cites a test file that no longer exists)
| TC | Cited test file | Issue |
|---|---|---|
| (none) | | |

## Traceability
- Drives: M3 gate (Traceability check #4 — every TC cites exactly 1 UC), Reviewer Phase 9 checks, `iconix-metrics` test-pass-rate metric
- Companion: `test-cases/`, `test-plan/test-plan-<date>.md`
