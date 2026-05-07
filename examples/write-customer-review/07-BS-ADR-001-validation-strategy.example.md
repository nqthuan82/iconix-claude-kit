# BS-ADR-001: Domain-object validation lives on the entity via `IValidatableObject`, not in a separate FluentValidation `AbstractValidator<T>` or service-layer method

## Status
**Accepted** — 2026-04-22

## Context
While drawing BS-RB-001 the Analyst identified four validation controllers for *Write Customer Review*: `IsBookReviewLengthOk`, `IsRatingInRange`, `IsUserLoggedIn`, plus the implicit *Book exists* check via `LoadBook`. ASP.NET Core 9 offers three idiomatic places where validation can live:

1. A dedicated FluentValidation `AbstractValidator<CustomerReview>` registered in DI and invoked by a model-binder filter.
2. The entity itself — using `[Range]` / `[StringLength]` / `[Required]` attributes from `System.ComponentModel.DataAnnotations` for simple bounds, plus `IValidatableObject.Validate(ValidationContext)` for cross-field rules. ASP.NET Core's MVC pipeline calls these automatically and surfaces failures via `ModelStateDictionary`.
3. A service-layer method (e.g., `ReviewSubmissionService.ValidateAndQueueAsync`) that throws a `ValidationException` (or returns a `Result` type).

We are about to enter detailed design (BS-SD-001) and need to decide *where* the validation behaviour lives, because the answer determines:
- which class owns the four `Check*` methods coming out of the robustness diagram;
- how many additional classes we ship per future use case;
- whether the rule "responsibility lives with the data" (BS-NFR-004 — Maintainability) holds across the codebase.

This is a code-organisation choice with cross-cutting consequences across every future "submit-something" use case (BS-UC-002 *Place Order*, BS-UC-003 *Update Address*, …). A use-case-local decision would be premature; the team needs an ADR.

- Driven by: BS-REQ-001, BS-NFR-004 (Maintainability — "validation logic must live with the data it validates"), implicit responsibility-driven design principle from BS-UC-001.
- Affected use cases: BS-UC-001 (Write Customer Review), and *all* future UCs that include validation controllers.
- Affected containers: `Bookstore.Web`, `Bookstore.Domain`.

## Options considered

### Option A: One `AbstractValidator<T>` per domain class (FluentValidation)
Add the [FluentValidation.AspNetCore](https://docs.fluentvalidation.net/) package. Author `CustomerReviewValidator : AbstractValidator<CustomerReview>` in `Bookstore.Application`. Register it via `services.AddValidatorsFromAssemblyContaining<CustomerReviewValidator>()` and `services.AddFluentValidationAutoValidation()`.

- **Pros:**
  - Most expressive validation DSL on .NET.
  - Pure .NET-attribute-free entities — keeps the domain model framework-neutral.
  - Asynchronous rules supported (e.g., DB lookups inside a rule).
- **Cons:**
  - Class count *doubles* — every domain class spawns a validator twin.
  - Behaviour is split from data, violating BS-NFR-004 and standard responsibility-driven design.
  - No single place to look when "what are the rules of this class?" is asked. The team will eventually ask, and the answer will be "search for `RuleFor` against this type."
  - Adds a third-party dependency for a problem the framework already solves.

### Option B: Validation methods on the domain class via `IValidatableObject` + DataAnnotations (chosen)
The `CustomerReview` entity carries DataAnnotations attributes for simple bounds (`[Required]`, `[StringLength(1_000_000, MinimumLength = 10)]`, `[Range(1, 5)]`) and implements `IValidatableObject` for the cross-field / lookup-dependent rules:

```csharp
public sealed class CustomerReview : IValidatableObject
{
    public int BookId { get; init; }
    public int CustomerId { get; init; }

    [Required(ErrorMessage = "Review text is required.")]
    [StringLength(1_000_000, MinimumLength = 10,
        ErrorMessage = "Review must be between 10 and 1,000,000 characters.")]
    public string Review { get; set; } = string.Empty;

    [Range(1, 5, ErrorMessage = "Rating must be between 1 and 5.")]
    public int Rating { get; init; }

    public IEnumerable<ValidationResult> Validate(ValidationContext context)
    {
        // Cross-field / DB-dependent rules — see CheckBookExists (BS-CI-001 will add CheckTitleLength here)
        var bookRepo = (IBookRepository)context.GetService(typeof(IBookRepository))!;
        if (!bookRepo.Exists(BookId))
            yield return new ValidationResult(
                "The selected book could not be found.",
                new[] { nameof(BookId) });
    }
}
```

ASP.NET Core's MVC model binder calls `Validate(...)` automatically; the controller checks `ModelState.IsValid` and re-displays the form with errors when needed. No separate `Validator` class is required.

- **Pros:**
  - One built-in mechanism for the whole app — bounded growth.
  - Rules live on the class they validate (BS-NFR-004 satisfied).
  - New domain classes get validation by adding attributes and (optionally) implementing one interface and one method.
  - Zero new dependencies — `System.ComponentModel.DataAnnotations` ships with .NET.
- **Cons:**
  - Slight coupling between the domain entity and `System.ComponentModel.DataAnnotations` namespace. This namespace is itself part of the framework BCL, so the coupling is to .NET, not to ASP.NET Core specifically — acceptable.
  - DataAnnotations message localisation requires an `IStringLocalizer` plumbing if we go multilingual; tracked as a follow-up.
  - Async DB-dependent rules are awkward inside synchronous `Validate` — for those we accept a synchronous repository check (`Exists`) or move the rule to a controller-side check before calling `ModelState.IsValid`.

### Option C: Service-layer validator with anaemic domain
Put validation in `IReviewSubmissionService.ValidateAndQueueAsync(SubmitReviewDto)`. Domain classes stay anaemic POCOs / EF entities only.

- **Pros:**
  - Familiar to teams coming from procedural backgrounds.
  - Trivial to mock services in tests.
- **Cons:**
  - Identical responsibility split as Option A but worse: rules are now two layers away from the data, and any code path that bypasses the service can write invalid data.
  - Service classes become god-objects fast.
  - Bypasses ASP.NET Core's model-state machinery, so we lose automatic 400-with-`ValidationProblemDetails` for free; we'd have to re-implement that manually per controller action.

## Decision
**Option B.** Validation belongs on the domain class. We will:

1. Annotate `CustomerReview` with DataAnnotations for the static bounds (`Required`, `StringLength`, `Range`).
2. Implement `IValidatableObject` on `CustomerReview` for cross-field and lookup-dependent rules (`CheckBookExists`, and — added in BS-CI-001 — `CheckTitleLength`).
3. Use ASP.NET Core's built-in MVC model-binding pipeline. `WriteCustomerReviewController` will rely on `ModelState.IsValid` rather than calling a separate validator service.
4. Author a single set of unit tests against `CustomerReview` that exercise both the attribute rules and the `Validate(ValidationContext)` body via `Validator.TryValidateObject`.

Rationale: this satisfies BS-NFR-004 (validation co-located with data), keeps class count linear in the number of domain classes (not quadratic), and removes the most common reason for rule drift — silent divergence between a `*Validator` class and the entity it validates. It also avoids introducing a third-party validation library when the framework already covers the use case.

## Consequences

| | Detail |
|---|---|
| **Positive** | Validation rules grep-able from the class they belong to (`CustomerReview.cs`). New domain classes inherit the pattern by example. ASP.NET Core's `ValidationProblemDetails` response is automatic when `[ApiController]` is applied. |
| **Negative** | Domain entities reference `System.ComponentModel.DataAnnotations` — minor coupling to a BCL namespace. Async DB lookups inside `Validate` are not natural; `CheckBookExists` therefore uses a synchronous `IBookRepository.Exists(int)` overload. |
| **Risks** | A future engineer might re-introduce a class-specific FluentValidation `AbstractValidator<T>` "because that's how the rest of the .NET community does it." Mitigation: an architecture-test (e.g., NetArchTest) that fails the build if any type derives from `AbstractValidator<>`, plus an entry in `CONTRIBUTING.md`. |
| **Follow-ups** | BS-ADR-002 (proposed) — adopt `Result<T, ValidationFailures>` return types in command handlers so that controller-level orchestration can short-circuit before calling repositories. BS-ADR-003 (proposed) — localisation strategy for DataAnnotations error messages. |

## Traceability
- **Drives:** BS-UC-001, BS-SD-001, every future UC with validation controllers.
- **Drives test design:** BS-TC-002 and BS-TC-003 invoke `Validator.TryValidateObject(review, …)` directly rather than going through a separate validator class.
- **Related ADRs:** BS-ADR-002 (proposed, command-result types); BS-ADR-003 (proposed, localisation).
- **Supersedes:** none.
