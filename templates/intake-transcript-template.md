# Interview: `<Stakeholder Name>` (`<Role>`) — `<YYYY-MM-DD>`

## Metadata
- **Interviewer:** `<name>`
- **Duration:** `<minutes>`
- **Recording:** `<link | "not recorded">`
- **Project:** `<project name>`
- **Next review:** `<date when output is expected>`

## Stakeholder profile
- **Role:** `<job title>` ← candidate Actor
- **Primary goals with the system:** `<what they use or will use the system for>`
- **Frequency of use:** daily | weekly | occasional | admin-only

## Current state — how it works today
`<Verbatim or paraphrased. Include screen and tool names wherever mentioned.>`

## Pain points
- `<one pain per bullet>`

## Desired future state (outcomes, not solutions)
- `<"I want to be able to <goal>" — not "we need feature X">`

## Scenario walkthrough — `<scenario name>`

> Ask: "Walk me through `<scenario>` step by step."

| Step | Who | Action / Response |
|---|---|---|
| 1 | `<Actor>` | Opens `<Screen name>`. |
| 2 | `<Actor>` | Enters `<field>` and clicks `<Button>`. |
| 3 | System | Shows `<named result / screen>`. |

### What if it fails?
- If `<condition>`, then `<observed system behaviour>`.
- If `<condition>`, then `<observed system behaviour>`.

<!-- Add more scenario walkthrough blocks as needed -->

## Constraints (NFR seeds)
| Category | Stated constraint | Measurable target (fill in or ask) |
|---|---|---|
| Performance | `<e.g., "must be fast">` | `<e.g., < 500 ms p95 — VERIFY>` |
| Security / compliance | `<e.g., "GDPR, audit trail">` | `<specific control — VERIFY>` |
| Availability | `<e.g., "always on">` | `<e.g., 99.9% monthly — VERIFY>` |
| Scale / volume | `<e.g., "many users">` | `<e.g., 5,000 concurrent — VERIFY>` |

## Open questions / parking lot
- [ ] `<question to follow up>`

---

> ⚠️ **Above this line: interview content captured live (input).**
> ⚠️ **Below this line: post-interview analysis for the Product Owner agent (output).**
>
> The interview content above is what was said during the meeting and should
> stay close to the stakeholder's words. The Analyst summary below is a
> structured hand-off to the PO agent — populated after the interview by the
> human analyst (the role conducting the interview, not the iconix-analyst
> agent). The PO agent reads this section as input to its intake checklist.

---

## Analyst summary
> Fill this in after the interview. This section is the hand-off to the Product Owner agent.

- **Candidate actors:** `<list of roles identified>`
- **Candidate use cases:** `<active-voice titles, noun-verb-noun>`
  - `<Actor> <verb> <object>` (e.g., "Operator places jackpot bet")
- **Candidate REQs:** `<observable "shall" statements — no tech names>`
  - The system shall `<behaviour>`.
- **Candidate NFRs:** `<category + measurable target>`
- **Gaps / must clarify before extraction:**
  - [ ] `<item marked [VERIFY]>`
