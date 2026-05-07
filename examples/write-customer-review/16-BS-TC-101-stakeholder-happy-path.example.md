# BS-TC-101: Customer submits a moderated review (acceptance)

## Type
**acceptance**

## Traceability
- **Requirement:** BS-REQ-001 (entire requirement; this is the stakeholder sign-off case)
- **Use Case:** BS-UC-001 (course: **basic**)
- **Robustness controllers exercised:** end-to-end — every controller in the basic course of BS-RB-001
- **Sequence diagram:** BS-SD-001 (Steps 1–5 — full happy path)
- **Supersedes TC:** *(n/a — first version)*

## Stakeholder sign-off
This scenario was reviewed in plain English with the people who own the outcome:

| Reviewer | Role | Approved | Date |
|---|---|---|---|
| Doug Rosenberg | Editor-in-Chief (originator of `BOOK-412`) | ✅ | 2026-04-29 |
| Sarah Patel | Customer Care Lead (owns the moderator team) | ✅ | 2026-04-29 |
| Linda Cheu | Compliance Officer | ✅ | 2026-04-30 |

If the Gherkin below is changed, this row block must be re-signed before the next release. The acceptance test failing in CI **blocks the release**, regardless of whether unit/integration/system tests pass.

## Why an acceptance test exists in addition to BS-TC-001 (system)
Both tests exercise the basic course end-to-end. The differences are intentional:

| | BS-TC-001 (system) | BS-TC-101 (acceptance) |
|---|---|---|
| Author | Tester (engineer) | Tester drafts from the feature request, **stakeholders sign off** |
| Language | C# / `MockMvc`-style assertions | Gherkin (plain English, framework-neutral) |
| Audience | Engineers reading the code | Doug, Sarah, Linda, auditors |
| What failure means | "The implementation has drifted" | "The agreement with the stakeholders is broken" |
| Lifecycle | Owned by the engineering team | Re-signed if the Gherkin changes |

A passing acceptance test is the contract between the bookstore team and the stakeholders that *this specific outcome* still works.

## Preconditions
- A `Customer` named *Alice Walker* (id `42`) is signed in.
- A `Book` titled *"The Lord of the Rings"* (id `1`) exists in the catalog.
- The Pending Reviews Queue is empty.

## Gherkin scenario (the contract)

```gherkin
Feature: A Customer can submit a moderated review for a Book
  As a logged-in Customer browsing a Book,
  I want to leave a star rating and a written review on the book's detail page,
  So that other Customers can use my opinion when deciding whether to buy.

Background:
  Given Alice is signed in as Customer 42
  And she is on the Book Detail page for "The Lord of the Rings"
  And the Pending Reviews Queue is empty

Scenario: Alice submits a thoughtful 4-star review
  When Alice clicks the "Write Review" button
  Then she sees the Write Review page for "The Lord of the Rings"

  When she enters the review text "A surprisingly clear introduction to OO design. Recommended."
  And she selects 4 stars
  And she clicks the "Send" button
  Then she sees the Confirmation page

  And the Pending Reviews Queue contains exactly one review by Alice for "The Lord of the Rings"
  And the Book Detail page for "The Lord of the Rings" shows zero published reviews
```

## Expected behaviour, in stakeholder terms
- Alice does not see her own review on the public Book Detail page until a Moderator approves it. *(BS-NFR-002 — Compliance: no review public without moderation.)*
- A Moderator will see Alice's review on the moderation queue when they next sign in. *(Out of scope for BS-UC-001; verified by BS-UC-002's acceptance suite.)*
- The Confirmation page tells Alice her review is awaiting approval. *(So Alice does not refresh the Book Detail page expecting to see it.)*

## Priority
**P0** — release-blocking. A red BS-TC-101 means the team must either fix the build or re-engage Doug, Sarah, and Linda for a contract renegotiation. There is no "let's ship it and follow up" path for an acceptance test.

## Edge case family
**n/a** — this is the canonical happy path. Edge cases live in BS-TC-002, BS-TC-003, BS-TC-004, BS-TC-005, etc.

## Implementation note (C# + Reqnroll, per BS-ADR-001)

The `.feature` file above lives at `tests/Bookstore.Tests.Acceptance/Reviews.feature`. Reqnroll is the active SpecFlow successor on .NET 9 — it parses the same Gherkin syntax and binds it to step definitions:

```csharp
[Binding]
public sealed class ReviewSubmissionSteps
{
    private readonly BookstoreApiFactory _factory;
    private readonly ScenarioContext      _ctx;
    private HttpClient                    _client = default!;
    private HttpResponseMessage?          _lastResponse;

    public ReviewSubmissionSteps(BookstoreApiFactory factory, ScenarioContext ctx)
        => (_factory, _ctx) = (factory, ctx);

    [Given(@"Alice is signed in as Customer (\d+)")]
    public async Task GivenAliceIsSignedIn(int customerId)
    {
        _client = _factory.CreateClient(new() { AllowAutoRedirect = false });
        await _client.SignInTestUserAsync(customerId);
        _ctx["customerId"] = customerId;
    }

    [Given(@"she is on the Book Detail page for ""(.*)""")]
    public async Task GivenSheIsOnBookDetail(string bookTitle)
    {
        var bookId = await BookCatalog.IdForTitleAsync(_factory.Services, bookTitle);
        _ctx["bookId"] = bookId;
        await _client.GetAsync($"/books/{bookId}");
    }

    [Given(@"the Pending Reviews Queue is empty")]
    public async Task GivenQueueEmpty()
        => await PendingReviewsQueue.PurgeAsync(_factory.Services);

    [When(@"Alice clicks the ""Write Review"" button")]
    public async Task WhenAliceClicksWriteReview()
        => _lastResponse = await _client.GetAsync($"/books/{_ctx["bookId"]}/review");

    [Then(@"she sees the Write Review page for ""(.*)""")]
    public async Task ThenSheSeesWriteReviewPage(string bookTitle)
    {
        _lastResponse!.StatusCode.Should().Be(HttpStatusCode.OK);
        var html = await _lastResponse.Content.ReadAsStringAsync();
        html.Should().Contain("Write Review")
                     .And.Contain(bookTitle);
    }

    // … further When/Then bindings follow the same pattern …

    [Then(@"the Pending Reviews Queue contains exactly one review by Alice for ""(.*)""")]
    public async Task ThenQueueContainsOneReview(string bookTitle)
    {
        var bookId  = await BookCatalog.IdForTitleAsync(_factory.Services, bookTitle);
        var queued  = await PendingReviewsQueue.PeekAllAsync(_factory.Services);
        queued.Should().ContainSingle(r =>
            r.CustomerId == (int)_ctx["customerId"] && r.BookId == bookId);
    }

    [Then(@"the Book Detail page for ""(.*)"" shows zero published reviews")]
    public async Task ThenBookDetailShowsZero(string bookTitle)
    {
        var bookId   = await BookCatalog.IdForTitleAsync(_factory.Services, bookTitle);
        var reviews  = await BookDetailPage.GetVisibleReviewsAsync(_client, bookId);
        reviews.Should().BeEmpty();
    }
}
```

> **Why this lives in its own project (`Bookstore.Tests.Acceptance`).** Acceptance tests run as a separate CI job with their own SLA — they take longer to set up, and they fail loudly. They are not folded into the unit test stage, because a slow flaky acceptance suite poisoning the unit test feedback loop would defeat the purpose of both.
