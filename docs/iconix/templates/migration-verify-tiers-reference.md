# [VERIFY] Severity Tiers — Migration Reference

Used by `iconix-migration-semantic` throughout Phases 5–7. Read before marking any `[VERIFY]` marker.
Every marker must carry a tier: `[VERIFY:HIGH]`, `[VERIFY:MEDIUM]`, or `[VERIFY:LOW]`.

## HIGH — blocks promotion; resolve before `/iconix-promote`

| Source | Examples |
|---|---|
| Cross-container UC grouping — MEDIUM confidence | URL prefix match only; method differs; "are these the same use case?" unclear |
| AMBIGUOUS graph edge used in any artifact | Concrete implementation unknown; cannot determine correct class |
| State machine sequence from SQL heuristic only (no ORM enum) | Transition order inferred from CHECK IN values alone — often wrong |
| Business rule Invariant or Transition guard from Track D or T (INFERRED) | Domain guard clause or trigger RAISERROR inferred as invariant |
| UC actor identity unknown or generic | Actor shown as "User", "System", or "Unknown" — cannot identify from code |
| Missing alternate course — try/catch present, business intent unknown | Exception handler found but whether it is a real user journey is unclear |

## MEDIUM — affects artifact quality; resolve before M1/M2 gate

| Source | Examples |
|---|---|
| Actor role name specific but unconfirmed | `Manager`, `Operator`, `Admin` — plausible from code context, not confirmed |
| Alternate course inferred from try/catch (intent is plausible) | Error mapped to alternate course — confirm it is a real user journey |
| Business rule Precondition, Authorization, or Workflow from Track D or T | INFERRED but lower-stakes than invariants and transition guards |
| State machine sequence from ORM enum (EXTRACTED order) | Declaration order reliable; business meaning of each state needs PO sign-off |
| MEDIUM-confidence cross-container grouping | URL prefix match with matching method — grouping likely correct but not certain |

## LOW — cosmetic; review last or skip under deadline pressure

| Source | Examples |
|---|---|
| FK-derived precondition | `Customer must exist` — almost always correct from FK constraint |
| Stored procedure verb → operation name | `sp_ApproveOrder → Approve` — reliably accurate |
| Entity or attribute names from ORM or SQL schema (EXTRACTED) | Field names from class definitions or normalized table names |
| Business rules from Track V (validator annotations, EXTRACTED) | `[NotNull]`, `[Range]`, `[StringLength]` — accurate, low business risk |
| UC package cluster grouping | Namespace/directory-based grouping — structural, not semantic |
| Cross-container grouping — HIGH confidence | Exact URL + method match; almost certainly correct |
