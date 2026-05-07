# BS-TC-001: Display Write Review page after successful submit (basic course)

## Type
**system**

## Traceability
- **Requirement:** BS-REQ-001
- **Use Case:** BS-UC-001 (course: **basic**)
- **Robustness controllers exercised:** `DisplayWriteReviewPage`, `SaveCustomerReview`, `AddToPendingReviewsQueue`, `DisplayConfirmationPage`
- **Sequence diagram:** BS-SD-001
- **Supersedes TC:** *(n/a — first version)*

## Preconditions
- A `Customer` with id `42` exists and is authenticated; the test host's cookie auth handler has issued a valid auth cookie. The `ClaimsPrincipal` carries `NameIdentifier = "42"`.
- A `Book` with id `1` exists in the database (seeded by the test fixture).
- The Pending Reviews Queue is empty for book `1`.

## Steps
<!-- Mirror the User Action column of BS-UC-001 exactly -->
1. Customer GETs `/books/1/review`.
2. Customer fills the form: 200-character `Review`, `Rating = 4`, and the anti-forgery token from the GET response.
3. Customer POSTs the form to `/books/1/review`.

## Expected results
<!-- Mirror the System Response column of BS-UC-001 exactly -->
1. The system returns HTTP 200 and renders `Views/Reviews/Write.cshtml` with the book title in the `<h1>` and an empty review form including a `__RequestVerificationToken`.
2. *(client-side step, no system response)*
3. The system returns HTTP 200 and renders `Views/Reviews/Confirm.cshtml`. A `CustomerReview` row exists in `dbo.CustomerReviews` with `BookId=1`, `CustomerId=42`, `Rating=4`, `State=Pending`. The review is **not** visible on the Book Detail page.

## Postconditions
- Exactly one new `CustomerReview` row in `dbo.CustomerReviews` for book `1`, owned by customer `42`, in `Pending` state.
- The Pending Reviews Queue contains exactly one entry referencing that review's `Id`.
- The Book Detail page for book `1` shows zero reviews.

## Priority
**P0** — must pass before release.

## Edge case family
**n/a** — basic-course happy path.

## Implementation note (C# + xUnit + WebApplicationFactory<Program>, per BS-ADR-001)

```csharp
public sealed class WriteCustomerReviewSystemTests
    : IClassFixture<BookstoreApiFactory>
{
    private readonly BookstoreApiFactory _factory;
    public WriteCustomerReviewSystemTests(BookstoreApiFactory factory) => _factory = factory;

    [Fact]
    public async Task BasicCourse_SubmitsReviewToPendingQueue()
    {
        // Arrange — sign the test client in as customer 42
        await using var scope = _factory.Services.CreateAsyncScope();
        await SeedBookAsync(scope, bookId: 1);
        var client = _factory.CreateClient(new() { AllowAutoRedirect = false });
        await client.SignInTestUserAsync(customerId: 42);

        // Step 1 — GET the form (also yields the antiforgery token)
        var getResponse = await client.GetAsync("/books/1/review");
        getResponse.StatusCode.Should().Be(HttpStatusCode.OK);
        var (cookie, formToken) = AntiForgery.Extract(getResponse);

        // Steps 2–3 — POST the filled form
        var form = new Dictionary<string, string>
        {
            ["BookId"]                     = "1",
            ["Review"]                     = new string('a', 200),
            ["Rating"]                     = "4",
            ["__RequestVerificationToken"] = formToken,
        };
        var post = new HttpRequestMessage(HttpMethod.Post, "/books/1/review")
        {
            Content = new FormUrlEncodedContent(form),
        };
        post.Headers.Add("Cookie", cookie);

        var postResponse = await client.SendAsync(post);

        // Assert — confirmation rendered
        postResponse.StatusCode.Should().Be(HttpStatusCode.OK);
        var html = await postResponse.Content.ReadAsStringAsync();
        html.Should().Contain("Thanks — your review will be reviewed");

        // Assert — postconditions in DB + queue
        var saved = await scope.ServiceProvider
            .GetRequiredService<ICustomerReviewRepository>()
            .FindLatestForBookAsync(bookId: 1);

        saved.Should().NotBeNull();
        saved!.CustomerId.Should().Be(42);
        saved.Rating.Should().Be(4);
        saved.State.Should().Be(ReviewState.Pending);

        var queue = scope.ServiceProvider.GetRequiredService<IPendingReviewsQueue>();
        (await queue.ContainsAsync(saved.Id)).Should().BeTrue();

        var visibleReviews = await BookDetailPage.GetVisibleReviewsAsync(client, bookId: 1);
        visibleReviews.Should().BeEmpty();
    }
}
```

`BookstoreApiFactory` is a `WebApplicationFactory<Program>` subclass that swaps the production EF Core provider for a Testcontainers-managed SQL Server instance and registers an in-memory `IPendingReviewsQueue` until INFRA-88 lands (see Outstanding Risks in the test plan).
