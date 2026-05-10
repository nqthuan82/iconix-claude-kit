# REQ-XXX: <Requirement Title>

## Statement
The system shall <observable behaviour — active voice, present tense, one sentence>.

## Rationale
<Why this requirement exists — stakeholder need, regulatory constraint, or business rule.>

## Acceptance criteria

> **Checkbox lifecycle:** unchecked when the REQ is drafted (PO at M1). The
> Tester ticks each criterion when at least one TC covering it passes (M3
> / Phase 9). The PO confirms all ticks at the M3 → Implementation merge
> during PR review. An unticked criterion at merge time is a Reviewer
> finding / blocker for the Implementation PR.

- [ ] <measurable condition 1>
- [ ] <measurable condition 2>

## Examples
<!-- Optional but encouraged — concrete scenarios make the requirement unambiguous -->
- **Example 1:** `<brief scenario that satisfies the requirement>`
- **Counter-example:** `<brief scenario that violates or is out of scope>`

## Priority
P0 — must have | P1 — should have | P2 — nice to have

## Traceability
- **Intakes:** <comma-separated list of intake files this REQ was extracted from — same convention as UC template's `Intakes:` field. For direct stakeholder requests with no intake artifact, capture an `intake-email` or `intake-transcript` first; do not put free-text stakeholder names here.>
- **Downstream UCs:** (filled by Product Owner)
- **Related NFRs:** <comma-separated list of NFR IDs from `docs/nfr-catalog.md` that this REQ implies, or "(none)". Pre-populated by PO from intake NFR seeds; refined by Architect at M2.>
- **Related BRs:** <comma-separated list of Business Rule IDs (BR-NNN) that this REQ depends on, or "(none — Business Rules not yet adopted)". BR-NNN is a planned kit feature; until then, leave as "(none)" or document inline rules in the Statement.>
