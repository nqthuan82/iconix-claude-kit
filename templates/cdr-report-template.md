# CDR Readiness — `<PREFIX>-UC-XXX` — `<YYYY-MM-DD>`

> Critical Design Review readiness report. Produced by the Developer at M3
> after the SD is stable (per Developer rule 6) and code skeletons are
> generated. One file per UC; save as `cdr-report-<PREFIX>-UC-XXX-<date>.md`.
>
> Read by:
> - Traceability agent at the M3 gate (per check sequence in
>   `iconix-traceability.md` Validation checks)
> - Tester at M3 to confirm test plan coverage matches the SD
> - Reviewer at Phase 9 PRs to verify the SD is what the code implements
>
> The Tester runs in parallel with the Developer at M3; this report's
> existence does NOT block the Tester. It blocks promotion to
> Implementation.

## Use case
- **ID:** `<PREFIX>-UC-XXX`
- **Title:** `<UC title>`
- **Robustness diagram:** `<PREFIX>-RB-XXX`
- **Sequence diagram:** `<PREFIX>-SD-XXX`
- **Class model:** `class-model/class-model.puml`

## SD coverage of RB controllers

> Per Developer rule 2: every RB controller becomes ≥1 message on the SD.
> One row per RB controller; cite the SD `group` block + message that
> realizes it.

| RB controller | SD group block | Message(s) | Allocated to class |
|---|---|---|---|
| `<Check login state>` | Step 1 | `Ctrl -> CS : IsLoggedIn` | `CustomerSession.IsLoggedIn` |
| `<Validate review length>` | Step 3 | `MVC -> CR : DataAnnotations` | `CustomerReview` (StringLength attr) |
| ... | ... | ... | ... |

## Lifelines introduced beyond the domain model

> Per Developer rule 4: domain classes from `domain-model.puml` are first-
> class. Architectural / DI interfaces (e.g., ICurrentUserService) require
> a one-sentence justification here.

| Lifeline | Why introduced (cite container-mapping or ADR) |
|---|---|
| `<ICurrentUserService>` | Container-mapping `Bookstore.Application` row — abstracts cookie auth from controllers |
| `<IBookRepository>` | Container-mapping `Bookstore.Infrastructure` row — repository pattern, BS-ADR-XXX |
| ... | ... |

## SD-rendering rules (per agent guidance)

> Mirror checks for the v0.9.19 SD-rendering rules. Each item must be
> satisfied or have a documented exception.

- [ ] **Invokes (UC calls):** every entry in the source UC's `Invokes (UC calls):` field renders on the SD as a synthetic boundary lifeline + explanatory note (or a `note over` block when the framework hides the invocation entirely)
- [ ] **UI dependencies:** every entry in `UI dependencies:` renders with `<<from PREFIX-UC-XXX Title>>` stereotype on the boundary lifeline
- [ ] **Downstream consumers:** every entry in `Downstream consumers:` appears as a lifeline at the diagram's right edge with a dashed `..>` message from the producing entity
- [ ] **Framework-helper lifelines:** non-trivial framework infrastructure (model binders, auto-validation) appears as a `control` lifeline; trivial infrastructure (DI resolution, routing) is omitted

## Behavior allocation summary

> One bullet per non-obvious allocation. If you used the cross-cutting-
> concerns override (Developer behavior allocation rule), list the
> override here so the Reviewer doesn't flag it as drift from the
> information-expert default.

- `<Auth check (IsLoggedIn / [Authorize])>` → `Bookstore.Web` (cross-cutting per container-mapping; data lives in `CustomerSession` but mechanism is controller attribute)
- `<...>`

## Code skeleton paths

> Per the new "Code skeleton paths align with the architecture package map"
> rule. List the source files this UC introduces; each path's first
> directory must match a row in `docs/architecture/package-map.md`.

| Source file | Package map row |
|---|---|
| `src/Bookstore.Web/Controllers/WriteCustomerReviewController.cs` | `Bookstore.Web` |
| `src/Bookstore.Domain/CustomerReview.cs` | `Bookstore.Domain` |
| ... | ... |

## CDR readiness checklist

> The full checklist from the Developer agent's `# CDR readiness check`.
> Must be 100% before M3 promotion.

- [ ] One sequence diagram for this UC
- [ ] Every robustness controller appears as ≥1 message on the SD
- [ ] Every SD lifeline introduced beyond the domain model has a justification (table above)
- [ ] All four SD-rendering rules satisfied (table above)
- [ ] `class-model/class-model.puml` exists; lists every class the SD references with attributes + operations
- [ ] No untyped attributes in the class model (Reviewer check #2)
- [ ] No attribute-sparse entities (Reviewer check #2)
- [ ] Code skeleton paths align with `docs/architecture/package-map.md`
- [ ] Code skeletons compile / lint cleanly
- [ ] Unit test stubs exist for every basic-course step + every alternate course + every RB controller
- [ ] Traceability comments present in every source file
- [ ] M2 PDR readiness was passed (prerequisite — confirm `milestone-reports/M2-<date>.md` exists with `Recommendation: READY`)

## Open questions for Tester

> Things the Tester should know before drafting TCs at M3. Do NOT block
> on these — Tester runs in parallel with you. List for awareness.

- `<e.g., "framework-helper lifeline 'MVC ModelBinder' is non-trivial; ensure TC-XXX exercises DataAnnotations failure path">`
- `<...>`

## Traceability
- Drives: `test-cases/<PREFIX>-TC-*.md` (Tester reads this report at M3 to align coverage)
- Read by: Traceability agent (M3 gate); Reviewer (Phase 9 PRs)
- Companion: `class-model/class-model.puml`, `sequence/<PREFIX>-SD-XXX-<slug>.puml`
