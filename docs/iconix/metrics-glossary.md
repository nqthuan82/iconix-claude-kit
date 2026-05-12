# ICONIX Metrics Glossary

Authoritative definitions for every metric the kit produces. If a dashboard or audit question depends on a metric, check this glossary first to verify the definition matches your interpretation.

> **Stable** — these definitions are versioned with the JSON schema. Breaking changes bump the schema version (currently `1.0`).

---

## 1. Throughput

### use_cases.total
Count of files matching `use-cases/UC-*.md` at snapshot time. Includes UCs in any phase, including Done.

### use_cases.by_phase
Each UC's current phase, derived from git history:
- **M1** — UC file exists; no `[<UC>] M1: ...` commit on `main` yet.
- **M2** — `[<UC>] M1: ...` commit on `main`; no `[<UC>] M2: ...` yet.
- **M3** — `[<UC>] M2: ...` on `main`; no `[<UC>] M3: ...` yet.
- **Implementation** — `[<UC>] M3: ...` on `main`; `[<UC>] Impl: ...` commit exists (anywhere) but not yet merged.
- **Done** — `[<UC>] Impl: ...` merged to `main`.

A UC counted as "Done" may still receive `[BUG-T1]` / `[BUG-T2]` fixes — those don't change phase.

### bugs.type_2_ratio
`bugs.type_2 / bugs.total`. Counted from branches matching `bugfix/T1-*` and `bugfix/T2-UC-*-*`. **Healthy range:** 0.10–0.25. Above 0.30 suggests upstream design quality issues; below 0.05 may suggest the bug-flow is being bypassed (Reviewer triage skipped).

---

## 2. Cycle time

All cycle-time metrics are measured in **days** (rounded to nearest 0.1) and reported as `{median, p90, samples}`.

### m1_entry_to_pass_days
For each UC: `commit_date(M1 pass commit) - commit_date(first commit creating the UC file)`. M1 pass = first commit on `main` matching `[<UC>] M1: ...` whose author/co-author includes a Traceability agent confirmation OR a milestone-report file.

### m1_to_m2_pass_days
For each UC: `commit_date(M2 pass) - commit_date(M1 pass)`.

### m2_to_m3_pass_days
For each UC: `commit_date(M3 pass) - commit_date(M2 pass)`.

### m3_to_impl_merge_days
For each UC: `commit_date(Implementation merge to main) - commit_date(M3 pass)`. The Implementation merge is the merge commit that brings `feature/UC-XXX-*` to `main` after CDR.

### branch_to_merge_days
For each UC: `commit_date(merge to main) - commit_date(branch creation)`. Whole-feature lifecycle.

**Caveat:** these depend on commit-message convention (v0.9.5+). UCs created before v0.9.5 may show `null` or be excluded from samples — the snapshot footnote reports excluded counts.

---

## 3. Quality

### gate_failure_rate.{m1, m2, m3}
`gate_failures / (gate_failures + gate_passes)` in the snapshot window. Each milestone-report file at `milestone-reports/M<N>-*.md` is counted. The "Recommendation" line in the report determines pass/fail (`READY` vs `NOT READY`).

### drift_findings_per_pr
Count of distinct findings (drift entries, traceability gaps, NFR concerns, framework/business issues) in `reviews/REVIEW-*.md`, divided by the number of review reports in the snapshot window.

### top_drift_patterns
The five most common drift patterns from `reviews/review-checklist.md`, ranked by occurrence count.

### concurrent_touch_at_m2.high_*
From `change-impact/CT-*.md` reports (v0.9.6+). `high_total = high_resolved + high_accepted + high_unresolved`. Unresolved HIGH conflicts surface as a blocker entry.

### traceability_hygiene.*
Counts from the most recent `orphan-report.md` produced by the Traceability agent. If no recent orphan report exists, the metric reports `null` and a blocker is emitted.

---

## 3.5. Phase 9 loop health (v0.9.8+)

Only populated when `phase9.enabled: true` in `iconix.config.yaml`. All fields are `null` when phase9 is disabled or no `phase9-cycles/` files exist.

### phase9.uc_total
Total count of `phase9-cycles/UC-*-cycle.md` files. One file per UC that entered Phase 9.

### phase9.uc_active
Cycle files where the `## Exit` section's `Final verdict:` is still a placeholder (not `APPROVE` or `APPROVE WITH NOTES`). Represents UCs currently in the implementation loop.

### phase9.uc_done
Cycle files with a completed `## Exit` section. UCs counted here have merged to `main`.

### phase9.iterations_per_uc
Distribution of iteration counts across `uc_done` UCs. Parsed from `Iterations used: N` in each Exit section. `{median, p90, samples}`.

**Healthy range:** median ≤ 2. Median > 3 consistently suggests M3 CDR is approving designs with too many open questions.

### phase9.cap_hit_count
Count of done UCs where `Cap hit? Yes`. These UCs escalated to Architect or PO — effectively Type 2 issues surfaced during implementation.

### phase9.cap_hit_pct
`cap_hit_count / uc_done`. `null` when `uc_done = 0`. **Target < 0.10** — if more than 10% of implementations hit the cap, M3 is not catching enough design issues.

### phase9.first_pass_approve_pct
`UCs where Iterations used = 1 AND Final verdict = APPROVE or APPROVE WITH NOTES / uc_done`. `null` when `uc_done = 0`. **Target > 0.70** — high values indicate M3 design quality is strong and the Reviewer rarely needs a second pass.

---

## 4. Process compliance

These four metrics are the ISO-audit-relevant ones. Target ≥ 0.95 (≥ 0.90 for NFR).

### uc_through_all_3_gates_pct
`UCs in phase Done OR Implementation / total UCs`. Captures whether UCs are following the gated pipeline rather than skipping ahead.

### trace_comment_coverage_pct
`source files with valid Traceability: comment / total source files under src/ and tests/`. Same check as `.ci/validate-traceability.sh`. The CI gate enforces this at 100% on PRs; the metric tracks it on `main`.

### req_with_downstream_uc_pct
`REQs cited by ≥1 UC / total REQs`. Should be 1.00 — the Traceability agent's M1 gate enforces this. Drift here usually means a REQ was added but its UC scope wasn't yet drafted.

### nfr_with_covering_adr_pct
`NFRs in iconix.config.yaml nfr_catalog cited by ≥1 ADR or container-mapping annotation / total NFRs`. Tracks Traceability check #9.

---

## 5. Trend deltas

Computed when `compared_to` is non-null. Each delta is the difference between current and prior values:
- For ratios / percentages: absolute difference (e.g., `+0.05` means improved by 5 percentage points).
- For counts: integer difference.
- For cycle times: difference in days.

The snapshot markdown shows directional emoji (✅ improving / ⚠️ degrading / ➖ flat — within ±5%).

---

## 6. Blockers

Each blocker has a `kind` (enum), `id` (artifact or branch ref), optional `since` and `age_days`, and `detail`. Blockers are not metrics themselves but actionable items that fall out of the metric computation:

| Kind | Triggered when |
|---|---|
| `orphan_uc`             | UC has no entry in any `use-case-packages/*.puml` |
| `ghost_uc`              | Package overview cites a UC-ID that has no file |
| `stale_branch`          | `feature/UC-*` branch with no commit in last 21 days |
| `missing_trace_comment` | source file on `main` lacks Traceability comment |
| `orphan_req`            | REQ has no downstream UC after 14 days |
| `untyped_attribute`     | Class-model attribute declared without type |
| `concurrent_high_unresolved` | HIGH conflict in CT-report not resolved or accepted in M2 PR |

---

## What's *not* a metric (intentional out-of-scope)

- **Code-level metrics** (cyclomatic complexity, test coverage %, LOC) — these are downstream tooling concerns. Use whatever your stack provides.
- **Velocity / story points** — ICONIX is artifact-driven, not story-driven; mapping ICONIX artifacts to agile points is left to the team.
- **Per-developer attribution** — the kit deliberately doesn't compute "drift findings per author" or similar; that's a culture/management concern outside the methodology.
- **Cost / effort estimates** — Ch13 #3 ("estimates from UC scenarios") is marked 🚫 out-of-scope in the process-reference matrix, requires team calibration data the kit doesn't have.
