# Customer writes a moderated Customer Review on a Book

## Story (Connextra)
**As a** logged-in Customer browsing a Book
**I want** to leave a star rating and a written review on the book's detail page
**So that** other Customers can use my opinion when deciding whether to buy

## Context / problem
The bookstore has no review feature today. Customers email Care to share opinions, and those opinions never reach other shoppers. Publishers and Customer Care both want a moderated review feature so that the bookstore can show social proof without exposing the storefront to spam or abuse. See the originating email thread `BOOK-412` and the interview with Sarah Patel (Customer Care Lead) on 2026-04-16.

## Acceptance criteria (Gherkin)

```gherkin
Feature: Submit a moderated review for a book

  Scenario: Basic — logged-in Customer submits a valid review
    Given a Customer is logged in
    And the Customer is on the Book Detail page for an existing Book
    When the Customer clicks the Write Review button
    Then the system displays the Write Review page

    When the Customer enters a 200-character Book Review and selects 4 stars
    And clicks Send
    Then the system displays the Confirmation page
    And the system adds the Customer Review to the Pending Reviews Queue
    And the Customer Review is not visible on the Book Detail page

  Scenario: Alternate — Customer is not logged in
    Given a Customer is not logged in
    And the Customer is on the Book Detail page for an existing Book
    When the Customer clicks the Write Review button
    Then the system invokes the Login flow
    And after successful login the system displays the Write Review page

  Scenario: Alternate — review text is too short
    Given a logged-in Customer is on the Write Review page
    When the Customer enters a 5-character Book Review and selects 3 stars
    And clicks Send
    Then the system rejects the review
    And the system re-displays the Write Review page with the entered text
    And the system shows the message "Review text must be at least 10 characters"

  Scenario: Alternate — review text is too long
    Given a logged-in Customer is on the Write Review page
    When the Customer enters a Book Review larger than 1 MB
    And clicks Send
    Then the system rejects the review
    And the system shows a message explaining why the review was rejected

  Scenario: Alternate — Book Rating outside allowed range
    Given a logged-in Customer is on the Write Review page
    When a Book Rating outside 1..5 reaches the system (via tampered form data)
    Then the system rejects the review
    And the system shows the message "Rating must be between 1 and 5"
```

## Out of scope
- The Moderator's approval workflow — covered by a separate use case (*Moderate Customer Reviews*).
- Editing or deleting a review after submission.
- Reviewer reputation, helpful-vote counts, photo attachments.
- Showing reviews on the Book Detail page (separate change in *Show Book Details*).
- Email notifications on publish — deferred to v2.
- Multiple reviews per Customer per Book — deferred to v2.

## NFR notes
| Category | Constraint | Measurable target |
|---|---|---|
| Performance | Submit feels snappy | Send-click to Confirmation page < 2 s p95 (BS-NFR-001). |
| Compliance | No review visible without moderator approval | 100% of submitted reviews enter pending state on submit (BS-NFR-002). |
| Scalability | Peak burst | Pending Reviews Queue accepts ≥50 submissions/s (BS-NFR-003). |
| Security | Authentication required | Submissions without an authenticated CustomerSession are redirected through Login. |

## UI / screens
- **Book Detail page** — existing screen. Adds one new control: **Write Review** button.
- **Write Review page** — new. Controls: review text area, 1–5 star selector, **Send** button.
- **Confirmation page** — new. Static "thanks" message with a link back to the Book Detail page.
- **Login page** — existing. Reused as-is.
- **Book Not Found page** — existing. Reused as-is when the URL points at a missing book.

## Dependencies and assumptions
- **Depends on:** existing CustomerSession / Login flow; existing Book Detail page; existing Pending Reviews Queue infrastructure (ticket `INFRA-88`).
- **Assumes:** the Moderator role and tooling (use case *Moderate Customer Reviews*) is delivered by 2026-06-30 — review-publication value is not realised before then.

## INVEST self-check
- [x] **Independent** — does not require Moderator UI to ship.
- [x] **Negotiable** — alternate courses (e.g., minimum length) can be discussed.
- [x] **Valuable** — Customer Care, Publishers, Doug all named the benefit.
- [x] **Estimable** — fits one sprint for one engineer.
- [x] **Small** — UC will fit two paragraphs (see UC-001).
- [x] **Testable** — every "Then" clause is observable.

## Priority
**P0** — must have for the Q3 release.

## Linked artifacts
- **Parent epic:** EPIC-Reviews-and-Ratings
- **REQs:** [BS-REQ-001](./04-BS-REQ-001-submit-customer-review.example.md)
- **UCs:** [BS-UC-001](./05-BS-UC-001-write-customer-review.example.md)
