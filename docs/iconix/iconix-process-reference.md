# ICONIX Process Reference & Kit Coverage Matrix

Source: *Use Case Driven Object Modeling with UML: Theory and Practice*
by Doug Rosenberg & Matt Stephens (Apress, 2007).

This document maps every Top 10 list and key rule from the book to the corresponding
agent, template, or command in the iconix-kit. Use it to audit coverage gaps.

**Status legend**
- ✅ Covered — rule is explicitly enforced in the kit
- ⚠️ Partial — rule is implied or partially present
- ❌ Missing — rule has no representation in the kit

---

## Chapter 1 — Introduction to ICONIX Process

### Core pipeline

| Concept | Kit coverage | Where |
|---|---|---|
| Requirements → Analysis/Preliminary Design → Detailed Design → Implementation | ✅ | `iconix-orchestrator.md` phase detection |
| Milestone 1 (Requirements Review) | ✅ | `iconix-traceability.md` M1 gate |
| Milestone 2 (Preliminary Design Review) | ✅ | `iconix-traceability.md` M2 gate |
| Milestone 3 (Critical Design Review) | ✅ | `iconix-traceability.md` M3 gate |
| Traceability chain REQ → UC → RB → SD → CLS → TC | ✅ | All agents; `iconix-traceability.md` validates at every gate |
| Persona analysis | ❌ | Not in kit — no persona template or agent step |
| Test-Driven Development (TDD) integration | ❌ | Not in kit — Tester drives tests from RBs, not from failing code first |
| Driving test cases from robustness diagrams | ✅ | `iconix-tester.md` — one TC per controller |

---

## Chapter 2 — Domain Modeling

### Top 10 Domain Modeling Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Focus on real-world objects (not technical/GUI) | ✅ | `iconix-analyst.md` `# Domain model rules` rule 1 — "real-world objects only" |
| 9 | Use generalization (is-a) and aggregation (has-a) relationships | ✅ | `iconix-analyst.md` `# Domain model rules` rule 4 |
| 8 | Time-box initial domain model to a couple of hours | ✅ | `iconix-analyst.md` `# Domain model rules` rule 5 |
| 7 | Organize around key abstractions from the problem domain | ✅ | `iconix-analyst.md` `# Domain model rules` rules 1 + 3 (real-world objects + glossary) |
| 6 | Don't mistake the domain model for a data model | ✅ | `iconix-analyst.md` `# Domain model rules` rule 2 |
| 5 | Don't confuse a domain object with a database table | ✅ | `iconix-analyst.md` `# Domain model rules` rule 2 |
| 4 | Use the domain model as the project glossary | ✅ | `iconix-analyst.md` `# Domain model rules` rule 3 — "domain model = project glossary" |
| 3 | Draw the domain model before writing use cases | ✅ | Orchestrator enforces Product Owner → Analyst order (domain model first) |
| 2 | Don't expect the domain model to match final class diagrams exactly | ✅ | `iconix-analyst.md` `# Domain model rules` rule 6 |
| 1 | Don't put GUI classes on the domain model | ✅ | `iconix-analyst.md` `# Domain model rules` rule 1 |

---

## Chapter 3 — Use Case Modeling

### Top 10 Use Case Modeling Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Two-paragraph rule — UC must fit in two paragraphs (basic + alternate courses) | ✅ | `iconix-product-owner.md` rule 3 + M1 checklist item 3 |
| 9 | Organize use cases with actors and use case diagrams (packages) | ⚠️ | Product Owner groups UCs but no use case diagram artifact |
| 8 | Write use cases in active voice | ✅ | `iconix-product-owner.md` — "active voice" stated |
| 7 | Write use case using event/response flow (user action → system response) | ✅ | Two-column UC format (User Action / System Response) |
| 6 | Use UI storyboards and attach them to use cases | ❌ | No storyboard template or guidance |
| 5 | Use case is a runtime behavior specification — drive design from it | ✅ | Full pipeline is UC-driven |
| 4 | Write use case in context of the object model (reference domain classes by name) | ✅ | Product Owner rule: "reference domain objects by name" |
| 3 | Write use cases using noun-verb-noun sentence structure | ⚠️ | Implied by robustness rules; not stated in Product Owner |
| 2 | Reference domain classes by name | ✅ | Product Owner |
| 1 | Reference boundary classes (screens) by name | ✅ | Product Owner and Analyst both enforce named screens |

**Gap summary:** Two-paragraph rule (#10) closed in v0.6.0. UI storyboard guidance (#6) remains absent (out of kit scope).

---

## Chapter 4 — Requirements Review (M1)

### Top 10 Requirements Review Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Domain model describes ≥80% of key problem-domain abstractions | ❌ | M1 gate checks REQ→UC links; does not audit domain model coverage |
| 9 | Domain model shows is-a and has-a relationships | ❌ | Not checked at M1 |
| 8 | Use cases describe both basic and alternate courses, in active voice | ✅ | M1 checklist in Product Owner |
| 7 | Passive-voice "shall" requirements are NOT mixed into active-voice UC text | ✅ | `iconix-product-owner.md` rule 6 + M1 checklist item 4 |
| 6 | Use cases organized into packages with at least one UC diagram per package | ❌ | No UC diagram artifact |
| 5 | Use cases written in context of the object model | ✅ | Product Owner rule |
| 4 | Use cases written in context of the user interface (screens named) | ✅ | Product Owner + Analyst rule |
| 3 | UCs supplemented with storyboard / screen mock-up / GUI prototype | ❌ | No storyboard step |
| 2 | Review with end users, stakeholders, marketing, and technical staff | ❌ | Kit is AI-agent-driven; human review gating is not modeled |
| 1 | Structure review using eight easy steps | ⚠️ | M1 checklist now has 8 items aligned to these steps; human review participation still not modeled |

**Eight easy steps to a better use case (M1 sub-checklist):**

| Step | Status | Kit location |
|---|---|---|
| 1. Remove everything out of scope | ❌ | Not in M1 checklist |
| 2. Change passive voice to active voice | ✅ | `iconix-product-owner.md` M1 checklist item 4 — no "shall" in UC text |
| 3. Check that use case text is not too abstract | ✅ | `iconix-product-owner.md` M1 checklist item 5 — every screen/field/object named |
| 4. Accurately reflect the GUI | ⚠️ | Screens-named rule covers this partially |
| 5. Name participating domain objects | ✅ | Explicitly in Product Owner |
| 6. Make sure you have all the alternate courses | ✅ | M1 checklist |
| 7. Trace each requirement to its use cases | ✅ | Traceability agent — REQ→UC allocation |
| 8. Make each use case describe what the users are trying to do | ⚠️ | Active voice rule covers this partially |

---

## Chapter 5 — Robustness Analysis

### Top 10 Robustness Analysis Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Paste the use case text directly onto the robustness diagram | ✅ | `iconix-analyst.md` step 4 — UC text embedded as comment block in `.puml` |
| 9 | Take entity classes from the domain model; add any missing ones | ✅ | Analyst rule |
| 8 | Expect to rewrite the use case while drawing the robustness diagram | ✅ | Analyst updates UC in parallel with RB |
| 7 | Make a boundary object for each screen (unambiguous names) | ✅ | `iconix-analyst.md` `# Boundary object naming` — generic labels rejected, real name required |
| 6 | Controllers are typically logical software functions, not control classes | ⚠️ | Mentioned implicitly; no explicit anti-controller-class rule |
| 5 | Don't worry about the direction of the arrows on a robustness diagram | ❌ | Not stated; arrow direction is irrelevant to the two RB goals |
| 4 | Show invoked use cases on the robustness diagram | ❌ | Not mentioned in Analyst |
| 3 | Robustness diagram = conceptual design, not literal detailed design | ⚠️ | Implied; not stated |
| 2 | Boundary/entity → object instances on SD; controllers → messages on SD | ✅ | Developer agent explicitly converts controllers to messages |
| 1 | RB is an "object picture" of a UC — forces refinement of UC text and object model | ✅ | Core purpose stated in Analyst |

### Connection rules (all four must be enforced)

| Rule | Status | Kit location |
|---|---|---|
| Actor ↔ Boundary: allowed | ✅ | `iconix-analyst.md` |
| Boundary ↔ Controller: allowed | ✅ | `iconix-analyst.md` |
| Controller ↔ Controller: allowed | ✅ | `iconix-analyst.md` |
| Controller ↔ Entity: allowed | ✅ | `iconix-analyst.md` |
| Actor → Controller or Entity: **FORBIDDEN** | ✅ | `iconix-analyst.md` |
| Boundary ↔ Entity (no controller): **FORBIDDEN** | ✅ | `iconix-analyst.md` |
| Entity ↔ Entity (no controller): **FORBIDDEN** | ✅ | `iconix-analyst.md` |
| Boundary ↔ Boundary (no controller): **FORBIDDEN** | ✅ | `iconix-analyst.md` |

---

## Chapter 6 — Preliminary Design Review (M2 gate)

### Top 10 PDR Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Highlighter test: UC text matches RB diagram, sentence by sentence | ✅ | M2 gate in `iconix-traceability.md` |
| 9 | All entities on all RBs appear in the updated domain model | ✅ | Analyst adds new entities to domain model |
| 8 | Trace data flow between entity classes and screens | ⚠️ | Not an explicit M2 check |
| 7 | Don't forget alternate courses; write behavior for each one | ✅ | Analyst rule |
| 6 | Each UC covers both sides of user/system dialogue | ✅ | Two-column format enforces this |
| 5 | Syntax rules for robustness analysis not violated | ✅ | Analyst validates four connection rules |
| 4 | Review includes both nontechnical (customer) and technical folks | ❌ | Human review step not modeled |
| 3 | Use cases in context of both object model and GUI — "magic abstraction level" | ✅ | Product Owner + Analyst both enforce this |
| 2 | Don't drift into detailed design territory on robustness diagrams | ⚠️ | Stated as conceptual design; no explicit guard |
| 1 | Follow "Six Easy Steps" to a better PDR (meta-checklist: match diagram to UC text, validate syntax rules, check domain model/GUI context, trace data flow, ensure both dialogue sides, include non-technical reviewers) | ⚠️ | Technical checks covered by M2 gate; human reviewer participation not modeled |

---

## Chapter 7 — Technical Architecture

### Top 10 Technical Architecture Errors ("Don'ts")

| # | Error | Status | Kit location |
|---|---|---|---|
| 10 | Picking architecture without considering hardware cost | ❌ | Not covered |
| 9 | Using old legacy architecture by default | ❌ | Not covered |
| 8 | Not considering scalability | ✅ | NFR catalog in `iconix.config.yaml` includes scalability |
| 7 | Not considering security | ✅ | NFR catalog includes security |
| 6 | Picking new technology without sufficient experience/evidence | ❌ | Not covered |
| 5 | Failing to formulate the TA objectively based on the project's requirements | ❌ | Not covered; Architect agent has no requirement-driven TA validation |
| 4 | Spending too long on the architecture before delving into design (architectural paralysis) | ❌ | Not covered |
| 3 | Forgetting how the system will be tested | ⚠️ | Tester agent is part of pipeline but not integrated with Architect |
| 2 | Defining TA before understanding what users need to do | ✅ | Orchestrator enforces: Product Owner → Analyst → Architect order |
| 1 | Failing to do an architecture at all | ✅ | Architect is a required pipeline phase |

**Key TA concepts covered by kit:**

| Concept | Status | Kit location |
|---|---|---|
| Container/layer mapping from use cases | ✅ | `iconix-architect.md` |
| NFR catalog (performance, availability, security, scalability, compliance, observability) | ✅ | `iconix.config.yaml` + Architect |
| Architecture Decision Records (ADRs) | ✅ | `templates/adr-template.md` + Architect |
| Layered architecture | ✅ | Architect — containers map to layers |

---

## Chapter 8 — Sequence Diagrams

### Top 10 Sequence Diagramming Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Understand why: allocate behavior (functions → operations on classes) | ✅ | Developer agent core purpose |
| 9 | Do a sequence diagram for every use case (basic + alternate courses on one diagram) | ✅ | `iconix-developer.md` — one SD per UC, all courses |
| 8 | Start from robustness diagram — objects from RB become objects on SD | ✅ | Developer agent step 1 |
| 7 | Show how UC behavior (all controllers from RB) is accomplished by objects | ✅ | Developer maps controllers to messages |
| 6 | Map UC text to messages on the SD; line up text and arrows | ✅ | `iconix-developer.md` step 2 — UC steps as `group` blocks in PlantUML |
| 5 | Don't spend too much time worrying about focus of control | ❌ | Not stated |
| 4 | Assign operations to classes while drawing messages | ✅ | Developer updates class model |
| 3 | Review class diagrams frequently while assigning operations | ✅ | Developer updates `class-model.puml` in parallel |
| 2 | Prefactor design on sequence diagrams before coding | ⚠️ | Implied; no explicit prefactoring instruction |
| 1 | Clean up the static model before proceeding to CDR | ✅ | M3 gate requires class model complete |

**Four Essential Steps (SD construction):**

| Step | Status | Kit location |
|---|---|---|
| 1. Copy use case text straight into the diagram | ✅ | `templates/sequence-template.puml` + Developer agent |
| 2. Place objects across the top (from RB boundary/entity objects) | ✅ | Developer agent — start from RB |
| 3. Add messages (from RB controllers) | ✅ | Developer agent — controllers → messages |
| 4. Assign operations to classes as messages are added | ✅ | Developer updates class model |

---

## Chapter 9 — Critical Design Review (M3 gate)

### Top 10 CDR Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Sequence diagram matches use case text | ✅ | `iconix-reviewer.md` drift detection + M3 gate |
| 9 | Each SD accounts for both basic and alternate courses of action | ✅ | Developer + Reviewer |
| 8 | Operations allocated to classes appropriately | ✅ | Developer + Reviewer |
| 7 | All classes have appropriate attributes and operations | ⚠️ | M3 checks SD→CLS links; attribute completeness not checked |
| 6 | Patterns/implementation constructs reflected on SD | ❌ | Not covered |
| 5 | Functional and NFR requirements traced to UCs and classes | ✅ | Traceability agent — full chain validation |
| 4 | Programmers "sanity check" — confident they can build it | ❌ | No human sanity-check step |
| 3 | Attributes typed correctly; return values and parameter lists complete | ❌ | Not in kit |
| 2 | Generate code headers and inspect them | ❌ | Not in kit |
| 1 | Review the test plan for the release | ⚠️ | Tester produces test matrix; no explicit CDR link to test plan |

---

## Chapter 10 — Implementation

### Top 10 Implementation Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Drive code directly from the design | ✅ | Developer agent core principle |
| 9 | If coding reveals design is wrong, change it and review the process | ✅ | Reviewer detects drift; bug Type 2 flow triggers design update |
| 8 | Hold regular code inspections | ✅ | `iconix-reviewer.md` — drift detection = code inspection |
| 7 | Always question the framework's design choices | ❌ | Not covered |
| 6 | Don't let framework issues take over business issues | ❌ | Not covered |
| 5 | If code gets out of control, revisit the design | ✅ | Bug Type 2 flow re-runs Traceability → full change pipeline |
| 4 | Keep design and code in sync | ✅ | Reviewer + M3 gate |
| 3 | Focus on unit testing while implementing code | ✅ | Developer is expected to write unit tests |
| 2 | Don't overcomment code | ❌ | Not in kit (out of scope for agent prompts) |
| 1 | Implement the alternate courses, not just the basic course | ✅ | Developer + Tester — both handle alternate courses |

---

## Chapter 11 — Code Review and Model Update

### Top 10 Code Review and Model Update Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Prepare for review; participants read material in advance | ❌ | Not modeled (human process) |
| 9 | Create high-level review list based on use case titles | ✅ | `iconix-reviewer.md` — checklist per UC |
| 8 | Break each UC item into a smaller checklist | ✅ | Reviewer walks RB controllers per UC |
| 7 | Review code at several levels (conventions, design adherence, UC trace) | ✅ | Reviewer checks code vs SD vs UC |
| 6 | Gather data; build boilerplate checklists for future reviews | ❌ | Reviewer produces one-shot report; no accumulation |
| 5 | Follow up review with action points | ✅ | Reviewer produces BLOCK/CHANGES/APPROVE report with items |
| 4 | Focus on error detection, not correction | ✅ | Reviewer identifies drift; Developer fixes |
| 3 | Use integrated code/model browser | ❌ | Tooling choice; not in kit scope |
| 2 | Keep it "just formal enough" | ✅ | Reviewer uses structured but lightweight format |
| 1 | Remember it is also a Model Update session | ✅ | Reviewer updates artifacts + flags design drift |

**Drift detection coverage:**

| Drift type | Status | Kit location |
|---|---|---|
| Code does not match sequence diagram | ✅ | Reviewer core function |
| Code does not match class model | ✅ | Reviewer |
| Code does not match NFRs | ✅ | Reviewer |
| SD does not match UC text | ✅ | Reviewer |
| Bug type classification (Type 1 vs Type 2) | ✅ | `iconix-reviewer.md` `# Bug triage` |

---

## Chapter 12 — Design-Driven Testing

### Top 10 Design-Driven Testing Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | "Testing mind-set": every bug found is a victory | ❌ | Philosophy; not in agent |
| 9 | Understand different kinds of testing (V-model) | ❌ | No test-type taxonomy in Tester |
| 8 | Create one or more TCs for each controller on each RB | ✅ | `iconix-tester.md` — one TC per controller |
| 7 | Don't leave testing until after the code has been written (test-first thinking) | ❌ | Kit creates TCs from RBs before coding but does not explicitly enforce test-first order |
| 6 | Requirement-level verification: each REQ is implemented | ✅ | Traceability validates REQ→UC→TC chain |
| 5 | Use a traceability matrix | ✅ | `iconix-traceability.md` + `test-matrix.md` |
| 4 | Scenario-level acceptance testing for each UC | ✅ | Tester produces TCs covering basic + alternate courses |
| 3 | Expand threads to cover complete path (basic + each alternate) | ✅ | Tester covers alternate courses |
| 2 | Use a testing framework (JUnit/xUnit) to store and organize tests | ✅ | `iconix.config.yaml` `test_framework` configures this |
| 1 | Keep unit tests fine-grained | ⚠️ | Implied; not stated as explicit Tester rule |

**Unit test derivation from RB controllers:**

| Concept | Status | Kit location |
|---|---|---|
| One unit test class per controller (test case) | ✅ | `iconix-tester.md` |
| One test method per UC scenario (basic + alternate) | ✅ | Tester TC format: Steps mirror UC rows |
| Test named after UC scenario of origin | ✅ | TC naming convention |
| Tests written from point of view of object calling controller | ⚠️ | Not explicitly stated |

### V-Model: test types vs. ICONIX stages

| Test type | ICONIX stage | Status |
|---|---|---|
| Unit testing | After detailed design | ✅ |
| Integration testing | After PDR | ⚠️ Partial — no explicit integration test guidance |
| System testing | After CDR | ⚠️ |
| Acceptance testing | After system testing | ❌ |
| Regression testing | After each release | ⚠️ Reviewer has regression check for bug fixes |

---

## Chapter 13 — Requirements Gathering and Traceability

### Top 10 Requirements Gathering Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Use a modeling tool with linkage and traceability between REQs and UCs | ✅ | Traceability agent + `ids.registry.md` |
| 9 | Link requirements to use cases (drag-and-drop / `## Traceability` block) | ✅ | Every artifact has `## Traceability` section |
| 8 | Avoid dysfunctional requirements — keep "shall" statements out of UC text | ✅ | `iconix-product-owner.md` rule 6 + M1 checklist item 4 |
| 7 | Write at least one test case for each requirement | ✅ | REQ→UC→TC chain; coverage matrix validates this |
| 6 | Treat requirements as first-class citizens (explicit REQ files) | ✅ | `requirements/REQ-XXX.md` per requirement |
| 5 | Distinguish between different types of requirements (functional vs. NFR) | ✅ | `iconix.config.yaml` NFR catalog; separate NFR annotation files |
| 4 | Avoid the "big monolithic document" syndrome | ✅ | One file per REQ/UC/RB/SD/TC |
| 3 | Create estimates from UC scenarios, not functional requirements | ❌ | No estimation guidance in kit |
| 2 | Don't be afraid of examples in functional requirements | ❌ | `req-template.md` has no examples guidance |
| 1 | Don't make requirements a technical fashion statement | ❌ | Not covered |

**Dysfunctional requirements detection:**

| Pattern | Status | Kit location |
|---|---|---|
| Passive voice "shall" statements in UC text | ✅ | `iconix-product-owner.md` rule 6 — detected and relocated to REQ file |
| Intermangled NFRs in UC text | ❌ | Not detected |
| Repeated requirements inline in multiple UCs | ❌ | Not detected |

---

## Summary Coverage Matrix

Coverage formula: (✅ × 1 + ⚠️ × 0.5) ÷ total items

| Chapter | Topic | ✅ | ⚠️ | ❌ | Coverage |
|---|---|---|---|---|---|
| 1 | ICONIX pipeline + milestones | 6 | 0 | 2 | **75%** |
| 2 | Domain modeling | 10 | 0 | 0 | **100%** |
| 3 | Use case modeling | 7 | 2 | 1 | **80%** |
| 4 | Requirements Review (M1) | 4 | 2 | 4 | **50%** |
| 5 | Robustness analysis (Top 10) | 6 | 2 | 2 | **70%** |
| 6 | PDR (M2) | 6 | 3 | 1 | **75%** |
| 7 | Technical architecture | 4 | 1 | 5 | **45%** |
| 8 | Sequence diagrams | 8 | 1 | 1 | **85%** |
| 9 | CDR (M3) | 4 | 2 | 4 | **50%** |
| 10 | Implementation | 7 | 0 | 3 | **70%** |
| 11 | Code review + model update | 7 | 0 | 3 | **70%** |
| 12 | Design-driven testing | 6 | 1 | 3 | **65%** |
| 13 | Requirements traceability | 7 | 0 | 3 | **70%** |

---

## Top Gap Areas (Prioritized)

### Closed in v0.6.0

- ~~Two-paragraph rule~~ (Ch3) — `iconix-product-owner.md` rule 3 + M1 checklist
- ~~Passive voice / "shall" guard~~ (Ch3/4/13) — `iconix-product-owner.md` rule 6 + M1 checklist
- ~~Boundary object per screen~~ (Ch5) — `iconix-analyst.md` `# Boundary object naming`
- ~~Domain model rules~~ (Ch2) — `iconix-analyst.md` `# Domain model rules`
- ~~Eight easy steps~~ (Ch4) — M1 checklist expanded and aligned

### Priority 1 — Medium impact, moderate effort

1. **CDR test plan review** (Ch9 #1): Tester should produce a test plan summary before CDR that the Orchestrator links to the M3 gate.
2. **NFR requirements in trace chain** (Ch9 #5): Traceability should explicitly validate NFRs → UCs, not just functional REQs.
3. **Integration and acceptance test types** (Ch12 V-model): Add a test type table to Tester showing when each type of test applies.
4. **Invoked use cases on RB** (Ch5 #4): Analyst should note when a controller represents an invoked use case and show it on the diagram.

### Priority 2 — Out of kit scope (human-process items)

5. **Human review participants** (Ch4, Ch6): Requirements Review and PDR should include customers, end users, and marketing. Kit cannot model this but README could document it.
6. **UI storyboards** (Ch3 #6, Ch4 #3): Kit does not produce UI prototypes — document this gap in README as a recommended human step.
7. **Estimation from UC scenarios** (Ch13 #3): Out of scope for AI agents.
8. **Code headers generation** (Ch9 #2): Tool-specific; out of kit scope.
9. **Persona analysis** (Ch1): Would require a new `iconix-persona.md` agent.
