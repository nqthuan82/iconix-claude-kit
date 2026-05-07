# Test Plan — Q3 *Reviews & Ratings* — Sprint 14 — 2026-04-30

## 1. Scope

| UC ID | Title | In scope? |
|---|---|---|
| BS-UC-001 | Write Customer Review | **Yes** |
| BS-UC-002 | Moderate Customer Reviews | No — separate sprint, separate plan |
| BS-UC-003 | Show Book Details | No — already in production; only regression-tested |

## 2. TC inventory

The robustness diagram BS-RB-001 has 8 basic-course controllers and 4 alternate-course controllers — 12 controllers total. Each becomes at least one test case; alternate scenarios add extra TCs as needed.

| Type | Count | Notes |
|---|---|---|
| Unit (one per RB controller) | 8 | One per controller in BS-RB-001. xUnit + NSubstitute. |
| Integration (boundary↔entity data flow) | 2 | `WriteCustomerReviewController` ↔ `EfCustomerReviewRepository` (Testcontainers SQL Server); enqueue path to `BusPendingReviewsQueue`. |
| System (full UC scenarios) | 5 | One per UC course (basic + alt A/B/C/D/E — alt E reuses existing BookNotFound coverage). Hosted via `WebApplicationFactory<Program>`. |
| Acceptance (stakeholder-reviewed scenarios) | 3 | Basic happy path; rejected too-short; rejected wrong-rating. Reviewed with Sarah Patel and Doug. Reqnroll bindings against the same `WebApplicationFactory<Program>` host. |
| Regression (post-change re-verification) | grows over time | Authored only when a change introduces cross-cutting risk to a previously-passing TC. After BS-CI-001: BS-TC-021 supersedes BS-TC-003. |
| **Total at release** | **18 + regression** | |

## 3. Automation status

Project layout (under `tests/`):

- `tests/Bookstore.Tests.Unit/` — xUnit + NSubstitute.
- `tests/Bookstore.Tests.Integration/` — xUnit + Testcontainers + EF Core 9.
- `tests/Bookstore.Tests.System/` — xUnit + `WebApplicationFactory<Program>` (full ASP.NET Core 9 host).

| TC ID | Title | Type | Automated? | Test file |
|---|---|---|---|---|
| BS-TC-001 | Display Write Review page (basic course) | system | Yes | `tests/Bookstore.Tests.System/Reviews/WriteCustomerReviewSystemTests.cs` |
| BS-TC-002 | Rating outside `[1..5]` is rejected | unit | Yes | `tests/Bookstore.Tests.Unit/Domain/CustomerReviewValidationTests.cs` |
| BS-TC-003 | Book Review under 10 chars is rejected | unit | Yes | `tests/Bookstore.Tests.Unit/Domain/CustomerReviewValidationTests.cs` |
| BS-TC-004 | Customer not logged in is sent through Login | system | Yes | `tests/Bookstore.Tests.System/Reviews/WriteCustomerReviewSystemTests.cs` |
| BS-TC-005 | Book Review over 1 MB is rejected | unit | Yes | `tests/Bookstore.Tests.Unit/Domain/CustomerReviewValidationTests.cs` |
| BS-TC-006 | EfBookRepository returns null for missing Book ID | integration | Yes | `tests/Bookstore.Tests.Integration/Repositories/EfBookRepositoryIntegrationTests.cs` |
| BS-TC-007 | Submitted review appears on Pending Reviews Queue | integration | Yes | `tests/Bookstore.Tests.Integration/Repositories/EfCustomerReviewRepositoryIntegrationTests.cs` — spec: [file 15](./15-BS-TC-007-pending-queue-integration.example.md) |
| BS-TC-021 | Review-length validation still works after BS-CI-001 | regression  | Yes | `tests/Bookstore.Tests.Unit/Domain/CustomerReviewValidationRegressionTests.cs` — spec: [file 17](./17-BS-TC-021-supersedes-BS-TC-003.example.md) |
| BS-TC-101 | Customer submits a moderated review (Gherkin)        | acceptance  | Yes | `tests/Bookstore.Tests.Acceptance/Reviews.feature` — spec: [file 16](./16-BS-TC-101-stakeholder-happy-path.example.md) |
| BS-TC-008 | `Validator.TryValidateObject` reports every rule violation | unit | Yes | `tests/Bookstore.Tests.Unit/Domain/CustomerReviewValidationTests.cs` |
| BS-TC-009 | Confirmation view is rendered after successful submit | unit | Yes | `tests/Bookstore.Tests.Unit/Web/WriteCustomerReviewControllerTests.cs` |
| BS-TC-010 | Submitted review is associated with the logged-in Customer (claims principal) | unit | Yes | `tests/Bookstore.Tests.Unit/Web/WriteCustomerReviewControllerTests.cs` |
| BS-TC-011..018 | … | various | Yes | (continued in `test-matrix.md`) |

## 4. Coverage status

Summary from `test-matrices/test-matrix-2026-04-30.md`:

| UC ID | TCs exist? | All courses covered? | Blocker? |
|---|---|---|---|
| BS-UC-001 | Yes | Yes (basic + 5 alternates) | No |

> Any UC with no TC is a **gate blocker** — the M3 gate will not pass until it is resolved.

## 5. Outstanding risks

| Risk | Affected TCs | Mitigation / Owner |
|---|---|---|
| The Pending Reviews Queue infrastructure (INFRA-88) is delivered Sprint 13 — slipping; integration tests may need a temporary in-memory queue. | BS-TC-007, BS-TC-009 | If INFRA-88 is not in CI by 2026-04-26, swap to `InMemoryPendingReviewsQueue : IPendingReviewsQueue` and add follow-up regression TCs once INFRA-88 lands. Owner: Matt. |
| Performance NFR (BS-NFR-001 — Confirmation page within 2 s p95) not yet exercised by any TC. | (new TC needed) | Add **BS-TC-019** load test (NBomber against staging) by 2026-05-04. Owner: Sarah (Performance). |
| Spam / abuse not testable until Moderate Customer Reviews ships. | n/a | Acceptance Criteria 3 of BS-REQ-001 ("not visible until approved") covered by BS-TC-007 — visibility check. The full moderator path is in the next sprint. |
| Anti-forgery token enforcement on POST may surface in system tests as 400s if not configured in the test host. | BS-TC-001 | `WebApplicationFactory<Program>` uses `services.AddAntiforgery(...)`; integration tests must obtain `__RequestVerificationToken` from the GET response or call `services.PostConfigure<AntiforgeryOptions>` to relax it for the test host. |

## 6. Traceability

The matrix below confirms one-to-one coverage from BS-RB-001 controllers to test cases. Run the Traceability Agent before the M3 gate to revalidate:

| RB-001 controller | Test case(s) |
|---|---|
| `IsUserLoggedIn` | BS-TC-004 |
| `LoadBook` | BS-TC-006 |
| `DisplayWriteReviewPage` | BS-TC-001 |
| `IsBookReviewLengthOk` | BS-TC-003, BS-TC-005 |
| `IsRatingInRange` | BS-TC-002 |
| `SaveCustomerReview` | BS-TC-009, BS-TC-010 |
| `AddToPendingReviewsQueue` | BS-TC-007 |
| `DisplayConfirmationPage` | BS-TC-009 |
| `InvokeLogin` | BS-TC-004 |
| `DisplayLengthError` | BS-TC-003, BS-TC-005 |
| `DisplayRatingError` | BS-TC-002 |
| `DisplayBookNotFoundPage` | BS-TC-006 (reuses existing *Show Book Details* coverage) |

Every controller has at least one TC; every alternate course has at least one TC. M3 gate is unblocked once BS-TC-019 is added for BS-NFR-001.
