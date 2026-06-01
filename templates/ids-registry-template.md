# ID Registry

Canonical ledger of issued ICONIX IDs. IDs are **never reused**, even after a
deletion — allocation is always highest-seen + 1 per type. Maintained by the
Traceability agent and `.claude/scripts/ids.py` / `promote.py`.

The **ID column is load-bearing**: `ids.py` parses only the first column of each table
row (a full-cell `<PREFIX>-<TYPE>-<NNN>` match), so IDs mentioned inside the Note column
— e.g. "promoted from UC-DRAFT-001" — are never miscounted. Keep one row per ID.

| ID | Slug | Path | Note |
|---|---|---|---|
| PRJ-UC-001 | checkout | use-cases/PRJ-UC-001-checkout.md | promoted from UC-DRAFT-001 on 2026-01-01 |
| PRJ-RB-001 | checkout | robustness/PRJ-RB-001-checkout.puml | promoted from RB-DRAFT-001 on 2026-01-01 |
