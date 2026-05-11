# System Architecture — `<Project name>`

> Canonical architecture reference for this project. The Architect agent reads
> this file as context when mapping use cases to containers, raising ADRs, and
> annotating NFRs.
>
> This is a **C4-flavoured** document (Context → Containers → Integration). You
> do not need to be rigorous about C4 — fill in what you know; the Architect
> agent will flag gaps it needs.
>
> Save at the path configured in `iconix.config.yaml` `architecture.canonical_doc`
> (default: `docs/architecture/system-architecture.md`).
>
> Point `canonical_doc` at this file even if it is incomplete — a partial
> picture is more useful to the agent than no file at all.

---

## 1. Context (C4 Level 1)

> One paragraph. Who uses the system, what it does at the highest level, and
> what external systems it depends on. No implementation detail here.

`<Project name>` provides `<one-sentence purpose>` for `<primary user roles>`.
It integrates with `<list key external systems>`.

---

## 2. Containers (C4 Level 2)

> One row per deployable/independently runnable unit. Must match the names in
> `iconix.config.yaml` `architecture.containers` — keep them in sync.
>
> **Layer** values: `Frontend` | `API` | `Backend` | `Worker` | `Database` |
> `Cache` | `Queue` | `External` | `Mobile` | `CLI`

| Container | Layer | Technology | Responsibility | Data stores owned |
|---|---|---|---|---|
| `<Backend>` | `Backend` | `<e.g., ASP.NET Core 9>` | `<Business logic, API endpoints>` | `<e.g., PostgreSQL — GameDB>` |
| `<WebAPI>` | `API` | `<e.g., FastAPI 0.110>` | `<REST/gRPC façade, auth, rate limiting>` | `(none — delegates to Backend)` |
| `<Frontend>` | `Frontend` | `<e.g., React 18, TypeScript>` | `<Player-facing UI, session state>` | `(none — stateless)` |
| `<Database>` | `Database` | `<e.g., PostgreSQL 16>` | `<Persistent storage>` | `<Tables / schemas owned>` |

<!-- Add or remove rows. Remove the example rows and replace with your own. -->

---

## 3. Container interactions

> Which containers talk to which, over what protocol, and in which direction.
> One row per interaction. Gaps here become the Integration Surface (produced
> by the Architect at M2 — see `templates/integration-surface-template.md`).

| From | To | Protocol | Direction | Notes |
|---|---|---|---|---|
| `<Frontend>` | `<WebAPI>` | `HTTPS / REST` | → | JWT bearer auth |
| `<WebAPI>` | `<Backend>` | `gRPC` | → | Internal only, mTLS |
| `<Backend>` | `<Database>` | `TCP / SQL` | ↔ | Connection pool, 10 max |

---

## 4. External systems

> Systems outside this codebase that containers depend on or are depended upon by.

| External system | Direction | Owning team / vendor | Protocol | Failure mode |
|---|---|---|---|---|
| `<Identity Provider>` | Inbound auth | `<e.g., Azure AD>` | OIDC | Fallback: cached token; hard fail after TTL |
| `<Payment Gateway>` | Outbound | `<Vendor>` | REST/HTTPS | Retry ×3, then error page |

---

## 5. Architectural constraints

> Hard rules the Architect agent must enforce when mapping UCs. If a UC
> violates one of these, the agent must raise an ADR rather than silently
> proceeding.

- All authentication and authorisation flows through `<Identity Provider>` — no container implements its own auth.
- `<Frontend>` never calls `<Backend>` directly; it always goes via `<WebAPI>`.
- `<Database>` is owned exclusively by `<Backend>`; no other container holds a connection string.
- `<add further constraints as needed>`

---

## 6. Scalability and deployment notes

> Enough context for the Architect to judge whether a UC's design fits the
> operational model. Full detail belongs in the NFR catalog.

- Deployment target: `<e.g., Kubernetes on AKS | single VM | serverless>`
- Horizontal scaling: `<which containers scale out, which are singletons>`
- State: `<which containers are stateless; which hold session/local state>`
- Significant traffic patterns: `<e.g., peak concurrent users, batch windows>`

---

## 7. Open architectural questions

> Unresolved decisions that the Architect agent should track. When a decision
> is made, move it to an ADR in `adrs/` and remove it from here.

- [ ] `<Question 1 — e.g., "Should real-time game events use WebSockets or SSE?">`
- [ ] `<Question 2>`

---

## C4 Level 3 — Components
Component-level decomposition (what's inside each container) is documented separately in
`docs/architecture/package-map.md`, produced by the Architect agent at M2 (or drafted by
the Migration agent when retrofitting ICONIX onto existing code).

---

## Traceability
- **Read by:** Architect agent (input for M2 — container mapping, ADRs, integration surface)
- **Kept in sync with:** `iconix.config.yaml` `architecture.containers` (container names must match)
- **Downstream artifacts:** `docs/architecture/package-map.md`, `docs/architecture/integration-surface.md`, `container-mapping/<PREFIX>-UC-XXX-containers.md`
- **Configured path:** `iconix.config.yaml` `architecture.canonical_doc`
