# TC-XXX: `<Test Case Title>`

## Type
unit | integration | system | acceptance | acceptance-bdd | regression

> **acceptance-bdd** — use for stakeholder-signed acceptance TCs that
> use Gherkin Given/When/Then format, even when the project's default
> `iconix.config.yaml` `bdd: false`. The Tester agent's per-TC BDD
> convention allows BDD-style ONLY for acceptance TCs in mixed-style
> projects.

## Status
active | superseded by TC-XXX | retired

> Default: `active`. When a regression TC supersedes this one (per
> change-impact event), set to `superseded by TC-YYY` and keep the
> file for audit/git-log clarity. Do NOT delete superseded TCs;
> the test-matrix relies on the chain.

## Traceability
- **Requirement:** REQ-XXX
- **Use Case:** UC-XXX (course: basic | alt-A | alt-B | ...)
- **Robustness controllers exercised:** RB-XXX: `<Controller1>`, `<Controller2>`, ...
  <!-- Plural — one TC may exercise multiple controllers transitively
       (especially system TCs). Required for unit / system / integration TCs;
       omit for acceptance / acceptance-bdd / regression. -->
- **Sequence diagram:** SD-XXX
  <!-- Required for unit / integration / regression (when re-verifying);
       omit for system / acceptance / acceptance-bdd. -->
- **Supersedes TC:** TC-XXX
  <!-- Regression only. The previously passing TC this re-verifies after a
       change-impact event. The superseded TC keeps its file but its Status
       field changes to `superseded by <this TC ID>`. -->

## Preconditions
- `<system state that must be true before the test begins>`

## Steps
<!-- For unit / integration / system / regression: mirror the User Action
     column of the UC exactly.
     For acceptance-bdd: use Gherkin Given/When/Then prose instead. The
     two-column Steps/Expected format is awkward for stakeholder-signed
     scenarios; Gherkin reads more naturally there. -->
1. `<step 1>`
2. `<step 2>`

## Expected results
<!-- For unit / integration / system / regression: mirror the System
     Response column of the UC exactly.
     For acceptance-bdd: this section may be empty (the Then clauses live
     inside Steps). -->
1. `<expected result 1>`
2. `<expected result 2>`

## Postconditions
- `<system state that must be true after the test completes>`

## Priority
P0 — must pass before release | P1 — should pass | P2 — nice to have

## Edge case family
<!-- Optional. Include this section ONLY if this TC tests one of the
     edge-case families from the Tester agent's `# Edge case generation
     rules`. Omit entirely for basic-course / happy-path TCs. -->
boundary | invalid-input | authorization | concurrency | resource-exhaustion | state-violation | domain-specific

## Implementation note (`<stack> + <test framework>`, per `<ADR-XXX>` if applicable)
<!-- The runnable test code or a recipe for it. Cite the stack from
     `iconix.config.yaml.stack`, the test framework from
     `iconix.config.yaml.stack.test_framework`, and any ADR(s) that
     motivated the test approach. List test-infrastructure dependencies
     (e.g., WebApplicationFactory, Testcontainers, NSubstitute, Reqnroll).
     This is what closes the gap between TC-as-spec and TC-as-runnable.

     Example header for the Internet Bookstore stack:
     ## Implementation note (C# + xUnit + WebApplicationFactory<Program>, per BS-ADR-001)

     Then the code block in the project's language. Test code lives here in
     prose form during M3 (TC authoring); the Tester translates it to real
     test files in tests/<package>/ during Phase 9.1 per `# Test
     implementation mode`. -->

```<lang>
// Test code goes here. Cite Traceability: PREFIX-UC-XXX | PREFIX-TC-XXX in
// the runnable test file's header comment when this is translated to
// `tests/<package>/...`.
```
