# BRD: `<Project Name>` v`<X.Y>` — `<YYYY-MM-DD>`

## 1. Executive summary
`<One paragraph: why this change, who benefits, expected outcome.>`

## 2. Business objectives
| ID | Objective | Measure of success |
|---|---|---|
| BO-1 | `<objective>` | `<KPI / target>` |

## 3. Scope
**In scope:**
- `<bullet>`

**Out of scope (explicit):**
- `<bullet>`

## 4. Stakeholders and actors
| Role | Description | Relationship to system |
|---|---|---|
| `<Operator>` | `<description>` | primary user / secondary / regulator |

<!-- Every role listed here is a candidate Actor in a use case. -->

## 5. Current state
`<Brief description of as-is process and systems. Diagram optional.>`

## 6. Future state — business processes
`<Per process: narrative or flow describing the to-be flow. Reference screens by name where known.>`

## 7. Functional requirements
<!-- One row = one REQ-XXX.md file. Active voice, observable behaviour, no technology names. -->
| ID | Requirement | Source | Priority |
|---|---|---|---|
| FR-001 | The system shall `<observable behaviour, no tech>`. | `<stakeholder / section ref>` | P0 \| P1 \| P2 |

## 8. Non-functional requirements
<!-- Keep these separate from §7 — they feed the NFR catalogue in iconix.config.yaml. -->
| ID | Category | Statement | Measurable target |
|---|---|---|---|
| NFR-001 | Performance | `<behaviour>` | `<e.g., < 500 ms p95>` |
| NFR-002 | Security | `<behaviour>` | `<e.g., all write actions logged with actor + timestamp>` |
| NFR-003 | Availability | `<behaviour>` | `<e.g., 99.9% monthly>` |
| NFR-004 | Scalability | `<behaviour>` | `<e.g., 5,000 concurrent users>` |
| NFR-005 | Compliance | `<regulation>` | `<specific control required>` |

## 9. Business rules
<!-- Business rules are the richest source of alternate courses and validation paths in UCs. -->
| ID | Rule | Applies to |
|---|---|---|
| BR-001 | `<constraint expressed as a domain rule>` | FR-00X |

## 10. Assumptions, constraints, dependencies
- **Assumption:** `<what is taken as true without verification>`
- **Constraint:** `<fixed boundary the solution cannot change>`
- **Dependency:** `<upstream system, team, or decision required>`

## 11. Glossary
<!-- Every term here is a candidate entity in the domain model and must match UC text exactly. -->
| Term | Definition |
|---|---|
| `<term>` | `<definition>` |

## 12. Acceptance criteria (per requirement)
<!-- Per-requirement acceptance criteria — not just project-level. -->
- **FR-001:** `<measurable condition that proves FR-001 is satisfied>`

## 13. Approvals
| Role | Name | Signature | Date |
|---|---|---|---|
| Product Owner | | | |
| Sponsor | | | |
