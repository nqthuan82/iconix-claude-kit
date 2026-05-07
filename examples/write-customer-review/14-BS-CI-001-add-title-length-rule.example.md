# Change Impact Report — CI-2026-05-04

## Trigger
- **Changed artifact:** **BS-REQ-001** (a new validation rule is added to the requirement)
- **Change summary:** A new business rule **BS-BR-003** ("Customer Review titles must be 5–100 characters") is added to BS-REQ-001 because Customer Care found that pending reviews with no title or with paste-bombed titles are clogging the Moderator queue.
- **Requested by:** Sarah Patel (Customer Care Lead) — ticket `BOOK-447`, 2026-05-03.

## Blast radius

```
BS-REQ-001 (changed: + new acceptance criterion for title length)
  └─► BS-UC-001               (add validation step + new alternate course "Title length out of bounds")
        ├─► BS-RB-001         (add new controller IsBookReviewTitleLengthOk; new DisplayTitleLengthError)
        │     └─► BS-SD-001   (add Title StringLength rule + new alternate-course group)
        │           └─► BS-CLS-CustomerReview
        │                       (add [StringLength(100, MinimumLength = 5)] on Title)
        │                 └─► BS-TC-003 (extend with title-length scenarios)  + new BS-TC-020 (boundary)
        └─► BS-UC-002 *(Moderate Customer Reviews)* — unchanged on input side; Moderator queue
                                                     just sees fewer broken titles.
```

## Affected artifacts (flat list, ordered by blast radius)

| ID | Type | File | Action required |
|---|---|---|---|
| BS-REQ-001 | Requirement | `04-BS-REQ-001-submit-customer-review.example.md` | Append acceptance criterion 7: *"A submission whose Book Review title length is outside `[5, 100]` is rejected with an explanatory message."* |
| BS-UC-001 | Use Case | `05-BS-UC-001-write-customer-review.example.md` | Add **Alternate Course F: Title length out of bounds**. Update Basic Course step 3 to mention title validation. |
| BS-RB-001 | Robustness | `06-BS-RB-001-write-customer-review.example.puml` | Add controller `IsBookReviewTitleLengthOk`; add error path through new `DisplayTitleLengthError` → `Write Review page`. |
| BS-SD-001 | Sequence | `08-BS-SD-001-write-customer-review.example.puml` | Add a `Title` field to the `CustomerReview` lifeline. Title rule is enforced declaratively (`[Required]` + `[StringLength(100, MinimumLength = 5)]`) — no new method, but add a new alternate-course group covering the rejection path. |
| BS-CLS-CustomerReview | Class | `src/Bookstore.Domain/CustomerReview.cs` | Add `Title` property with `[Required]` + `[StringLength(100, MinimumLength = 5)]`. No change to `Validate(ValidationContext)` is needed unless cross-field rules apply. |
| BS-CLS-CustomerReviewDbConfig | EF Mapping | `src/Bookstore.Infrastructure/Persistence/CustomerReviewConfiguration.cs` | Confirm `dbo.CustomerReviews.Title` column exists with `nvarchar(100)`. If not, add an EF Core 9 migration (`dotnet ef migrations add AddCustomerReviewTitle`). |
| BS-TC-003 | Test Case | `12-BS-TC-003-review-too-short.example.md` | No change — test still valid. |
| BS-TC-020 *(new)* | Test Case | (to be created) | New unit test `Title_Length_Boundaries_Are_Enforced` covering 4-char title (rejected), 5-char (accepted), 100-char (accepted), 101-char (rejected). |

## Artifacts NOT affected

- BS-ADR-001 — the validation strategy already accommodates new rules; this change is exactly the kind of evolution Option B was chosen to support. A `[StringLength]` attribute on `Title` is added in-place.
- BS-NFR-001 (performance), BS-NFR-002 (compliance), BS-NFR-003 (scalability) — adding one length check does not move any of these targets.
- BS-UC-002 *(Moderate Customer Reviews)* — its inputs change *favourably* (fewer broken titles), but no contract change.
- Existing test cases BS-TC-001, BS-TC-002, BS-TC-004, BS-TC-005, BS-TC-006, BS-TC-007 — none of them assert anything about title length, so all still pass; M3 gate does not require them to be touched.
- Database schema — if `dbo.CustomerReviews.Title` already exists with a wide `nvarchar`, the new rule tightens the application-level bound but does not require an EF Core migration. Otherwise: a single `dotnet ef migrations add ...` covers it.

## Recommended dispatch order

1. **Product Owner** — update **BS-REQ-001** and **BS-UC-001** (Change mode); record the new business rule **BS-BR-003**.
2. **M1 gate** — Traceability re-validates REQ→UC links; check that the new alt-F course is referenced from REQ-001 acceptance criterion 7.
3. **Analyst** — update **BS-RB-001** (Change mode); add new controllers and ensure ICONIX connection rules still hold.
4. **M2 gate** — Traceability re-validates UC→RB links; check that every new sentence in UC-001 has a matching controller in RB-001.
5. **Developer + Tester (parallel)**
   - Developer — update **BS-SD-001** and the `CustomerReview.cs` entity (add `Title` property + attributes); generate EF Core migration if needed.
   - Tester — author **BS-TC-020** (`[Theory]` boundary test for title length); extend the test plan inventory.
6. **M3 gate** — Traceability re-validates SD→CLS→TC links; confirm `IsBookReviewTitleLengthOk` controller maps to the `[StringLength]` attribute on `Title` *and* is exercised by BS-TC-020.

## Effort estimate

| Phase | Effort | Notes |
|---|---|---|
| Product Owner | 30 min | Edit two markdown files. |
| Analyst | 45 min | Two new controllers + one new error path on the diagram. |
| Developer | 1 h | Add `Title` property + attributes; one-line EF mapping; `dotnet ef migrations add AddCustomerReviewTitle` if the column is new. |
| Tester | 1 h | One new `[Theory]` boundary test. |
| **Total** | **~3.5 h** | |

This is the cheap-end of an ICONIX change because BS-ADR-001 made validation extensible by design. Without that ADR, a similar change would have required modifying a separate FluentValidation `AbstractValidator<CustomerReview>` *and* the entity — more files, more risk of drift between the two.
