# Architecture Package Map — `<Project name>`

> Code/deployment-level package decomposition. Produced by the Architect at M2.
>
> **NOT to be confused with `use-case-packages/`** (PO-owned: UC groupings for
> readability of the requirements catalog). This file documents *code*
> packages — assemblies, modules, microservices, deployable units.
>
> Save at `docs/architecture/package-map.md`.

## Package list

> One row per code package. The "Layer" column distinguishes the architectural
> tier. Use **`Infrastructure (external)`** for containers owned by another team
> or external infrastructure (queues, identity providers, payment processors,
> third-party APIs) that appear in `iconix.config.yaml` `architecture.containers`
> but are **not implemented by this codebase**. External packages are exempt
> from the cross-package rules below — they're contracts, not source.

> **Effective stack** — resolve per package: container-level `stack.language` / `stack.test_framework`
> from `iconix.config.yaml` if present; otherwise the top-level `stack.*` values. Format: `<language> / <test_framework>`.
> Infrastructure (external) packages may use `n/a`. Must match the "Effective stack" column in every
> `container-mapping/*` file that references this package.

| Package name | Effective stack | Responsibility | Layer | Owns | Allowed dependencies | Bounded Context reasoning |
|---|---|---|---|---|---|---|
| `<Web>` | csharp / xunit | HTTP entry point | Boundary | Controllers, model binding, view rendering | `<Domain>`, `<Application>` (no `<Infrastructure>`) | Delivery mechanism only — no domain logic; no BC boundary question applies. |
| `<Application>` | csharp / xunit | Use-case orchestration | Application service | Command handlers, DTOs, application-level interfaces | `<Domain>`, `<Infrastructure>` (via interfaces) | Orchestrates UCs within a single BC; if UCs from multiple BCs land here, split. |
| `<Domain>` | csharp / xunit | Business logic | Entity / domain | Entities, value objects, domain services, validation | (none — domain is dependency-free) | Core domain of `<BC name>`. "Order" means the same to all actors in scope — no linguistic split detected. Deploys independently. Owns the primary business invariants. |
| `<Infrastructure>` | csharp / xunit | External integrations | Persistence / I/O | Repositories, external service clients, file/queue adapters | `<Domain>` (implements its interfaces) | Infrastructure (external) — BC boundary question not applicable. |
| `<PendingReviewsQueue>` | n/a | Async-output queue used by Moderate Customer Reviews | **Infrastructure (external)** | (owned by INFRA-88; this codebase publishes only) | n/a — not implemented here; cross-package rules don't apply | Infrastructure (external) — BC boundary question not applicable. |

## Cross-package rules

> Architectural invariants. Violation should fail the build (architecture tests).

- `<Domain>` has zero outbound dependencies (excluding the language runtime / BCL).
- `<Web>` does not directly reference `<Infrastructure>`; goes through `<Application>` interfaces.
- `<other invariant>` …

## UC → package allocation

> One row per UC, showing which packages each UC's flow traverses. Cross-references
> with `container-mapping/<PREFIX>-UC-XXX-containers.md` per-UC files.

| UC | Boundary package | Application package | Domain package | Persistence package |
|---|---|---|---|---|
| `<PREFIX>-UC-001` | `<Web>` | `<Application>` | `<Domain>` | `<Infrastructure>` |
| `<PREFIX>-UC-002` | … | … | … | … |

## Quality checks (for the Architect at M2)

- [ ] Every UC appears in the UC→package allocation table above
- [ ] Cross-package rules above are enforceable (e.g., NetArchTest, ArchUnit, dependency-cruiser, or equivalent for the stack)
- [ ] Architecture-test fixture exists in `tests/Architecture` (or stack-equivalent) that fails the build on rule violation
- [ ] Each package's responsibility is one-sentence-describable; multi-clause descriptions are a smell
- [ ] Every container in `iconix.config.yaml` `architecture.containers` appears here as an internal package OR as `Infrastructure (external)` with the owning team / system referenced
- [ ] Every internal package row has a non-empty "Effective stack" column; derive from `iconix.config.yaml` (container-level `stack.*` → global `stack.*` fallback); must be consistent with the "Effective stack" column in every `container-mapping/*` file that references this package
- [ ] `Infrastructure (external)` packages are explicitly excluded from architecture-test rules (otherwise the build fails because the package has no source)
- [ ] Every internal package row has a non-empty "Bounded Context reasoning" column (per `iconix-architect.md` `# Bounded Context reasoning`); an empty cell means the boundary was not consciously evaluated

## Traceability
- **Drives:** `container-mapping/<PREFIX>-UC-XXX-containers.md` (per-UC; should be consistent with the allocation table above)
- **ADRs related:** `<list of ADRs that established or changed package structure>`
- **Architecture canonical doc:** `<docs/architecture/system-architecture.md or as configured>`
