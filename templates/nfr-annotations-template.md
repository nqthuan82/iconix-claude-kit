# NFR Annotations — `<PREFIX>-UC-XXX`

> Per-UC non-functional-requirement enforcement. Produced by the Architect at M2.
> Read by the Reviewer at Implementation PRs (`iconix-reviewer.md` check #5 — "NFR compliance hints")
> and by the Tester at M3 to ensure NFR-relevant tests exist.
>
> Save as `nfr-annotations/<PREFIX>-UC-XXX-nfr.md` (one file per UC).

## Use case
- **ID:** `<PREFIX>-UC-XXX`
- **Title:** `<UC title>`
- **Container mapping:** `<PREFIX>-UC-XXX-containers.md`

## Applied NFRs

> One row per NFR that meaningfully applies to this UC. NFR IDs come from
> the project NFR catalog at `docs/nfr-catalog.md` (or as configured). Do
> NOT introduce new NFR IDs here — add them to the catalog first.

| NFR ID | Category | Target | Where enforced (container + class) | Reviewer-checkable signal |
|---|---|---|---|---|
| `<PREFIX>-NFR-001` | Performance | `<measurable, e.g., <2s p95 from request to response>` | `<Container.Class>` (e.g., `Bookstore.Web.RequestTimerMiddleware`) | `<observable signal, e.g., HTTP response time logged per request; assertion in integration test>` |
| `<PREFIX>-NFR-002` | Compliance | `<measurable, e.g., 100% of submissions enter pending state>` | `<Container.Class>` | `<observable signal>` |

## Out-of-scope NFRs

> Catalog NFRs that the Architect determined don't apply to this UC.
> Whether out-of-scope is the common case or the rare case depends on
> the project's NFR-catalog size:
>
> - **Small catalog (≤5 NFRs):** most NFRs typically apply to most UCs;
>   `(none)` is a common answer here.
> - **Large catalog (regulatory / security suites — 20+ NFRs):** explicit
>   out-of-scope is the common case; document each non-applicable NFR.
>
> The rule (in either size): if an NFR is in the catalog but not applied
> to this UC, list it here with a one-line reason. Silent omission of an
> applicable NFR is a smell; explicit out-of-scope is fine.

- `<PREFIX>-NFR-XXX` — `<reason this NFR was excluded for this UC>`
- (or `(none)` when all catalog NFRs apply)

## Test-design hints for the Tester

> Per NFR, what kind of test exercises it? The Tester at M3 reads this to
> decide which test types (unit / integration / system / regression) cover
> which NFRs.

| NFR | Test type that exercises it | Suggested TC scope |
|---|---|---|
| `<PREFIX>-NFR-001` | System (timed) | TC asserts response time below target across N samples |
| `<PREFIX>-NFR-002` | Integration | TC asserts post-submit state transition |

## Traceability
- **UC:** `<PREFIX>-UC-XXX`
- **NFR catalog:** `docs/nfr-catalog.md`
- **Container mapping:** `<PREFIX>-UC-XXX-containers.md`
- **Driving ADRs:** `<list ADRs that decided how each NFR is enforced, or "(none)">`
