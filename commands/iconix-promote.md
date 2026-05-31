---
description: "Promote reviewed migration DRAFTs to permanent ICONIX IDs. Run after human review of UC/RB/SD/domain-model/class-model DRAFTs produced by iconix-migration. Invokes the Traceability agent in DRAFT-promotion mode."
argument-hint: "[<DRAFT-slug>|all]   # optional: a specific DRAFT slug to promote, or 'all' for all confirmed DRAFTs"
---

Invoke the iconix-traceability agent in **DRAFT promotion mode** with: $ARGUMENTS

The agent runs its `# DRAFT promotion` workflow, which calls the promotion script:

```bash
python3 .claude/scripts/promote.py --args "$ARGUMENTS"   # add --dry-run to preview
```

The script does it all deterministically: scan DRAFTs (restricted to a slug when `$ARGUMENTS` is one, otherwise all), skip any file with unresolved `[VERIFY]` markers (matched as `[VERIFY`, so `[VERIFY:HIGH]` / `[VERIFY — …]` are caught) and any slug already in `ids.registry.md`, assign permanent IDs (highest + 1 per type, project prefix from `iconix.config.yaml`), rename files, rewrite internal IDs and cross-references (preserving `Source-container:` lines), and append the registry. The agent renders the summary (promoted / skipped-[VERIFY] / skipped-already / multi-container) from the script's JSON and trusts it; it falls back to the manual steps in `docs/iconix/templates/promote-fallback-reference.md` only if `python3` is unavailable.

After promotion, the artifacts are ready for the normal ICONIX pipeline. Run `/iconix-next` to proceed to M1 (or M2 if UC and RB are both promoted).
