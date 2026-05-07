# Worked Example — Write Customer Review

A single feature traced end-to-end through every ICONIX phase. Use this as a reference for what "good" looks like at each artifact level.

## Source

Adapted from the canonical worked example in:

> Doug Rosenberg & Matt Stephens, *Use Case Driven Object Modeling with UML: Theory and Practice* (Apress, 2007) — chapters 3, 5, 8, 10, 11, 12.

The book threads the **Internet Bookstore / Write Customer Review** use case from raw stakeholder text all the way to source code and unit tests. We replay that thread here using the templates and traceability conventions of this kit.

## Project context

| | |
|---|---|
| **Project** | Internet Bookstore |
| **Prefix** | `BS` |
| **Stack** | C# + ASP.NET Core 9 (MVC + Razor) + EF Core 9 + xUnit |
| **Domain** | E-commerce / online retail |

> The book uses Java + Spring + JSP for the implementation chapters. This worked example replays the same use case on the .NET stack — domain text, requirements, use case, robustness, and tests all stay tech-agnostic; only the ADR, sequence diagram, and code samples change.

See [`iconix.config.example.yaml`](./iconix.config.example.yaml) for the project configuration.

## Thread map — one feature, ten artifacts, one traceability chain

Two artifacts span the whole project rather than belonging to a single phase: the **domain model** (continuously updated) and the **use case package overview** (updated whenever the package's UC roster changes). They appear before the per-feature thread and are referenced from it.

```
project-wide artifacts (continuously updated)
  ├─► domain-model.example.puml          (Analyst owns; updated when entities are discovered)
  └─► use-case-diagram.example.puml      (Product Owner owns; updated when UC roster changes)

per-feature thread for "Write Customer Review"
  intake email          ┐
  intake transcript     ├──► Product Owner ──► BS-REQ-001          (M1 gate)
  feature request       ┘                  └─► BS-UC-001
                                                  │
                                                  ▼
                                           Analyst ──► BS-RB-001   (object picture of UC)
                                                  │                    + may update domain model
                                                  ▼
                                         Architect ──► BS-ADR-001  (M2 gate)
                                                  │
                                                  ▼
                                         Developer ──► BS-SD-001   (sequence + class model)
                                                  │
                                                  ▼
                                            Tester ──► test plan
                                                  ├─► BS-TC-001 (system   — basic course)
                                                  ├─► BS-TC-002 (unit     — rating out of range)
                                                  ├─► BS-TC-003 (unit     — review too short)
                                                  ├─► BS-TC-004 (system   — not logged in)
                                                  ├─► BS-TC-007 (integration — pending queue)
                                                  ├─► BS-TC-101 (acceptance  — stakeholder-signed)
                                                  └─► BS-TC-021 (regression  — supersedes BS-TC-003)  (M3 gate)

                                         Maintenance ──► BS-CI-001 (change impact: add title-length rule)
                                                                    + updates domain model + UC diagram
```

## File index

| # | File | Phase | Artifact |
|---|---|---|---|
| 00 | [`README.md`](./README.md) | — | this file |
| — | [`domain-model.example.puml`](./domain-model.example.puml) | project-wide | Domain model (continuously updated) |
| — | [`use-case-diagram.example.puml`](./use-case-diagram.example.puml) | project-wide | UC package overview (updated when roster changes) |
| 01 | [`01-intake-email.example.md`](./01-intake-email.example.md) | Intake | Stakeholder email |
| 02 | [`02-intake-transcript.example.md`](./02-intake-transcript.example.md) | Intake | Analyst interview |
| 03 | [`03-feature-request.example.md`](./03-feature-request.example.md) | Intake | Connextra-style request |
| 04 | [`04-BS-REQ-001-submit-customer-review.example.md`](./04-BS-REQ-001-submit-customer-review.example.md) | Product Owner | Requirement |
| 05 | [`05-BS-UC-001-write-customer-review.example.md`](./05-BS-UC-001-write-customer-review.example.md) | Product Owner | Use case |
| 06 | [`06-BS-RB-001-write-customer-review.example.puml`](./06-BS-RB-001-write-customer-review.example.puml) | Analyst | Robustness diagram |
| 07 | [`07-BS-ADR-001-validation-strategy.example.md`](./07-BS-ADR-001-validation-strategy.example.md) | Architect | Architecture decision |
| 08 | [`08-BS-SD-001-write-customer-review.example.puml`](./08-BS-SD-001-write-customer-review.example.puml) | Developer | Sequence diagram |
| 09 | [`09-test-plan.example.md`](./09-test-plan.example.md) | Tester | Test plan |
| 10 | [`10-BS-TC-001-display-write-review-page.example.md`](./10-BS-TC-001-display-write-review-page.example.md) | Tester | Test case (basic course) |
| 11 | [`11-BS-TC-002-rating-out-of-range.example.md`](./11-BS-TC-002-rating-out-of-range.example.md) | Tester | Test case (alt course) |
| 12 | [`12-BS-TC-003-review-too-short.example.md`](./12-BS-TC-003-review-too-short.example.md) | Tester | Test case (alt course) |
| 13 | [`13-BS-TC-004-not-logged-in.example.md`](./13-BS-TC-004-not-logged-in.example.md) | Tester | Test case (alt course) |
| 14 | [`14-BS-CI-001-add-title-length-rule.example.md`](./14-BS-CI-001-add-title-length-rule.example.md) | Maintenance | Change impact report |
| 15 | [`15-BS-TC-007-pending-queue-integration.example.md`](./15-BS-TC-007-pending-queue-integration.example.md) | Tester | Test case (integration — boundary↔entity) |
| 16 | [`16-BS-TC-101-stakeholder-happy-path.example.md`](./16-BS-TC-101-stakeholder-happy-path.example.md) | Tester | Test case (acceptance — Reqnroll, stakeholder-signed) |
| 17 | [`17-BS-TC-021-supersedes-BS-TC-003.example.md`](./17-BS-TC-021-supersedes-BS-TC-003.example.md) | Tester | Test case (regression — supersedes BS-TC-003 after BS-CI-001) |
| — | [`iconix.config.example.yaml`](./iconix.config.example.yaml) | — | Project config |

## How to read this example

1. **Start at the intake** (files 01–03). Notice that early stakeholder text is verbose, ambiguous, and full of solution-language — exactly what you will receive in real life.
2. **Watch the disambiguation** as you move into the Product Owner phase (files 04–05). Domain nouns get pinned down. Alternate courses surface. Validation rules become explicit.
3. **At the Analyst phase** (file 06), the use case text is pasted directly onto the robustness diagram. Each controller will become a method on the sequence diagram and a test case in the test plan.
4. **At the Architect phase** (file 07), an ADR captures the only *novel* design decision in the use case — where validation logic lives. Routine framework choices do not need an ADR.
5. **At the Developer phase** (file 08), the sequence diagram has one lifeline per entity/boundary from the robustness diagram. Each controller is converted to a message.
6. **At the Tester phase** (files 09–13), each robustness controller becomes a test case. Each alternate course produces at least one alternate test scenario.
7. **For change management** (file 14), see how a single rule addition (review title length validation) ripples through every downstream artifact.

## Traceability you can verify

Pick any ID in the chain and grep the directory — every artifact that mentions it is the set of artifacts impacted by that ID:

```bash
grep -r BS-REQ-001 examples/write-customer-review/
grep -r BS-UC-001  examples/write-customer-review/
grep -r BS-RB-001  examples/write-customer-review/
```

That is the same property the Traceability Agent checks at every milestone gate.
