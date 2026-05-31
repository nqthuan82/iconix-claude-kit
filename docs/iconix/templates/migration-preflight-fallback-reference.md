# Migration pre-flight — manual fallback reference

This is the **manual fallback** for `iconix-migration-infra` Steps 0–4b, used only when
`python3 .claude/scripts/migration_preflight.py` is unavailable or errors. The script is
the primary path; it returns the same detections as booleans. The human decisions
(Step 0a STOP, Step 4b continue/cancel) always stay with the agent — see the agent's
`# Pre-run idempotency check` gate.

This file is loaded on demand, so it does not count against the agent's token budget.

---

## Step 0 — Greenfield artifact collision check

Migration is designed to retrofit ICONIX onto code that has no existing artifacts. If the project already has greenfield (non-DRAFT) UCs, RBs, SDs, class model, or use-case packages, migration would either overwrite them or pollute the folder with mixed `UC-*.md` + `UC-DRAFT-*.md` files that confuse downstream agents (Analyst, Tester).

Scan for greenfield artifacts:

| Path | Greenfield filename pattern | Migration filename pattern |
|---|---|---|
| `use-cases/*.md` | `UC-*.md` (no DRAFT in name) | `UC-DRAFT-*.md` |
| `robustness/*.puml` | `RB-*.puml` (no DRAFT) | `RB-DRAFT-*.puml` |
| `sequence/*.puml` | `SD-*.puml` (no DRAFT) | `SD-DRAFT-*.puml` |
| `use-case-packages/*.puml` | `*.puml` not ending `-DRAFT.puml` | `*-DRAFT.puml` |
| `class-model/class-model.puml` | canonical filename | **same filename** — REAL collision risk |

`domain-model/domain-model.puml` (greenfield) and `domain-model/domain-model-DRAFT.puml` (migration) use different filenames — no collision. Same for the `-DRAFT` patterns above. The only true filename collision is `class-model/class-model.puml`.

### Step 0a — Abort if greenfield detected (default behavior)

If **any** greenfield artifact is detected AND `--allow-greenfield` is NOT in `$ARGUMENTS`:

STOP. Print:
```
Greenfield ICONIX artifacts detected — migration is for retrofitting code
that has NO existing artifacts. Running migration here would overwrite
class-model/class-model.puml (filename collision) and produce a confusing
mix of greenfield UC-*.md and migration UC-DRAFT-*.md in use-cases/.

Detected greenfield files:
<list, one per line>

Options:
(a) If this project is already on the ICONIX greenfield path, do NOT run
    migration — continue with /iconix-next.
(b) If you genuinely need migration coexistence (e.g., adding a new
    untouched module to a project that already has greenfield ICONIX work
    elsewhere), re-run with --allow-greenfield. Migration will write the
    class-model output to class-model/class-model-DRAFT.puml instead of
    overwriting the greenfield one, and the greenfield class-model.puml
    becomes a read-only input.
```

Do NOT proceed.

### Step 0b — Proceed with greenfield coexistence (--allow-greenfield)

If `--allow-greenfield` IS in `$ARGUMENTS`:
- Record `greenfield_coexistence: true` and `greenfield_files: [...]` in the checkpoint (Step 5).
- `iconix-migration-structural` Phase 2 will use this flag to write `class-model/class-model-DRAFT.puml` instead of overwriting the greenfield canonical file.
- Print a single-line acknowledgement: `Greenfield coexistence enabled — class-model output redirected to class-model-DRAFT.puml`.

## Step 1 — Detect previous migration runs
Check whether `migration/` contains any `checkpoint-*.json` or `survey-*.md` files. If yes, record the most recent date as `<last-run-date>`.

## Step 2 — Check for promoted artifacts
Read `ids.registry.md` (maintained by Traceability). For each permanent ID of type UC, RB, SD, CLS, TC — check whether a corresponding DRAFT file exists in the output paths below. If a permanent ID exists for a slug, that artifact has already been promoted and must not be overwritten. Report it as **already promoted — skipping**.

## Step 3 — Check for human-edited DRAFTs
For each of the following output paths, check if the file exists AND was last modified after `<last-run-date>`:

```
docs/architecture/system-architecture.md
docs/architecture/package-map.md
migration/coverage-gaps.md
class-model/class-model.puml
sequence/SD-DRAFT-*.puml
robustness/RB-DRAFT-*.puml
domain-model/domain-model-DRAFT.puml
use-cases/UC-DRAFT-*.md
use-case-packages/*-DRAFT.puml
```

If a file has been modified after the last survey date, a human has likely edited it. **Do not overwrite silently.** Report each such file as:

```
⚠ DRAFT modified since last run: use-cases/UC-DRAFT-001-checkout.md
  Last migration: 2026-04-10 | File modified: 2026-04-15
  Options: (a) skip this artifact, (b) overwrite and lose edits
  → Defaulting to SKIP. Pass --force to overwrite.
```

Proceed only with artifacts that are:
- Not yet promoted (no permanent ID in registry), AND
- Not modified since the last migration run (or `--force` was passed)

## Step 4 — Report before proceeding

Before starting Phase 1, output a pre-run summary:

```
## Idempotency check
- Previous run detected: <last-run-date> | none
- Artifacts already promoted (will skip): <list or "none">
- DRAFTs modified by humans (will skip): <list or "none">
- Artifacts safe to (re)generate: <list>
```

If all artifacts are already promoted or human-edited, abort and tell the user there is nothing left to migrate.

## Step 4b — Database container readiness check (scoped runs only)

Run this check only when `scope` is non-null AND the current scope container is an application container (has entry points such as controllers, handlers, CLI, gRPC services).

**Step 1 — Detect database-like containers in config**

Scan all containers in `architecture.containers` *other than* the current scope. For each, check for database container signals:
- Schema files present: `*.sql`, `*.sqlproj`, `schema.prisma`, `V*__*.sql`, `*.flyway.sql`, `db/migrate/*.rb`, `alembic/versions/*.py`
- Zero application entry points (no controllers, handlers, gRPC services, CLI entry points)

**Step 2 — Check for existing domain-glossary.md**

Check whether `migration/domain-glossary.md` exists.

**Step 3 — Warn if needed**

If **at least one database-like container is found** AND **no `domain-glossary.md` exists**, STOP and output:

```
⚠️  Database container detected — BDD generation will be skipped

Containers with SQL schema files and no entry points:
  - <ContainerName(s)>

No domain-glossary.md exists yet. Continuing with --scope <AppContainer> will:
  ✅ Produce UC-DRAFTs and structural artifacts
  ⛔ Skip BDD generation (Phase 5c) — no schema in scope, no glossary from a previous DB run

Options:
  1. Cancel  — run `--scope <DBContainerName>` first to build domain-glossary.md,
               then return to `--scope <AppContainer>` to get BDD alongside UC-DRAFTs
  2. Continue — get UC-DRAFTs now; re-run `--scope <AppContainer>` after the DB
               container run to generate BDD from the glossary

Reply "continue" or "cancel".
```

Wait for user reply before proceeding.
- **"cancel"**: STOP. Do not write checkpoint. Do not proceed further.
- **"continue"**: proceed to Step 5 normally.

**Step 4 — Skip condition**

If `domain-glossary.md` already exists → skip this warning entirely (Phase 5c Case B will fire — BDD will be generated from the existing glossary). Proceed directly to Step 5.
