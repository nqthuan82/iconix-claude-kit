---
description: "Detect class- and container-level conflicts between in-flight use cases (UCs on open feature branches or unpromoted DRAFTs). Advisory by default."
argument-hint: "[<UC-ID>]   # optional: focus the report on conflicts involving this UC"
---

Invoke the iconix-traceability agent in **concurrent-touch detection mode** with: $ARGUMENTS

The agent should follow its `# Concurrent touch detection` workflow:

1. Read `iconix.config.yaml` `concurrent_check:` section. If missing, default to `enabled: true, block_on_high_conflict: false, detect_boundaries: true, detect_db_containers: true`.
2. Identify in-flight UCs:
   - Open `feature/UC-XXX-*` branches (via `git branch -r --list 'origin/feature/UC-*'`)
   - Unpromoted DRAFT artifacts in `use-cases/`, `robustness/`, `sequence/`
   - UCs past M2 with no Implementation PR merged
3. For each in-flight UC, build the class-touch map:
   - Parse robustness diagrams to extract referenced classes (entities, controllers)
   - Cross-reference `class-model.puml` to identify added operations / attributes (writes) vs unchanged references (reads)
   - For database touches, parse `container-mapping/` to identify DB-container writes
4. For each pair of in-flight UCs, classify shared touches:
   - **HIGH** — both writes; or same-named controller across UCs; or both writing the same DB container
   - **MEDIUM** — one write, one read of the same class
   - **LOW** — both reads (informational)
5. If `$ARGUMENTS` is a UC-ID, filter the report to conflicts involving that UC.
6. Produce `change-impact/CT-<today>.md` from `templates/concurrent-touch-template.md` (or its installed copy at `docs/iconix/templates/`).
7. Print a summary: counts of HIGH / MEDIUM / LOW conflicts, with one-line teaser per HIGH.
8. If `block_on_high_conflict: true` and HIGH conflicts exist, exit non-zero (so CI fails). Otherwise exit 0 regardless of findings.

Do not modify code, artifacts, or branches. The Architect agent is the canonical resolver — recommend `/iconix-next` if HIGH conflicts need architectural resolution before M2 promotion.

This check is also run automatically by the Traceability agent at M2 gate; this command is the on-demand mid-phase shortcut.
