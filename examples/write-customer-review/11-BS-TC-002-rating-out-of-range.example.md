# BS-TC-002: Book Rating outside `[1..5]` is rejected (alternate course D)

## Type
**unit**

## Traceability
- **Requirement:** BS-REQ-001 (acceptance criterion 5)
- **Use Case:** BS-UC-001 (course: **alt-D**)
- **Robustness controller:** BS-RB-001: `IsRatingInRange`
- **Sequence diagram:** BS-SD-001 (group "Alternate D — rating out of range")
- **Supersedes TC:** *(n/a — first version)*

## Preconditions
- A new `CustomerReview` instance is constructed with:
  - `BookId = 1` (a real book that the mocked `IBookRepository.Exists` returns `true` for).
  - `CustomerId = 42`.
  - `Review = new string('a', 200)` (a 200-character non-blank string — passes `[StringLength]`).
  - `Rating` — varies per scenario (see below).
- A `List<ValidationResult>` collector is provided to `Validator.TryValidateObject`.
- An `IBookRepository` substitute (NSubstitute) where `Exists(1)` returns `true`.

## Steps
<!-- Mirror the User Action column of BS-UC-001 alt-D exactly -->
1. Build a `CustomerReview` whose `Rating` is `0`. Call `Validator.TryValidateObject(review, ctx, results, validateAllProperties: true)`.
2. Build a `CustomerReview` whose `Rating` is `6`. Same call.
3. Build a `CustomerReview` whose `Rating` is `-1`. Same call.
4. Build a `CustomerReview` whose `Rating` is `1`. Same call. *(boundary — must pass)*
5. Build a `CustomerReview` whose `Rating` is `5`. Same call. *(boundary — must pass)*

## Expected results
<!-- Mirror the System Response column of BS-UC-001 alt-D exactly -->
1. `TryValidateObject` returns `false`; `results` contains a `ValidationResult` whose `MemberNames` includes `"Rating"` and whose `ErrorMessage` is `"Rating must be between 1 and 5."`.
2. Same as 1.
3. Same as 1.
4. `TryValidateObject` returns `true` (rating is on the lower boundary, no other rule fails). No `ValidationResult` for `Rating`.
5. Same as 4.

## Postconditions
- No interaction with `ICustomerReviewRepository` occurred (this is a unit test on the entity).
- No interaction with `IPendingReviewsQueue` occurred.
- `IBookRepository.Exists(1)` was called at most once per scenario (cross-field rule).

## Priority
**P0** — must pass before release.

## Edge case family
**boundary**

## Implementation note (C# + xUnit + NSubstitute, per BS-ADR-001)

```csharp
public sealed class CustomerReviewValidationTests
{
    private readonly IBookRepository _bookRepo = Substitute.For<IBookRepository>();

    public CustomerReviewValidationTests()
    {
        _bookRepo.Exists(1).Returns(true);
    }

    private (bool ok, List<ValidationResult> results) Validate(int rating)
    {
        var review = new CustomerReview
        {
            BookId     = 1,
            CustomerId = 42,
            Review     = new string('a', 200),
            Rating     = rating,
        };

        var services = new ServiceCollection()
            .AddSingleton(_bookRepo)
            .BuildServiceProvider();

        var ctx     = new ValidationContext(review, services, items: null);
        var results = new List<ValidationResult>();
        var ok      = Validator.TryValidateObject(review, ctx, results, validateAllProperties: true);
        return (ok, results);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(6)]
    [InlineData(-1)]
    public void Rating_Outside_1_To_5_Is_Rejected(int rating)
    {
        var (ok, results) = Validate(rating);

        ok.Should().BeFalse();
        results.Should().Contain(r =>
            r.MemberNames.Contains(nameof(CustomerReview.Rating)) &&
            r.ErrorMessage == "Rating must be between 1 and 5.");
    }

    [Theory]
    [InlineData(1)]
    [InlineData(5)]
    public void Rating_On_Boundary_Is_Accepted(int rating)
    {
        var (ok, results) = Validate(rating);

        ok.Should().BeTrue();
        results.Should().NotContain(r =>
            r.MemberNames.Contains(nameof(CustomerReview.Rating)));
    }
}
```
