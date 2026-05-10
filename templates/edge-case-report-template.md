# Edge Case Report — `<PREFIX>-UC-XXX`

> Per-UC edge-case enumeration. Produced by the Tester at M3 alongside
> the per-course TCs. Each row maps to ≥1 TC OR a documented waiver.
>
> Save as `edge-case-reports/<PREFIX>-UC-XXX-edge-cases.md` (one file
> per UC).
>
> Read by:
> - Reviewer at Phase 9 PRs to confirm edge-case coverage isn't gapped
> - Architect at M2 to validate that NFRs cover the edge cases (e.g.,
>   resource-exhaustion edge cases need a corresponding latency / quota NFR)
> - Tester at the M3 coverage gate (per `# Coverage gates (run before
>   release)` rule: "Edge case families covered or explicitly waived")

## Use case
- **ID:** `<PREFIX>-UC-XXX`
- **Title:** `<UC title>`
- **Test plan:** `test-plan/test-plan-<date>.md`

## Edge case families (per Tester agent `# Edge case generation rules`)

> One row per family. **Either** name a covering TC **or** mark explicitly
> waived with a one-sentence reason. Silent omission is a coverage gap.

### 1. Boundary values

> Min/max for every numeric or length-bounded input.

| Input | Min | Max | Covered by |
|---|---|---|---|
| `<e.g., Book Review length>` | `<10 chars>` | `<1,000,000 chars>` | `<TC-XXX (boundary at min); TC-YYY (boundary at max)>` |
| `<e.g., Book Rating>` | `<1>` | `<5>` | `<TC-XXX>` |

### 2. Invalid input

> Wrong format, missing required field, type mismatch.

| Input | Invalid case | Expected | Covered by |
|---|---|---|---|
| `<e.g., Book Rating>` | `<non-integer>` | `<reject with 400>` | `<TC-XXX>` |
| `<e.g., Book Review>` | `<empty / whitespace-only>` | `<reject with min-length error>` | `<TC-XXX>` |

### 3. Authorization

> Unauthenticated, wrong role, expired session.

| Scenario | Expected | Covered by |
|---|---|---|
| `<unauthenticated submit>` | `<redirect to Login>` | `<TC-XXX>` |
| `<expired session>` | `<re-auth challenge>` | `<TC-XXX or "(waived — covered by upstream auth UC)">` |

### 4. Concurrency

> Simultaneous actions, double-submission, race conditions.

| Scenario | Expected | Covered by |
|---|---|---|
| `<double-submit (user clicks Send twice fast)>` | `<one queue entry, not two>` | `<TC-XXX or "(waived — anti-forgery token prevents)">` |
| `<two customers submit reviews for same book simultaneously>` | `<both queued; no DB collision>` | `<TC-XXX>` |

### 5. Resource exhaustion

> Timeout, quota exceeded, downstream unavailable.

| Scenario | Expected | Covered by |
|---|---|---|
| `<queue unavailable>` | `<HTTP 500; user notified>` | `<TC-XXX>` |
| `<DB write timeout>` | `<retry per ADR-XXX or fail with explicit message>` | `<TC-XXX>` |

### 6. State violations

> Action performed in wrong state.

| Scenario | Expected | Covered by |
|---|---|---|
| `<edit / delete an already-submitted review>` | `<not supported in v1; UC out-of-scope per BS-UC-001>` | `<(waived — out of scope)>` |

### 7. Domain-specific

> From `iconix.config.yaml.domain_test_families` if present. List each
> family that applies and how it's covered.

| Family (from config) | Applies to this UC? | Covered by |
|---|---|---|
| `<e.g., moderation-bypass>` | Yes | `<TC-XXX asserts review never reaches Book Detail page without moderation>` |
| `<e.g., input-tampering>` | Yes | `<TC-XXX uses tampered form data with rating outside [1..5]>` |

## Coverage summary

- **Families with ≥1 covering TC:** `<count>`/7
- **Families explicitly waived (with reason):** `<count>`
- **Families silently uncovered:** `<count>` ← MUST be 0 for the M3 gate to pass

## Traceability
- UC: `<PREFIX>-UC-XXX`
- Test plan: `test-plan/test-plan-<date>.md`
- TCs covering edge cases: `<list of TC-IDs referenced above>`
- NFRs related (resource-exhaustion edge cases ↔ latency / quota NFRs): `<list of NFR-IDs from nfr-annotations/<UC>-nfr.md>`
