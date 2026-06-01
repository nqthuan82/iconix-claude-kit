# DRAFT promotion — manual fallback reference

This is the **manual fallback** for `iconix-traceability` DRAFT-promotion and the
`/iconix-promote` command, used only when `python3 .claude/scripts/promote.py` is
unavailable or errors. The script is the primary path; it performs the same steps and
returns a JSON summary. Loaded on demand, so it does not count against the agent's token
budget.

The single most important rule: count `[VERIFY]` with a match on **`[VERIFY`** (open
bracket + VERIFY, no closing bracket), so `[VERIFY:HIGH]` and `[VERIFY — note]` are
caught — not just a literal `[VERIFY]`.

---

## Step 1 — Identify promotion candidates
Scan for DRAFT artifacts:
- `use-cases/UC-DRAFT-*.md`
- `robustness/RB-DRAFT-*.puml`
- `sequence/SD-DRAFT-*.puml`
- `domain-model/domain-model-DRAFT.puml`
- `class-model/class-model.puml` (check for `DRAFT` stamp in file header)
- `use-case-packages/*-DRAFT.puml`

If `$ARGUMENTS` is a specific slug (e.g., `UC-DRAFT-001`), restrict to that file. If `all` or empty, process every DRAFT found.

## Step 2 — Safety checks (per candidate)
For each candidate, run these checks before assigning an ID:

1. **Unresolved `[VERIFY]` markers** — count occurrences matching `[VERIFY` in the file. If count > 0 → **skip** and warn:
   ```
   ⚠ Skipped UC-DRAFT-001-checkout.md — 3 [VERIFY] items unresolved.
     Resolve all [VERIFY] markers before promoting.
   ```
2. **Already promoted** — check `ids.registry.md` for any permanent ID whose slug matches this file's slug. If found → **skip** as already promoted.
3. **Not found in migration survey** — if `migration/survey-*.md` exists and does not mention this DRAFT, warn but do not block (the DRAFT may have been created manually after the survey).

## Step 3 — Assign permanent IDs
Read `ids.registry.md` to find the highest existing ID per type. Use the project prefix from `iconix.config.yaml`.

| DRAFT type | ID pattern | Example |
|---|---|---|
| `UC-DRAFT-*.md` | `<PREFIX>-UC-NNN` | `PRJ-UC-001` |
| `RB-DRAFT-*.puml` | `<PREFIX>-RB-NNN` | `PRJ-RB-001` |
| `SD-DRAFT-*.puml` | `<PREFIX>-SD-NNN` | `PRJ-SD-001` |
| `domain-model-DRAFT.puml` | _(no ID; remove DRAFT stamp only)_ | — |
| `class-model.puml` (DRAFT) | _(no ID; remove DRAFT stamp only)_ | — |
| `*-DRAFT.puml` (UC packages) | _(no ID; remove DRAFT stamp only)_ | — |

Assign IDs sequentially in the order DRAFTs appear (sorted by filename). Never reuse a retired ID.

## Step 4 — Rename, update, register
For each eligible DRAFT:
1. **Rename the file** — replace `DRAFT-NNN` with the assigned permanent ID:
   - `use-cases/UC-DRAFT-001-checkout.md` → `use-cases/<PREFIX>-UC-001-checkout.md`
   - `robustness/RB-DRAFT-001-checkout.puml` → `robustness/<PREFIX>-RB-001-checkout.puml`
   - For no-ID artifacts (domain model, class model, UC packages): remove the `-DRAFT` suffix from the filename only
2. **Update internal ID references** in the renamed file:
   - `**ID:** UC-DRAFT-001` → `**ID:** <PREFIX>-UC-001`
   - Traceability block — replace old DRAFT ID with permanent ID
   - PlantUML header comment `' Traceability: ... UC-DRAFT-001 ...` → permanent ID
   - `Source-container:` annotation — **preserve as-is**; do not remove or modify.
     This annotation is the Developer's routing signal for multi-repo code placement.
3. **Update cross-references** — scan all other DRAFT files in `use-cases/`, `robustness/`, `sequence/`, `use-case-packages/` for the old DRAFT ID string; replace with the new permanent ID. Use a full-token match so `UC-DRAFT-1` does not match inside `UC-DRAFT-10`.
4. **Register in `ids.registry.md`** — add one entry per promoted ID:
   ```
   | <PREFIX>-UC-001 | checkout | use-cases/<PREFIX>-UC-001-checkout.md | promoted from UC-DRAFT-001 on <date> |
   ```

## Step 5 — Print summary
```
DRAFT promotion complete — <date>

Promoted:
  UC-DRAFT-001 → <PREFIX>-UC-001  (use-cases/<PREFIX>-UC-001-checkout.md)
  RB-DRAFT-001 → <PREFIX>-RB-001  (robustness/<PREFIX>-RB-001-checkout.puml)

Skipped — [VERIFY] pending:
  UC-DRAFT-003-payment.md — 2 [VERIFY] items unresolved

Skipped — already promoted:
  (none)

Next: run /iconix-next to continue the pipeline from the promoted artifacts.
```

After printing the main summary, check each promoted UC file for a multi-value
`Source-container:` annotation (i.e., it contains `,` — more than one container entry).
If any exist, append:

```
Multi-container UCs promoted:
  <PREFIX>-UC-001 (checkout): spans
    Frontend @ ../frontend/src/
    Backend  @ ../backend/src/
  → Developer must create feature/UC-001-checkout in each repo before coding.
    Code for each container goes under that container's resolved source root.
```

If no multi-container UCs were promoted, omit this section entirely.
