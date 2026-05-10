# ICONIX Metrics Snapshot — <date>

> Produced by the iconix-metrics agent on demand or in CI. Snapshot-based:
> reads current artifact state + git history at run-time. Companion
> machine-readable file: `metrics/snapshot-<date>.json`.
>
> This document is an **audit artifact** — preserve it under your
> retention policy (default: 12 most recent snapshots).

## Project

- **Name:** <project name>
- **Prefix:** <PRJ>
- **Snapshot generated:** <ISO timestamp>
- **Git HEAD:** <short SHA>
- **Compared to:** <prior snapshot path, if trend mode>

---

## 1. Throughput

| Metric | Total | Last 30 days | Last 7 days |
|---|---|---|---|
| Use cases (total)     | NN  | NN | NN |
| Requirements          | NN  | NN | NN |
| Bug reports filed     | NN  | NN | NN |

### Use cases by phase
| Phase | Count | % of total |
|---|---|---|
| M1 (in requirements)            | NN | NN% |
| M2 (in preliminary design)      | NN | NN% |
| M3 (in critical design)         | NN | NN% |
| Implementation (in flight)      | NN | NN% |
| Done (merged to main)           | NN | NN% |

### Bug type distribution (Type 2 ratio is the headline)
- Type 1 (implementation): NN
- Type 2 (design): NN
- **Type 2 / total ratio: 0.NN** — high ratio (>0.30) suggests upstream design quality issues; very low (<0.05) may suggest the bug-flow is being bypassed

---

## 2. Cycle time

> Days from phase entry to phase pass, per UC. Measured from git commit
> dates on `[<UC>] <phase>: ...` commits.

| Phase transition | Median (days) | p90 (days) | Samples |
|---|---|---|---|
| M1 entry → M1 pass             | N.N | N.N | NN |
| M1 pass → M2 pass              | N.N | N.N | NN |
| M2 pass → M3 pass              | N.N | N.N | NN |
| M3 pass → Implementation merge | N.N | N.N | NN |
| Branch creation → merge        | N.N | N.N | NN |

If the M3-to-merge gap is the largest, your bottleneck is implementation throughput. If the M1-to-M2 gap dominates, the analysis/design phase is the constraint.

---

## 3. Quality

### Milestone gate failure rates
| Gate | Pass | Fail | Failure rate | Top failure causes |
|---|---|---|---|---|
| M1 | NN | NN | NN% | <e.g., orphan UCs (3); missing alternate courses (2)> |
| M2 | NN | NN | NN% | <e.g., RB rule violations (4); attribute-untyped (2)> |
| M3 | NN | NN | NN% | <e.g., test plan missing (1); class-attribute sparse (3)> |

### Drift findings per Implementation PR (Reviewer reports)
- Median drift findings per PR: NN
- Max drift findings on a single PR: NN
- Total drift findings last 30 days: NN
- Top recurring drift patterns:
  - <pattern 1 — e.g., method exists in code but not on SD (8 occurrences)>
  - <pattern 2>

### Concurrent-touch outcomes (v0.9.6)
- HIGH conflicts detected at M2 last 30 days: NN
  - Resolved (architecture change): NN
  - Accepted (`[CT-ACCEPT-XXX]`): NN
- MEDIUM coordination notes: NN
- LOW informational: NN

### Traceability hygiene
- Orphan UCs (no package entry): NN
- Ghost UCs (package entry, no file): NN
- Title-drifted UCs: NN
- Dangling cross-package links: NN

---

## 4. Process compliance (audit evidence)

These are the metrics ISO auditors care about most. Aim for ≥95% on all four.

| Metric | Value | Notes |
|---|---|---|
| % of UCs that passed all 3 gates           | NN.N% | Target ≥ 95% |
| % of source files with valid Traceability  | NN.N% | Target = 100%; CI gate enforces |
| % of REQs with ≥1 downstream UC            | NN.N% | Target = 100% (Traceability enforces) |
| % of NFRs with covering ADR / container    | NN.N% | Target ≥ 90% |

If a metric is below target, the corresponding section above lists the failing artifacts so the team can act.

---

## 5. Trend (when comparison snapshot exists)

> Filled in when prior snapshots are present. Skipped on first run.

Compared to **<prior snapshot date>** (NN days ago):

| Metric | Δ |
|---|---|
| UC throughput (last 30d)            | +N or -N |
| Type 2 / total ratio                | +0.NN or -0.NN |
| M2 gate failure rate                | +0.NN or -0.NN |
| Median branch-to-merge cycle (days) | +N.N or -N.N |
| Drift findings per PR (median)      | +N or -N |
| Process compliance (avg of 4 KPIs)  | +0.NN or -0.NN |

**Direction notes:** ✅ improving, ⚠️ degrading, ➖ flat (Δ within ±5%).

---

## 6. Blockers and stale state

> Items the team should action this week.

- <e.g., UC-024 has been on `feature/UC-024-discount-cart` branch for 35 days with no Implementation PR — investigate or close>
- <e.g., REQ-091 has no downstream UC and was added 12 days ago — Product Owner should resolve>
- <e.g., 2 source files merged to main without Traceability comments — pre-merge gate may be misconfigured>

---

## Methodology footnote (for ISO audits)

ICONIX itself does not prescribe project-wide metrics — this is a kit
extension supporting Ch11 #6 ("Use data gathered during the review to
accumulate boilerplate checklists for future reviews") extended to
project-wide aggregation, and the Code-Inspection-vs-Code-Review
sidebar in Ch11 acknowledging that formal code inspections gather
metrics. See `docs/iconix/iconix-process-reference.md` and
`docs/iconix/metrics-glossary.md`.

## Traceability

- Snapshot generator: `agents/iconix-metrics.md` (kit version v0.9.7+)
- Source artifacts read:
  - `requirements/`, `use-cases/`, `robustness/`, `sequence/`, `class-model/`, `test-cases/`, `adrs/`, `nfr-annotations/`
  - `milestone-reports/M[1-3]-*.md`
  - `reviews/REVIEW-*.md`, `reviews/review-checklist.md`
  - `change-impact/CT-*.md` (concurrent-touch reports), `change-impact/CI-*.md` (change-impact reports)
  - `bug-reports/BUG-*.md`
  - `git log` from project inception (or `metrics.git_history_window` if set)
- Companion JSON: `metrics/snapshot-<date>.json` (schema: `docs/iconix/templates/metrics-schema.json`)
