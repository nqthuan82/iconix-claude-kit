# Concurrent Touch Report — <date>

> Produced by the Traceability agent at M2 gate, or on demand via
> `/iconix-concurrent`. Surfaces class- and container-level conflicts
> between in-flight UCs *before* they manifest as merge conflicts at
> Implementation. Advisory by default — set
> `concurrent_check.block_on_high_conflict: true` in `iconix.config.yaml`
> to fail M2 PR builds on HIGH conflicts.

## Detection scope

- **Domain entities** — read/write of attributes or operations; operation-name collisions (same name added by two UCs) escalate to HIGH
- **Boundary controllers** — same-named controllers across UCs
- **Database containers** — multiple UCs writing to the same DB container
- **Previously accepted conflicts** — tagged `[ACCEPTED]`; excluded from active HIGH count and M2 gate readiness

## In-flight UCs

> Detected from open `feature/UC-XXX-*` branches and unpromoted DRAFTs.
> Format: `UC-XXX (phase, branch-age)`.

- UC-XXX-<slug> (M2, 3 days)
- UC-YYY-<slug> (M1, 1 day)
- UC-ZZZ-<slug> (M2 done — Impl PR pending, 5 days)

## Class-touch map

> Cell legend: `W(op1, op2)` = adds/modifies named operations or attributes;
> `R` = read-only reference; `-` = not touched.
> Operation names are shown to enable collision detection.

| Class / Resource | UC-XXX | UC-YYY | UC-ZZZ |
|---|---|---|---|
| <EntityA>           | W(foo()) | -        | R     |
| <EntityB>           | -        | W(bar()) | W(baz()) |
| <SharedController>  | W(save()) | W(save()) | -   |
| db:<container>      | W    | W     | -     |

## Hot classes

> Classes or resources touched by ≥3 in-flight UCs. Ranked by write count descending.
> Omit this section if fewer than 3 UCs are in-flight.
> Hot spots are **advisory** — they signal architectural bottlenecks for the Architect to review.
> They do not block M2 on their own.

| Class / Resource | UCs touching | Writers | Risk | Involved UCs |
|---|---|---|---|---|
| <ClassName> | 5 | 4 | HIGH | UC-011, UC-014, UC-017, UC-020, UC-023 |
| <EntityB>   | 3 | 1 | MEDIUM | UC-011, UC-014, UC-020 |

**Risk legend:**
- **HIGH** — ≥3 UCs write; likely needs extraction or decomposition before Implementation
- **MEDIUM** — ≥3 UCs touch, ≥1 writes; coordination needed to avoid semantic drift
- **LOW** — ≥3 UCs touch, all read; informational

If a HIGH hot spot exists: recommend the Architect review whether the class should be split or a service layer introduced before M2 promotion. Use the Architect agent (`/iconix-next`) for resolution.

## Conflicts detected

> One section per conflict, ordered by: active HIGH → active MEDIUM → active LOW → accepted.
> If no conflicts: write "No concurrent-touch conflicts detected." and stop here.

### CONFLICT-001 — <ClassName> [HIGH]

**Type:** operation-name collision | entity write/write | controller name collision | DB container write/write

**UCs involved:** UC-XXX, UC-YYY

**Detail:**
- UC-XXX (RB-XXX) adds: `<ClassName>.save(...)` ← name collision
- UC-YYY (RB-YYY) adds: `<ClassName>.save(...)`

**Why this matters:** <one sentence — typically merge conflict + semantic conflict>

**Recommended resolution:**
- <option 1 — e.g., rename to disambiguate: `UC-XXX` uses `saveAsDraft()`, `UC-YYY` uses `saveAsPublished()`>
- <option 2 — e.g., extract `<ClassName>Service` aggregating both operations; both UCs depend on the service>
- <option 3 — e.g., land UC-XXX first via `arch/<scope>` branch; UC-YYY rebases>

---

### CONFLICT-002 — <ClassName> [HIGH] [ACCEPTED — CT-2026-04-15]

> This conflict was accepted on 2026-04-15 (see `change-impact/CT-2026-04-15.md`, CONFLICT-003).
> It is shown here for transparency but **excluded from the active HIGH count**.
> Re-raise if the acceptance rationale no longer applies.

**Type:** entity write/write

**UCs involved:** UC-AAA, UC-BBB

**Acceptance rationale:** <paste from original CT report or PR description>

### NOTE-001 — <Resource> [MEDIUM]

**Type:** read/write coordination

**UCs involved:** UC-XXX (writes), UC-YYY (reads)

**Detail:**
UC-YYY reads `<Resource>.<attr>`, which UC-XXX is changing the
semantics of. Verify UC-YYY's read remains consistent with UC-XXX's
new write semantics (idempotency, ordering, default values).

**Recommended action:** 30-min sync between UC-XXX and UC-YYY owners; document the agreed contract in an ADR if not already covered.

### INFO-001 — <Resource> [LOW]

UC-XXX and UC-YYY both reference `<Resource>` but neither modifies it. Informational — included so reviewers see the full picture.

## Recommendations

- [ ] CONFLICT-001 resolved before M2 promotion
- [ ] NOTE-001 acknowledged by both UC owners
- [ ] To accept a conflict instead of resolving it: add `[CT-ACCEPT-001]` with rationale to the M2 PR description; future `/iconix-concurrent` runs will suppress it

## Summary

- Active HIGH conflicts: <N>
- Accepted HIGH conflicts: <N>
- MEDIUM: <N>
- LOW: <N>
- Hot spots (HIGH risk): <N>
- Hot spots (MEDIUM risk): <N>

## Configuration

- `concurrent_check.enabled`: <true|false>
- `concurrent_check.block_on_high_conflict`: <true|false> (counts active HIGH only)
- `concurrent_check.detect_boundaries`: <true|false>
- `concurrent_check.detect_db_containers`: <true|false>

## Traceability

- Generated: <date>
- Triggered by: M2 gate | `/iconix-concurrent` invocation | manual
- Affected UCs: UC-XXX, UC-YYY, UC-ZZZ
- Source artifacts read:
  - `robustness/RB-*.puml`
  - `class-model/class-model.puml`
  - `domain-model/domain-model.puml`
  - `container-mapping/<PREFIX>-UC-XXX-containers.md` (when present)
  - Open feature branches via `git branch -r --list 'origin/feature/UC-*'`
