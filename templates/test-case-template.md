# TC-XXX: `<Test Case Title>`

## Type
unit | integration | system | acceptance | regression

## Traceability
- **Requirement:** REQ-XXX
- **Use Case:** UC-XXX (course: basic | alt-A | alt-B | ...)
- **Robustness controller:** RB-XXX: `<ControllerName>` ← unit only; omit for other types
- **Sequence diagram:** SD-XXX ← unit / integration / regression (when re-verifying a unit or integration TC); omit for system / acceptance
- **Supersedes TC:** TC-XXX ← regression only; the previously passing TC this re-verifies

## Preconditions
- `<system state that must be true before the test begins>`

## Steps
<!-- Mirror the User Action column of the UC exactly -->
1. `<step 1>`
2. `<step 2>`

## Expected results
<!-- Mirror the System Response column of the UC exactly -->
1. `<expected result 1>`
2. `<expected result 2>`

## Postconditions
- `<system state that must be true after the test completes>`

## Priority
P0 — must pass before release | P1 — should pass | P2 — nice to have

## Edge case family
boundary | invalid-input | authorization | concurrency | resource-exhaustion | state-violation | domain-specific | n/a
