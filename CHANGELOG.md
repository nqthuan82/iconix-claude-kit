# Changelog

All notable changes to the ICONIX Claude Kit.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.9.18] — 2026-05-10

Round 5 — first **real M2 Architect** forcing-function run.
Followed the v0.9.14 Architect prompt to actually produce all 5
Architect artifact categories for BS-UC-001 (container-mapping,
nfr-annotations, NFR catalog, package-map, integration-surface),
then diffed against the example's BS-ADR-001 (the only Architect
artifact the example ships) plus the stack info in
`iconix.config.example.yaml`.

**Ten issues** only visible by producing artifacts — the largest
real-run finding count yet, matching v0.9.14's prompt-review count.
Architect templates were brand-new in v0.9.14 and untested under
real input; this run exercises all 5 of them at once.

Pattern continues:
  - M1 PO: prompt review 13 + real run 7 (v0.9.10/11 + v0.9.15)
  - M2 Analyst: prompt review 8 + real run 6 (v0.9.13 + v0.9.17)
  - M2 Architect: prompt review 10 + real run 10 (v0.9.14 + v0.9.18)

Ten fixes:

  M2A-R-#1 Example pre-dates v0.9.14 catalog template (NFRs are in
        config comments instead of `docs/nfr-catalog.md`). Known
        retrofit gap; deferred to example refresh.

  M2A-R-#2 Container-mapping testability column doesn't model
        "indirect seam via upstream container" (e.g., Database
        tested through Infrastructure adapter). Fix: explicit
        `(out of scope — covered via <upstream-container>'s seam)`
        convention added to template's testability values list.

  M2A-R-#3 NFR applicability duplicated across catalog ↔
        container-mapping ↔ nfr-annotations with no consistency
        check. Fix: new Traceability check #15 — per-UC NFR-list
        match between container-mapping and nfr-annotations is an
        M2 blocker. Closes the duplication trap.

  M2A-R-#4 nfr-annotations "Out-of-scope NFRs" framing biased
        toward expecting exclusions. For small catalogs, all NFRs
        usually apply; for large regulatory/security suites,
        explicit out-of-scope is the common case. Reworded to be
        size-aware.

  M2A-R-#5 package-map template has no convention for cross-team /
        infra-owned containers (e.g., PendingReviewsQueue owned by
        INFRA-88). Fix: new `Infrastructure (external)` layer
        marker; external packages exempt from cross-package /
        architecture-test rules.

  M2A-R-#6 integration-surface "Bidirectional integrations"
        section almost always empty for typical UCs. Fix: moved to
        commented-out optional block; uncomment-and-fill only if
        actually needed. Same pattern as v0.9.13's Alternate Course
        handling.

  M2A-R-#7 container-mapping "Open architectural questions"
        section had unclear format. Fix: standardized to
        `<question>. [Proposed ADR-XXX]` so future Traceability
        checks can mechanically validate the link.

  M2A-R-#8 nfr-catalog `Owner:` field couldn't model split
        ownership (PO defines target, Architect enforces). Common
        in regulated environments. Fix: split into `Defined by:`
        and `Enforced by:` fields.

  M2A-R-#9 integration-surface had a redundant `Failure handling`
        column AND a per-touchpoint failure-modes sub-section.
        Fix: dropped the column; kept the prose-friendly
        sub-sections. Failure handling needs prose, not keywords.

  M2A-R-#10 No template for the M2 milestone report (Traceability
        produces these but format was inline-prompt-only — same
        gap Architect had pre-v0.9.14). Fix: new
        `templates/milestone-report-template.md` formalizing
        gate-specific checks (M1/M2/M3 sub-sections), the
        machine-readable `Recommendation` token (`READY` /
        `NOT READY` — parsed by `iconix-metrics` for
        `gate_failure_rate`), and concurrent-touch summary
        section. Traceability agent's inline format pointer now
        delegates to this template.

Methodology audit per CLAUDE.md: methodology-surface change
(template + Traceability validation rule additions). All cited
rules already approved; v0.9.18 enriches kit-location citations
and closes the per-UC NFR-consistency gap. No status shifts.
Cited Ch7 Top 10 (architecture decisions, cross-cutting concerns,
testability seams), Ch6 PDR, Ch4 #5 (REQ traceability — extended
via NFR-list check #15).

Cumulative: 8 forcing-function rounds, 60 issues fixed
(13+8+10+5+7+6+1[v0.9.16]+10). Real-run methodology continues to
match or exceed prompt-review counts.

### Added
- `templates/milestone-report-template.md` — M1/M2/M3 readiness
  format. Machine-readable Recommendation token; gate-specific
  check sub-sections; M2 concurrent-touch summary. Subsumes the
  inline format previously in `iconix-traceability.md`.

### Changed
- `templates/container-mapping-template.md`:
  - Testability seam values list adds `(out of scope — covered
    via <upstream-container>'s seam)` for indirect seams (M2A-R-#2)
  - Open architectural questions section formalized to
    `<question>. [Proposed ADR-XXX]` format with usage example
    (M2A-R-#7)
- `templates/nfr-annotations-template.md` — Out-of-scope NFRs
  section reworded to be size-aware (M2A-R-#4)
- `templates/nfr-catalog-template.md` — `Owner:` field split into
  `Defined by:` + `Enforced by:` for split-ownership NFRs
  (M2A-R-#8)
- `templates/architecture-package-map-template.md`:
  - Package list table gains `Infrastructure (external)` example
    row + Layer-column note explaining the convention (M2A-R-#5)
  - Quality checks add the external-package coverage check and
    the architecture-test exclusion check
- `templates/integration-surface-template.md`:
  - Outbound integrations table drops the `Failure handling`
    column (M2A-R-#9)
  - Bidirectional integrations section moved to a commented
    optional block (M2A-R-#6)
- `agents/iconix-traceability.md`:
  - New validation check #15 — per-UC NFR-list consistency
    between container-mapping and nfr-annotations is an M2 blocker
    (M2A-R-#3)
  - `# Milestone gate report format` section now delegates to
    `templates/milestone-report-template.md` instead of carrying
    the inline format (M2A-R-#10)
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers copy `milestone-report-template.md` to
  `docs/iconix/templates/`.
- `.github/workflows/validate.yml` — smoke test asserts the new
  template is installed.
- `README.md` — `milestone-report-template.md` added to the
  templates listing.
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.18 with the Round-5-real audit summary.

## [0.9.17] — 2026-05-10

Round 4 — first **real M2 Analyst** forcing-function run. Followed
the v0.9.13 Analyst prompt to actually produce a fresh BS-RB-001
robustness diagram from BS-UC-001 + the PO-only initial domain
model, then diffed against the example's RB-001. **Six issues**
only visible by producing the diagram — net-new findings prompt
review couldn't catch.

The pattern from v0.9.15 holds: prompt-review of M2 Analyst
(v0.9.13) found 8 issues; real run added 6 more. Real production
keeps surfacing things prompt review missed.

Six fixes:

  R4-#1 Example RB violates v0.9.13's verb-led controller rule —
        uses question-form names like `Is user logged in?`, `Is
        Book Review length OK?`. Methodologically wrong (the
        v0.9.13 rule says controllers are *actions*, not
        *predicates*). Known limitation: example refresh deferred;
        v0.9.17 keeps the rule and notes the example needs retrofit.

  R4-#2 Analyst rules silent on rendering v0.9.15's `UI
        dependencies (page/component reuse)` sub-field. Both my
        run and the example drew reused pages identically to
        UC-owned pages — visually indistinguishable. Fix: new
        Analyst section `# Rendering UI dependencies and
        downstream consumers on the RB` — UI-reused boundaries get
        a `<<from PREFIX-UC-XXX Title>>` stereotype.

  R4-#3 Same gap for v0.9.15's `Downstream consumers` sub-field.
        Same fix: dashed arrow (`..>`) from produced entity to
        consumer actor distinguishes async handoff from
        synchronous flow.

  R4-#4 Analyst lacked a controller-granularity rule equivalent
        to PO rule 13. New section `# Controller granularity` —
        consolidate similar error paths producing the same
        response (alt B "too short" + alt C "too long" → one
        controller); split paths producing different responses.
        Default to consolidation; don't pre-fragment for testability.

  R4-#5 Workflow step 6 was unconditionally imperative ("Rewrite
        UC text"). Reworded to "Verify mapping; rewrite ONLY if
        mismatches surface." On real runs UC text often already
        maps cleanly — the prior wording read as "always rewrite."

  R4-#6 Analyst rules didn't say what to do with PO's `' VERIFY:`
        notes (v0.9.15 R3-#3 introduced them on the PO side
        without specifying Analyst-side processing). Asymmetric:
        PO wrote, Analyst silently improvised. Fix: Domain model
        rule 5 now mandates `' RESOLVED at M2:` reword OR class
        removal; unresolved VERIFY notes are an M2 PDR blocker.

Methodology audit per CLAUDE.md: methodology-surface change. All
cited rules already approved; v0.9.17 enriches kit-location
citations and resolves the PO↔Analyst handoff asymmetry from v0.9.15.
No status shifts. Cited Ch5 Top 10 #5 (RB syntax), Ch5
controller-as-action principle, Ch6 PDR.

Cumulative: 7 forcing-function rounds, 50 issues fixed
(7+6+5+8+10+7+6+1[v0.9.16]). Real-run methodology continues to
outpace prompt review by ~3-7 net-new findings per agent. M2
Architect (real run), M3, Phase 9 still ahead.

### Changed
- `agents/iconix-analyst.md`:
  - Workflow step 6 reworded from imperative-rewrite to verify-
    then-rewrite-only-if (R4-#5)
  - Workflow step 7 now references "Resolve every PO `' VERIFY:`
    note" (R4-#6)
  - New section `# Controller granularity (when to consolidate
    vs split)` — mirrors PO rule 13 at the controller level
    (R4-#4)
  - New section `# Rendering UI dependencies and downstream
    consumers on the RB` — formalizes the rendering rules for
    v0.9.15's three Invokes sub-categories (R4-#2, R4-#3)
  - Domain model rule 5 gains explicit `' VERIFY:` → `' RESOLVED at
    M2:` resolution procedure (R4-#6)
  - PDR readiness checklist gains four mirror checks: Invokes /
    UI dependencies / Downstream consumers / VERIFY-resolved
    (R4-#2, R4-#3, R4-#6)
- `templates/robustness-template.puml`:
  - Adds commented examples for UI-dependency boundary syntax
    (`<<from ...>>` stereotype) (R4-#2)
  - Adds commented examples for downstream-consumer dashed-arrow
    syntax (R4-#3)
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.17 with the Round-4-real audit summary

## [0.9.16] — 2026-05-10

PlantUML validation in CI. The forcing-function-within-forcing-
function pattern hit twice — v0.9.13 caught a robustness-template
bug at preview time (bare `<...>` in arrow labels), and v0.9.15
caught a domain-model-template bug (every line commented out;
PlantUML rendered nothing). Both were invisible to prompt review;
both got past every CI check we had until a human opened the file
in a previewer. v0.9.16 adds the missing CI step.

The new `validate-plantuml` job runs on every push and PR. It:

  1. Installs PlantUML on the runner (`apt-get install plantuml`).
  2. For every `.puml` file in the repo (templates/, examples/,
     root): runs `plantuml -checkonly` for syntax, AND counts
     diagram declarations + arrows for content.
  3. Fails the build with file-pinned errors if either check fails.

The content check specifically catches the v0.9.15 class of bug
(empty-but-syntactically-valid diagrams). Some PlantUML versions
return exit 0 even on parse warnings, so the syntax check also
greps output for known error markers as a safety net.

This is a tooling-only commit. No methodology changes, no
template additions, no new agents. Theory audit consciously
skipped per CLAUDE.md (same convention as v0.9.9 and v0.9.12).

### Added
- `.github/workflows/validate.yml` — new `validate-plantuml` job
  parallel to `validate-agents` and `smoke-test-installer`.
  Catches the two classes of rendering bug we hit in v0.9.13
  and v0.9.15.

### Carry-forward note
This was carried over as a robustness item across multiple
recent commits (v0.9.13, v0.9.15). Closing it now means future
PlantUML template work doesn't need preview-by-human as the
last line of defense.

## [0.9.15] — 2026-05-10

Round 3 — the **first real forcing-function run**. v0.9.10–v0.9.14
called themselves "forcing-function rounds" but were actually prompt
review: read the agent prompt, read the example, find gaps, fix.
v0.9.15 went further — produced fresh REQ + initial domain model +
UC by following the v0.9.14 PO prompt as if running it for the first
time, then diffed the fresh artifacts against the example's. Seven
issues that prompt review couldn't have caught surfaced — they only
became visible when actually producing artifacts and comparing.

The methodology shift matters: prompt review catches *prompt clarity*
problems; only artifact production catches *agent-execution* problems
(places where the prompt is clear but executing it on real input
reveals format gaps, missing fields, or arbitrary-judgment
requirements). v0.9.15 closes seven such gaps.

Seven fixes:

  R3-#1 REQ template gains `Related NFRs:` and `Related BRs:`
        fields. The example uses both; the kit had never
        standardized them. NFR linkage at REQ time means the
        Architect doesn't have to re-derive applicable NFRs at M2.
        BR linkage anticipates the deferred BR-NNN feature with
        a clean migration path ("(none — Business Rules not yet
        adopted)" until BR-NNN ships).

  R3-#2 Domain model template gains an "ownership over time"
        header (PO drafts initial at M1; Analyst refines at M2;
        both gates re-validate). The example's domain-model.example.puml
        has a similar header but with stale (pre-v0.9.3) "PO +
        Analyst joint initial pass" wording. The kit's template now
        ships the correct version.

  R3-#3 PO rule 9 + domain model template now formalize a
        `' VERIFY:` convention for PO-introduced ambiguities.
        When the PO is unsure whether a noun is a real entity or
        a state/value (e.g., "PendingQueue" in the WCR example),
        the PO marks the class with a `' VERIFY:` comment block
        for the Analyst to resolve at M2. Mirrors intake `[VERIFY]`.

  R3-#4 UC template's `Invokes:` field SPLIT into three sub-fields
        (`Invokes (UC calls)`, `UI dependencies (page/component
        reuse)`, `Downstream consumers`). The fresh-run UC for
        WCR exposed three meaningfully different cross-UC
        dependencies that v0.9.11's single `Invokes:` field
        conflated: alt A invokes Login (true call); alt E reuses
        the Book Not Found page (UI reuse, no flow invocation);
        Moderate Customer Reviews consumes the queue this UC
        writes to (downstream handoff, not invocation). PO rule 12
        rewritten with the three categories and the mirror rule
        per sub-field.

  R3-#5 PO rule 13 added: row granularity for the Basic Course
        table. One row per (a) user action + immediate system
        response, OR (b) system-only step that the Analyst would
        model as a separate controller at M2. Multiple system
        steps mapping to ONE controller collapse; multiple
        steps mapping to DIFFERENT controllers stay separate.
        "When in doubt, expand" — the Analyst can collapse but
        splitting later is harder.

  R3-#6 UC template's `Domain entities introduced or used:` field
        SPLIT into `introduced` (net-new on the domain model) and
        `used` (already on the model). The Analyst at M2 needs to
        know which entities are new vs reused; the prior single
        list didn't say.

  R3-#7 REQ acceptance criteria checkbox lifecycle documented
        (deferred from v0.9.11 / R2-#7). Tester ticks per TC pass
        (M3 / Phase 9); PO confirms at M3→Implementation merge
        during PR review; an unticked criterion at merge time is a
        Reviewer finding / blocker on the Implementation PR.

Methodology audit per CLAUDE.md: methodology-surface change. All
cited rules already approved; v0.9.15 enriches kit-location
citations. No status shifts. Cited rules: Ch3 #4 (UC in context
of object model), Ch3 #7 (event/response flow), Ch4 #5 (REQ
traced to UCs), Ch5 #1 (no GUI on domain model).

Cumulative: forcing-function arc has now produced 6 rounds
(prompt review v0.9.10/0.9.11/0.9.13/0.9.14, dogfood v0.9.12, real
run v0.9.15) and 43 issues fixed (7+6+5+8+10+7). v0.9.15 marks the
methodology shift to actual artifact production going forward.

### Changed
- `templates/req-template.md`:
  - `## Acceptance criteria` gets a checkbox-lifecycle note (R3-#7)
  - `## Traceability` gains `Related NFRs:` and `Related BRs:`
    fields (R3-#1)
- `templates/domain-model-initial-template.puml`:
  - New "Ownership over time" header explaining the v0.9.3+
    PO/Analyst split (R3-#2)
  - New rule 8 in the rules block: `' VERIFY:` convention for
    PO-introduced ambiguities (R3-#3); the rule places VERIFY
    comments IMMEDIATELY ABOVE the ambiguous class declaration
    (PlantUML treats `'` lines mid-class-block inconsistently)
  - **PlantUML rendering hardening** (caught at preview time —
    same forcing-function-within-forcing-function as v0.9.13's
    robustness template): the v0.9.10 file shipped with
    everything between `@startuml` and `@enduml` commented out,
    so PlantUML had no diagram content to render. v0.9.15 ships
    a worked example (Customer / Book / CustomerReview / status
    enum + PendingReviewsQueue with VERIFY example) that
    actually renders, with a loud "DELETE AND REPLACE" header
    instructing users to substitute their own domain entities.
    Lesson: kit-shipped PlantUML files must *render* on first
    open — empty-but-syntactically-valid `@startuml/@enduml`
    blocks aren't actually valid for users.
- `templates/use-case-template.md`:
  - `Invokes:` field replaced by three sub-fields:
    `Invokes (UC calls):`, `UI dependencies (page/component reuse):`,
    `Downstream consumers:` (R3-#4)
  - `Domain entities introduced or used:` split into
    `Domain entities introduced (new on domain model):` and
    `Domain entities used (already on domain model):` (R3-#6)
- `agents/iconix-product-owner.md`:
  - Rule 9 gains "Mark your ambiguities for the Analyst" sub-section
    on the `' VERIFY:` convention (R3-#3)
  - Rule 12 rewritten — now distinguishes three sub-categories
    of cross-UC dependency (Invokes/UI dependencies/Downstream
    consumers) with mirror rule per sub-field (R3-#4)
  - New rule 13: "Basic course row granularity" (R3-#5)
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.15 with the Round-3-real audit summary

### Note on the WCR example
The fresh-run M1 artifacts produced during this round were used as
diff input only; they were not committed. The example's existing
artifacts remain in their pre-v0.9.10 state and will surface as
Layer-D findings when `/iconix-upgrade` is run on the example.
Example refresh remains a deferred task.

## [0.9.14] — 2026-05-10

Round 2 forcing-function fixes (M2 Architect phase). We continued
the WCR run from v0.9.13 into M2 Architect. **Ten issues** found —
the largest single-agent finding count of any forcing-function
round. Why so many? The Architect was the most under-templated
agent in the kit: it produces 5 artifact categories but only ADRs
had a template, and the worked example only demonstrates 1 of the
5. Fresh users had no format guidance for 4 of the 5 outputs.

This commit ships 5 new templates and a substantial overhaul of
the Architect agent prompt to close the gap.

Ten fixes:

  M2A-#1 4 of 5 Architect artifacts had no template. Added
         container-mapping, nfr-annotations, nfr-catalog,
         architecture-package-map, integration-surface templates.
  M2A-#2 WCR example only demonstrates ADR. (Example expansion
         deferred to a future refresh; v0.9.14 ships the templates
         so future projects have format guidance.)
  M2A-#3 Folder mismatch — installer didn't create `packages/`
         or `integration-points/`. Resolved by relocating these
         project-wide artifacts to `docs/architecture/` (already
         created by installer).
  M2A-#4 "package-map" was semantically ambiguous (UC packages vs
         code packages). Renamed agent's output to
         `docs/architecture/package-map.md` and clarified in the
         prompt + template that this is CODE/deployment-level
         packaging, distinct from PO-owned `use-case-packages/`.
  M2A-#5 No template for `nfr-catalog.md`. Added.
  M2A-#6 Architect's input list named `nfr-catalog.md` (bare); the
         actual configured path is `docs/nfr-catalog.md`. Updated
         the agent prompt to read from the configured path.
  M2A-#7 Container-mapping format unspecified. Template added
         (containers + role + testability seam + NFR refs +
         cross-cutting concerns + open architectural questions).
  M2A-#8 NFR-annotations format unspecified. Template added
         (NFR ID + target + where enforced + Reviewer-checkable
         signal + test-design hints for Tester).
  M2A-#9 PDR readiness checklist had no item for "open
         architectural questions" per Decision rule 5. Added: "No
         blocking architectural questions remain open without a
         Proposed ADR."
  M2A-#10 Concurrent-touch resolver scope vs "never rewrite UCs"
         was ambiguous. Clarified routing: UC splits, entity-name
         changes in UC text, and RB updates are dispatched via
         /iconix-next to PO/Analyst respectively; the Architect
         never edits those files even when its decision drove the
         change.

Methodology audit per CLAUDE.md: methodology-surface change. All
cited rules already approved; v0.9.14 enriches kit-location
citations and closes a major template-coverage gap. No status
shifts. Cited Ch7 Top 10 (architecture decisions documented;
testability seams; cross-cutting concerns) and Ch6 PDR.

### Added
- `templates/container-mapping-template.md` — per-UC container
  mapping with role, testability seams, NFR refs, cross-cutting
  concerns, open architectural questions, traceability footer.
- `templates/nfr-annotations-template.md` — per-UC NFR
  enforcement detail with target, where-enforced, Reviewer-
  checkable signal, test-design hints for the Tester.
- `templates/nfr-catalog-template.md` — project-wide NFR catalog
  with stable IDs, categories, measurable targets, ownership,
  UC-applicability, covering-ADR references.
- `templates/architecture-package-map-template.md` — code /
  deployment package decomposition with allowed-dependencies
  matrix, UC→package allocation, architecture-test enforcement
  guidance.
- `templates/integration-surface-template.md` — inbound /
  outbound / bidirectional integration touchpoints with auth,
  rate limits, failure modes, ADR refs.

### Changed
- `agents/iconix-architect.md`:
  - `# Inputs you rely on` — NFR catalog path now references
    `iconix.config.yaml` `nfr_catalog` configuration; mentions
    template for first-time setup (M2A-#5, M2A-#6)
  - `# Artifacts you produce` — restructured into per-UC,
    project-wide, and ADR groups; each artifact references its
    template; project-wide artifacts relocated to
    `docs/architecture/` (M2A-#1, M2A-#2, M2A-#3, M2A-#4,
    M2A-#7, M2A-#8)
  - `# Resolving concurrent touches` — added explicit routing for
    UC splits, entity-name changes, RB updates (M2A-#10)
  - `# PDR readiness check` — expanded to enforce all 5 Architect
    artifacts; new "no blocking architectural questions without a
    Proposed ADR" item (M2A-#9)
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers copy the 5 new templates to `docs/iconix/templates/`.
- `.github/workflows/validate.yml` — smoke test asserts all 5 new
  templates are installed.
- `README.md` — 5 new templates added to the directory listing.
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.14 with the M2-Architect audit summary.

## [0.9.13] — 2026-05-10

Round 2 forcing-function fixes (M2 Analyst phase). We continued
the WCR run from v0.9.10/v0.9.11 into M2, walking the Analyst
agent prompt mentally against the example RB-001. Eight gaps
surfaced, all in the Analyst's prompt and the robustness template.

Eight fixes:

  M2-#1 UI sub-elements (buttons, fields, dropdowns) are NOT
        boundaries. The agent's `# Boundary object naming` rule now
        says so explicitly. Naive runs would have produced
        `boundary "Send button"` for every UI control mentioned.

  M2-#2 `Display X page` and `Load X entity` are SEPARATE
        controllers. The prior `# Display controllers` section
        conflated them. Renamed to `# Display vs data-fetch
        controllers` with explicit guidance: when the UC has "load
        then display", produce two controllers, connected.

  M2-#3 Robustness template's comment-block format mismatched the
        canonical example. Template had `User: <action>` /
        `System: <response>` literal labels; example uses concrete
        actor names. Aligned template to the example pattern.

  M2-#4 Robustness template shipped with `actor User as U`
        (generic). The kit's PO rule explicitly forbids generic
        actor names. Replaced with `actor "<Actor name from UC>"
        as Actor` placeholder.

  M2-#5 Robustness template used !define BOUNDARY()/ENTITY()/
        CONTROLLER() macros; example uses native PlantUML keywords
        (`boundary`, `entity`, `control`). Templates and examples
        now match — both use native keywords. Cleaner, more
        idiomatic, easier to read raw.

  M2-#6 Agent prompt and example disagreed on invoked-UC
        representation. Prompt: "use a usecase node, not a
        controller." Example: `control "Invoke Login"`. **Example
        violates the rule.** v0.9.13 keeps the rule (methodology-
        correct: use cases at this level are the thing being
        invoked, not implementation controllers) and adds rationale
        + a concrete PlantUML snippet. The example will surface as
        a Layer-D finding when /iconix-upgrade is run on it; an
        example refresh is deferred.

  M2-#7 Analyst's domain-model rule 5 said "Time-box the INITIAL
        domain model to ~2 hours." But since v0.9.3, the PO owns
        the initial draft. The Analyst REFINES. Reworded to
        "refinement at M2" with explicit reference to PO rule 9.

  M2-#8 Analyst's PDR readiness checklist had no item to validate
        v0.9.11's PO rule 12 mirror (Invokes: Traceability field
        ↔ usecase nodes on the RB). Added the mirror check; cited
        Traceability check #14 as the gate enforcer.

Methodology audit per CLAUDE.md: methodology-surface change
(Analyst rules + RB template). All cited rules already ✅;
v0.9.13 enriches kit-location citations. No status shifts.
Cited Ch5 #5 (RB syntax), Ch5 #1 (no GUI on domain model),
Ch6 #2 (no detailed design on RB).

### Changed
- `agents/iconix-analyst.md`:
  - `# Boundary object naming` adds the UI-sub-element exclusion
    rule (M2-#1)
  - `# Display controllers` renamed to `# Display vs data-fetch
    controllers` with the separate-controllers rule (M2-#2)
  - `# Invoked use cases on robustness diagrams` rewritten with
    a "why not a controller" rationale + native PlantUML example
    snippet (M2-#6)
  - `# Domain model rules` rule 5 reworded — "initial" → "refinement
    at M2"; references PO rule 9 explicitly (M2-#7)
  - `# PDR readiness check` gains three items: UI-sub-element
    check (M2-#1), human-verification note on the every-sentence-
    maps-to-element check, and Invokes-mirror check (M2-#8)
- `templates/robustness-template.puml` — full rewrite:
  - Comment block format aligned to example (no User:/System:
    label prefix; concrete actor names) (M2-#3)
  - `actor User as U` replaced by `<Actor name from UC>` placeholder
    (M2-#4)
  - !define macros removed; native `boundary`, `entity`, `control`,
    `usecase` keywords used throughout (M2-#5)
  - Header comment block adds notes referencing the agent's three
    new rules (UI sub-elements, invoked-UC representation, Display
    vs Load)
  - Example wiring shows the `usecase` node pattern for invoked UCs
    (M2-#6)
  - Layout defaults (`left to right direction`, `skinparam
    shadowing false`, `skinparam ArrowColor`) added — match the
    example's defaults
  - **PlantUML rendering hardening** (caught at preview time):
    arrow labels use `[bracket]` placeholders instead of
    `<angle-bracket>` (PlantUML interprets unquoted `<...>` in
    arrow labels as HTML/creole markup, which broke preview);
    `note bottom` block uses literal `PREFIX-UC-XXX` instead of
    `<PREFIX>-UC-XXX` (notes accept HTML markup, so unclosed
    `<PREFIX>` tags broke rendering); inline `' comment` after
    `as ALIAS` declarations moved to separate lines (mid-line
    comments were unreliable). Template header now documents the
    placeholder conventions explicitly so future template
    additions don't repeat the mistake.
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.13 with the M2-Analyst audit summary

## [0.9.12] — 2026-05-10

The v0.9.9 dogfood test we owed. We pointed `/iconix-upgrade
--dry-run` at the Write Customer Review example to exercise the
upgrade agent for the first time on a real-world target. The
forcing function found bugs in `/iconix-upgrade` itself — the
upgrade was designed for "freshly iconix-init'd standard project"
and didn't account for either tutorial structures (the example) or
projects with custom layouts (renamed config, custom doc paths,
flat directories). v0.9.12 closes all five issues found.

Issues #U-#1 through #U-#5:

  U-#1 Agent assumed config file is `iconix.config.yaml`. Wouldn't
       find `iconix.config.example.yaml` (the example) or any
       project-specific variant. Fix: explicit Step 1a config
       resolution with refusal messages — refuses on example-only
       configs ("this looks like a kit demo, not an installed
       project"); refuses on no-config-at-all; asks for choice on
       multiple variants.

  U-#2 Heuristic detection was path-exact, brittle to renames.
       The example has `domain-model.example.puml` (equivalent to
       v0.9.x's `domain-model/domain-model.puml`); heuristic only
       saw the latter and detected v0.3.0 even though the example
       was authored in v0.9.1+. Fix: two-pass detection — Pass 1
       canonical paths (existing), Pass 2 content-based search
       (UCs by `## Basic Course` content; REQs by `## Statement`
       content; source by `Traceability:` comment). When Pass 2
       finds higher version evidence, it's used AND recorded as a
       layout discrepancy in the report.

  U-#3 Layer C (template refresh) didn't handle missing parent
       directory. If `docs/iconix/templates/` doesn't exist, the
       agent's prompt was silent on what to do. Fix: explicit
       create-the-directory rule (it's harmless reference docs);
       opt-out via `--layers` for projects deliberately not using
       the docs/ pattern. Hand-edited templates now preserved with
       `.backup` suffix instead of overwritten.

  U-#4 Layer D (artifact detection) scanned canonical paths only.
       A project with flat or renamed structure returned "0
       artifacts found" even when artifacts clearly existed. Fix:
       same two-pass approach as U-#2 — Pass 1 canonical paths,
       Pass 2 content-based fallback. Layer D additionally now
       checks for v0.9.10+ and v0.9.11+ field gaps (Intakes, Invokes,
       Domain entities, Postconditions multi-state, alt-course
       preamble) which were missing from the agent's check list
       even though Layer-D's purpose was exactly this.

  U-#5 No per-layer opt-in. The upgrade was "all layers or
       dry-run" — no way to run "just the detection report." Fix:
       new `--layers <A,B,C,D,E>` flag (any subset). Combinable
       with `--dry-run`. Layers run is now surfaced in the
       report's Summary so reviewers know the scope.

Methodology audit: tooling-only change per CLAUDE.md (same as
v0.9.9). `/iconix-upgrade` is kit-version maintenance, not
methodology. Theory audit consciously skipped.

### Changed
- `agents/iconix-upgrade.md`:
  - Step 1 split into Step 1a (config-file resolution with refusal
    rules) and Step 1b (two-pass version detection) (U-#1, U-#2)
  - New Step 1.5 — `--layers <list>` filter handling (U-#5)
  - Layer C now handles missing `docs/iconix/templates/` parent;
    .backup suffix policy for hand-edited templates (U-#3)
  - Layer D now has Pass 1 canonical + Pass 2 content-based
    detection; expanded check list to include v0.9.10+ and v0.9.11+
    field gaps (Intakes, Invokes, Domain entities, multi-state
    Postconditions, alt-course preamble) (U-#4)
- `commands/iconix-upgrade.md`:
  - `argument-hint` advertises `--layers <A,B,C,D,E>` flag
  - Body explains useful `--dry-run --layers D` and similar combos
  - Explicit refusal-on-missing-config rule referenced (U-#1)
- `templates/upgrade-report-template.md` — Summary section
  expanded to surface: detection method (Pass 1 / Pass 2 / override),
  layers run, config-file used, layout (canonical / non-canonical).

### Note on the WCR example test run
This commit also serves as a record that `/iconix-upgrade --dry-run`
was first exercised on `examples/write-customer-review/` and that
the example deliberately remains a tutorial layout (flat numbered
files; `iconix.config.example.yaml` not `iconix.config.yaml`). With
v0.9.12 fixes, future upgrade attempts on similar non-canonical
projects will refuse cleanly (example case) or fall back to content-
based detection (real projects with custom layouts).

## [0.9.11] — 2026-05-10

Round 2 forcing-function fixes. We continued the real-world test
run from v0.9.10 (Write Customer Review example, M1 gate review).
Six more issues surfaced — gaps in template fields, the cross-UC
invocation citation rule, and the Traceability gate's coverage of
in-text UC references. v0.9.11 closes them.

Issues #R2-#1, #R2-#2, #R2-#3 — template gaps:

  R2-#1: UC template missing `Invokes:` and `Domain entities` fields
         that the example uses but the template doesn't ship. These
         carry real traceability value: Domain entities tells the
         Analyst which entities to expect on the robustness diagram;
         Invokes tells everyone downstream which UCs this one depends
         on.

  R2-#2: UC template's Postconditions field was a single string;
         real UCs split outcomes (Success vs Rejection vs ...). The
         example used `Success:` / `Rejection:` sub-headings; the
         template now formalizes that pattern.

  R2-#3: REQ template used `Source:` (free text); UC template uses
         `Intakes:` (structured list). Same concept, different field
         names — inconsistent. v0.9.11 aligns REQ to `Intakes:`.

Issues #R2-#4, #R2-#5, #R2-#6 — cross-UC invocation handling:

  R2-#4: The "cite invoked UCs with explicit IDs" rule lived only
         in the Analyst agent (M2) — but the PO drafts UC text at
         M1, before the Analyst sees it. So the Analyst had to
         retrofit invocation citations during M2 instead of finding
         them already correct. v0.9.11 adds rule 12 to the PO so
         the citation convention ships from M1.

  R2-#5: PO M1 checklist had no item for "UC-text invocations match
         the Traceability Invokes: block." Drift between the two
         was easy and undetected.

  R2-#6: Traceability agent had 13 validation checks; none covered
         in-text UC invocations. A UC saying "system invokes
         BS-UC-999" with no `BS-UC-999.md` file would slide past
         the M1 gate. v0.9.11 adds check #14 (invocation drift).

### Methodology audit (per CLAUDE.md)
- **Cited rules:** Ch3 #7 (two-column UC format), Ch4 #1 (8 easy
  steps to better use case), Ch3 #2 (UCs in context of object
  model — Domain entities field strengthens UC↔domain-model
  tracing). All already ✅.
- **Status shifts:** none. Citations get richer.
- **No contradictions found.** v0.9.11 unifies a citation
  convention that had been split across PO and Analyst agents.

### Changed
- `templates/use-case-template.md`:
  - Postconditions structured as Success/Rejection sub-bullets with
    a comment about additional states (R2-#2)
  - Traceability block adds `Invokes:` and `Domain entities
    introduced or used:` fields with example syntax (R2-#1)
- `templates/req-template.md` — `Source:` field replaced by
  `Intakes:` with same structure as UC template (R2-#3)
- `agents/iconix-product-owner.md`:
  - New rule 12 "Cross-UC invocations cite explicit IDs" with
    format spec `<PREFIX>-UC-XXX | <Title> | <Package>`, mirror
    rule between UC text and Traceability block, and
    `(downstream — not yet drafted)` escape for forward references
    (R2-#4)
  - M1 checklist gains an item enforcing the mirror rule (R2-#5)
- `agents/iconix-traceability.md` — new check #14 "invocation
  drift" added to the validation suite (R2-#6); broken / unmatched
  invocations are M1 blockers
- `docs/iconix/iconix-process-reference.md` — "Last reviewed"
  bumped to v0.9.11 with the Round-2 audit summary

### Note on the example
The Write Customer Review example was authored before v0.9.11 and
will not match the new template fields. This is intentional —
running `/iconix-upgrade --dry-run examples/write-customer-review/`
should now flag the example's UC as needing retrofit (missing
`Intakes:` field per v0.9.10, alt course A's preamble per v0.9.10,
plus the new v0.9.11 gaps). That's the v0.9.9 dogfood test we owe;
the example refresh itself is intentionally deferred until the
Round-2-and-beyond fixes are done.

## [0.9.10] — 2026-05-10

Forcing-function fixes. We started a real-world test run of the kit
on the Write Customer Review example (driving its 3 intakes through
the PO agent's intake checklist + REQ/UC drafting). Seven concrete
issues surfaced before reaching M1 gate — issues that no amount of
agent-prompt review could have caught. v0.9.10 fixes all seven.

This is exactly the kind of feedback that confirms the v0.9.5–v0.9.9
agent prompts need real-world exercise, not just internal logic
review. Future versions should keep running real examples through
the kit and folding back the findings.

### Issues found and fixed

1. **Multi-input intake convergence was unspecified.** Real projects
   often deliver several intakes (email + transcript + ticket) for
   the same feature. The PO agent told you what to do with one input,
   not several. Fix: new `## When multiple intakes describe the same
   goal` section in `agents/iconix-product-owner.md` with a 4-step
   consolidation rule. UC's Traceability block now lists ALL source
   intakes, not just the most recent one.

2. **REQ atomicity criteria not defined.** The kit said "atomic
   functional requirements" without telling you what *atomic* meant.
   You could plausibly produce 1, 2, or 3 REQs from the same intake.
   Fix: new rule 10 in PO agent — "one REQ per testable observable
   behaviour; alternates extending the same goal stay in the parent
   REQ unless they introduce a distinct measurable target, distinct
   user goal, or pass an orthogonality test." Bias toward fewer REQs
   with richer alternate-course coverage.

3. **Initial domain model lacked a template + inline guidance.** PO
   rule 9 said "draw an attribute-only class diagram" but shipped no
   PUML template, no concrete heuristic for "is this noun an entity
   or a state on another entity?", and forced you to bounce to the
   Analyst agent file for the rules. Fix: new
   `templates/domain-model-initial-template.puml` with inline rule
   comments AND the most critical heuristics inlined into PO rule 9
   (real-world only; attributes-only; type everything; skip state-
   machine entities; show relationships; domain model = glossary).

4. **Two-column UC format had no convention for runtime forks.**
   Some user actions branch on a runtime precondition (logged in
   yes/no). The format has no inline conditional. Fix: new rule 11
   in PO agent + comment in `templates/use-case-template.md` —
   "basic course is the happy path with preconditions met; runtime
   forks become alternate courses with `At step N, if <condition>:`
   preamble." Static preconditions go in the Preconditions metadata,
   not in alternates.

5. **"Two paragraphs total" prompt rule contradicted the UC template
   structure.** The PO agent's rule said "no UC exceeds two
   paragraphs total: paragraph 1 = basic course, paragraph 2 = all
   alternate courses" — but `templates/use-case-template.md` has
   separate `## Alternate Course A: <name>` H2 sections (one per
   alternate). A UC with 5 alternates (like Write Customer Review)
   has 5 H2 sections — clearly not "two paragraphs." Fix: rule 3
   restated as "fits on one page when rendered" (preserves the
   book's brevity intent without the literal-paragraph-count
   contradiction); template comment clarifies that the structured
   H2 alternates are correct format but total length stays
   page-length. M1 checklist item updated; feature-request
   template's INVEST line updated.

6. **Intake templates blurred raw input and PO output.** The email
   template had `## Verbatim text` (input) and `## PO restatement`
   (output) in the same file separated only by a `---`. A fresh
   reader couldn't tell at a glance what the email *was* vs what
   the PO *added*. Fix: explicit ⚠️ banner separator in
   `intake-email-template.md` and `intake-transcript-template.md`
   making input/output ownership unmistakable. (BRD and
   feature-request templates are single-author; no banner needed.)

7. **Intake `## Status` Ready/Blocked checkbox was never enforced.**
   The PO agent could happily extract REQs from an intake whose
   Status was still `Blocked` or unchecked, since nothing in the
   prompt told it to verify. Fix: new "Status-Ready check" paragraph
   in PO intake-checklist section — "before any REQ/UC drafting,
   verify the intake's `## Status` block is `Ready` and all
   `[VERIFY]` items resolved. If `Blocked`, refuse and surface the
   open items."

### Added
- `templates/domain-model-initial-template.puml` — new (issue #3).
  PUML skeleton with all six initial-domain-model rules as inline
  comments. Replaces the implicit "go read the analyst's rules"
  pointer.

### Changed
- `agents/iconix-product-owner.md`:
  - Rule 3 restated (issue #5 — "two-paragraph" → "one-page" + UC-template alignment)
  - Rule 9 expanded with inline critical heuristics + reference to
    new template (issue #3)
  - New rules 10 and 11 (issues #2 and #4 — REQ atomicity, conditional path forks)
  - New Status-Ready check paragraph in `# Intake checklist` (issue #7)
  - New `## When multiple intakes describe the same goal` section
    in `# Intake checklist` (issue #1)
  - M1 checklist item updated for one-page rule (issue #5)
  - Split-signals list adds "rendered UC overflows one page" (issue #5)
- `templates/intake-email-template.md` — ⚠️ banner between Verbatim
  text and PO restatement (issue #6)
- `templates/intake-transcript-template.md` — ⚠️ banner between
  interview content and Analyst summary (issue #6)
- `templates/intake-feature-request-template.md` — INVEST line
  updated from "two-paragraph rule" to "one page when rendered"
  (issue #5)
- `templates/use-case-template.md`:
  - Header comment block explaining the brevity rule + when to use
    Alternate Courses vs Preconditions vs basic-course path (issues #4 and #5)
  - Alternate course tables now have a leading "At step N, if
    `<condition>`:" example row (issue #4)
  - Traceability block adds an `Intakes:` field for multi-intake
    consolidation (issue #1)
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers copy `domain-model-initial-template.puml` to
  `docs/iconix/templates/`.
- `.github/workflows/validate.yml` — smoke test asserts
  `domain-model-initial-template.puml` is installed.
- `README.md` — `domain-model-initial-template.puml` in templates
  listing.
- `docs/iconix/iconix-process-reference.md` — "Last reviewed" bumped
  to v0.9.10. No status shifts (all fixes clarify existing ✅ rules);
  rationale notes the cited Ch3, Ch2, Ch4 rules.

### Methodology audit (per CLAUDE.md `# Auditing kit changes against ICONIX Theory`)
- **Cited rules:** Ch3 #7 (two-column UC format) — already ✅, fixes
  #4 and #5 strengthen citations. Ch3 #1 (UC brevity — "typically
  two paragraphs", but a *typical*, not *maximum*) — fix #5 restates
  the kit's hardened "no UC exceeds two paragraphs" to align with the
  book's softer intent. Ch2 #3 (initial domain model before UCs) —
  already ✅, fix #3 adds the missing template. Ch4 #1 (8 easy steps
  to better use case) — already ⚠️, no change to status.
- **Status shifts:** none. All seven fixes clarify or refine existing
  ✅ rows; the cited fixes don't move any cell from one status to
  another. Citations get more specific.
- **No contradictions found.** Fix #5 actually *resolved* a
  contradiction the kit had been shipping for several versions
  (agent prompt vs UC template).

## [0.9.9] — 2026-05-10

Closes the kit-version-evolution loop that v0.9.5–v0.9.8 implicitly
opened: every minor version added new templates, folders, or config
sections, but existing projects had no way to pick those up without
re-running `iconix-init --force` (which works for templates and
config but doesn't surface what's *different* about authored
artifacts). v0.9.9 adds `/iconix-upgrade` — a kit-version migration
agent that auto-applies safe additive changes and produces a
detect-and-report for project artifacts.

Three-layer migration model:

  Layer A (folders)     — auto-apply via mkdir -p
  Layer B (config)      — auto-apply with conservative defaults
                          (every new boolean toggle = false on upgrade,
                          even if the kit's seeded template has true)
  Layer C (templates)   — auto-apply, refresh reference docs
  Layer D (artifacts)   — DETECT ONLY. Never touch UCs / source /
                          tests / bug reports. Report what differs.
  Layer E (CI / git)    — auto-apply based on git.provider

The "conservative defaults during upgrade" rule is deliberate: the
upgrade itself must not change runtime behaviour. The user opts in
by editing iconix.config.yaml after reading the report.

Distinct from iconix-migration (which retrofits ICONIX onto legacy
CODE). Upgrade migrates the kit VERSION. Same word, different
problems; intentionally separate agents.

This is a **tooling-only** change per CLAUDE.md (no ICONIX rules
introduced; no methodology shifts). Theory audit consciously skipped
and noted here for clarity.

### Added
- `agents/iconix-upgrade.md` — new agent. Detects current installed
  version (from `kit_version` field, or heuristic feature-presence),
  computes the diff, applies layers A/B/C/E, produces a
  detect-and-report for layer D, updates `kit_version`. Read-only on
  project artifacts. Idempotent. Refuses if detected version < 0.9.0
  (recommends fresh install instead).
- `commands/iconix-upgrade.md` — new slash command. Supports
  `--dry-run` for preview-only, `--from <version>` to override
  detection, `--source <path>` to specify a kit-source path
  different from the original install.
- `templates/upgrade-report-template.md` — report format. Sections:
  Summary, Auto-applied (per layer), Detected for review (per
  artifact category), Suggested config flips, Recommended manual
  actions, Rollback notes, Traceability footer.
- `templates/iconix.config.yaml` — new `kit_version: "0.9.9"` field
  at the top of the config. Set automatically by `iconix-init` on
  fresh install; bumped by `/iconix-upgrade` after a successful
  migration. Used by `iconix-upgrade` for version detection (with
  heuristic fallback for pre-v0.9.9 projects).
- New folder seed: `upgrades/` — where upgrade reports are written.

### Changed
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers now create `upgrades/` folder, copy
  `upgrade-report-template.md` to `docs/iconix/templates/`, and
  list the new agent + command in the Next-steps output.
- `agents/iconix-orchestrator.md` — routing heuristic for "we're on
  an older kit version" / "how do I upgrade" → Upgrade agent
  (`/iconix-upgrade` or `/iconix-upgrade --dry-run`).
- `README.md` — `iconix-upgrade.md` in agents and commands listings;
  `upgrade-report-template.md` in templates listing; new full
  **Upgrading an existing installation** section explaining the
  three-layer model, what's auto-applied, what's never touched,
  what gets detected-and-reported, version detection logic, and
  the distinction from `iconix-migration`.
- `.github/workflows/validate.yml` — smoke test asserts
  `kit_version` field present in seeded `iconix.config.yaml`,
  `upgrade-report-template.md` installed, `upgrades/` folder exists.

### Methodology audit (per CLAUDE.md `# Auditing kit changes against ICONIX Theory`)
- **Tooling-only change.** `/iconix-upgrade` is kit-version
  maintenance — it does not introduce ICONIX rules, does not change
  any phase semantics, does not modify the matrix's coverage.
  Theory audit consciously skipped per CLAUDE.md's guidance: *"Tooling-
  only changes (installer scripts, CI workflow, version bumps, typo
  fixes, methodology-neutral bug fixes, formatting) do not require
  a theory audit."*
- The agent's "detect-and-report" of artifacts that don't match
  current template format is methodology-aware (it knows what
  current templates require) but doesn't change the rules — it
  surfaces drift between authored artifacts and the kit's evolved
  templates, leaving remediation to the user.

## [0.9.8] — 2026-05-10

Closes the largest remaining behavioural gap from the v0.9.4 kit
assessment: **Phase 9 — the implementation loop**. Until now, the
post-CDR phase was a one-line placeholder in the orchestrator
("Developer + Tester iterate") with no specification of who owns
which iteration, when the Reviewer kicks in, or what triggers
"done." v0.9.8 expands Phase 9 into 4 explicit sub-states
(9.1 kickoff → 9.2 pre-merge drift → 9.3 fix loop → 9.4 merge)
with handoff conditions, an iteration cap, and escalation paths.

Bundles backlog item #2 — **Reviewer Type 2 closure**. After a Type 2
bug's REQ change flow completes, the Reviewer now re-confirms the
*original* bug report against the *new* SD, appending a `## Closure`
section to the bug report. Without this, a Type 2 fix could merge
without anyone re-checking it actually solved the reported problem.
Both changes ship together because Phase 9 is the natural home for
the bug-fix paths.

Methodology audit: operationalizes existing Ch10 rules (#10, #9, #8,
#5, #4, #3, #1) — no new rules introduced. Verified via PDF read of
the Ch10 Top 10 list. Type 2 closure is a small refinement of Ch10
#9 ("review the process") — closing a missing step in the kit's
prior bug flow rather than inventing a new methodology.

### Added
- `templates/phase9-cycle-template.md` — optional per-UC cycle log.
  Records each Developer ↔ Tester ↔ Reviewer iteration's verdict and
  the final exit state. For teams wanting audit-grade evidence of
  the loop history (lives in `phase9-cycles/UC-XXX-cycle.md`).
- `agents/iconix-reviewer.md` — three new mode sections:
  - **Pre-merge drift mode (Phase 9.2)** — the canonical Phase 9
    review. Aggregates code↔SD, code↔class-model, robustness, NFR,
    framework/business-logic checks into one verdict (APPROVE /
    APPROVE WITH NOTES / REQUEST CHANGES / BLOCK MERGE). Drives 9.4
    or 9.3 routing.
  - **Bug-fix verification mode (post-Type 1)** — focused re-check
    that the *specific drift the original triage flagged* is closed.
    Not a full pre-merge review; just verification.
  - **Type 2 closure mode (post-REQ-change-flow)** — re-confirms the
    *original bug report* against the *new* SD. Appends a `## Closure`
    section to the bug report on success; recommends `REOPEN` if the
    new design or implementation doesn't address the reported issue.
- `agents/iconix-developer.md` — new **Implementation mode (Phase 9)**
  section with two sub-modes: initial implementation (9.1) and drift
  fix iteration (9.3). Cites Ch10 #1 explicitly for alternate-course
  coverage.
- `agents/iconix-tester.md` — new **Test implementation mode (Phase 9)**
  section with two sub-modes: initial test implementation (9.1) and
  test re-run after drift fix (9.3). Tester runs in parallel with
  Developer on the same `feature/UC-XXX-<slug>` branch.
- `templates/iconix.config.yaml` — new `phase9:` section with
  `enabled` (default true), `max_iterations_per_uc` (default 5 — the
  9.2↔9.3 cap), `reviewer_required_for_merge` (default true).

### Changed
- `agents/iconix-orchestrator.md`:
  - Phase 9 in the phase-order list expanded from one-line placeholder
    to a pointer to the new `# Phase 9 routing` section.
  - New section **Phase 9 routing — the implementation loop** with
    explicit 9.1 / 9.2 / 9.3 / 9.4 sub-state semantics, exit conditions,
    and the iteration-cap escalation logic (architectural drift →
    Architect; requirements-shaped → PO; either path effectively bumps
    a stuck Type 1 to Type 2).
  - Type 1 bug flow now ends with **Reviewer bug-fix verification mode**
    (the missing closure step the prior version skipped).
  - Type 2 bug flow now ends with **Reviewer Type 2 closure mode**.
- `iconix-state-machine.puml`:
  - `Implementation` state expanded to a composite state with
    sub-states 9.1 / 9.2 / 9.3 / 9.4 and an `Escalate` change-state.
    Loop transition 9.3 → 9.2; cap-hit transition 9.3 → escalate;
    merge transition 9.4 → done.
  - **Removed standalone `BugFix` and `BugVerify` states** — they
    redundantly modelled the same loop as Phase 9.3 → 9.2. The
    Type 1 bug flow now re-enters the Implementation Loop at 9.3
    on a `bugfix/T1-*` branch (book Ch10 #9 treats fix-and-verify
    as one process; the kit shouldn't draw two loops). Reviewer
    mode selection (Pre-merge drift mode vs Bug-fix verification
    mode) is an internal detail of the agent at 9.2 — not a
    separate state-machine flow. `Done` now has an outbound
    `--> BugTriage` transition for "bug reported on shipped feature."
- `agents/iconix-orchestrator.md` — `# Bug flow` Type 1 narrative
  rewritten to acknowledge it's the same loop as Phase 9.3 → 9.2,
  with the only differences being the branch name and the Reviewer's
  mode at 9.2. No new behaviour; just stops drawing the loop twice.
- `README.md`:
  - `phase9-cycle-template.md` added to the templates listing.
  - Pipeline diagram now shows `Implementation loop` with the four
    sub-states inline.
  - New full **Phase 9 — the implementation loop** section explaining
    the 4-sub-state flow, configuration, three new Reviewer modes,
    optional cycle log, and the methodology mapping to Ch10.
- `docs/iconix/iconix-process-reference.md`:
  - Ch10 row citations refreshed (#10, #9, #8, #5, #4, #3, #1) to
    point at the new Phase 9 sub-states and Reviewer modes. Status
    unchanged on every row (already ✅).
  - "Last reviewed" bumped to v0.9.8 with rationale citing PDF read
    of book p. 259.
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell):
  - Both create `phase9-cycles/` folder during folder-structure
    seeding.
  - Both copy `phase9-cycle-template.md` to `docs/iconix/templates/`.
- `.github/workflows/validate.yml` — smoke test asserts
  `phase9-cycle-template.md`, `phase9-cycles/` folder, and the
  `phase9:` section in seeded `iconix.config.yaml`.

### Methodology audit (per CLAUDE.md `# Auditing kit changes against ICONIX Theory`)
- **Cited rules:** Ch10 #10 (drive code from design), #9 (if coding
  reveals design wrong, change it AND review the process), #8 (regular
  code inspections), #5 (if code gets out of control, revisit the
  design), #4 (keep design and code in sync), #3 (focus on unit
  testing while implementing), #1 (implement alternate courses too).
- **Book verification:** PDF read of Ch10 Top 10 list (book p. 259).
  Confirmed Phase 9's sub-state design maps cleanly to Ch10's
  guidelines without inventing new ones.
- **Status shifts:** none. Every Ch10 ✅ row gets a richer kit-location
  citation pointing at the new Phase 9 sub-states / Reviewer modes.
- **Type 2 closure framing:** small refinement of Ch10 #9's "AND
  review the process" — closing a missing step in the prior bug flow.
  Not classified as a new methodology rule.
- **No contradictions found.**

## [0.9.7] — 2026-05-10

Closes the #1 gap from the v0.9.6 backlog: **metrics & audit evidence**.
The kit produces well-structured artifacts at every phase, but until
now there was no aggregation showing teams whether the process was
actually paying off — and no single artifact a regulated-environment
auditor could point at and say "this is your ICONIX evidence." v0.9.7
adds an `iconix-metrics` agent that scans the project's current state
+ git history at run-time and produces audit-friendly snapshots
(markdown for humans + JSON for dashboards).

Snapshot-based, not event-based. The agent reads everything that
already exists (artifacts, milestone reports, reviews, change-impact
reports, bug reports, git log) and computes ~15 metrics across 5
categories. No external state, no new infrastructure — fits the kit's
"all artifacts are files" principle.

Provider-neutral on visualization: the JSON conforms to a stable
schema (v1.0); teams build their own dashboards in Power BI, Grafana,
Azure Workbooks, GitHub Insights, or anything else that reads JSON.
The kit ships no vendor templates — same provider-neutrality stance
as v0.9.5 git integration.

Honestly marked as a kit extension. The book has only incidental
mentions of metrics (per-review data on Ch11 line 12405; the Code-
Inspection-vs-Code-Review sidebar acknowledging that formal
inspections gather metrics). v0.9.7 extends these to project-wide
aggregation, justified by Ch11 #6 and SME / regulated-environment
audit needs (ISO 27001 + 9001).

### Added
- `agents/iconix-metrics.md` — new read-only agent. Produces
  `metrics/snapshot-<date>.md` (audit-friendly markdown) and
  `metrics/snapshot-<date>.json` (validates against schema v1.0). On
  `/iconix-metrics trend`, also produces `metrics/trend-<date>.md`
  with deltas vs the prior snapshot. Read-only on everything except
  `metrics/`. Eight-step computation algorithm specified in the agent
  prompt: read config → throughput → cycle time (from
  `[<UC>] <phase>: ...` commits) → quality → process compliance →
  trends → blockers → render. Retention enforced: prunes old
  snapshots beyond `metrics.retention` (default 12).
- `commands/iconix-metrics.md` — new slash command.
  `/iconix-metrics` produces a snapshot; `/iconix-metrics trend`
  also produces the trend report.
- `templates/metrics-snapshot-template.md` — markdown format. Six
  numbered sections: throughput, cycle time, quality, process
  compliance, trend (when applicable), blockers and stale state.
  Includes ISO-audit framing.
- `templates/metrics-schema.json` — formal JSON schema (Draft
  2020-12, schema version 1.0). Stable contract for downstream
  dashboards. Required and optional fields explicitly documented.
- `docs/iconix/metrics-glossary.md` — authoritative definitions for
  every metric. Lists what's intentionally **not** a metric (no
  per-developer attribution, no LOC, no story-point velocity, no
  cost estimates — Ch13 #3 stays 🚫).

### Changed
- `templates/iconix.config.yaml` — new `metrics:` section with
  `enabled` (default true), `output_dir` (default `metrics`),
  `ci_snapshot` (default false), `retention` (default 12),
  `git_history_window` (default 12 months).
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell):
  - Both create `metrics/` folder during folder-structure seeding
  - Both copy `metrics-snapshot-template.md` and
    `metrics-schema.json` to `docs/iconix/templates/`
  - Both copy `metrics-glossary.md` to `docs/iconix/`
  - Bash "Next steps" lists `/iconix-metrics`
- `agents/iconix-orchestrator.md` — routing heuristic for "how is
  the project doing?" / "ISO audit evidence" → Metrics agent.
- `README.md` — `iconix-metrics.md` in agents listing;
  `iconix-metrics.md` command listing; `metrics-snapshot-template.md`
  and `metrics-schema.json` in templates listing; new full **Metrics
  & audit evidence** section explaining the 5 metric categories,
  output layout, configuration, and ISO-audit framing.
- `docs/iconix/iconix-process-reference.md`:
  - Drift-detection sub-table gains a "Project-wide metrics + audit
    evidence (kit extension)" row marked ✅, explicitly framed as
    not-in-book.
  - Ch11 #6 kit-location updated to cite the project-wide extension.
  - "Last reviewed" bumped to v0.9.7 with rationale (PDF grep
    confirms only incidental coverage of "metric/dashboard/measure/kpi").
- `.github/workflows/validate.yml` — smoke test asserts
  `metrics-snapshot-template.md`, `metrics-schema.json`,
  `metrics-glossary.md`, `metrics/` folder, and `metrics:` section
  in the seeded `iconix.config.yaml`.

### Methodology audit (per CLAUDE.md `# Auditing kit changes against ICONIX Theory`)
- **Cited rules:** Ch11 #6 (Gather data during the review) — kit
  location updated to add project-wide extension. Ch11
  Code-Inspection-vs-Code-Review sidebar — explicitly acknowledges
  formal code inspections gather metrics.
- **Book verification:** PDF grep for `metric|dashboard|measure|
  gate-failure|drift rate|kpi|throughput` returned only incidental
  hits (class-count metrics on line 648; the per-review note on
  line 12405). Confirmed: project-wide metrics is a kit extension.
- **Status shifts:** new ✅ row added to the Drift-detection
  sub-table for "Project-wide metrics + audit evidence", explicitly
  marked as kit extension. Ch11 #6 status unchanged (already ✅;
  citation extended).
- **No contradictions found.** The book's bias toward small co-
  located teams doesn't conflict with project-wide metrics — it just
  doesn't address them. Adding metrics doesn't violate any canonical
  principle.

## [0.9.6] — 2026-05-09

Closes the second-largest gap from the v0.9.4 kit assessment: **multi-
developer concurrency upfront detection**. Until now, two devs working
on UCs that quietly converged on the same domain class (or controller,
or DB table) only discovered the conflict when the Reviewer ran post-
implementation drift detection. v0.9.6 shifts that detection left to
**M2 / PDR**, when the robustness diagrams already make class
references explicit. Advisory by default — teams enable CI blocking
after they trust the detector.

This is honestly a **kit extension** over the canonical ICONIX text.
The book assumes a small co-located team sharing one whiteboard model;
it doesn't address cross-UC conflict detection (verified via grep of
the PDF: "concurrent" appears only in unrelated contexts). v0.9.6 fills
that gap, justified by Ch11 #1 (Model Update at every gate) extended
to the multi-dev reality. The matrix marks this clearly as a kit
extension rather than misclaiming book coverage.

### Added
- `commands/iconix-concurrent.md` — new slash command. Standalone
  invocation of the concurrent-touch detection (the same routine also
  runs automatically at M2 gate). Accepts an optional UC-ID to filter
  the report to conflicts involving that UC.
- `templates/concurrent-touch-template.md` — report format. Sections:
  detection scope, in-flight UCs, class-touch matrix, per-conflict
  detail with severity (HIGH / MEDIUM / LOW) and recommended
  resolutions, configuration echo, traceability footer. Installer
  copies it to `docs/iconix/templates/`; CI smoke test asserts it
  exists.
- `templates/iconix.config.yaml` — new `concurrent_check:` section:
  `enabled` (default true), `block_on_high_conflict` (default false —
  advisory), `detect_boundaries` (default true), `detect_db_containers`
  (default true).

### Changed
- `agents/iconix-traceability.md` — new section **Concurrent touch
  detection**. Six-step routine: read config → identify in-flight UCs
  via `git branch -r --list 'origin/feature/UC-*'` (or DRAFT artifacts
  as fallback) → build class-touch maps from RBs and class model →
  detect conflicts pairwise → recommend resolutions → render report.
  Integrated into the M2 gate report.
- `agents/iconix-architect.md` — new section **Resolving concurrent
  touches**. Architect is the canonical resolver for HIGH conflicts,
  proposing options (extract shared service, rename controllers, share
  migration, etc.) but never unilaterally rewriting UCs/RBs. PDR
  readiness checklist gains a concurrent-touch review item.
- `agents/iconix-orchestrator.md` — phase 5 (M2 gate) now explicitly
  includes concurrent-touch detection; HIGH conflicts route back to
  Architect before M2 promotion. New routing heuristic for
  `/iconix-concurrent`.
- `agents/iconix-git.md` — new section **In-flight UC detection** as a
  helper for Traceability's concurrent-touch check. Returns the list
  of `(UC-ID, phase, branch-age)` tuples from open feature branches.
  Falls back to empty list when no git context is available.
- `iconix-state-machine.puml` — M2 gate now branches to a new
  `Concurrent-touch resolution (Architect)` state on HIGH conflicts;
  loops back to the gate after resolution.
- `templates/git-integration/github/PULL_REQUEST_TEMPLATE/m2.md` and
  `templates/git-integration/azure-devops/pull_request_templates/m2.md`
  — both M2 PR templates gain a checklist item for concurrent-touch
  review with `[CT-ACCEPT-XXX]` markers for explicitly-accepted
  conflicts.
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers copy `concurrent-touch-template.md` to
  `docs/iconix/templates/`. Bash "Next steps" output mentions
  `/iconix-concurrent`.
- `README.md` — `iconix-concurrent.md` added to the commands listing;
  `concurrent-touch-template.md` added to the templates listing; new
  full **Multi-developer concurrency** section explaining detection
  scope, the M2 → Traceability → Architect flow, and configuration.
- `docs/iconix/iconix-process-reference.md` — new row in the Drift-
  detection sub-table for "Concurrent class touches across in-flight
  UCs" marked ✅ with explicit "kit extension" framing. "Last reviewed"
  bumped to v0.9.6 with rationale citing the book grep that confirmed
  no canonical coverage.
- `.github/workflows/validate.yml` — smoke test asserts
  `concurrent-touch-template.md` exists and the seeded
  `iconix.config.yaml` contains the `concurrent_check:` section.

### Methodology audit (per CLAUDE.md `# Auditing kit changes against ICONIX Theory`)
- **Cited rules:** Ch11 #1 (Model Update at every gate) — concurrent-
  touch detection extends the model-update concept across UCs at M2.
  Ch6 PDR readiness — gains a new technical check, no shift to
  existing rule statuses.
- **Book verification:** grep of the PDF for "concurrent / parallel
  develop / multi-dev / merge conflict / shared class" returned only
  unrelated hits (transaction throughput in REQ wording, concurrent
  activities in activity diagrams). Confirmed: this is a kit
  extension, not a re-derivation of an existing rule.
- **Status shifts:** new row added to the Drift-detection sub-table.
  Marked ✅ for the new check itself, with explicit "kit extension"
  framing in the kit-location cell so future audits aren't misled
  about book coverage.
- **No contradictions found.**

## [0.9.5] — 2026-05-09

Closes the largest gap identified in the v0.9.4-session kit assessment:
**git integration**. Until now only the Reviewer was git-aware (it read
`git diff`); no agent created branches, opened PRs, or enforced commit
hygiene. The kit's careful artifact discipline could be undone at the
merge stage by inconsistent git history. v0.9.5 adds a provider-agnostic
core (branch + commit conventions + a shell-script merge-gate) plus
first-class adapters for **GitHub** and **Azure DevOps** — chosen because
they cover the vast majority of regulated/enterprise iGaming
environments. GitLab and Bitbucket are deferred to a later version; the
generic adapter (any CI that can run a shell script) keeps them usable
in the meantime.

### Added
- `agents/iconix-git.md` — new agent. Owns branch creation/validation,
  PR opening, commit-message format checking, posting Reviewer findings
  as PR comments. Reads `git.provider` from `iconix.config.yaml`.
  Read-only on ICONIX artifacts; never force-pushes; never bypasses
  branch protection or required CI checks.
- `commands/iconix-pr.md` — opens a phase-appropriate draft PR (M1 / M2
  / M3 / Implementation) using the matching template. Detects phase
  from the diff; refuses on mixed-phase commits. Routes through `gh`
  (GitHub) or `az` (Azure DevOps) when configured; prints the suggested
  URL when `pr_cli: none`.
- `commands/iconix-trace-check.md` — runs the traceability validator
  locally with the same checks the CI merge-gate runs. Pre-push guard.
- `templates/git-integration/` — new top-level templates folder:
  - `branch-conventions.md` — `feature/UC-XXX-<slug>`, `arch/<scope>`,
    `bugfix/T1-<slug>`, `bugfix/T2-UC-XXX-<slug>`, `hotfix/T1-<slug>`,
    `release/<version>`. Trunk vs. GitFlow strategies.
  - `commit-conventions.md` — `[<artifact-id>] <phase>: <summary>`
    format. Phases: M1 / M2 / M3 / Impl / Fix / Doc / Refactor / Chore.
    Mixed-phase commits flagged. Optional work-item ref footer.
  - `generic/validate-traceability.sh` — provider-agnostic merge-gate.
    Checks every changed file under `src/` and `tests/` for a
    `Traceability:` comment; checks every cited ID points to an
    existing artifact. Self-contained POSIX shell; runs identically in
    CI containers and on developer laptops.
  - `generic/README.md` — how to wire the script into any CI provider
    not covered by a first-class adapter.
  - `github/workflows/iconix-validate.yml` — GitHub Actions workflow
    that runs the validator on every PR and pushes comment with fix
    instructions on failure.
  - `github/pull_request_template.md` + `PULL_REQUEST_TEMPLATE/{m1,m2,m3,implementation}.md`
    — default + phase-specific PR templates.
  - `azure-devops/azure-pipelines-iconix-validate.yml` — Azure
    Pipelines equivalent. Uses `SYSTEM_PULLREQUEST_TARGETBRANCH` for
    base-ref detection; posts a PR comment via REST on failure.
  - `azure-devops/pull_request_templates/{default,m1,m2,m3,implementation}.md`
    — Azure DevOps PR templates (loaded from
    `.azuredevops/pull_request_templates/`).
- `templates/iconix.config.yaml` — new `git:` section: `provider`
  (github / azure-devops / generic), `default_branch`,
  `branch_strategy` (trunk / gitflow), `work_item_prefix` (optional;
  `AB#` for Azure Boards, `#` for GitHub Issues, empty to disable),
  `pr_cli` (gh / az / none), `impl_squash`. Default `provider:
  generic`, `pr_cli: none` — the kit doesn't assume a provider until
  configured.

### Changed
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers now read `git.provider` from the just-seeded
  `iconix.config.yaml` and copy the matching subtree:
  - Always: `validate-traceability.sh` to `.ci/`; conventions docs to
    `docs/iconix/templates/git-integration/`.
  - `github`: workflow to `.github/workflows/`, PR templates to
    `.github/` and `.github/PULL_REQUEST_TEMPLATE/`.
  - `azure-devops`: pipeline to repo root, PR templates to
    `.azuredevops/pull_request_templates/`.
  - `generic`: just the script + a README explaining manual wiring.
  - "Next steps" output now lists the new agents and commands.
- `agents/iconix-orchestrator.md` — routing heuristics gain an entry
  for the Git agent (`/iconix-pr`, `/iconix-trace-check`).
- `agents/iconix-reviewer.md` — new section "Posting reviews on PRs"
  explaining that when git integration is configured, the Git agent
  posts the review report as a structured PR comment. Reviewer doesn't
  post directly — produces the report; Git agent handles delivery.
  When recommendation is BLOCK MERGE / REQUEST CHANGES, the Git agent
  also sets the PR to draft (when supported).
- `agents/iconix-traceability.md` — new section "CI counterpart"
  acknowledging that `.ci/validate-traceability.sh` runs a subset of
  the agent's validation as a fast pre-merge gate. The agent remains
  the canonical auditor for the full chain.
- `README.md` — `iconix-git.md` added to the agents listing;
  `iconix-pr.md`, `iconix-trace-check.md` added to the commands
  listing; `templates/git-integration/` added to the templates
  listing; new full **Git integration** section explaining
  configuration, conventions, what the installer drops in per
  provider, the merge-gate, and the Reviewer-as-PR-bot flow.
- `docs/iconix/iconix-process-reference.md` — Ch11 #5 row gains a
  citation for Reviewer-as-PR-bot (already ✅; kit-location updated
  only). "Last reviewed" bumped to v0.9.5.
- `.github/workflows/validate.yml` — smoke test now asserts
  `branch-conventions.md`, `commit-conventions.md`, and a working
  executable `validate-traceability.sh` are installed.

### Methodology audit (per CLAUDE.md `# Auditing kit changes against ICONIX Theory`)
- Cited rules: **Ch11 #5** (Follow up review with action points) — kit
  location updated; **Ch11 #2** (Just formal enough) — PR templates
  and check runs are "structured but lightweight"; **Ch11 #6** (Gather
  data; build boilerplate checklists) — already ✅, no shift; **Ch1
  milestones** — gates as PR boundaries doesn't change the methodology,
  it just expresses it through git.
- Status shifts: none. Git/PR is a tooling integration over existing
  rules.
- Out-of-scope unchanged: "Human review meeting" remains 🚫 — a PR
  comment thread is async/asynchronous, not the in-person whiteboard
  session the book describes.
- No contradictions found.

## [0.9.4] — 2026-05-08

Two changes that travel together: (1) a procedural rule in `CLAUDE.md`
forcing Claude to audit every methodology-surface kit change against the
process-reference matrix and the book before treating it complete — this
is the upstream check that prevents kit drift from accumulating one
well-intentioned edit at a time. (2) `/iconix-bug` exposes the Reviewer's
existing bug-triage workflow as a first-class slash command. The
workflow itself was already in `iconix-reviewer.md` `# Bug triage` and
already credited ✅ in the matrix (Ch10 #9, Ch10 #5, Ch11 #1,
Drift-detection sub-table); previously users had to invoke it
conversationally or wait for the Orchestrator to detect the input. Now
they can route directly. This v0.9.4 work was itself the first
methodology-surface change to follow the new audit rule from (1) — book
Ch11 cited inline in the new command for traceability.

### Added
- `commands/iconix-bug.md` — new slash command. Direct entry point to the
  Reviewer's `# Bug triage` workflow. Accepts a bug description, source
  path, or UC-ID; produces the standard `## Bug triage` block (Type 1
  implementation defect vs Type 2 design defect) and recommends the next
  step (Developer bug-fix mode for Type 1; `/iconix-impact` → REQ change
  flow for Type 2). Reviewer-only — no fixes made by this command.
- `templates/bug-report-template.md` — optional structured input for
  `/iconix-bug`, mirroring the existing intake-template pattern for the
  Product Owner. Sections: affected artifact, observed behaviour,
  **exception / stack trace** (top application frame is the Reviewer's
  direct anchor against SD methods; exception type often pre-classifies
  Type 1 vs Type 2), expected behaviour, reproduction, optional triage
  hint, Reviewer-filled traceability block. Installer (bash + PowerShell)
  copies it to `docs/iconix/templates/` alongside the intake templates;
  CI smoke test asserts it exists.
- `CLAUDE.md` — new section **Auditing kit changes against ICONIX
  Theory**. Defines what counts as a methodology-surface change (agent
  rules, templates, gates, pipeline order, the matrix itself,
  methodology-bearing commands) and what does not (installer scripts,
  CI, version bumps, typos, methodology-neutral bug fixes). Specifies a
  4-step audit procedure: cite the matrix row → verify against the book
  PDF when the matrix doesn't resolve the question → update the matrix
  in the same change if coverage shifted → surface contradictions
  rather than silently introducing them. Requires Claude to state in
  the response which rules were audited and what was cited.

### Changed
- `README.md` — `/iconix-bug` added to the directory listing and the
  command-routing table; the bug-flow narrative (Step 1 — Always triage
  first) gains a three-row **Input form** table (UC-ID / Source path /
  Free-text) showing example invocations and what the Reviewer does
  first for each; mentions both entry points (`/iconix-bug` direct and
  `/iconix-next` via Orchestrator); points users at the new template
  for larger bugs with stack traces. Templates listing in the directory
  layout adds `bug-report-template.md`.
- `iconix-state-machine.puml` — `BugTriage` state's note reframed from
  single-trigger ("Triggered at any time by the Orchestrator") to
  two-entry-point ("/iconix-bug" direct, "/iconix-next" via Orchestrator).
- `agents/iconix-orchestrator.md` — `# Bug flow` Step 1 now acknowledges
  the `/iconix-bug` direct entry point for users who already know it's
  a bug (the Orchestrator's input-detection is bypassed in that case;
  same triage workflow either way).
- `docs/iconix/iconix-process-reference.md`:
  - Drift-detection sub-table row "Bug type classification (Type 1 vs
    Type 2)" kit-location cell now cites both `iconix-reviewer.md`
    `# Bug triage` and `/iconix-bug <ref>`. Status unchanged (already ✅).
  - **Ch11 #10** ("Prepare for review; participants read material in
    advance") flips from ❌ to ⚠️ — `bug-report-template.md` forces the
    bug reporter to surface affected artifact, observed-vs-expected,
    exception trace, and reproduction *before* the Reviewer is invoked,
    which partially covers "prepare review material in advance"; full
    guideline still includes a human meeting the kit does not convene.
  - Summary Coverage Matrix: Ch11 chapter row updated from `8|0|2|0`
    (80%) to `8|1|1|0` (85%). "Last reviewed" bumped to v0.9.4 with
    inline rationale.
- `iconix-init` (bash) and `iconix-init.ps1` (PowerShell) — both
  installers now copy `bug-report-template.md` to
  `docs/iconix/templates/` alongside the intake templates.
- `.github/workflows/validate.yml` — smoke test asserts
  `docs/iconix/templates/bug-report-template.md` exists after install,
  mirroring the assertions for the four intake templates.

## [0.9.3] — 2026-05-08

Two themes: (1) corrects a misattribution of book Ch2 rule #3 ("Draw the
domain model before writing use cases") — the matrix marked it ✅ because
the Orchestrator forced PO → Analyst order, but in practice neither agent
drew an initial domain model from REQs; the Analyst drew the only one
*after* UC text was already written. v0.9.3 reassigns initial domain-model
authorship to the Product Owner, as the book intends, and reframes the
Analyst's role as "refine, not create." (2) post-v0.9.0 audit of the
process-reference matrix introduces a 🚫 (Out of scope) marker so
deliberate boundaries (persona research, TDD red-green, storyboards,
human review meetings, code-header generation, UC-point estimation) stop
appearing as ❌ gaps and inflating the apparent missing-coverage count.

### Changed
- `agents/iconix-product-owner.md` — role expanded to own the **initial
  domain model**; new rule 9 mandates drawing it after REQs and before UC
  flows (book Ch2 guideline #3); adds `domain-model/domain-model.puml` to
  the artifact list; adds matching M1 checklist item.
- `agents/iconix-analyst.md` — role reframed: Analyst now **refines** the
  domain model started by the PO rather than creating it; step 7 and the
  artifact-list comment updated accordingly.
- `agents/iconix-orchestrator.md` — phase 1 description now states the
  Product Owner produces "REQs, **initial domain model**, UCs, glossary".
- `iconix-state-machine.puml` — Product Owner state machine now has an
  explicit `DraftDomainModel` substate between `DraftREQs` and `DraftUCs`,
  matching the new rule 9 ordering.
- `examples/write-customer-review/README.md` — project-wide artifacts
  callout corrected: domain model is "Product Owner drafts; Analyst
  refines as entities are discovered" (was: "Analyst owns").
- `README.md` — pipeline diagram adds the **Implementation** phase
  (Developer + Tester iterate after M3); PO bullet mentions "initial
  domain model"; templates listing adds `use-case-diagram-template.puml`
  (already present in `templates/`, was missing from the doc).
- `CLAUDE.md` — pipeline diagram adds **Implementation** as phase 9,
  matching the orchestrator and state machine.
- `docs/iconix/iconix-process-reference.md` — Ch2 rule #3 row rewritten
  to credit the PO and note the v0.9.3 correction.

### Added
- `docs/iconix/iconix-process-reference.md` — new `🚫 Out of scope`
  status marker. Six items reclassified from ❌ to 🚫 because they are
  deliberate kit boundaries, not gaps:
  - Ch1: Persona analysis (requires primary user research)
  - Ch1: TDD red-green-refactor cycle (kit derives TCs from RBs;
    "test-first thinking" is separately ⚠️ in scope per Ch12 #7)
  - Ch3 #6 / Ch4 #3: UI storyboards (external tools — Figma, Balsamiq)
  - Ch4 #2 / Ch6 #4: Human review meetings (kit produces artifacts
    *for* meetings; doesn't convene them)
  - Ch9 #2: Generate code headers (IDE/toolchain concern)
  - Ch13 #3: Estimates from UC scenarios (UC-point estimation needs
    team calibration data)
- `docs/iconix/iconix-process-reference.md` — Summary Coverage Matrix
  now shows a 🚫 column; coverage formula updated to exclude 🚫 from
  the denominator (out-of-scope items don't penalize coverage).
- `CLAUDE.md` — new **ICONIX Theory References** section pointing
  Claude at `docs/iconix/iconix-process-reference.md` (committed) and
  the gitignored `Use Case Driven Object Modeling with UML.pdf` for
  resolving methodology questions, with guidance to always read the
  PDF with the `pages` parameter.
- `CLAUDE.md` — new **Keeping README and state machine in sync**
  section instructing Claude to review `README.md` and
  `iconix-state-machine.puml` whenever a change touches the kit's
  user-facing surface.

### Fixed
- `docs/iconix/iconix-process-reference.md` — Summary Coverage Matrix
  count errors corrected: Ch4 was listed `7|2|1`, actual was `7|1|2`
  (one ⚠️, two ❌); Ch7 was listed `7|1|2`, actual was `7|0|3`. Ch7
  coverage corrects from 75% to 70%; remaining ❌ items (#10 hardware
  cost, #9 legacy default, #6 unproven tech) are genuine gaps, not
  out-of-scope.

## [0.9.2] — 2026-05-07

Closes a gap left in v0.9.0: the migration agent now reverse-engineers all
project-wide ICONIX artifacts, not just the per-feature ones. Without this,
human reviewers had to author the domain model and UC package overviews on
a second pass — even though the migration agent already had the information
needed.

### Changed
- `agents/iconix-migration.md` — two new phases added to both workflows
  (graph-assisted and code-walking fallback):
  - **Phase 4b — Domain model synthesis.** Filters the Phase 2 class model
    down to entity classes (drops Boundary / Controller classes from RBs,
    drops framework-typed fields, drops methods); maps inheritance and
    field references to is-a / has-a relationships; emits
    `domain-model/domain-model-DRAFT.puml` with provenance per class.
  - **Phase 5b — Use case package overview synthesis.** Clusters UC drafts
    by source directory / namespace (or graph community-detection in
    graph-assisted mode); emits one
    `use-case-packages/<package-slug>-DRAFT.puml` per cluster; flags any
    UC that does not fit a cluster as an orphan in the handoff report.
- `agents/iconix-migration.md` — pre-run idempotency check (Step 3) now
  detects human-edited DRAFTs of the two new artifacts; agent description
  in YAML frontmatter mentions them.
- `agents/iconix-migration.md` — *Output structure* section updated.
- `agents/iconix-migration.md` — non-HTTP entry points are now recognised
  as first-class boundaries: `BackgroundService` / `IHostedService`,
  message-bus consumers (`IConsumer<T>`, MassTransit / Azure Service Bus
  handlers), Azure Functions, AWS Lambda handlers. Phase 1 entry-point
  detection (graph-assisted + code-walking) and Phase 4 boundary mapping
  both updated. New mixed-responsibility check in Phase 4: when a
  background-service node also has direct outbound edges to entity / DB
  nodes, the agent flags the class `[VERIFY]` and recommends extracting
  a controller so the boundary stays thin.

### Fixed
- `agents/iconix-migration.md` — Phase 3 (sequence diagram extraction)
  was overpromising in graph-assisted mode. The previous wording told
  the agent to use `shortest_path` and treat the result as a sequence
  diagram, but `shortest_path` returns *one* topological route and is
  blind to branching, loops, async semantics (`await` vs
  `Task.WhenAll`), exception flow, fire-and-forget patterns, and
  polymorphic dispatch — all of which a sequence diagram must capture.
  Phase 3 now mandates a two-step extraction in both modes:
  (a) bound the call graph by enumerating **all simple paths** to leaf
  operations; (b) recover behaviour by reading the source at each
  visited node (the graph already gives `file_path` + `line_range`),
  mapping `if` / `try-catch` / loops / `await` / `Task.WhenAll` to
  PlantUML `alt` / `loop` / `par` groups. Provenance discipline
  extended: every group is marked `INFERRED (control-flow: <kw>)`
  with the source file:line cited. The agent now states the
  topology-vs-behaviour disclaimer to the user at the start of Phase 3.
- `agents/iconix-migration.md` — entry-point detection (Phase 1, both
  modes) and stereotype mapping (Phase 4 graph-assisted) were leaning
  on .NET-flavoured class-name lists. Restructured to be tech-stack
  neutral: detection is now by **responsibility shape** (universal
  signals: inbound dispatch, outbound infrastructure imports,
  conditional logic over domain values), with cross-stack reference
  tables covering C#/.NET, Java, Python, Node.js/TypeScript, Go, and
  Ruby. The agent reads `iconix.config.yaml` `stack.language` to
  weight the most likely patterns first.
- `agents/iconix-migration.md` — added explicit **Outbound Boundary**
  classification for repositories, SDK / API clients, message
  publishers, file/blob writers, and email/SMS senders. Previously
  the Phase 4 mapping recognised only inbound boundaries (controllers
  / hubs / consumers / hosted services); outbound adapters were
  silently miscategorised as Controllers because of their
  `*Service` / `*Repository` names. Outbound boundaries now render
  on the right side of their controller on the SD and carry an
  `<<outbound>>` stereotype on the RB.
- `agents/iconix-migration.md` — added a **disambiguation rule**:
  when a node's name suggests one stereotype but its imports suggest
  another, trust the imports. (A class named `OrderService` that
  imports a Stripe SDK and a DbContext is an outbound boundary's
  worth of work, not a controller.)
- `agents/iconix-migration.md` — broadened the Phase 4
  mixed-responsibility check beyond background-service-with-DB-edges:
  it now triggers on **any** boundary node (inbound or outbound) that
  carries domain conditionals in its body, recommending a Controller
  extraction so the boundary stays thin.

## [0.9.1] — 2026-05-07

### Added
- `examples/write-customer-review/` — end-to-end worked example replaying
  the canonical *Internet Bookstore / Write Customer Review* use case from
  Rosenberg & Stephens (2007), adapted to this kit's templates and the
  C# / ASP.NET Core 9 / EF Core 9 / xUnit + NSubstitute stack. 21 files
  threading one feature through every ICONIX phase:
  - 3 intake artifacts (email, transcript, feature request)
  - 1 requirement (BS-REQ-001)
  - 1 use case (BS-UC-001) with basic + 5 alternate courses
  - 1 domain model (project-wide, continuously updated)
  - 1 UC package overview (Reviews & Ratings package)
  - 1 robustness diagram (BS-RB-001)
  - 1 ADR (BS-ADR-001 — IValidatableObject vs FluentValidation vs service-layer)
  - 1 sequence diagram (BS-SD-001) with full class model
  - 1 test plan + 7 test cases covering all five V-model levels:
    - unit (BS-TC-002 rating, BS-TC-003 review length)
    - system (BS-TC-001 basic course via WebApplicationFactory, BS-TC-004 not-logged-in)
    - integration (BS-TC-007 — Testcontainers SQL Server + Service Bus emulator)
    - acceptance (BS-TC-101 — Reqnroll Gherkin, stakeholder-signed by Doug, Sarah, Linda)
    - regression (BS-TC-021 — supersedes BS-TC-003 after BS-CI-001 lands)
  - 1 change-impact report (BS-CI-001 — adding a title-length rule)
  - 1 project config (`iconix.config.example.yaml`)
- Worked-example `README.md` documents the thread map, file index, and
  traceability chain (`grep -r BS-REQ-001 examples/write-customer-review/`
  recovers the full chain).
- Demonstrates the v0.9.0 UC-package-overview methodology in context, plus
  the test-case template's `Type` field (unit | integration | system |
  acceptance | regression) and `Supersedes TC` field for regression tests.

## [0.9.0] — 2026-05-07

Closes the methodology gaps tracked in `iconix-process-reference.md` as
Ch3 #9 (use cases organised with actors and use case diagrams / packages)
and Ch4 #6 (use cases organised into packages with at least one UC diagram
per package).

### Added
- `templates/use-case-diagram-template.puml` — PlantUML template for the
  per-package UC overview diagram. Actors, package boundary as a labelled
  rectangle, in-package use cases, cross-package use cases shown outside,
  `<<include>>` / `<<extend>>` arrow guidance, and a maintenance reminder
  note
- `use-case-packages/` — new ICONIX folder seeded by both installers; one
  `<package-slug>.puml` file per UC package
- `agents/iconix-product-owner.md` — new section `# Use case packaging rules`
  with five rules covering one-package-per-UC, one-overview-per-package, how
  to draw cross-package invocations, when to update the diagram, and the
  exact-title-match rule
- `agents/iconix-product-owner.md` — three new M1 checklist items: every UC
  belongs to one package and appears on its overview, every overview entry
  has a matching UC file, no dangling cross-package `<<include>>` /
  `<<extend>>` links
- `agents/iconix-traceability.md` — four new validation checks (#10–13):
  orphan UCs (file with no package entry), ghost UCs (overview entry with
  no file), title drift (overview label mismatched against UC heading),
  dangling cross-package links

### Changed
- `iconix-init` and `iconix-init.ps1` — both create `use-case-packages/`
  during folder seeding and copy `use-case-diagram-template.puml` into
  `docs/iconix/templates/`
- `.github/workflows/validate.yml` — smoke test now asserts the new
  template and folder are present after install
- `.gitignore` — adds `/use-case-packages/` so installed projects don't
  ship their UC packages back into the kit
- `agents/iconix-traceability.md` — orphan report scope expanded to cover
  the four new UC-overview check types
- `docs/iconix/iconix-process-reference.md` — Ch3 #9 (UC packages) moved
  ⚠️ → ✅; Ch4 #6 (one UC diagram per package) moved ❌ → ✅; Ch3 coverage
  85% → 90%, Ch4 coverage 70% → 80%; "Closed in v0.9.0" entry added

## [0.8.11] — 2026-05-07

### Added
- `README.md` — `## AI agent patterns` section documenting the four Anthropic
  agent design patterns the kit applies: orchestrator → subagents, prompt
  chaining, parallelization, and evaluator / gate

## [0.8.10] — 2026-05-05

### Changed
- `.github/workflows/validate.yml` — smoke test now asserts all four intake
  templates (`intake-transcript-template.md`, `intake-brd-template.md`,
  `intake-email-template.md`, `intake-feature-request-template.md`) are
  present in `docs/iconix/templates/` after installation

## [0.8.9] — 2026-05-05

### Added
- `templates/intake-transcript-template.md` — structured template for stakeholder
  interviews and meeting notes: metadata, stakeholder profile, current-state narrative,
  pain points, desired future state, scenario walkthrough table (Who/Action/Response),
  what-if-fails probes, NFR seeds, open questions, and analyst summary with candidate
  actors, UC stubs, and REQ stubs
- `templates/intake-brd-template.md` — 13-section Business Requirements Document template:
  executive summary, business objectives, explicit scope (in/out), stakeholders/actors,
  current state, future state, functional requirements table (observable behaviour, no tech
  names), NFR table (5 categories with measurable targets), business rules, assumptions /
  constraints / dependencies, glossary, per-requirement acceptance criteria, and approvals
- `templates/intake-email-template.md` — email/written-request intake template: source
  metadata, verbatim text block, PO restatement layer (stated request, inferred goal
  `[VERIFY]`, inferred actors, scope, NFR seeds, ambiguity questions), candidate artifacts
  section, and Blocked / Ready status
- `templates/intake-feature-request-template.md` — Connextra story + Gherkin acceptance
  criteria template with inline comments mapping Given/When/Then to two-column UC format;
  includes out-of-scope section, NFR notes table (separate from Gherkin), UI/screens,
  INVEST self-check, priority, and linked artifacts
- `agents/iconix-product-owner.md` — `# Intake checklist` section: maps each input type
  to its template, defines six cross-cutting quality checks (named actor, goal vs solution,
  alternate path, quantified constraints, named screens/domain objects, scope boundary),
  enforces `[VERIFY]` for all inferences, and requires multi-UC decomposition before
  drafting any artifacts
- `iconix-init` / `iconix-init.ps1` — both installers updated to copy the four new intake
  templates into `docs/iconix/templates/` during project-scope installation

## [0.8.8] — 2026-05-05

### Changed
- `README.md` — updated to reflect all changes since v0.7.2:
  - Added `iconix-state-machine.puml` to the kit tree listing
  - `/iconix-status` description updated to reflect 6-section output (artifact inventory,
    NFR coverage, test matrix, open CI reports, milestone readiness, next action)
  - Pipeline diagram: Architect now shows "testability seams"; M2 gate notes NFR→ADR
    validation; M3 gate notes test plan existence and completeness check
  - Bug triage section: added note on `reviews/review-checklist.md` accumulation
  - Philosophy footer: corrected "six primary agents" → "ten agents, seven commands"

## [0.8.7] — 2026-05-05

### Added
- `agents/iconix-product-owner.md` — `# When to split a use case` section: five split
  signals (basic course >~6 rows, >~4 alternate courses, alternate courses cover different
  goals, "and" in UC title, unreadable RB), step-by-step split procedure with invoked UC
  reference guidance, and three "do NOT split" counter-examples; rule 3 updated to
  reference the new section

## [0.8.6] — 2026-05-05

### Added
- `agents/iconix-developer.md` — rule 8: show design patterns on the SD as lifelines;
  a pattern hidden in code but absent from SD is flagged as drift (Ch9 #6 ❌→✅)
- `agents/iconix-reviewer.md` — check #2: untyped attributes in class model flagged as
  "attribute untyped" (Ch9 #3 ❌→✅)
- `agents/iconix-tester.md` — ICONIX rules: TCs are authored before code skeletons;
  deferring TC authoring until after implementation defeats design-first intent (Ch12 #7 ❌→⚠️)

### Fixed
- `docs/iconix/iconix-process-reference.md` — Ch4 Eight-steps #8 corrected ⚠️→✅; rule was
  already implemented in v0.6.0 M1 checklist item 8 but matrix was not updated

### Changed
- `docs/iconix/iconix-process-reference.md` — Ch9 60%→80%, Ch12 80%→85%; added "Closed in
  v0.8.6"; last-reviewed bumped to v0.8.6

## [0.8.5] — 2026-05-05

### Added
- `agents/iconix-reviewer.md` — check #6: Framework vs. business logic — flags framework
  concerns mixed into business classes, boilerplate-only methods, and framework trade-offs
  without an ADR (Ch10 #7 ❌→✅, Ch10 #6 ❌→✅); `Framework/business issues` count added
  to review report summary
- `agents/iconix-reviewer.md` — Rules: Reviewer accumulates recurring defect patterns into
  `reviews/review-checklist.md` after each review (Ch11 #6 ❌→✅)
- `agents/iconix-product-owner.md` — rule 8: requirements must describe observable
  behaviour, not implementation technology; REQs naming frameworks/libraries rejected and
  rewritten as constraints (Ch13 #1 ❌→✅)
- `agents/iconix-product-owner.md` — M1 checklist: two new items — domain model abstraction
  coverage (UC nouns with no model counterpart flagged, Ch4 #10 ❌→✅) and domain model
  relationship coverage (isolated entities with real-world relationships flagged, Ch4 #9 ❌→✅)

### Changed
- `docs/iconix/iconix-process-reference.md` — Ch4 50%→70%, Ch10 70%→90%, Ch11 70%→80%,
  Ch13 80%→90%; added "Closed in v0.8.5"; last-reviewed bumped to v0.8.5

## [0.8.4] — 2026-05-05

### Added
- `agents/iconix-analyst.md` — PDR readiness check: two new gate items: data flow
  documentation (Boundary↔Entity paths must have named data in UC text or analysis notes,
  Ch6 #8 ⚠️→✅) and no-detailed-design guard (method signatures/types on RB are a blocker,
  Ch6 #2 ⚠️→✅)
- `agents/iconix-reviewer.md` — check #2 attribute completeness: entity classes with ≥2
  operations and 0 attributes flagged as "attribute-sparse" (Ch9 #7 ⚠️→✅)

### Changed
- `docs/iconix/iconix-process-reference.md` — Ch6 75%→85%, Ch9 55%→60%; added "Closed in
  v0.8.4"; last-reviewed bumped to v0.8.4

## [0.8.3] — 2026-05-05

### Added
- `agents/iconix-developer.md` — rule 6: prefactor on SD before writing code; SD is
  complete when every RB controller has a message and every message has an allocated
  operation (Ch8 #2 ⚠️→✅)
- `agents/iconix-developer.md` — rule 7: don't worry about focus of control; activation
  bars are optional detail; SD purpose is operation allocation (Ch8 #5 ❌→✅)
- `agents/iconix-tester.md` — ICONIX rules expanded: explicit fine-grained unit test rule
  (one controller operation per TC, Ch12 #1 ⚠️→✅) and caller-POV unit test rule (test the
  contract the controller exposes to its caller, Ch12 unit test sub-table ⚠️→✅)
- `templates/req-template.md` — `## Examples` section: optional but encouraged; concrete
  example + counter-example per requirement (Ch13 #2 ❌→✅)

### Changed
- `docs/iconix/iconix-process-reference.md` — Ch8 85%→100%, Ch12 75%→80%, Ch13 70%→80%;
  added "Closed in v0.8.3" section; last-reviewed bumped to v0.8.3

## [0.8.2] — 2026-05-05

### Changed
- `commands/iconix-status.md` — expanded from a 4-line stub to a structured 6-section
  report template: artifact inventory (REQ/UC/RB/SD/CLS/TC/ADR + test plan + open CI
  reports), NFR coverage from `nfr_catalog`, test coverage summary from `test-matrix.md`
  (automated vs manual, UC coverage gaps), open change impact reports with blast-radius
  and pipeline re-run status, milestone readiness (M1/PDR/CDR), and next recommended action

## [0.8.1] — 2026-05-05

### Added
- `agents/iconix-analyst.md` — `# Robustness diagram principles` section with three explicit rules:
  arrow direction is irrelevant (Ch5 #5 ❌→✅); RB is conceptual design only — no method names
  or types (Ch5 #3 ⚠️→✅); controllers are logical functions, not control classes — map to
  messages on SD, not instantiated classes (Ch5 #6 ⚠️→✅)
- `agents/iconix-product-owner.md` — rule 7: noun-verb-noun sentence structure with rewrite
  instruction (Ch3 #3 ⚠️→✅)

### Changed
- `docs/iconix/iconix-process-reference.md` — Ch3 80%→85%, Ch5 75%→100%; added "Closed in
  v0.8.1" section; last-reviewed bumped to v0.8.1

## [0.8.0] — 2026-05-05

### Added
- `agents/iconix-architect.md` — rule 5: time-box architecture work; unresolved decisions
  become `Proposed` ADRs so the pipeline is not blocked (guards against architectural
  paralysis, Ch7 #4)
- `agents/iconix-architect.md` — rule 6: every ADR must cite ≥1 REQ-ID, NFR ID, or UC-ID
  in its Context section; uncited ADRs are flagged (requirement-driven TA validation, Ch7 #5)
- `agents/iconix-architect.md` — `# Testability annotations` section: every container with
  significant business logic must have ≥1 test seam (unit / integration / system) noted in
  the container mapping; no-seam containers flagged as testability risks at M2 gate (Ch7 #3)
- `agents/iconix-architect.md` — PDR readiness checklist expanded with two new items:
  ADR upstream traceability check and container testability seam check

### Changed
- `docs/iconix/iconix-process-reference.md` — Ch7 coverage updated: #3 ⚠️→✅, #4 ❌→✅,
  #5 ❌→✅; summary table Ch7 45%→75%; added "Closed in v0.8.0" section to gap list;
  last-reviewed version bumped to v0.8.0

## [0.7.6] — 2026-05-05

### Changed
- `docs/iconix/iconix-process-reference.md` — coverage matrix updated to v0.7.5:
  - Added `_Last reviewed: v0.7.5_` to summary table
  - Replaced "Priority 2 — Out of kit scope" list with a structured
    "Documented as intentionally out-of-scope in v0.7.2" table (6 items with
    rationale column: UI storyboards, stakeholder reviews, persona analysis,
    effort estimation, code headers, TDD red-green cycle)
  - Added "Added in v0.7.3/v0.7.4/v0.7.5" sections documenting
    `test-plan-template.md`, TC `## Type` field, and state machine diagram

## [0.7.5] — 2026-05-04

### Added
- `iconix-state-machine.puml` — PlantUML state machine diagram of the full ICONIX kit
  workflow: Idle → Requirements (M1 gate) → Preliminary Design (M2 gate) → CDR Phase
  (M3 gate) → Implementation → Done; includes bug triage flow (CDRPhase / Implementation /
  Done → BugTriage → BugFix → BugVerify) and REQ change flow (any active phase →
  REQChange → Requirements); states colour-coded by stereotype: `<<agent>>` blue,
  `<<gate>>` yellow, `<<bug>>` red, `<<change>>` green

## [0.7.4] — 2026-05-04

### Changed
- `templates/test-case-template.md` — added `## Type` field
  (unit | integration | system | acceptance | regression) with inline
  guidance on which traceability fields apply per type: `Robustness
  controller` for unit only; `Sequence diagram` for unit/integration only;
  `Supersedes TC` for regression only; angle-bracket placeholders wrapped
  in backticks for correct VS Code preview rendering
- `agents/iconix-tester.md` — test case template reference now instructs
  agent to set `## Type` and omit non-applicable traceability fields

## [0.7.3] — 2026-05-04

### Added
- `templates/test-plan-template.md` — pre-CDR test plan template with five sections:
  release scope (UC table), TC inventory by type, automation status, coverage status
  (blocker check), and outstanding risks
- `agents/iconix-tester.md` — `# Pre-CDR test plan summary` now references
  `templates/test-plan-template.md` as the authoritative format
- `agents/iconix-tester.md` — `test-plan/test-plan-<date>.md` added to
  `# Artifacts you produce` with downstream consumers noted (Traceability M3 gate, Docs)
- `agents/iconix-docs.md` — `test-plan/test-plan-<date>.md` added to `# Inputs you use`;
  release notes section now includes a test coverage summary from the test plan
- `iconix-init` + `iconix-init.ps1` — both installers now copy `test-plan-template.md`
  to `docs/iconix/templates/`

## [0.7.2] — 2026-05-04

### Added
- `README.md` — `## What the kit intentionally does not cover` section: six
  documented gaps (UI storyboards, stakeholder review meetings, persona analysis,
  effort estimation, code header generation, TDD red-green cycle) each with a
  brief rationale and recommended practice for teams

## [0.7.1] — 2026-05-04

### Added
- `agents/iconix-analyst.md` — `# Invoked use cases on robustness diagrams`: when a UC
  step invokes another UC, drag the invoked UC onto the diagram as a use case node (not a
  plain controller); it connects to the triggering controller following normal connection rules

## [0.7.0] — 2026-05-04

### Added
- `agents/iconix-tester.md` — `# Test types (V-model)` table: maps each test type
  (unit / integration / system / acceptance / regression) to the ICONIX phase that
  triggers it, its primary inputs, and its scope
- `agents/iconix-tester.md` — `# Pre-CDR test plan summary` section: Tester must
  produce `test-plan/test-plan-<date>.md` before the M3 gate, covering release scope,
  TC inventory by type, automation status, coverage status, and outstanding risks
- `agents/iconix-traceability.md` — NFR validation check (#9): every NFR in
  `iconix.config.yaml` `nfr_catalog` must be cited by ≥1 ADR or container-mapping
  annotation; uncovered NFRs are flagged as orphans
- `agents/iconix-traceability.md` — NFR added to the traceability chain diagram
  (`NFR-XXX → ADR-XXX / container-mapping`)
- `agents/iconix-traceability.md` — milestone gate report now includes NFR coverage
  row and test plan existence/completeness check

## [0.6.0] — 2026-05-04

### Added
- `agents/iconix-analyst.md` — `# Domain model rules` section: six explicit constraints
  (real-world objects only, not a data model, domain model = project glossary, only real-world
  relationships, time-box to ~2 hours, domain model will not match final class diagram)
- `agents/iconix-analyst.md` — `# Boundary object naming` rule: every distinct UI screen,
  page, dialog, or API surface must appear as a **named** boundary object; generic labels
  like "web page" are rejected; vague UC text must be rewritten before diagramming

### Changed
- `agents/iconix-product-owner.md` — added rule #6: "shall" statements belong in
  `requirements/REQ-XXX.md`, not in UC text; passive-voice statements found in UC flows
  must be moved to a REQ file and replaced with the active-voice behavior they imply
- `agents/iconix-product-owner.md` — M1 checklist expanded from 5 → 8 items, aligned to the
  book's eight-step Requirements Review: fixed "per course" wording (rule is two paragraphs
  **total**, not per course); added passive-voice/shall check; added abstraction-level check
  (no "the system", "a page", "the data"); added goal-oriented framing check
- `docs/iconix/iconix-process-reference.md` — coverage matrix updated: all five
  "Not fully extracted" placeholder rows filled in (Ch5 #5, Ch6 #1, Ch7 #4/#5, Ch8 #9,
  Ch12 #7); summary table percentages recalculated with consistent formula
  (✅×1 + ⚠️×0.5) ÷ total

## [0.5.3] — 2026-05-04

### Added
- `templates/adr-template.md` — Architecture Decision Record template with Status,
  Context (REQ/NFR/UC refs), Options considered, Decision with rationale, Consequences
  table (positive/negative/risks/follow-ups), and Traceability block

### Changed
- `agents/iconix-architect.md` — replaced inline ADR template block with reference to
  `templates/adr-template.md`; artifact declaration updated to reference the file
- `iconix-init` + `iconix-init.ps1` — both installers now copy `adr-template.md`
  to `docs/iconix/templates/`

## [0.5.2] — 2026-05-04

### Added
- `templates/sequence-template.puml` — PlantUML sequence diagram template with UC step
  text embedded as `group` blocks (basic course + alternate courses shaded `#Pink`)
- `templates/req-template.md` — atomic requirement template with statement, rationale,
  acceptance criteria, priority, and traceability block
- `templates/test-case-template.md` — test case template extracted from Tester agent
  inline format; mirrors UC two-column steps and expected results exactly
- `templates/change-impact-template.md` — CI report template with blast radius tree,
  flat affected artifact table, and recommended dispatch order

### Changed
- `templates/robustness-template.puml` — now embeds full UC scenario text (basic +
  alternate courses) as a numbered comment block at the top of the file
- `agents/iconix-analyst.md` — workflow step 4 now requires UC scenario text to be
  embedded in the RB `.puml` header comment block (references robustness-template.puml)
- `agents/iconix-developer.md` — workflow step 2 now requires each UC step to be wrapped
  in a PlantUML `group` block in the SD `.puml` (references sequence-template.puml)
- `agents/iconix-product-owner.md` — artifact declarations now reference
  `req-template.md` and `use-case-template.md` explicitly
- `agents/iconix-tester.md` — replaced inline test case template block with reference
  to `templates/test-case-template.md`; file template is the authoritative format
- `agents/iconix-traceability.md` — CI report artifact declaration now references
  `templates/change-impact-template.md`
- `iconix-init` + `iconix-init.ps1` — both installers now copy all 7 templates to
  `docs/iconix/templates/` (previously only 3 were copied)

## [0.5.1] — 2026-05-04

### Fixed
- **Product Owner change mode — brand new REQ detection**: when a new REQ has no
  existing UC citations, Traceability's CI report is empty and the change mode previously
  skipped straight to editing with no affected UCs identified. Added Step 0 (check CI
  report content) and Step 1 (manual candidate identification with human confirmation)
  before any UC edits are made. Uncertain candidates are flagged with `[VERIFY]` and
  require explicit user approval before proceeding.

## [0.5.0] — 2026-05-03

### Added
- **Bug flow in Orchestrator**: new `# Bug flow` section routes bug reports through a
  mandatory triage step before dispatching to Developer:
  - Type 1 (implementation bug — code diverges from correct design): Reviewer → Developer
    bug fix mode → Tester bug verification mode; no artifacts change
  - Type 2 (design bug — design is wrong): Reviewer → Traceability impact → full REQ
    change flow
- **Bug triage in Reviewer**: new `# Bug triage` section classifies bugs as Type 1 or
  Type 2 and appends a `## Bug triage` block to the review report with root artifact,
  affected UC, rationale, and recommended next step
- **Bug fix mode in Developer**: new `# Bug fix mode` section — fixes only the code
  identified in the Reviewer's drift-report; explicitly forbids modifying SDs, class
  model, or UCs; re-runs drift detection after fix to confirm the gap is closed
- **Bug verification mode in Tester**: new `# Bug verification mode` section — re-runs
  failing TCs for Type 1 fixes; follows Change mode for Type 2 fixes; includes a
  regression check for UCs sharing classes touched by the fix
- README: documented the bug triage flow with Type 1 / Type 2 decision table and agent
  dispatch diagrams

## [0.4.1] — 2026-05-03

### Fixed
- **Migration idempotency guard**: `iconix-migration` now runs a `# Pre-run idempotency
  check` before any Phase 1 work in both modes, preventing silent overwrites on repeated
  `/iconix-migrate` runs:
  - Detects artifacts already promoted to permanent IDs (via `ids.registry.md`) and skips them
  - Detects DRAFT files modified by humans since the last run and skips them by default
  - Outputs a pre-run summary before proceeding so the user knows exactly what will be (re)generated
  - Aborts cleanly if everything is already promoted or human-edited
  - Two new rules added to `# What you never do` to reinforce the constraints

## [0.4.0] — 2026-05-03

### Added
- **Change mode for artifact-producing agents**: Product Owner, Analyst, and Tester
  each have a new `# Change mode` section. When given a `change-impact/CI-<date>.md`
  report, each agent self-scopes to the blast radius only:
  - Product Owner: updates only the affected UCs and re-runs M1 checklist scoped to those UCs
  - Analyst: updates only the affected RBs in place; updates domain model only if new entities appear
  - Tester: revises only the affected TCs and `test-matrix.md` rows; re-runs coverage gates scoped to changed UCs
- **REQ change flow in Orchestrator**: new `# REQ change flow` section drives the full
  scoped pipeline automatically via `/iconix-next` when a REQ change is detected —
  Traceability → Product Owner → M1 → Analyst → M2 → Developer+Tester (parallel) → M3

### Changed
- Orchestrator passes the CI report path in its dispatch plan so downstream agents
  can self-scope without manual instruction
- README: documented the REQ change flow, plan mode behaviour per agent,
  migration→pipeline handoff, and added a Notation & abbreviations glossary

## [0.3.0] — 2026-04-19

### Added
- **Graphify integration (Phase 1, migration agent only)**: `iconix-migration`
  now runs in graph-assisted mode when `iconix.config.yaml` enables Graphify.
  In graph-assisted mode:
  - Phase 1 (code survey) uses graph queries instead of code walking
  - Phases 2-3 (class model, sequence diagrams) seed from graph nodes/edges
  - Every artifact carries a `## Provenance` footer showing
    EXTRACTED / INFERRED / AMBIGUOUS edge counts
  - Stale graphs (>30 days) block migration; >7 days warns
- `knowledge_graph:` section in `iconix.config.yaml` template
  (disabled by default; portability preserved)
- `/iconix-graphify` slash command — bootstraps Graphify in a project
- `templates/graphify-setup.md` — full setup guide with confidence tuning,
  MCP server config, troubleshooting

### Changed
- `iconix-migration` agent now declares "operating mode" at start of every
  run (graph-assisted | code-walking)
- Orchestrator routing recognizes graph-assisted vs code-walking flow
- Installer copies Graphify setup guide into project templates

### Notes
- Other 9 agents (orchestrator, product-owner, analyst, architect,
  developer, tester, traceability, reviewer, docs) are **unchanged** in this
  release. Phase 2 will extend graph integration to architect/reviewer/
  traceability/docs once Phase 1 is validated in real use.
- This is an additive change. Existing projects on v0.2.0 continue to work
  identically without enabling `knowledge_graph`.

## [0.2.0] — 2026-04-19

### Added
- `iconix-reviewer` agent — detects drift between code and design artifacts
  (sequence diagram, class model, NFRs); produces review reports with
  BLOCK / CHANGES / APPROVE recommendations
- `iconix-docs` agent — generates user guides, developer onboarding, API
  reference, release notes, and SRE runbooks from ICONIX artifacts
- `iconix-migration` agent — reverse-engineers draft ICONIX artifacts from
  existing legacy codebases in a 7-phase workflow
- `/iconix-review`, `/iconix-docs`, `/iconix-migrate` slash commands
- PowerShell installer (`iconix-init.ps1`) for Windows users
- GitHub Actions validation workflow
- `CONTRIBUTING.md`, `LICENSE` (MIT), `CHANGELOG.md`

### Changed
- Orchestrator routing heuristics extended to cover review, docs, and
  migration flows
- Installer success message now lists all 10 agents and 6 commands

## [0.1.0] — 2026-04-19

### Added
- Initial kit with 7 agents: orchestrator, product-owner, analyst, architect,
  developer, tester, traceability
- 3 slash commands: `/iconix-next`, `/iconix-status`, `/iconix-impact`
- Bash installer (`iconix-init`) with project-scope and user-scope modes
- `iconix.config.yaml` template with prefix, stack, containers, NFRs
- Use case and robustness diagram templates
- README with install recipe and portability matrix
