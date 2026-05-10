# `<Verb-led title — noun-verb-noun>`

## Story (Connextra)
**As a** `<specific role — not "user">`
**I want** `<observable outcome — not a solution or technology>`
**So that** `<business or user benefit>`

## Context / problem
`<One paragraph: what is wrong or missing today, what triggers this request.>`

## Acceptance criteria (Gherkin)

```gherkin
Feature: <feature name>

  Scenario: Basic — <happy path name>
    Given <precondition with named screen or system state>
    And <precondition>
    When <Actor> <action> on <named UI element / screen>
    Then the system <observable response>
    And the system <observable response>

  Scenario: Alternate — <error or branch name>
    Given <precondition>
    When <Actor> <action>
    Then the system <observable failure response>
    And the system <observable recovery or message>

  Scenario: Alternate — <second branch if needed>
    Given <precondition>
    When <Actor> <action>
    Then the system <observable response>
```

<!-- Each Scenario maps to one course of action in the two-column UC:           -->
<!-- Basic Scenario  → Basic Course table                                        -->
<!-- Alternate Scenario → Alternate Course table                                 -->
<!-- Given           → Preconditions                                             -->
<!-- When <action>   → User Action column row                                    -->
<!-- Then <response> → System Response column row                                -->

## Out of scope
- `<explicit exclusion>`

## NFR notes
<!-- Do NOT put NFRs inside Gherkin Then-clauses. List them here instead.       -->
<!-- They feed iconix.config.yaml nfr_catalog and ADRs, not UC text.            -->
| Category | Constraint | Measurable target |
|---|---|---|
| Performance | `<e.g., page load>` | `<e.g., < 2 s for 10k records>` |
| Security | `<e.g., auth required>` | `<specific control>` |
| Compliance | `<regulation>` | `<specific requirement>` |
| Availability | `<e.g., always available>` | `<e.g., 99.9% monthly>` |

## UI / screens
- `<Screen name>` — `<link to mock | "TBD">`
- Named controls used: `<Button name>`, `<field name>`, `<menu item>`

## Dependencies and assumptions
- **Depends on:** `<ticket / REQ / external system>`
- **Assumes:** `<shared state or precondition>`

## INVEST self-check
- [ ] **Independent** — no hidden coupling to other open stories
- [ ] **Negotiable** — scope can be discussed before extraction
- [ ] **Valuable** — benefit clause describes real stakeholder value
- [ ] **Estimable** — clear enough to size
- [ ] **Small** — fits a sprint; UC will fit on one page when rendered (split if not)
- [ ] **Testable** — every "Then" clause is observable and unambiguous

## Priority
P0 — must have | P1 — should have | P2 — nice to have

## Linked artifacts
- **Parent epic:** `<id>`
- **REQs** (filled by Product Owner): *(to be added)*
- **UCs** (filled by Product Owner): *(to be added)*
