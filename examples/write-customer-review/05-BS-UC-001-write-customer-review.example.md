# BS-UC-001: Write Customer Review

## Metadata
- **ID:** BS-UC-001
- **Actor(s):** Customer (primary); Moderator (secondary, downstream — handled by *Moderate Customer Reviews*)
- **Preconditions:**
  - The Customer has navigated to the Book Detail page for an existing Book.
  - The CustomerSession exists in the HTTP session (anonymous or authenticated).
- **Postconditions:**
  - **Success:** A new CustomerReview is on the Pending Reviews Queue. The Confirmation page is displayed. The review is **not** visible on the Book Detail page until moderated.
  - **Rejection:** No CustomerReview is created or queued. The Customer is on the Write Review page with their entered text preserved and an error message visible.

## Basic Course

| User Action | System Response |
|---|---|
| 1. On the Book Detail page for the Book currently being viewed, the Customer clicks the **Write Review** button. | 1. The system retrieves the CustomerSession and confirms the Customer is logged in. |
| 2. *(none — system step)* | 2. The system displays the **Write Review page** with the Book title and an empty form (review text area, 1–5 star selector, **Send** button). |
| 3. The Customer types a Book Review (≥ 10 chars, ≤ 1 MB), selects a Book Rating between 1 and 5 stars, and clicks **Send**. | 3. The system validates that the Book Review length is in `[10, 1 MB]` and that the Book Rating is in `[1..5]`. |
| 4. *(none — system step)* | 4. The system creates a CustomerReview from the form data, associates it with the Book and the Customer, and adds it to the Pending Reviews Queue. |
| 5. *(none — system step)* | 5. The system displays the **Confirmation page**. |

## Alternate Course A: Customer is not logged in

| User Action | System Response |
|---|---|
| A1. The Customer clicks **Write Review** on the Book Detail page while not logged in. | A1. The system retrieves the CustomerSession, sees that the Customer is not logged in, and invokes the **Login** use case. |
| A2. The Customer completes Login successfully. | A2. The system displays the Write Review page; flow continues from Basic Course step 3. |

## Alternate Course B: Book Review text is too short

| User Action | System Response |
|---|---|
| B1. From step 3 of the Basic Course, the Customer submits a Book Review shorter than 10 characters. | B1. The system rejects the submission, re-displays the Write Review page with the entered text preserved, and shows the message *"Review text must be at least 10 characters."* No CustomerReview is created. |

## Alternate Course C: Book Review text is too long

| User Action | System Response |
|---|---|
| C1. From step 3 of the Basic Course, the Customer submits a Book Review larger than 1 MB. | C1. The system rejects the submission, re-displays the Write Review page, and shows the message *"The review you entered is a novel in itself; please try to shorten it."* No CustomerReview is created. |

## Alternate Course D: Book Rating is outside the allowed range

| User Action | System Response |
|---|---|
| D1. From step 3 of the Basic Course, a Book Rating outside `[1..5]` reaches the system (typically from a tampered HTML form). | D1. The system rejects the submission, re-displays the Write Review page, and shows the message *"Rating must be between 1 and 5."* No CustomerReview is created. |

## Alternate Course E: Book ID does not exist

| User Action | System Response |
|---|---|
| E1. The Customer arrives at the Write Review page via a URL whose Book ID does not exist. | E1. The system displays the existing **Book Not Found page** (reused from *Show Book Details*). |

## Traceability
- **Requirements:** BS-REQ-001 — *Submit a moderated Customer Review for a Book*.
- **Robustness diagram:** [BS-RB-001](./06-BS-RB-001-write-customer-review.example.puml).
- **Sequence diagram:** [BS-SD-001](./08-BS-SD-001-write-customer-review.example.puml).
- **Test cases:**
  - [BS-TC-001](./10-BS-TC-001-display-write-review-page.example.md) — Display Write Review page (basic course).
  - [BS-TC-002](./11-BS-TC-002-rating-out-of-range.example.md) — Rating out of range (alt D).
  - [BS-TC-003](./12-BS-TC-003-review-too-short.example.md) — Review too short (alt B).
  - [BS-TC-004](./13-BS-TC-004-not-logged-in.example.md) — Customer not logged in (alt A).
- **Domain entities introduced or used:** Book, Customer, CustomerSession, CustomerReview, BookRating (value), BookReview (value), PendingReviewsQueue.
- **Invokes:** *Login* use case (alt A); *Moderate Customer Reviews* use case (downstream, separate thread).
