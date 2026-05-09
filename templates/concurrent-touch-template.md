# Concurrent Touch Report — <date>

> Produced by the Traceability agent at M2 gate, or on demand via
> `/iconix-concurrent`. Surfaces class- and container-level conflicts
> between in-flight UCs *before* they manifest as merge conflicts at
> Implementation. Advisory by default — set
> `concurrent_check.block_on_high_conflict: true` in `iconix.config.yaml`
> to fail M2 PR builds on HIGH conflicts.

## Detection scope

- **Domain entities** — read/write of attributes or operations
- **Boundary controllers** — same-named controllers across UCs
- **Database containers** — multiple UCs writing to the same DB container

## In-flight UCs

> Detected from open `feature/UC-XXX-*` branches and unpromoted DRAFTs.
> Format: `UC-XXX (phase, branch-age)`.

- UC-XXX-<slug> (M2, 3 days)
- UC-YYY-<slug> (M1, 1 day)
- UC-ZZZ-<slug> (M2 done — Impl PR pending, 5 days)

## Class-touch map

> Cell legend: `W` = adds/modifies operations or attributes;
> `R` = read-only reference; `-` = not touched.

| Class / Resource | UC-XXX | UC-YYY | UC-ZZZ |
|---|---|---|---|
| <EntityA>           | W (add foo()) | -     | R     |
| <EntityB>           | -    | W (add bar()) | W (add baz()) |
| <SharedController>  | W    | W     | -     |
| db:<container>      | W    | W     | -     |

## Conflicts detected

> One section per conflict, ordered by severity (HIGH → MEDIUM → LOW).
> If no conflicts: write "No concurrent-touch conflicts detected." and
> stop here.

### CONFLICT-001 — <ClassName> [HIGH]

**Type:** entity write/write | controller name collision | DB container write/write

**UCs involved:** UC-XXX, UC-YYY

**Detail:**
- UC-XXX (RB-XXX) adds: `<ClassName>.<operation>(...)` and attribute `<attr>`
- UC-YYY (RB-YYY) adds: `<ClassName>.<other-operation>(...)`

**Why this matters:** <one sentence — typically merge conflict + semantic conflict>

**Recommended resolution:**
- <option 1 — e.g., extract `<ClassName>Service` aggregating both operations; both UCs depend on the service>
- <option 2 — e.g., land UC-XXX first via `arch/<scope>` branch; UC-YYY rebases>
- <option 3 — e.g., split `<ClassName>` into two classes if responsibilities are distinct>

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
- [ ] If CONFLICT-001 was deliberately accepted, document the rationale in the M2 PR description

## Configuration

- `concurrent_check.enabled`: <true|false>
- `concurrent_check.block_on_high_conflict`: <true|false>
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
  - `container-mapping/<UC>-mapping.md` (when present)
  - Open feature branches via `git branch -r --list 'origin/feature/UC-*'`
