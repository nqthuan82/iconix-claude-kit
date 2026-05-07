# BS-TC-004: Customer not logged in is sent through Login (alternate course A)

## Type
**system**

## Traceability
- **Requirement:** BS-REQ-001 (acceptance criterion 2)
- **Use Case:** BS-UC-001 (course: **alt-A**)
- **Robustness controllers exercised:** `IsUserLoggedIn`, `InvokeLogin`, `DisplayWriteReviewPage`
- **Sequence diagram:** BS-SD-001 (group "Alternate A — Customer not logged in")
- **Supersedes TC:** *(n/a — first version)*

## Preconditions
- The HTTP client has no auth cookie. ASP.NET Core's cookie-auth handler is registered with `LoginPath = "/login"`.
- A `Book` with id `1` exists in the database.
- A `Customer` with username `alice@example.com` and password `correct horse` exists.

## Steps
<!-- Mirror the User Action column of BS-UC-001 alt-A exactly -->
1. Anonymous user GETs `/books/1/review`.
2. User submits the Login form at `/login` with valid credentials and `ReturnUrl=/books/1/review`.
3. After login, the user follows the redirect.

## Expected results
<!-- Mirror the System Response column of BS-UC-001 alt-A exactly -->
1. The system returns HTTP 302 with `Location: /login?ReturnUrl=%2Fbooks%2F1%2Freview`. (`[Authorize]` on `WriteAsync` triggers the cookie-auth `Challenge`.)
2. The system authenticates, sets the auth cookie (`.AspNetCore.Cookies`), and returns HTTP 302 with `Location: /books/1/review`.
3. The system returns HTTP 200 and renders `Views/Reviews/Write.cshtml` for book `1`.

## Postconditions
- The auth cookie is present on the client.
- No `CustomerReview` rows have been created (the user has not submitted yet).
- The Pending Reviews Queue is unchanged.

## Priority
**P0** — must pass before release.

## Edge case family
**authorization**

## Implementation note (C# + xUnit + WebApplicationFactory<Program>)

```csharp
public sealed class WriteCustomerReviewAuthSystemTests
    : IClassFixture<BookstoreApiFactory>
{
    private readonly BookstoreApiFactory _factory;
    public WriteCustomerReviewAuthSystemTests(BookstoreApiFactory factory) => _factory = factory;

    [Fact]
    public async Task Anonymous_Is_Redirected_Through_Login_And_Back()
    {
        var client = _factory.CreateClient(new() { AllowAutoRedirect = false });
        await using var scope = _factory.Services.CreateAsyncScope();
        await SeedBookAsync(scope, bookId: 1);
        await SeedCustomerAsync(scope, "alice@example.com", "correct horse");

        // Step 1 — anonymous GET → 302 to /login
        var firstHit = await client.GetAsync("/books/1/review");

        firstHit.StatusCode.Should().Be(HttpStatusCode.Redirect);
        firstHit.Headers.Location!.OriginalString
            .Should().Be("/login?ReturnUrl=%2Fbooks%2F1%2Freview");

        // Step 2 — POST credentials to /login
        var loginPage  = await client.GetAsync(firstHit.Headers.Location);
        var (cookie, formToken) = AntiForgery.Extract(loginPage);

        var loginForm = new Dictionary<string, string>
        {
            ["Username"]                   = "alice@example.com",
            ["Password"]                   = "correct horse",
            ["ReturnUrl"]                  = "/books/1/review",
            ["__RequestVerificationToken"] = formToken,
        };
        var loginPost = new HttpRequestMessage(HttpMethod.Post, "/login")
        {
            Content = new FormUrlEncodedContent(loginForm),
        };
        loginPost.Headers.Add("Cookie", cookie);

        var loggedIn = await client.SendAsync(loginPost);
        loggedIn.StatusCode.Should().Be(HttpStatusCode.Redirect);
        loggedIn.Headers.Location!.OriginalString.Should().Be("/books/1/review");
        loggedIn.Headers.Should().ContainKey("Set-Cookie")
            .WhoseValue.Should().Contain(v => v.StartsWith(".AspNetCore.Cookies"));

        // Step 3 — follow redirect with the auth cookie attached
        var authCookie = loggedIn.Headers
            .GetValues("Set-Cookie")
            .First(v => v.StartsWith(".AspNetCore.Cookies"))
            .Split(';')[0];

        var followUp = new HttpRequestMessage(HttpMethod.Get, "/books/1/review");
        followUp.Headers.Add("Cookie", authCookie);
        var page = await client.SendAsync(followUp);

        page.StatusCode.Should().Be(HttpStatusCode.OK);
        var html = await page.Content.ReadAsStringAsync();
        html.Should().Contain("Write Review");

        // Postcondition — no review created yet
        var reviewCount = await scope.ServiceProvider
            .GetRequiredService<ICustomerReviewRepository>()
            .CountAllAsync();
        reviewCount.Should().Be(0);
    }
}
```
