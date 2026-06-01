# Phase 5d/6 Detection Tables — Migration Reference

Used by `iconix-migration-semantic` during Phase 5d (business rule extraction, Steps 1–4)
and Phase 6 Step 1 (test coverage mapping). Read before Phase 5d Step 1.

## Phase 5d — Track V: Validator classes (language-aware)

| Language | File scope | Signals |
|---|---|---|
| C# / .NET | `**/*.cs` | `AbstractValidator<T>` (FluentValidation) → `.RuleFor().NotNull()`, `.GreaterThan()`, `.Matches()`; `[Range]`, `[StringLength]`, `[RegularExpression]`, `[EmailAddress]` DataAnnotations; `ValidationAttribute` subclasses |
| Java | `**/*.java` | `@NotBlank`, `@NotNull`, `@Size`, `@Min`, `@Max`, `@Pattern`, `@Email` (Bean Validation); `ConstraintValidator<A,T>` implementations |
| Python (Django) | `**/models.py`, `**/forms.py` | `clean()` / `clean_<field>()` methods; `validators=[...]` on field; `ValidationError` raised |
| Python (SQLAlchemy) | `**/*.py` | `@validates` decorator |
| PHP | `**/*.php` | Symfony `Constraint` subclasses; Laravel Form Request `rules()` method |
| Ruby | `app/models/**/*.rb` | `validates :field, presence:`, `length:`, `numericality:`, `format:`; `validate :method_name` callbacks |
| TypeScript / JS | `**/*.ts`, `**/*.js` | class-validator `@IsEmail`, `@Min`, `@Max`, `@IsNotEmpty`, `@Length`, `@Matches` |
| Go | `**/*.go` | struct tags `validate:"required,min=0,max=100"` (go-playground/validator) |

Label all validator-derived rules `EXTRACTED`.

## Phase 5d — Track D: Domain-layer guard clauses (language-aware)

Restrict to domain / service / application layer paths — exclude `Controllers/`, `Repositories/`,
`Adapters/`, `Infrastructure/`, `Migrations/`.

*Guard clauses:*

| Language | Patterns |
|---|---|
| C# | `throw new.*Exception` / `Guard.Against.*` inside domain entity or service methods |
| Java | `Objects.requireNonNull`, `Preconditions.checkArgument`, `throw new IllegalArgumentException` |
| Python | `raise ValueError` / `raise TypeError` in model or domain service methods |
| PHP | `throw new \InvalidArgumentException` / `throw new DomainException` |
| Ruby | `raise ArgumentError` / custom domain exceptions |
| TypeScript | `throw new Error` / custom domain exception classes |
| Go | early `return err` with named domain error types |

*Specification / policy classes:* Grep for classes matching `(?i)(Specification|Spec|Policy|Rule|Guard|Criteria)` suffix, or implementing `ISpecification<T>` / `is_satisfied_by` / `satisfied_by?`. Extract the predicate body as a candidate **Precondition** or **Invariant**.

*Calculation methods:* Grep for methods named `Calculate*`, `Compute*`, `Derive*`, `Get*Total`, `Get*Amount` in domain layer. Extract method body for formula inference; label `INFERRED [VERIFY]`.

Label all Track D results `INFERRED [VERIFY]`.

## Phase 5d — Step 2: Rule classification table

| Category | When to use | Typical source |
|---|---|---|
| **Invariant** | Always true on entity, regardless of operation | NOT NULL, CHECK, validator annotations, guard in constructor |
| **Precondition** | Must hold before operation proceeds | Guard clause at method entry, specification.IsSatisfiedBy |
| **Postcondition** | Observable entity state guaranteed after operation | Trigger SET, method return contract |
| **Transition guard** | Controls whether a state machine transition is allowed | `if (status != Pending) throw`, state-aware specification |
| **Calculation** | Formula or derivation rule | `Calculate*` method body, trigger SET formula |
| **Authorization** | Role or permission constraint | `[Authorize]`, `HasRole()` guard, `@PreAuthorize` |
| **Workflow** | Sequencing constraint between operations | `if (!invoice.Exists) throw`, phase-ordering guard |

Classification heuristics (priority order):
- Track S NOT NULL / CHECK → **Invariant**; Track S CHECK IN / ORM enum → **Transition guard**
- Track V field annotation → **Invariant**; Track V role annotation → **Authorization**
- Track D guard `if (status !=) throw` → **Transition guard**; Track D guard at method entry (non-status) → **Precondition**
- Track D `Calculate*` / `Compute*` → **Calculation**; Track D specification / policy → **Precondition** or **Invariant**
- Track T RAISERROR / THROW → **Invariant** or **Precondition**; Track T SET formula → **Calculation**

When a rule fits multiple categories, prefer the most specific: `Transition guard > Precondition > Invariant`.

## Phase 5d — Step 4: UC annotation match signals

| Rule category | Match signal | Adds to UC as |
|---|---|---|
| **Precondition** | Rule entity in UC entity set OR operation verb matches UC main course | `## Preconditions` entry `[VERIFY]` |
| **Transition guard** | State change mentioned in UC main/alt course | `## Preconditions` entry `[VERIFY]` |
| **Authorization** | Role in rule matches UC Actor name or role description | `## Preconditions` entry `[VERIFY]` |
| **Invariant** | Rule entity in UC entity set | Cross-reference table only (invariants always hold) |
| **Calculation** | Rule entity in UC entity set | Cross-reference table only (informs Tester of derived values) |
| **Workflow** | Operation in UC's main/alt course appears in rule | `## Preconditions` entry `[VERIFY]` |

## Phase 6 — Step 1: Test node patterns (language-aware)

| Language | File patterns | Class / function signals |
|---|---|---|
| C# | `**/*.Tests/**/*.cs`, `**/*Test*.cs`, `**/*Spec*.cs` | `[TestClass]`, `[Fact]`, `[Theory]`, `[Test]` attributes |
| Java | `src/test/**/*.java`, `**/*Test*.java`, `**/*Spec*.java` | `@Test`, `@ParameterizedTest` |
| Python | `test_*.py`, `*_test.py` | `pytest` functions, `unittest.TestCase` subclasses |
| TypeScript/JS | `*.test.ts`, `*.spec.ts`, `*.test.js`, `*.spec.js` | `describe(`, `it(`, `test(` calls |
| Go | `*_test.go` | `func Test*` |
| Ruby | `spec/**/*_spec.rb`, `test/**/*_test.rb` | `describe`, `it`, `RSpec` |
