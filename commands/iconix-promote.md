---
description: "Promote reviewed migration DRAFTs to permanent ICONIX IDs. Run after human review of UC/RB/SD/domain-model/class-model DRAFTs produced by iconix-migration. Invokes the Traceability agent in DRAFT-promotion mode."
argument-hint: "[<DRAFT-slug>|all]   # optional: a specific DRAFT slug to promote, or 'all' for all confirmed DRAFTs"
---

Invoke the iconix-traceability agent in **DRAFT promotion mode** with: $ARGUMENTS

The agent should follow its `# DRAFT promotion` workflow:

1. Identify promotion candidates: scan `use-cases/UC-DRAFT-*.md`, `robustness/RB-DRAFT-*.puml`, `sequence/SD-DRAFT-*.puml`, `domain-model/domain-model-DRAFT.puml`, `class-model/class-model.puml` (DRAFT-stamped header), `use-case-packages/*-DRAFT.puml`.
   - If `$ARGUMENTS` is a slug (e.g., `UC-DRAFT-001`), promote only that artifact.
   - If `$ARGUMENTS` is `all` or empty, process all DRAFTs found.

2. For each candidate, run safety checks before promoting:
   - Count `[VERIFY]` occurrences in the file. If > 0 → **skip** and warn: "N [VERIFY] items unresolved — resolve before promoting."
   - Check `ids.registry.md` — if a permanent ID already exists for this slug → **skip** as already promoted.

3. Assign permanent IDs from `ids.registry.md` (highest existing ID + 1 per type). Use the project prefix from `iconix.config.yaml`.

4. For each eligible DRAFT:
   - Rename the file: `use-cases/UC-DRAFT-001-checkout.md` → `use-cases/<PREFIX>-UC-001-checkout.md`
   - Replace the ID header in the file (`**ID:** UC-DRAFT-001` → `**ID:** <PREFIX>-UC-001`)
   - Update self-references in the `## Traceability` block
   - Scan all other DRAFT files for references to the old DRAFT ID and update them
   - Register the new permanent ID in `ids.registry.md`

5. Print a summary:
   - Promoted: N (list IDs assigned)
   - Skipped — [VERIFY] pending: N (list files + unresolved count)
   - Skipped — already promoted: N

After promotion, the artifacts are ready for the normal ICONIX pipeline. Run `/iconix-next` to proceed to M1 (or M2 if UC and RB are both promoted).
