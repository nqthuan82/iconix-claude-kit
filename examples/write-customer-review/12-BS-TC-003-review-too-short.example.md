# BS-TC-003: Book Review under 10 characters is rejected (alternate course B)

## Type
**unit**

## Traceability
- **Requirement:** BS-REQ-001 (acceptance criterion 4)
- **Use Case:** BS-UC-001 (course: **alt-B**)
- **Robustness controller:** BS-RB-001: `IsBookReviewLengthOk`
- **Sequence diagram:** BS-SD-001 (group "Alternate B/C — review too short / too long")
- **Supersedes TC:** *(n/a — first version)*

## Preconditions
- A new `CustomerReview` instance is constructed with:
  - `BookId = 1` (a real book that the mocked `IBookRepository.Exists` returns `true` for).
  - `CustomerId = 42`.
  - `Rating = 3` (a valid value, so rating is not the cause of rejection).
  - `Review` — varies per scenario (see below).
- A `List<ValidationResult>` collector is provided to `Validator.TryValidateObject`.
- An `IBookRepository` substitute (NSubstitute) where `Exists(1)` returns `true`.

## Steps
<!-- Mirror the User Action column of BS-UC-001 alt-B exactly -->
1. Set `Review` to `""` (empty string). Call `Validator.TryValidateObject(...)`.
2. Set `Review` to `"   "` (whitespace only). Same call.
3. Set `Review` to `"good"` (4 characters). Same call.
4. Set `Review` to `new string('a', 9)` (1 char short of the minimum). Same call.
5. Set `Review` to `new string('a', 10)` (boundary — must pass). Same call.

## Expected results
<!-- Mirror the System Response column of BS-UC-001 alt-B exactly -->
1. `TryValidateObject` returns `false`; `results` contains a `ValidationResult` whose `MemberNames` includes `"Review"` and whose `ErrorMessage` matches `"Review text is required."` (the `[Required]` attribute fires before `[StringLength]`).
2. Same as 1.
3. `TryValidateObject` returns `false`; `results` contains a `ValidationResult` for `"Review"` with the message `"Review must be between 10 and 1,000,000 characters."`.
4. Same as 3.
5. `TryValidateObject` returns `true`; `results` contains no entry for `"Review"`.

## Postconditions
- No interaction with `ICustomerReviewRepository` occurred.
- No interaction with `IPendingReviewsQueue` occurred.

## Priority
**P0** — must pass before release.

## Edge case family
**boundary**

## Implementation note (C# + xUnit, per BS-ADR-001)

```csharp
public sealed class CustomerReviewLengthValidationTests
{
    private readonly IBookRepository _bookRepo = Substitute.For<IBookRepository>();

    public CustomerReviewLengthValidationTests()
    {
        _bookRepo.Exists(1).Returns(true);
    }

    private (bool ok, List<ValidationResult> results) Validate(string reviewText)
    {
        var review = new CustomerReview
        {
            BookId     = 1,
            CustomerId = 42,
            Rating     = 3,
            Review     = reviewText,
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
    [InlineData("")]
    [InlineData("   ")]
    public void Empty_Or_Whitespace_Review_Is_Rejected_As_Required(string reviewText)
    {
        var (ok, results) = Validate(reviewText);

        ok.Should().BeFalse();
        results.Should().Contain(r =>
            r.MemberNames.Contains(nameof(CustomerReview.Review)) &&
            r.ErrorMessage == "Review text is required.");
    }

    [Theory]
    [InlineData("good")]   // 4 chars
    [InlineData("aaaaaaaaa")] // 9 chars — one below the minimum
    public void Review_Below_Ten_Chars_Is_Rejected_As_Too_Short(string reviewText)
    {
        var (ok, results) = Validate(reviewText);

        ok.Should().BeFalse();
        results.Should().Contain(r =>
            r.MemberNames.Contains(nameof(CustomerReview.Review)) &&
            r.ErrorMessage == "Review must be between 10 and 1,000,000 characters.");
    }

    [Fact]
    public void Review_On_Lower_Boundary_Is_Accepted()
    {
        var (ok, results) = Validate(new string('a', 10));

        ok.Should().BeTrue();
        results.Should().NotContain(r =>
            r.MemberNames.Contains(nameof(CustomerReview.Review)));
    }
}
```
