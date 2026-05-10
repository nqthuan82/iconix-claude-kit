# UC-XXX: <Use Case Title>

<!--
  Brevity rule: this whole file should fit on ONE PAGE when rendered.
  The structured `## Alternate Course A` / `B` / ... headings below are the
  correct format (one H2 per alternate), but the total length stays
  readable. If it overflows one page, split per
  agents/iconix-product-owner.md `# When to split a use case`.

  Conditional path forks at a step (e.g., "if logged in then X else Y") do
  NOT go in the Basic Course. The Basic Course is the happy path with all
  preconditions met; runtime forks become Alternate Courses. Static
  preconditions go in the Preconditions metadata field.
-->

## Metadata
- **ID:** `<PREFIX>-UC-XXX`
- **Actor(s):** <primary actor>
- **Preconditions:** <what must be true before — static preconditions only; runtime branches go in alternate courses>
- **Postconditions:** <what is true after basic course>

## Basic Course

| User Action | System Response |
|---|---|
| 1. ... | 1. ... |
| 2. ... | 2. ... |

## Alternate Course A: <name>

> Convention: the first row's `User Action` cell starts with "At step N, if <condition>:" so the deviation point in the basic course is obvious.

| User Action | System Response |
|---|---|
| A1. At step N, if `<condition>`: ... | A1. ... |

## Alternate Course B: <name>

| User Action | System Response |
|---|---|
| B1. At step N, if `<condition>`: ... | B1. ... |

<!-- Add ## Alternate Course C, D, ... as needed; one H2 per alternate. -->

## Traceability
- **Intakes:** <comma-separated list of intake files this UC consolidates — see PO agent `# When multiple intakes describe the same goal`>
- **Requirements:** REQ-XXX, REQ-YYY
- **Robustness diagram:** (filled by Analyst)
- **Sequence diagram:** (filled by Developer)
- **Test cases:** (filled by Tester)
