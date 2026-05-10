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
> tier (boundary / domain / persistence / cross-cutting / external-integration).

| Package name | Responsibility | Layer | Owns | Allowed dependencies |
|---|---|---|---|---|
| `<Web>` | HTTP entry point | Boundary | Controllers, model binding, view rendering | `<Domain>`, `<Application>` (no `<Infrastructure>`) |
| `<Application>` | Use-case orchestration | Application service | Command handlers, DTOs, application-level interfaces | `<Domain>`, `<Infrastructure>` (via interfaces) |
| `<Domain>` | Business logic | Entity / domain | Entities, value objects, domain services, validation | (none — domain is dependency-free) |
| `<Infrastructure>` | External integrations | Persistence / I/O | Repositories, external service clients, file/queue adapters | `<Domain>` (implements its interfaces) |

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

## Traceability
- **Drives:** `container-mapping/<PREFIX>-UC-XXX-containers.md` (per-UC; should be consistent with the allocation table above)
- **ADRs related:** `<list of ADRs that established or changed package structure>`
- **Architecture canonical doc:** `<docs/architecture/system-architecture.md or as configured>`
