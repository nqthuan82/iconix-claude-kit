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

| Container | Role in this UC | What this UC does here | Testability seam |
|---|---|---|---|
| `<Container1>` | Boundary | Receives HTTP request; binds form data; redirects on validation failure | **System seam:** HTTP POST endpoint usable in WebApplicationFactory tests |
| `<Container2>` | Domain entity + validation | Constructs and validates the entity per its DataAnnotations + IValidatableObject | **Unit seam:** entity class instance + Validator.TryValidateObject |
| `<Container3>` | Persistence | Saves entity to repository; enqueues for downstream | **Integration seam:** repository interface mockable in service-layer tests |

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
> ADR; do NOT block M2 promotion waiting for a perfect answer. List them here
> with `[Proposed ADR-XXX]` references when an ADR has been drafted.

- (none) | `<question + ADR ref if drafted>`

## Container-name testability check

- [ ] Every container with significant business logic has ≥1 testability seam noted above
- [ ] Containers flagged as testability risks are listed in the M2 milestone report

## Traceability
- **UC:** `<PREFIX>-UC-XXX`
- **RB:** `<PREFIX>-RB-XXX`
- **NFR annotations:** `<PREFIX>-UC-XXX-nfr.md` (companion file)
- **ADRs:** `<list of ADRs that drove decisions affecting this UC, or "(none)">`
- **Architecture canonical doc:** `<docs/architecture/system-architecture.md or as configured>`
