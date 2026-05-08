## Implementation PR

## Summary
<one sentence — what this PR implements>

## Affected use cases
<list UC-IDs>

## What's in the diff
- New / changed source files: <count, key paths>
- New / changed test files: <count, key paths>
- Migrations / schema changes: <yes/no — link to migration if yes>

## Implementation checklist
- [ ] Every new source file under `src/` carries a `Traceability:` comment with UC/RB/SD IDs
- [ ] Every new test file under `tests/` cites the UC and TC IDs
- [ ] All TCs from M3 for the affected UCs are implemented and passing
- [ ] Code follows the SD's call order
- [ ] No methods exist in code that aren't on the SD (or vice versa)
- [ ] No framework concerns mixed into business logic (or, if forced, an ADR exists)
- [ ] ICONIX traceability gate (build) is green

## Reviewer notes
- Run `/iconix-review` against this PR diff. Drift findings should be addressed before merge.
- If drift is acceptable, document the exception in the PR description and tag `@iconix-reviewer ack` in the PR thread.

## Traceability
<paste the chain — should match the touched files>

## Work item
AB#<N>
