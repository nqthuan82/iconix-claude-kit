# Integration Surface — `<Project name>`

> All external touchpoints (APIs, message queues, file drops, third-party SDKs)
> the system communicates with. Produced by the Architect at M2.
>
> Save at `docs/architecture/integration-surface.md`.
>
> Read by:
> - Architect: when a new UC needs an integration, check whether the touchpoint
>   is already documented before adding a new one
> - Tester: at M3, integration-level test cases derive from inbound + outbound rows
> - Reviewer: at Implementation PRs, verifies that new integration code matches a
>   row here (or that a new row is added in the same PR)

## Inbound integrations (system receives data)

> One row per surface where external traffic *enters* the system. Each gets
> its own NFRs (typically performance, throughput, auth) and failure modes.

| Touchpoint | Protocol | Trigger | Used by UC | NFRs | Auth | Rate limits |
|---|---|---|---|---|---|---|
| `<endpoint, e.g., POST /api/reviews>` | `<HTTPS / gRPC / WebSocket / SOAP>` | `<who/what calls this and when>` | `<UC-XXX>` | `<NFR-XXX, NFR-YYY>` | `<auth scheme>` | `<rate limit if any>` |
| … | … | … | … | … | … | … |

## Outbound integrations (system sends data)

> One row per surface where this system *initiates* external communication.

| Touchpoint | Protocol | Reason | Triggered by UC | NFRs | Auth | Failure handling |
|---|---|---|---|---|---|---|
| `<system / endpoint, e.g., Pending Reviews Queue>` | `<AMQP / HTTPS / SDK>` | `<why this system calls out, e.g., "submitted review enqueued for moderation">` | `<UC-XXX>` | `<NFR-XXX>` | `<auth scheme, e.g., "managed identity">` | `<retry / dead-letter / circuit-breaker>` |

## Bidirectional integrations

> Surfaces where the system both sends and receives — e.g., webhooks where we
> register an endpoint and a third-party calls back. Document both directions.

| Touchpoint | Direction-out | Direction-in | UCs | Notes |
|---|---|---|---|---|
| … | … | … | … | … |

## Per-touchpoint failure modes

> For each integration above, document what happens when it's unavailable,
> slow, or returns errors. Drives circuit-breaker / fallback ADRs.

### `<touchpoint name>`
- **When unavailable:** `<system response, e.g., return 503 with retry-after, or queue locally>`
- **When slow:** `<timeout policy, fallback>`
- **When wrong:** `<validation, error logging, user-facing message>`
- **Owning ADR:** `<ADR-XXX if a decision exists, or "(none)">`

## Quality checks (for the Architect at M2)

- [ ] Every UC's flow that touches an external system has at least one row here
- [ ] Every row cites the UC IDs it serves (no orphan touchpoints — Reviewer flags these)
- [ ] Every inbound endpoint has an explicit auth row (no "unauthenticated" without an ADR)
- [ ] Per-touchpoint failure modes documented (or marked `(deferred — ADR-XXX proposed)`)

## Traceability
- **Drives:** test cases in `test-cases/` (integration-level), Reviewer's framework-vs-business check at Implementation PRs
- **ADRs related:** `<list of ADRs that established or changed integration patterns>`
- **NFRs:** `<NFR IDs related to integration, e.g., availability, latency-of-downstream>`
