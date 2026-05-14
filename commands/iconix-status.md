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
| BR | (EXTRACTED: N, INFERRED: N) — omit row when `migration/business-rules.md` absent | Broken ADR citations: N |
| Test plan (`test-plan/test-plan-<date>.md`) | exists? | — |
| Change impact reports (`change-impact/CI-*.md`) | open count | — |

## 2. NFR coverage

From `iconix.config.yaml` `nfr_catalog`: how many NFRs are cited by ≥1 ADR or container-mapping annotation? List any uncovered NFRs as orphans.

## 2b. Business rules coverage (migration mode only)

Skip this section when `migration/business-rules.md` is absent.

When present, read `migration/business-rules.md` and report:

- **Total rules:** N — EXTRACTED: N | INFERRED [VERIFY]: N | AMBIGUOUS: N
- **⚠ Investigate categories with no covering ADR** (Invariant / Authorization / Transition guard / Workflow / Calculation): N rules — list BR-IDs. These are ADR candidates the Architect has not yet addressed.
- **Broken ADR citations** (Traceability check #17): scan every `adrs/*.md` `## Context` for `BR-\d+` patterns; verify each against `business-rules.md`. Report: N broken — list `ADR-ID cites BR-NNN (not found)`.
- **Unlinked rules** (no UC references this BR-ID in `## Business rules cross-reference`): N rules — list BR-IDs. Investigate whether Phase 5d entity names failed to match any UC.

## 3. Test coverage summary

From `test-matrix.md` (if it exists):
- Total TCs vs. UCs with ≥1 TC
- Automated vs. manual TC count
- Any UC with no TC (gate blocker)

## 4. Open change impact reports

List any `change-impact/CI-*.md` files present. For each, note: which REQ triggered it, which artifacts are in the blast radius, and whether the scoped pipeline has been re-run.

## 5. Milestone readiness

Run the standard M1 / PDR / CDR gate checks scoped to current artifact state. Report READY or NOT READY with specific blockers.

For M2, include BR-NNN check #17 in the blocker list when `migration/business-rules.md` exists:
- **BR-NNN citation integrity:** N broken citations (ADR cites BR-ID not in `business-rules.md`) — list each. Each broken citation is an M2 blocker.

## 6. Next recommended action

One concrete next step based on the current project state.
