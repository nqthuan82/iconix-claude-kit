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
   - Cross-reference `class-model.puml` to identify added operations / attributes (writes, recording specific names) vs unchanged references (reads)
   - For database touches, parse `container-mapping/` to identify DB-container writes
4. Load previously accepted conflicts from `change-impact/CT-*.md` (last 90 days) and `git log --grep="CT-ACCEPT"` — build an accepted set keyed by `(UC-A, UC-B, class-or-resource)` tuple.
5. For each pair of in-flight UCs, classify shared touches:
   - **HIGH** — operation/attribute name collision (same name added by both UCs); or same-named controller; or both writing the same DB container
   - **MEDIUM** — both write same class but add distinct operations (no name collision); or one write, one read
   - **LOW** — both reads (informational)
   - **[ACCEPTED]** — previously accepted HIGH conflict; shown for transparency, excluded from active HIGH count
6. If `$ARGUMENTS` is a UC-ID, filter the report to conflicts involving that UC.
7. Produce `change-impact/CT-<today>.md` from `templates/concurrent-touch-template.md` (or its installed copy at `docs/iconix/templates/`).
8. Print a summary: active HIGH / accepted HIGH / MEDIUM / LOW counts, with one-line teaser per active HIGH.
9. If `block_on_high_conflict: true` and **active** HIGH conflicts exist, exit non-zero (so CI fails). Accepted conflicts do not trigger a non-zero exit.

Do not modify code, artifacts, or branches. The Architect agent is the canonical resolver — recommend `/iconix-next` if HIGH conflicts need architectural resolution before M2 promotion.

This check is also run automatically by the Traceability agent at M2 gate; this command is the on-demand mid-phase shortcut.
