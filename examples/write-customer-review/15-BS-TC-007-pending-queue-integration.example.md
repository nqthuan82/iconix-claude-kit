# BS-TC-007: Submitted review appears on Pending Reviews Queue (integration)

## Type
**integration**

## Traceability
- **Requirement:** BS-REQ-001 (acceptance criterion 3 — review must be queued for moderation, not visible publicly)
- **Use Case:** BS-UC-001 (course: **basic**, steps 4)
- **Robustness controllers exercised:** `SaveCustomerReview`, `AddToPendingReviewsQueue`
- **Sequence diagram:** BS-SD-001 (group "Step 4 — Save & enqueue")
- **Supersedes TC:** *(n/a — first version)*

## What this test proves (and what BS-TC-001 does not)
BS-TC-001 covers the same use-case end-to-end at the *system* level — it drives the controller through `WebApplicationFactory<Program>` and asserts the database row + queue entry exist. **This test is narrower and harder.** It exercises the *boundary↔entity* contract directly:

- Real EF Core 9 against a real SQL Server 2022 container (no in-memory provider, no SQLite fallback — the production schema must apply cleanly).
- Real serialisation onto the Pending Reviews Queue transport (Azure Service Bus emulator in the container, not the in-memory test double used by unit/system tests).
- Tests `EfCustomerReviewRepository.AddAsync` + `BusPendingReviewsQueue.EnqueueAsync` together, because in the production code they are called from the same controller method and a partial failure of one against the other is the failure mode this test is designed to catch.

If BS-TC-001 passes but BS-TC-007 fails, the bug is in the persistence/transport layer, not the controller. That is the diagnostic value of having both tests.

## Preconditions
- A SQL Server 2022 Testcontainer is running with the production EF Core migrations applied.
- A Service Bus emulator (or real Service Bus dev instance) is running with the `pending-reviews` queue created.
- The DI container is configured exactly like production for `Bookstore.Infrastructure` — no overrides for repository or queue interfaces.
- A `Customer` row with id `42` and a `Book` row with id `1` are seeded in the database.

## Steps
<!-- Mirror the System Response column of BS-UC-001 step 4 -->
1. Construct a valid `CustomerReview { BookId = 1, CustomerId = 42, Review = new string('a', 200), Rating = 4 }`.
2. Call `await repository.AddAsync(review)` against the live `EfCustomerReviewRepository`.
3. Call `await queue.EnqueueAsync(review.Id)` against the live `BusPendingReviewsQueue`.
4. Read back from the database via a fresh `BookstoreDbContext` (different scope) and from the queue via a fresh `IPendingReviewsQueueReader`.

## Expected results
1. `repository.AddAsync` assigns the `CustomerReview` an integer `Id` and returns the populated entity. No exception.
2. `queue.EnqueueAsync` returns successfully. No exception.
3. Reading the database from a *new* DbContext returns a row with the supplied values and `State == ReviewState.Pending`. (Reading from the same context that wrote the row would prove nothing — EF would return the in-memory tracked entity.)
4. Reading the queue returns one message whose body deserialises to the `Id` written in step 1.

## Postconditions
- One `CustomerReview` row exists in the live SQL Server database.
- One message exists on the live `pending-reviews` queue, referencing that row's id.
- The Book Detail page does not surface the review (visibility test deferred to BS-UC-003 once that ships; for this TC we assert the *negative* indirectly: `state = Pending`, not `Published`).

## Priority
**P0** — must pass before release.

## Edge case family
**n/a** — happy path through the persistence/transport boundary.

## Implementation note (C# + xUnit + Testcontainers .NET, per BS-ADR-001)

```csharp
public sealed class EfCustomerReviewRepositoryIntegrationTests
    : IClassFixture<BookstoreInfrastructureFixture>
{
    private readonly BookstoreInfrastructureFixture _fx;
    public EfCustomerReviewRepositoryIntegrationTests(BookstoreInfrastructureFixture fx) => _fx = fx;

    [Fact]
    public async Task SubmittedReview_Lands_In_Database_And_On_Pending_Queue()
    {
        // Arrange — fresh scope using the production DI graph
        await using var writeScope = _fx.RootProvider.CreateAsyncScope();
        var repository = writeScope.ServiceProvider.GetRequiredService<ICustomerReviewRepository>();
        var queue      = writeScope.ServiceProvider.GetRequiredService<IPendingReviewsQueue>();

        var review = new CustomerReview
        {
            BookId     = 1,
            CustomerId = 42,
            Review     = new string('a', 200),
            Rating     = 4,
        };

        // Act — drive the two boundary calls in the same order as the controller
        var saved = await repository.AddAsync(review);
        await queue.EnqueueAsync(saved.Id);

        // Assert — read back with a *different* DbContext to bypass EF tracking
        await using var readScope = _fx.RootProvider.CreateAsyncScope();
        var freshDb     = readScope.ServiceProvider.GetRequiredService<BookstoreDbContext>();
        var fromDb      = await freshDb.CustomerReviews.AsNoTracking()
                                                       .SingleAsync(r => r.Id == saved.Id);
        fromDb.CustomerId.Should().Be(42);
        fromDb.BookId.Should().Be(1);
        fromDb.Rating.Should().Be(4);
        fromDb.State.Should().Be(ReviewState.Pending);

        // Assert — read back from the live queue
        var reader  = readScope.ServiceProvider.GetRequiredService<IPendingReviewsQueueReader>();
        var message = await reader.ReceiveOneAsync(timeout: TimeSpan.FromSeconds(5));
        message.Should().NotBeNull();
        message!.ReviewId.Should().Be(saved.Id);
    }
}

public sealed class BookstoreInfrastructureFixture : IAsyncLifetime
{
    private readonly MsSqlContainer _sql = new MsSqlBuilder()
        .WithImage("mcr.microsoft.com/mssql/server:2022-latest")
        .Build();

    private readonly ServiceBusEmulatorContainer _bus = new ServiceBusEmulatorBuilder()
        .WithQueue("pending-reviews")
        .Build();

    public ServiceProvider RootProvider { get; private set; } = default!;

    public async Task InitializeAsync()
    {
        await Task.WhenAll(_sql.StartAsync(), _bus.StartAsync());

        var services = new ServiceCollection();
        services.AddBookstoreInfrastructure(opts =>
        {
            opts.SqlConnectionString = _sql.GetConnectionString();
            opts.ServiceBusConnectionString = _bus.GetConnectionString();
        });
        RootProvider = services.BuildServiceProvider();

        // Apply migrations + seed
        await using var scope = RootProvider.CreateAsyncScope();
        var db = scope.ServiceProvider.GetRequiredService<BookstoreDbContext>();
        await db.Database.MigrateAsync();
        await Seed.CustomerAsync(db, id: 42);
        await Seed.BookAsync(db, id: 1);
    }

    public async Task DisposeAsync()
    {
        await RootProvider.DisposeAsync();
        await Task.WhenAll(_sql.StopAsync(), _bus.StopAsync());
    }
}
```

> **Why NSubstitute is absent here.** Integration tests prove that *real* implementations cooperate. Substituting either the repository or the queue would defeat the test's purpose. Mocks belong in unit tests (BS-TC-002, BS-TC-003); this test sits one level up the V-model.

> **Why a fresh `DbContext` for the read.** Reading from the same context that wrote the row would return the cached, tracked entity and tell us nothing about whether the row reached SQL. Using a sibling scope forces the query to round-trip the database and asserts the persistence side-effect.
