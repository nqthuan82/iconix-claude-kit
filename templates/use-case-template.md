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
- **Actor(s):** <primary actor>; <secondary actors with role notes>
- **Preconditions:** <what must be true before — static preconditions only; runtime branches go in alternate courses>
- **Postconditions:**
  - **Success:** <what is true when the basic course completes successfully>
  - **Rejection:** <what is true when the UC ends in a rejection alternate course>
  <!-- Add additional outcome states (e.g., "Cancelled:", "Partial:") if the UC has more than two distinct end states. Most UCs need only Success + Rejection. -->

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
- **Invokes (UC calls):**
  <!-- This UC's basic or alternate course CALLS another UC's flow and waits for its
       result (control transfers and returns). Format: `<PREFIX>-UC-XXX | <Title> | <Package> (course-ref)`.
       Write `(none)` if this UC invokes no others. See PO agent rule 12. -->
  - <PREFIX>-UC-XXX | <Title> | <Package> (alt A)
- **UI dependencies (page/component reuse):**
  <!-- This UC reuses a UI element (page, component, dialog) owned by another UC,
       but does NOT invoke that UC's flow. Common case: error pages, shared chrome. -->
  - <PREFIX>-UC-XXX | <Title> | <Package> (alt E reuses <Page Name>)
- **Downstream consumers:**
  <!-- Other UCs that consume artifacts this UC produces (queued items, events, side
       effects). NOT an invocation — handoff is async/decoupled. -->
  - <PREFIX>-UC-XXX | <Title> | <Package> (consumes <produced thing>)
- **Domain entities introduced (new on domain model):** <comma-separated list of entities this UC adds to the domain model for the first time, or "(none — all already present)">
- **Domain entities used (already on domain model):** <comma-separated list of entities this UC references but didn't introduce>
- **Robustness diagram:** (filled by Analyst)
- **Sequence diagram:** (filled by Developer)
- **Test cases:** (filled by Tester)
