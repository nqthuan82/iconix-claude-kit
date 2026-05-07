# Interview: Sarah Patel (Customer Care Lead) — 2026-04-16

## Metadata
- **Interviewer:** Matt Stephens (Analyst)
- **Duration:** 35 minutes
- **Recording:** internal://meet-recordings/2026-04-16-sarah-patel.mp4
- **Project:** Internet Bookstore
- **Next review:** 2026-04-18 (REQ + UC draft due)

## Stakeholder profile
- **Role:** Customer Care Lead — first line of contact for customer complaints and content disputes ← candidate Actor (proxy for Customer + Moderator)
- **Primary goals with the system:** Customer Care reads incoming complaints and assigns them to internal staff; Sarah does not personally moderate reviews, but she will brief whoever does.
- **Frequency of use:** daily (complaint queue); the moderation tool would be used by **two new "Moderator" staff** that her team is hiring.

## Current state — how it works today
There is no review feature on the bookstore today. Customers email customer-care@bookstore.com when they want to praise or complain about a book. Care logs the email, replies, and discards it. Nothing is shown to other customers. Doug has been asking for this since the site launched.

## Pain points
- "We get the same five questions about every popular book — *Is it any good?* — and we have nothing to point people at."
- "When a customer does email us a review, it dies in our inbox."
- "Publishers keep asking us why we have no social proof."

## Desired future state (outcomes, not solutions)
- *"I want a logged-in customer to be able to share their take on a book in writing, on the book's own page."*
- *"I want a moderator to be able to review pending submissions before they appear publicly."*
- *"I want abusive or empty submissions to never reach the moderator's queue at all."*

## Scenario walkthrough — *Customer leaves a five-star review*

> Asked: "Walk me through how you imagine a customer would do this."

| Step | Who | Action / Response |
|---|---|---|
| 1 | Customer | Browses to the **Book Detail page** for the book they want to review. |
| 2 | Customer | Clicks the **Write Review** button. |
| 3 | System | If the Customer is not logged in, takes them to the **Login page** first, then back. |
| 4 | System | Shows the **Write Review page** with the book title, an empty review text area, and a 1–5 star selector. |
| 5 | Customer | Types the review and selects a star rating, then clicks **Send**. |
| 6 | System | Validates the input and shows the **Confirmation page** ("Thanks — your review will be reviewed by our team"). |
| 7 | System | Sends the review to the **Pending Reviews Queue** for moderation (separate use case). |

### What if it fails?
- If the Customer enters fewer than 10 characters of review text, the system rejects the review and re-displays the Write Review page with the typed text intact and an error message.
- If the Customer enters more than 1 MB of review text, the system rejects the review and shows an explanatory message.
- If the Customer's star rating is not in the range 1–5 (e.g., from a tampered HTML page), the system rejects the review.
- If the Book ID in the URL does not exist, the system shows the existing **Book Not Found page** (the page used by the Show Book Details flow).

## Constraints (NFR seeds)
| Category | Stated constraint | Measurable target (fill in or ask) |
|---|---|---|
| Performance | "Submit feels snappy, no slower than the rest of the site" | < 2 s p95 from Send-click to Confirmation page. |
| Security / compliance | "Logged-in only — no anonymous reviews" | All submissions tied to an authenticated `Customer`. |
| Compliance | "Nothing goes public without a moderator" | 100% of submissions enter pending state, never published state, on submit. |
| Availability | "Same as the rest of the storefront" | 99.9% monthly — inherits the storefront SLO; no new target. |
| Scale / volume | "We expect ~5,000 submissions/day at peak" | Pending Reviews Queue must accept 50 submissions/second burst. |

## Open questions / parking lot
- [ ] Multiple reviews per Customer per Book? Sarah leans no, "but it is not a hill I will die on" — defer to Doug.
- [ ] Email Customer when their review is published? "Yes eventually, but not in v1."

---

## Analyst summary
> Hand-off to the Product Owner agent.

- **Candidate actors:** Customer (primary), Moderator (secondary, addressed in a separate use case).
- **Candidate use cases:**
  - Customer writes Customer Review *(this thread)*
  - Moderator moderates Customer Reviews *(separate thread)*
- **Candidate REQs:**
  - The system shall allow a logged-in Customer to submit a Customer Review consisting of a Book Review (10 chars to 1 MB) and a Book Rating (1–5 stars) for a Book.
  - The system shall add every submitted Customer Review to the Pending Reviews Queue and shall not display it on the Book Detail page until approved.
  - The system shall reject submissions whose Book Review length is outside `[10, 1 MB]` or whose Book Rating is outside `[1, 5]`.
- **Candidate NFRs:** performance (`<2 s p95`), compliance (no review visible without moderation), scalability (50 submissions/s peak).
- **Gaps / must clarify before extraction:**
  - [ ] Multiple reviews per Customer per Book — defer to v2 *(confirmed with Doug 2026-04-16)*.
  - [ ] Email notification on publish — defer to v2 *(confirmed with Doug 2026-04-16)*.
