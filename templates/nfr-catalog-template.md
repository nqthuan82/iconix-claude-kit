# NFR Catalog — `<Project name>`

> Project-wide non-functional-requirements catalog. Single source of truth.
>
> Each NFR has a stable ID (`<PREFIX>-NFR-NNN`), a category, an observable
> measurable target, and a list of UCs it applies to. New NFRs are added
> here first; UCs reference them by ID via
> `nfr-annotations/<PREFIX>-UC-XXX-nfr.md`.
>
> Save at the path configured in `iconix.config.yaml` `nfr_catalog`
> (default: `docs/nfr-catalog.md`).

## Categories used in this project

> Categorise each NFR using one of the labels below. Add a new category
> only if a stakeholder or regulation forces it — do not invent.

- **Performance** — latency, throughput, response time
- **Scalability** — concurrent users, transaction rate, growth ceilings
- **Availability** — uptime, recovery time, SLO targets
- **Security** — authentication, authorization, encryption, secrets
- **Compliance** — regulatory, data-residency, retention, audit-trail
- **Maintainability** — testability, observability, code-quality targets
- **Usability** — accessibility, localisation, response-feedback (UI-side)

## NFRs

### `<PREFIX>-NFR-001` — `<one-line title>`
- **Category:** `<one of the categories above>`
- **Statement:** `<observable, measurable target. NO implementation specifics. Example: "Customer Review submissions return a Confirmation page within 2 seconds at the 95th percentile">`
- **Source:** `<stakeholder name + date | regulation reference | business need>`
- **Defined by:** `<role that owns the target — typically Product Owner for compliance / business NFRs, Architect for technical NFRs>`
- **Enforced by:** `<role that owns the architectural enforcement — typically Architect; same as "Defined by" when there's no split>`
- **Applies to UCs:** `<comma-separated UC-IDs, or "all" for cross-cutting>`
- **Covering ADR:** `<ADR-XXX when an architectural decision exists for this NFR, or "(none)">`

### `<PREFIX>-NFR-002` — `<one-line title>`
- **Category:** `<...>`
- **Statement:** `<...>`
- **Source:** `<...>`
- **Owner:** `<...>`
- **Applies to UCs:** `<...>`
- **Covering ADR:** `<...>`

<!-- Add as many NFR sections as needed, one per requirement. -->

## Quality checks (for the Architect at M2)

- [ ] Every NFR has a measurable target (no "fast", "secure", "always available" without numbers / assertions)
- [ ] Every NFR is cited by ≥1 ADR or container-mapping annotation, or marked `(none — out of scope at M2)`. Traceability check #9 enforces this at the M2 gate.
- [ ] Every UC's `nfr-annotations/<PREFIX>-UC-XXX-nfr.md` references only NFR IDs that exist here

## Traceability
- **Read by:** Architect agent (input), Traceability agent (M2 gate check #9), Reviewer (NFR compliance check #5)
- **Configured path:** `iconix.config.yaml` `nfr_catalog`
