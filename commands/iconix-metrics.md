---
description: "Produce an ICONIX metrics snapshot (markdown + JSON) for the project. Audit-friendly. Snapshot-based; reads current artifact state and git history."
argument-hint: "[trend]   # optional: also produce a trend report comparing to the prior snapshot"
---

Invoke the iconix-metrics agent with: $ARGUMENTS

The agent should:

1. Read `iconix.config.yaml` `metrics:` section (defaults if missing: `enabled: true, output_dir: metrics, retention: 12, git_history_window: 12 months`). If `enabled: false`, refuse and tell the user to enable it.
2. Run the snapshot computation (full algorithm specified in `agents/iconix-metrics.md`):
   - Throughput (UCs by phase, REQs, bugs)
   - Cycle time (M1→M2→M3→merge intervals from git log)
   - Quality (gate-failure rates, drift findings, concurrent-touch outcomes, traceability hygiene)
   - Process compliance (UC-through-all-gates %, trace-comment coverage %, REQ-with-UC %, NFR-with-ADR %)
3. Produce two paired files:
   - `metrics/snapshot-<today>.md` (from `templates/metrics-snapshot-template.md`) — human-readable, audit-friendly
   - `metrics/snapshot-<today>.json` (conforming to `templates/metrics-schema.json`, schema v1.0) — machine-readable
4. If `$ARGUMENTS` is `trend`: also produce `metrics/trend-<today>.md` comparing the new snapshot to the most recent prior snapshot. Show deltas with directional emoji (✅ improving, ⚠️ degrading, ➖ flat).
5. After writing, prune `metrics/snapshot-*.{md,json}` pairs older than `metrics.retention` (default 12). Print which files were pruned.
6. Print a one-screen summary to the terminal: top-line throughput / cycle / quality numbers + count of blockers + file paths to the new artifacts.

Do not modify any other directory. Do not modify ICONIX artifacts, source code, or git history. The agent is read-only on everything except `metrics/`.

If the project has fewer than ~5 UCs, the agent should call out that cycle-time samples are too small for meaningful aggregation. If UCs predate the v0.9.5 commit convention (no phase-tagged commits), they're excluded from cycle-time samples — the snapshot footnote reports the count.
