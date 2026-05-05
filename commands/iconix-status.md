---
description: Show ICONIX project status and milestone readiness
---

Invoke the iconix-traceability agent. Ask it to produce a read-only status report with the following sections — do not create or modify any artifacts:

## 1. Artifact inventory

Count all artifacts by type. Flag any that are missing an expected downstream artifact.

| Type | Count | Orphans / gaps |
|---|---|---|
| REQ | | |
| UC | | |
| RB | | |
| SD | | |
| CLS | | |
| TC | | |
| ADR | | |
| Test plan (`test-plan/test-plan-<date>.md`) | exists? | — |
| Change impact reports (`change-impact/CI-*.md`) | open count | — |

## 2. NFR coverage

From `iconix.config.yaml` `nfr_catalog`: how many NFRs are cited by ≥1 ADR or container-mapping annotation? List any uncovered NFRs as orphans.

## 3. Test coverage summary

From `test-matrix.md` (if it exists):
- Total TCs vs. UCs with ≥1 TC
- Automated vs. manual TC count
- Any UC with no TC (gate blocker)

## 4. Open change impact reports

List any `change-impact/CI-*.md` files present. For each, note: which REQ triggered it, which artifacts are in the blast radius, and whether the scoped pipeline has been re-run.

## 5. Milestone readiness

Run the standard M1 / PDR / CDR gate checks scoped to current artifact state. Report READY or NOT READY with specific blockers.

## 6. Next recommended action

One concrete next step based on the current project state.
