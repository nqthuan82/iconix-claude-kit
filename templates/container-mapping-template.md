# Container Mapping — `<PREFIX>-UC-XXX`

> Per-UC architectural mapping. Produced by the Architect agent at M2.
> Read by the Reviewer at Implementation PRs (`iconix-reviewer.md` check #5)
> to verify code lives in the right container and that NFRs are honored.
>
> Save as `container-mapping/<PREFIX>-UC-XXX-containers.md` (one file per UC).

## Use case
- **ID:** `<PREFIX>-UC-XXX`
- **Title:** `<UC title>`
- **Robustness diagram:** `<PREFIX>-RB-XXX`

## Containers traversed

> One row per container this UC's flow touches. List the containers from
> `iconix.config.yaml` `architecture.containers`. The "Role" column says
> what this container *does* in this UC's flow (boundary, processor,
> persistence, external integration, etc.).
>
> **Derive container rows from the robustness diagram** using the classification
> table in `iconix-architect.md` `# Controller-to-container classification`.
> Fill "Source RB nodes" with the RB element names (Controller / Boundary / Entity)
> that drove each row — this is the traceability link from RB to container mapping.
>
> **Effective stack** — resolve per container:
> container-level `stack.language` / `stack.test_framework` from `iconix.config.yaml`
> if present; otherwise the top-level `stack.*` values. The Developer and Tester agents
> read this column — fill it in so they don't have to re-derive it.

| Container | Effective stack | Role in this UC | What this UC does here | Source RB nodes | Testability seam |
|---|---|---|---|---|---|
| `<Container1>` | csharp / xunit | Boundary | Receives HTTP request; binds form data; redirects on validation failure | `Submit Review Form` (Inbound Boundary) | **System seam:** HTTP POST endpoint usable in WebApplicationFactory tests |
| `<Container2>` | csharp / xunit | Application Service | Validates input; orchestrates entity creation and persistence | `Validate Review`, `Save Review` (Controllers) | **Unit seam:** service class with repository interface injected; no I/O in unit tests |
| `<Container3>` | csharp / xunit | Domain | Constructs and validates the entity per business invariants | `Review` (Entity) | **Unit seam:** entity class instance + domain validation logic |
| `<Container4>` | csharp / xunit | Persistence | Saves entity to repository; enqueues for downstream | `ReviewRepository` (Outbound Boundary) | **Integration seam:** repository interface mockable in service-layer tests |

> **Testability seam values** — pick one per row:
> - **System seam** — HTTP/CLI/queue surface exercisable end-to-end
> - **Integration seam** — interface boundary that test doubles can replace
> - **Unit seam** — class with no I/O, exercisable in pure unit tests
> - **(out of scope — covered via `<upstream-container>`'s seam)** — for containers without business logic that another container abstracts (e.g., a database accessed only through a repository). Don't invent a fake seam; don't leave the column blank.
>
> **Source RB nodes** — list the names of the RB elements (Boundary / Controller / Entity)
> whose classification (per `iconix-architect.md` `# Controller-to-container classification`)
> drove this container row. Two Controllers that map to the same container share one row;
> list both names separated by a comma.

## NFRs applicable

> List NFR IDs from `nfr-catalog.md`. Detailed targets and enforcement live
> in `nfr-annotations/<PREFIX>-UC-XXX-nfr.md` (companion file).

- `<PREFIX>-NFR-XXX` — `<one-line summary, e.g., performance <2s p95>`
- `<PREFIX>-NFR-YYY` — `<one-line summary>`

## Cross-cutting concerns

> Per Architect decision rule 3: enumerate cross-cutting concerns; do NOT
> re-invent them per UC.

- **Auth:** `<which container enforces; reference to existing auth flow>`
- **Logging / observability:** `<container; what's logged at boundary, controller, entity layers>`
- **Audit:** `<which writes are auditable; reference compliance NFR if relevant>`
- **Licensing / regulatory:** `<jurisdictional constraints if any>`

## Open architectural questions

> Per Architect decision rule 5: time-box. Unresolved questions get a Proposed
> ADR; do NOT block M2 promotion waiting for a perfect answer.
>
> **Standard format** (mechanically grep-able by Traceability):
> `<question statement>. [Proposed ADR-XXX]`
>
> Every entry MUST end with a `[Proposed ADR-XXX]` reference, OR be omitted.
> If you have an open question without a Proposed ADR, draft a `Proposed`
> ADR shell first (status + context only — decision deferred); then reference
> it here. Entries without `[Proposed ADR-XXX]` are M2 PDR blockers.
>
> Use `(none)` if no open questions remain.

- (none)
<!-- Example with open question:
- Should review attachments be stored inline or via blob storage? [Proposed ADR-007]
-->


## Container-name testability check

- [ ] Every container with significant business logic has ≥1 testability seam noted above
- [ ] Containers flagged as testability risks are listed in the M2 milestone report

## Traceability
- **UC:** `<PREFIX>-UC-XXX`
- **RB:** `<PREFIX>-RB-XXX`
- **NFR annotations:** `<PREFIX>-UC-XXX-nfr.md` (companion file)
- **ADRs:** `<list of ADRs that drove decisions affecting this UC, or "(none)">`
- **Architecture canonical doc:** `<docs/architecture/system-architecture.md or as configured>`
