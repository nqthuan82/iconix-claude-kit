# ICONIX Process Reference & Kit Coverage Matrix

Source: *Use Case Driven Object Modeling with UML: Theory and Practice*
by Doug Rosenberg & Matt Stephens (Apress, 2007).

This document maps every Top 10 list and key rule from the book to the corresponding
agent, template, or command in the iconix-kit. Use it to audit coverage gaps.

**Status legend**
- ✅ Covered — rule is explicitly enforced in the kit
- ⚠️ Partial — rule is implied or partially present
- ❌ Missing — rule has no representation in the kit (gap to close)
- 🚫 Out of scope — deliberate boundary, see `README.md` `## What the kit intentionally does not cover`

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
| Persona analysis | 🚫 | Out-of-scope — see README footnote (requires primary user research) |
| TDD red-green-refactor cycle | 🚫 | Out-of-scope — kit derives TCs from RBs (design-driven test-first); see README footnote. **Distinct from "test-first thinking"** which IS in scope (Ch12 #7 ⚠️) |
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
| 3 | Draw the domain model before writing use cases | ✅ | `iconix-product-owner.md` rule 9 — PO drafts initial domain model after REQs and **before** UC flows; Analyst refines through robustness analysis (corrected v0.9.3) |
| 2 | Don't expect the domain model to match final class diagrams exactly | ✅ | `iconix-analyst.md` `# Domain model rules` rule 6 |
| 1 | Don't put GUI classes on the domain model | ✅ | `iconix-analyst.md` `# Domain model rules` rule 1 |

---

## Chapter 3 — Use Case Modeling

### Top 10 Use Case Modeling Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Two-paragraph rule — UC must fit in two paragraphs (basic + alternate courses) | ✅ | `iconix-product-owner.md` rule 3 + M1 checklist item 3 |
| 9 | Organize use cases with actors and use case diagrams (packages) | ✅ | `iconix-product-owner.md` `# Use case packaging rules` + M1 checklist; one `use-case-packages/<package-slug>.puml` per package; template at `templates/use-case-diagram-template.puml` (added v0.9.0) |
| 8 | Write use cases in active voice | ✅ | `iconix-product-owner.md` — "active voice" stated |
| 7 | Write use case using event/response flow (user action → system response) | ✅ | Two-column UC format (User Action / System Response) |
| 6 | Use UI storyboards and attach them to use cases | 🚫 | Out-of-scope — UI design tools (Figma, Balsamiq) are external; see README footnote |
| 5 | Use case is a runtime behavior specification — drive design from it | ✅ | Full pipeline is UC-driven |
| 4 | Write use case in context of the object model (reference domain classes by name) | ✅ | Product Owner rule: "reference domain objects by name" |
| 3 | Write use cases using noun-verb-noun sentence structure | ✅ | `iconix-product-owner.md` rule 7 — explicit noun-verb-noun rule with rewrite instruction |
| 2 | Reference domain classes by name | ✅ | Product Owner |
| 1 | Reference boundary classes (screens) by name | ✅ | Product Owner and Analyst both enforce named screens |

**Gap summary:** Two-paragraph rule (#10) closed in v0.6.0. UC package overview diagram (#9) closed in v0.9.0. UI storyboard guidance (#6) remains absent (out of kit scope).

---

## Chapter 4 — Requirements Review (M1)

### Top 10 Requirements Review Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Domain model describes ≥80% of key problem-domain abstractions | ✅ | `iconix-product-owner.md` M1 checklist — UC nouns with no domain model counterpart flagged for Analyst |
| 9 | Domain model shows is-a and has-a relationships | ✅ | `iconix-product-owner.md` M1 checklist — isolated floating entities with obvious real-world relationships flagged |
| 8 | Use cases describe both basic and alternate courses, in active voice | ✅ | M1 checklist in Product Owner |
| 7 | Passive-voice "shall" requirements are NOT mixed into active-voice UC text | ✅ | `iconix-product-owner.md` rule 6 + M1 checklist item 4 |
| 6 | Use cases organized into packages with at least one UC diagram per package | ✅ | `iconix-product-owner.md` `# Use case packaging rules`; M1 checklist enforces every UC belongs to one package; Traceability validates UC↔package overview links (added v0.9.0) |
| 5 | Use cases written in context of the object model | ✅ | Product Owner rule |
| 4 | Use cases written in context of the user interface (screens named) | ✅ | Product Owner + Analyst rule |
| 3 | UCs supplemented with storyboard / screen mock-up / GUI prototype | 🚫 | Out-of-scope — see README footnote |
| 2 | Review with end users, stakeholders, marketing, and technical staff | 🚫 | Out-of-scope — kit produces artifacts for human review meetings but does not convene them; see README footnote |
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
| 8. Make each use case describe what the users are trying to do | ✅ | `iconix-product-owner.md` M1 checklist item 8 — goal-oriented framing check (added v0.6.0) |

---

## Chapter 5 — Robustness Analysis

### Top 10 Robustness Analysis Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Paste the use case text directly onto the robustness diagram | ✅ | `iconix-analyst.md` step 4 — UC text embedded as comment block in `.puml` |
| 9 | Take entity classes from the domain model; add any missing ones | ✅ | Analyst rule |
| 8 | Expect to rewrite the use case while drawing the robustness diagram | ✅ | Analyst updates UC in parallel with RB |
| 7 | Make a boundary object for each screen (unambiguous names) | ✅ | `iconix-analyst.md` `# Boundary object naming` — generic labels rejected, real name required |
| 6 | Controllers are typically logical software functions, not control classes | ✅ | `iconix-analyst.md` `# Robustness diagram principles` — explicit anti-controller-class rule; maps to message on SD, not a class |
| 5 | Don't worry about the direction of the arrows on a robustness diagram | ✅ | `iconix-analyst.md` `# Robustness diagram principles` — arrow direction irrelevant; validate connection pair, not arrowhead |
| 4 | Show invoked use cases on the robustness diagram | ✅ | `iconix-analyst.md` `# Invoked use cases on robustness diagrams` |
| 3 | Robustness diagram = conceptual design, not literal detailed design | ✅ | `iconix-analyst.md` `# Robustness diagram principles` — explicit conceptual-only rule; method names/types forbidden |
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
| 8 | Trace data flow between entity classes and screens | ✅ | `iconix-analyst.md` PDR readiness check — unnamed Boundary↔Entity data flows flagged as ambiguities |
| 7 | Don't forget alternate courses; write behavior for each one | ✅ | Analyst rule |
| 6 | Each UC covers both sides of user/system dialogue | ✅ | Two-column format enforces this |
| 5 | Syntax rules for robustness analysis not violated | ✅ | Analyst validates four connection rules |
| 4 | Review includes both nontechnical (customer) and technical folks | 🚫 | Out-of-scope — see README footnote (human review meeting) |
| 3 | Use cases in context of both object model and GUI — "magic abstraction level" | ✅ | Product Owner + Analyst both enforce this |
| 2 | Don't drift into detailed design territory on robustness diagrams | ✅ | `iconix-analyst.md` PDR readiness check — method signatures/types on RB are a blocker before handoff |
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
| 5 | Failing to formulate the TA objectively based on the project's requirements | ✅ | `iconix-architect.md` rule 6 — every ADR must cite ≥1 REQ/NFR/UC; uncited ADRs flagged |
| 4 | Spending too long on the architecture before delving into design (architectural paralysis) | ✅ | `iconix-architect.md` rule 5 — time-box rule; unresolved decisions become `Proposed` ADRs, pipeline unblocked |
| 3 | Forgetting how the system will be tested | ✅ | `iconix-architect.md` `# Testability annotations` — every container must have ≥1 test seam; no-seam containers flagged at M2 gate |
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
| 5 | Don't spend too much time worrying about focus of control | ✅ | `iconix-developer.md` rule 7 — activation bars optional; SD purpose is operation allocation, not control timing |
| 4 | Assign operations to classes while drawing messages | ✅ | Developer updates class model |
| 3 | Review class diagrams frequently while assigning operations | ✅ | Developer updates `class-model.puml` in parallel |
| 2 | Prefactor design on sequence diagrams before coding | ✅ | `iconix-developer.md` rule 6 — SD must be complete before code skeletons are generated |
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
| 7 | All classes have appropriate attributes and operations | ✅ | `iconix-reviewer.md` check #2 — attribute completeness: entity classes with ≥2 operations and 0 attributes flagged as "attribute-sparse" |
| 6 | Patterns/implementation constructs reflected on SD | ✅ | `iconix-developer.md` rule 8 — design patterns shown on SD as lifelines; pattern hidden in code but absent from SD is drift |
| 5 | Functional and NFR requirements traced to UCs and classes | ✅ | Traceability agent — full chain + NFR→ADR validation check #9 |
| 4 | Programmers "sanity check" — confident they can build it | ❌ | No human sanity-check step |
| 3 | Attributes typed correctly; return values and parameter lists complete | ✅ | `iconix-reviewer.md` check #2 — untyped attributes flagged as "attribute untyped" |
| 2 | Generate code headers and inspect them | 🚫 | Out-of-scope — IDE/toolchain concern; see README footnote |
| 1 | Review the test plan for the release | ✅ | `iconix-tester.md` `# Pre-CDR test plan summary` — `test-plan/test-plan-<date>.md` checked at M3 gate |

---

## Chapter 10 — Implementation

### Top 10 Implementation Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Drive code directly from the design | ✅ | Developer agent core principle; `iconix-developer.md` `# Implementation mode` (Phase 9.1) makes this explicit (added v0.9.8) |
| 9 | If coding reveals design is wrong, change it and review the process | ✅ | Reviewer detects drift; bug Type 2 flow triggers design update; Reviewer's `# Type 2 closure mode` (v0.9.8) re-confirms the change actually addressed the reported issue |
| 8 | Hold regular code inspections | ✅ | `iconix-reviewer.md` `# Pre-merge drift mode` — Phase 9.2 makes the inspection routine on every Implementation PR (added v0.9.8) |
| 7 | Always question the framework's design choices | ✅ | `iconix-reviewer.md` check #6 — flags framework concerns mixed into business logic; no-ADR framework trade-offs flagged |
| 6 | Don't let framework issues take over business issues | ✅ | `iconix-reviewer.md` check #6 — flags methods with framework boilerplate but no visible domain behaviour |
| 5 | If code gets out of control, revisit the design | ✅ | Bug Type 2 flow re-runs Traceability → full change pipeline; Phase 9 iteration cap (`phase9.max_iterations_per_uc`) escalates a stuck Type 1 to Architect / PO before it becomes Type 2 (added v0.9.8) |
| 4 | Keep design and code in sync | ✅ | Reviewer + M3 gate; Phase 9.2 pre-merge drift check is the per-PR enforcement (added v0.9.8) |
| 3 | Focus on unit testing while implementing code | ✅ | Developer is expected to write unit tests; `iconix-tester.md` `# Test implementation mode` runs Tester in parallel with Developer at Phase 9.1 (added v0.9.8) |
| 2 | Don't overcomment code | ❌ | Not in kit (out of scope for agent prompts) |
| 1 | Implement the alternate courses, not just the basic course | ✅ | Developer + Tester — both handle alternate courses; Phase 9 Implementation mode explicitly cites Ch10 #1 (added v0.9.8) |

---

## Chapter 11 — Code Review and Model Update

### Top 10 Code Review and Model Update Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | Prepare for review; participants read material in advance | ⚠️ | `docs/iconix/templates/bug-report-template.md` (added v0.9.4) forces the bug reporter to surface the affected artifact, observed-vs-expected behaviour, exception trace, and reproduction *before* the Reviewer is invoked — partial coverage of "prepare review material in advance"; full guideline still includes a human meeting that the kit does not convene |
| 9 | Create high-level review list based on use case titles | ✅ | `iconix-reviewer.md` — checklist per UC |
| 8 | Break each UC item into a smaller checklist | ✅ | Reviewer walks RB controllers per UC |
| 7 | Review code at several levels (conventions, design adherence, UC trace) | ✅ | Reviewer checks code vs SD vs UC |
| 6 | Gather data; build boilerplate checklists for future reviews | ✅ | `iconix-reviewer.md` Rules — recurring defect patterns appended to `reviews/review-checklist.md` after each review; `iconix-metrics.md` extends per-review data to project-wide trend (added v0.9.7) |
| 5 | Follow up review with action points | ✅ | Reviewer produces BLOCK/CHANGES/APPROVE report with items; Git agent posts the report as a structured PR comment when `git.provider` is set (added v0.9.5) |
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
| Bug type classification (Type 1 vs Type 2) | ✅ | `iconix-reviewer.md` `# Bug triage`; `/iconix-bug <ref>` direct entry point (added v0.9.4) |
| Concurrent class touches across in-flight UCs (kit extension) | ✅ | `iconix-traceability.md` `# Concurrent touch detection`; `/iconix-concurrent` (added v0.9.6); `iconix-architect.md` `# Resolving concurrent touches` is the resolver. **Not in book Top 10s** — kit extension justified by Ch11 #1 (Model Update at every gate) extended to multi-dev contexts the canonical 2-author/whiteboard model doesn't address |
| Project-wide metrics + audit evidence (kit extension) | ✅ | `iconix-metrics.md` + `/iconix-metrics` (added v0.9.7) — produces `metrics/snapshot-<date>.{md,json}` and `metrics/trend-<date>.md`; JSON schema at `templates/metrics-schema.json`; definitions at `docs/iconix/metrics-glossary.md`. **Not prescribed by the book** — closest references are Ch11 #6 (per-review data gathering) and the Code-Inspection-vs-Code-Review sidebar acknowledging metrics in formal inspections. v0.9.7 extends these to project-wide aggregation. ISO-audit-relevant for SMEs in regulated environments. |

---

## Chapter 12 — Design-Driven Testing

### Top 10 Design-Driven Testing Guidelines

| # | Guideline | Status | Kit location |
|---|---|---|---|
| 10 | "Testing mind-set": every bug found is a victory | ❌ | Philosophy; not in agent |
| 9 | Understand different kinds of testing (V-model) | ✅ | `iconix-tester.md` `# Test types (V-model)` table |
| 8 | Create one or more TCs for each controller on each RB | ✅ | `iconix-tester.md` — one TC per controller |
| 7 | Don't leave testing until after the code has been written (test-first thinking) | ⚠️ | `iconix-tester.md` ICONIX rules — TCs exist before code skeletons; kit cannot enforce developer discipline but the rule is explicit |
| 6 | Requirement-level verification: each REQ is implemented | ✅ | Traceability validates REQ→UC→TC chain |
| 5 | Use a traceability matrix | ✅ | `iconix-traceability.md` + `test-matrix.md` |
| 4 | Scenario-level acceptance testing for each UC | ✅ | Tester produces TCs covering basic + alternate courses |
| 3 | Expand threads to cover complete path (basic + each alternate) | ✅ | Tester covers alternate courses |
| 2 | Use a testing framework (JUnit/xUnit) to store and organize tests | ✅ | `iconix.config.yaml` `test_framework` configures this |
| 1 | Keep unit tests fine-grained | ✅ | `iconix-tester.md` ICONIX rules — explicit fine-grained rule; one controller operation per unit TC |

**Unit test derivation from RB controllers:**

| Concept | Status | Kit location |
|---|---|---|
| One unit test class per controller (test case) | ✅ | `iconix-tester.md` |
| One test method per UC scenario (basic + alternate) | ✅ | Tester TC format: Steps mirror UC rows |
| Test named after UC scenario of origin | ✅ | TC naming convention |
| Tests written from point of view of object calling controller | ✅ | `iconix-tester.md` ICONIX rules — explicit caller-POV rule |

### V-Model: test types vs. ICONIX stages

| Test type | ICONIX stage | Status |
|---|---|---|
| Unit testing | After detailed design | ✅ | `iconix-tester.md` `# Test types` |
| Integration testing | After PDR | ✅ | `iconix-tester.md` `# Test types` |
| System testing | After CDR | ✅ | `iconix-tester.md` `# Test types` |
| Acceptance testing | After system testing | ✅ | `iconix-tester.md` `# Test types` |
| Regression testing | After each release | ✅ | `iconix-tester.md` `# Test types` + Reviewer regression check |

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
| 3 | Create estimates from UC scenarios, not functional requirements | 🚫 | Out-of-scope — UC-point estimation requires team calibration data; see README footnote |
| 2 | Don't be afraid of examples in functional requirements | ✅ | `templates/req-template.md` `## Examples` section — optional but encouraged; example + counter-example |
| 1 | Don't make requirements a technical fashion statement | ✅ | `iconix-product-owner.md` rule 8 — REQs naming frameworks/libraries rejected; rewritten as behaviour/constraint; technology in ADRs |

**Dysfunctional requirements detection:**

| Pattern | Status | Kit location |
|---|---|---|
| Passive voice "shall" statements in UC text | ✅ | `iconix-product-owner.md` rule 6 — detected and relocated to REQ file |
| Intermangled NFRs in UC text | ❌ | Not detected |
| Repeated requirements inline in multiple UCs | ❌ | Not detected |

---

## Summary Coverage Matrix

_Last reviewed: v0.9.20 (Round 7 — first **real M3 Tester** forcing-function run, producing fresh test plan + per-course TCs + per-controller unit TCs from the v0.9.13 Tester prompt; diffed against the example's 7 TCs + test plan + sampled BS-TC-001 (system/basic) and BS-TC-002 (unit/alt-D) for code-level structure. Ten issues only visible by producing artifacts. **Coverage strategy** (2): "one test per controller" rule reworded — every controller exercised by ≥1 TC (unit OR system-transitive); plural `Robustness controllers exercised:` field replaces singular. **Implementation surface** (4): TC template gains `## Implementation note (<stack> + <test framework>, per <ADR>)` section — the example's runnable code blocks finally have a home in the kit; test-plan template gains §6 "Test framework / dependencies" declaring mocking lib + integration infra + BDD framework + builders; new `templates/edge-case-report-template.md` (one row per family with covering TC OR documented waiver); new `templates/test-matrix-template.md` (REQ↔UC↔TC matrix + superseded-TC ledger + orphan/gap audit). **Convention / lifecycle** (4): per-TC BDD convention — new `acceptance-bdd` Type variant lets stakeholder-signed acceptance TCs use Gherkin even when project default is xUnit (matches example's BS-TC-101); acceptance-bdd uses Given/When/Then in Steps, Expected may be empty; superseded-TC lifecycle — new `## Status` field, old TC keeps file but Status flips to `superseded by <new TC>`, ledger entry in test-matrix; `## Edge case family` made conditional (omit for happy-path TCs). **No status shifts.** Cited rules: Ch12 Top 10 (test-design rules), Ch12 #7 (test-first thinking), Ch11 #6 (gather data; build boilerplate checklists — extended to test-matrix template). v0.9.19 entries unchanged._

Coverage formula: (✅ × 1 + ⚠️ × 0.5) ÷ (✅ + ⚠️ + ❌) — 🚫 (out-of-scope) excluded from denominator

| Chapter | Topic | ✅ | ⚠️ | ❌ | 🚫 | Coverage |
|---|---|---|---|---|---|---|
| 1 | ICONIX pipeline + milestones | 6 | 0 | 0 | 2 | **100%** |
| 2 | Domain modeling | 10 | 0 | 0 | 0 | **100%** |
| 3 | Use case modeling | 9 | 0 | 0 | 1 | **100%** |
| 4 | Requirements Review (M1) | 7 | 1 | 0 | 2 | **94%** |
| 5 | Robustness analysis (Top 10) | 10 | 0 | 0 | 0 | **100%** |
| 6 | PDR (M2) | 8 | 1 | 0 | 1 | **94%** |
| 7 | Technical architecture | 7 | 0 | 3 | 0 | **70%** |
| 8 | Sequence diagrams | 10 | 0 | 0 | 0 | **100%** |
| 9 | CDR (M3) | 8 | 0 | 1 | 1 | **89%** |
| 10 | Implementation | 9 | 0 | 1 | 0 | **90%** |
| 11 | Code review + model update | 8 | 1 | 1 | 0 | **85%** |
| 12 | Design-driven testing | 8 | 1 | 1 | 0 | **85%** |
| 13 | Requirements traceability | 9 | 0 | 0 | 1 | **100%** |

**Notes on count corrections (v0.9.3 audit):**
- Ch4: prior summary read `7|2|1` — actual is `7|1|2` (one ⚠️, two ❌). After 🚫 reclassification: `7|1|0|2` → 94%.
- Ch7: prior summary read `7|1|2` — actual is `7|0|3` (no ⚠️, three ❌). Coverage corrects from 75% to 70%; remaining ❌ items (#10 hardware cost, #9 legacy default, #6 unproven tech) are genuine gaps, not out-of-scope.

---

## Top Gap Areas (Prioritized)

### Closed in v0.9.0

- ~~UC packages with one diagram per package~~ (Ch3 #9, Ch4 #6) — `templates/use-case-diagram-template.puml` + `agents/iconix-product-owner.md` `# Use case packaging rules` + `agents/iconix-traceability.md` validation checks 10–13 (orphan / ghost / title-drift / dangling cross-package link)

### Closed in v0.6.0

- ~~Two-paragraph rule~~ (Ch3) — `iconix-product-owner.md` rule 3 + M1 checklist
- ~~Passive voice / "shall" guard~~ (Ch3/4/13) — `iconix-product-owner.md` rule 6 + M1 checklist
- ~~Boundary object per screen~~ (Ch5) — `iconix-analyst.md` `# Boundary object naming`
- ~~Domain model rules~~ (Ch2) — `iconix-analyst.md` `# Domain model rules`
- ~~Eight easy steps~~ (Ch4) — M1 checklist expanded and aligned

### Closed in v0.7.0

- ~~CDR test plan review~~ (Ch9 #1) — `iconix-tester.md` `# Pre-CDR test plan summary` + M3 gate check
- ~~NFR requirements in trace chain~~ (Ch9 #5) — `iconix-traceability.md` validation check #9 + chain diagram
- ~~Integration and acceptance test types~~ (Ch12 V-model) — `iconix-tester.md` `# Test types (V-model)` table

### Closed in v0.7.1

- ~~Invoked use cases on RB~~ (Ch5 #4) — `iconix-analyst.md` `# Invoked use cases on robustness diagrams`

### Closed in v0.8.6

- ~~Matrix inconsistency fixed~~ — Ch4 Eight-steps #8 "goal-oriented framing" corrected ⚠️→✅ (was already implemented in v0.6.0 M1 checklist)
- ~~Patterns/implementation constructs on SD~~ (Ch9 #6) — `iconix-developer.md` rule 8 — design patterns shown as SD lifelines
- ~~Attribute types in class model~~ (Ch9 #3) — `iconix-reviewer.md` check #2 — untyped attributes flagged
- ~~Don't defer testing until after code~~ (Ch12 #7) — `iconix-tester.md` ICONIX rules — TCs exist before code skeletons (❌→⚠️; cannot enforce developer discipline beyond stating the rule)

### Closed in v0.8.5

- ~~Domain model abstraction coverage~~ (Ch4 #10) — `iconix-product-owner.md` M1 checklist — UC nouns with no domain model counterpart flagged
- ~~Domain model shows is-a/has-a relationships~~ (Ch4 #9) — `iconix-product-owner.md` M1 checklist — isolated entities with real-world relationships flagged
- ~~Always question framework design choices~~ (Ch10 #7) — `iconix-reviewer.md` check #6
- ~~Don't let framework issues dominate business issues~~ (Ch10 #6) — `iconix-reviewer.md` check #6
- ~~Gather data; build boilerplate checklists~~ (Ch11 #6) — `iconix-reviewer.md` Rules — findings accumulated in `reviews/review-checklist.md`
- ~~Requirements not a technical fashion statement~~ (Ch13 #1) — `iconix-product-owner.md` rule 8

### Closed in v0.8.4

- ~~Trace data flow between entity classes and screens~~ (Ch6 #8) — `iconix-analyst.md` PDR readiness check — unnamed Boundary↔Entity data flows flagged
- ~~Don't drift into detailed design on RBs~~ (Ch6 #2) — `iconix-analyst.md` PDR readiness check — method signatures/types on RB are a pre-handoff blocker
- ~~All classes have appropriate attributes and operations~~ (Ch9 #7) — `iconix-reviewer.md` check #2 — attribute-sparse entity classes flagged

### Closed in v0.8.3

- ~~Prefactor design on SD before coding~~ (Ch8 #2) — `iconix-developer.md` rule 6
- ~~Don't worry about focus of control~~ (Ch8 #5) — `iconix-developer.md` rule 7
- ~~Keep unit tests fine-grained~~ (Ch12 #1) — `iconix-tester.md` ICONIX rules
- ~~Tests from point of view of calling controller~~ (Ch12 unit test sub-table) — `iconix-tester.md` ICONIX rules
- ~~Examples in functional requirements~~ (Ch13 #2) — `templates/req-template.md` `## Examples` section

### Closed in v0.8.1

- ~~Noun-verb-noun sentence structure~~ (Ch3 #3) — `iconix-product-owner.md` rule 7
- ~~RB = conceptual design, not detailed design~~ (Ch5 #3) — `iconix-analyst.md` `# Robustness diagram principles`
- ~~Arrow direction is irrelevant~~ (Ch5 #5) — `iconix-analyst.md` `# Robustness diagram principles`
- ~~Controllers = logical functions, not control classes~~ (Ch5 #6) — `iconix-analyst.md` `# Robustness diagram principles`

### Closed in v0.8.0

- ~~Architectural paralysis guard~~ (Ch7 #4) — `iconix-architect.md` rule 5 — time-box rule; unresolved decisions become `Proposed` ADRs
- ~~Requirement-driven TA validation~~ (Ch7 #5) — `iconix-architect.md` rule 6 — every ADR must cite ≥1 REQ/NFR/UC
- ~~Testability integration with Architect~~ (Ch7 #3) — `iconix-architect.md` `# Testability annotations` — container test seams required; no-seam flagged at M2

### Documented as intentionally out-of-scope in v0.7.2

`README.md` `## What the kit intentionally does not cover` explicitly acknowledges these items. They remain ❌ in the coverage tables above — the kit does not implement them — but they are not omissions; they are deliberate boundaries.

| Item | Chapter(s) | Rationale |
|---|---|---|
| UI storyboards | Ch3 #6, Ch4 #3 | Requires a human designer; not an AI-agent deliverable |
| Stakeholder review meetings | Ch4 #2, Ch6 #4 | Human governance step; kit routes work but cannot convene people |
| Persona analysis | Ch1 | Pre-project marketing work; out of kit scope |
| Effort estimation | Ch13 #3 | UC-point estimation requires team calibration data |
| Code header generation | Ch9 #2 | IDE/toolchain concern; not an ICONIX artifact |
| TDD red-green cycle | Ch1 | Kit derives TCs from RBs (design-first); TDD is a separate practice |

### Added in v0.7.3

- `templates/test-plan-template.md` — pre-CDR test plan template; `iconix-tester.md` and `iconix-traceability.md` now reference it at the M3 gate (supports Ch9 #1 ✅ and Ch12 V-model ✅)

### Added in v0.7.4

- `templates/test-case-template.md` `## Type` field — V-model classification (unit / integration / system / acceptance / regression) on every TC; aligns Ch12 #9 ✅

### Added in v0.7.5

- `iconix-state-machine.puml` — visual reference diagram of the full kit workflow; documentation only, no coverage impact
