# BS-TC-021: Review-length validation still works after BS-CI-001 (regression)

## Type
**regression**

## Traceability
- **Requirement:** BS-REQ-001 (now extended by BS-CI-001 — title length rule, BS-BR-003)
- **Use Case:** BS-UC-001 (basic + alt-B + new alt-F from BS-CI-001)
- **Robustness controller:** BS-RB-001: `IsBookReviewLengthOk` (the controller this test re-verifies after BS-CI-001 added a sibling controller `IsBookReviewTitleLengthOk`)
- **Sequence diagram:** BS-SD-001 (post-BS-CI-001 revision)
- **Supersedes TC:** **BS-TC-003** ← this regression run re-verifies BS-TC-003's behaviour after the title-length rule was added

## Why a regression test exists
BS-CI-001 added a new validation rule (title length 5–100) and wired it into `CustomerReview.Validate(ValidationContext)` alongside the existing review-length rule. The risk is straightforward and observed historically in this codebase:

> When a developer adds a new validation rule to a method that already runs other rules, the new rule's `yield return` / early-exit / DataAnnotations attribute placement can unintentionally short-circuit later rules. The compiler will not warn — every existing test (BS-TC-003) keeps passing if the rules execute in the *original* order, but breaks silently if the developer reorders them.

BS-TC-021 is the explicit re-verification that **BS-TC-003 still passes** in the post-BS-CI-001 codebase, AND that the new title-length rule does not interact incorrectly with the existing review-length rule.

This is the regression-test design pattern: **for every controller already covered, after every cross-cutting change, run one test that asserts the existing controller's behaviour is intact in the new context.** It is *not* a re-author of BS-TC-003 — it is a regression run with cross-product scenarios.

## Preconditions
- Codebase contains the BS-CI-001 changes: `Title` property on `CustomerReview` with `[Required]` + `[StringLength(100, MinimumLength = 5)]`; `Validate(ValidationContext)` calls `CheckBookExists` (unchanged).
- BS-TC-003 has been re-run and still passes in isolation.
- An `IBookRepository` substitute (NSubstitute) where `Exists(1)` returns `true`.

## Steps
<!-- Cross-product of {valid title, invalid title} × {valid review, invalid review} -->

| # | Title | Review | What this scenario proves |
|---|---|---|---|
| 1 | `"Brilliant"` (valid, 9 chars) | `"good"` (4 chars, invalid) | BS-TC-003 still works — invalid review still rejected |
| 2 | `"Brilliant"` (valid) | `"a".repeat(10)` (valid) | Both rules pass — review accepted (regression baseline) |
| 3 | `"Hi"` (invalid, 2 chars — new rule) | `"good"` (4 chars, invalid — old rule) | **Both** rules report errors; neither rule short-circuits the other |
| 4 | `"Hi"` (invalid, new rule) | `"a".repeat(200)` (valid) | New title rule reports its error without masking the old rule's pass |
| 5 | `"a".repeat(101)` (invalid, new rule, too long) | `"good"` (invalid, old rule) | Same as 3 with a different title-rule failure mode |

## Expected results
1. `Validator.TryValidateObject` returns `false`. `results` contains exactly one entry, for `Review`, with code `"too_short"`. **Critically: no entry for `Title`.** This proves BS-TC-003's assertion path still functions.
2. `TryValidateObject` returns `true`. `results` is empty. Regression baseline.
3. `TryValidateObject` returns `false`. `results` contains **two** entries — one for `Title`, one for `Review`. This is the test that catches accidental short-circuits: if the new title rule throws / yields-and-returns-early, scenario 3 will fail with only one error and the regression is caught here.
4. `TryValidateObject` returns `false`. `results` contains exactly one entry, for `Title`. No entry for `Review`.
5. `TryValidateObject` returns `false`. `results` contains exactly two entries (one per field).

## Postconditions
- No interaction with `ICustomerReviewRepository` or `IPendingReviewsQueue` — pure unit-level regression on the entity.
- The full scenario set runs in well under 100 ms; this test joins the unit test stage in CI, gating PRs.

## Priority
**P0** — must pass after BS-CI-001 ships and stays in the regression suite indefinitely.

## Edge case family
**state-violation** (specifically: rule-execution-order invariant)

## Implementation note (C# + xUnit + NSubstitute, per BS-ADR-001)

```csharp
public sealed class CustomerReviewValidationRegressionTests
{
    private readonly IBookRepository _bookRepo = Substitute.For<IBookRepository>();

    public CustomerReviewValidationRegressionTests()
    {
        _bookRepo.Exists(1).Returns(true);
    }

    public static IEnumerable<object[]> Scenarios() => new[]
    {
        // title,           review,                expectedTitleError, expectedReviewError
        new object[] { "Brilliant",        "good",                false, true  },  // #1
        new object[] { "Brilliant",        new string('a', 10),   false, false },  // #2
        new object[] { "Hi",               "good",                true,  true  },  // #3
        new object[] { "Hi",               new string('a', 200),  true,  false },  // #4
        new object[] { new string('a', 101), "good",              true,  true  },  // #5
    };

    [Theory]
    [MemberData(nameof(Scenarios))]
    public void Title_And_Review_Rules_Do_Not_Short_Circuit_Each_Other(
        string title, string review, bool expectedTitleError, bool expectedReviewError)
    {
        var customerReview = new CustomerReview
        {
            BookId     = 1,
            CustomerId = 42,
            Title      = title,
            Review     = review,
            Rating     = 3,
        };

        var services = new ServiceCollection()
            .AddSingleton(_bookRepo)
            .BuildServiceProvider();

        var ctx     = new ValidationContext(customerReview, services, items: null);
        var results = new List<ValidationResult>();
        Validator.TryValidateObject(customerReview, ctx, results, validateAllProperties: true);

        var hasTitleError  = results.Any(r => r.MemberNames.Contains(nameof(CustomerReview.Title)));
        var hasReviewError = results.Any(r => r.MemberNames.Contains(nameof(CustomerReview.Review)));

        hasTitleError.Should().Be(expectedTitleError,
            because: "the title rule must report (or not report) errors independently of the review rule");
        hasReviewError.Should().Be(expectedReviewError,
            because: "BS-TC-003's coverage of the review rule must remain intact after BS-CI-001");
    }
}
```

> **Why this is its own test, not a fold-in to BS-TC-003.** BS-TC-003's `## Steps` mirror BS-UC-001's alt-B exactly. Adding cross-product scenarios about Title would dilute BS-TC-003's traceability link to alt-B and to its `IsBookReviewLengthOk` controller. Regression coverage belongs in a regression test that names what it supersedes.

> **Why this is unit-level regression, not system-level.** The risk is in `Validate(ValidationContext)` — a single method on a single entity. Driving this through the controller and HTTP would obscure where a regression originates. The right altitude for a rule-interaction regression is the entity itself.
