# BS-REQ-001: Submit a moderated Customer Review for a Book

## Statement
The system shall allow a logged-in Customer to submit a Customer Review for an existing Book, consisting of a Book Review of 10 characters to 1 MB and a Book Rating of 1–5 stars; the system shall add every submitted Customer Review to the Pending Reviews Queue and shall not display it on the Book Detail page until a Moderator approves it.

## Rationale
Customer Care receives daily requests to share opinions about books and has nowhere to route them. Publishers want social proof on book pages. The bookstore needs a controlled channel for reader opinions that prevents spam and abusive content from reaching shoppers — hence the mandatory moderation step before publication. This requirement implements the customer-care request captured in `BOOK-412` (Doug Rosenberg, 2026-04-15) and the workflow described in the interview with Sarah Patel on 2026-04-16.

## Acceptance criteria
- [ ] A logged-in Customer on a Book Detail page can submit a Book Review (10 chars ≤ length ≤ 1 MB) with a Book Rating in `[1..5]`, and receives a Confirmation page within 2 seconds (p95).
- [ ] An unauthenticated user clicking **Write Review** is sent through the Login flow and returned to the Write Review page.
- [ ] A submitted Customer Review is present in the Pending Reviews Queue immediately after the Confirmation page is shown, and is **not** present on the Book Detail page.
- [ ] A submission with a Book Review shorter than 10 characters or longer than 1 MB is rejected; the Customer is shown an error message explaining why and is returned to the Write Review page with the entered text preserved.
- [ ] A submission whose Book Rating is outside `[1..5]` is rejected with an error message.
- [ ] A submission for a Book ID that does not exist is shown the existing **Book Not Found page**.

## Examples
- **Example 1:** Customer submits *"A surprisingly clear introduction to OO design. Recommended."* (78 characters) with a 4-star rating → Confirmation page shown; review queued for moderation.
- **Example 2:** Customer submits *"good"* (4 characters) → review rejected; Write Review page redisplayed with entered text and a "must be at least 10 characters" message.
- **Counter-example:** Customer submits a tampered request with a 7-star rating → review rejected; not added to queue; not visible anywhere on the storefront.

## Priority
**P0** — required for the Q3 *Reviews & Ratings* release.

## Traceability
- **Source:** Email `BOOK-412` from Doug Rosenberg (2026-04-15); Sarah Patel interview transcript (2026-04-16); feature request [`03-feature-request.example.md`](./03-feature-request.example.md).
- **Downstream UCs:** [BS-UC-001](./05-BS-UC-001-write-customer-review.example.md) — *Customer writes a moderated Customer Review*.
- **Related NFRs:**
  - BS-NFR-001 (Performance — Confirmation page within 2 s p95)
  - BS-NFR-002 (Compliance — no review public without moderation)
  - BS-NFR-003 (Scalability — 50 submissions/s peak)
- **Related BRs:**
  - BS-BR-001 — Book Review length must be in `[10, 1 MB]`.
  - BS-BR-002 — Book Rating must be an integer in `[1, 5]`.
