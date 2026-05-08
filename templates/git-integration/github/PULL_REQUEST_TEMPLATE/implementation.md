## Implementation PR

## Summary
<one sentence — what this PR implements>

## Affected use cases
<list UC-IDs — the source files in this PR should match these>

## What's in the diff
- New / changed source files: <count, key paths>
- New / changed test files: <count, key paths>
- Migrations / schema changes: <yes/no — link to migration if yes>

## Implementation checklist
- [ ] Every new source file under `src/` carries a `Traceability:` comment with UC/RB/SD IDs
- [ ] Every new test file under `tests/` cites the UC and TC IDs
- [ ] All TCs from M3 for the affected UCs are implemented and passing
- [ ] Code follows the SD's call order (Reviewer will verify)
- [ ] No methods exist in code that aren't on the SD (or vice versa)
- [ ] No framework concerns mixed into business logic (or, if forced, an ADR exists)
- [ ] ICONIX traceability gate (CI) is green

## Reviewer notes
- The Reviewer should run `/iconix-review` against this PR diff. Drift findings (code ↔ SD, code ↔ class model, NFR violations) should be addressed before merge.
- If drift is acceptable (e.g., ad-hoc method on a test fixture), document the exception in the PR description and tag `@iconix-reviewer ack` in the comment thread.

## Traceability
<paste the chain — should match what the Reviewer extracts from the touched files>

## Work item
<optional>
