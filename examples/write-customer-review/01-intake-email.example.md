# Email request: Reader reviews on book pages — 2026-04-15

## Source
- **From:** Doug Rosenberg, Editor-in-Chief
- **To:** Bookstore product team
- **Thread / ticket:** BOOK-412
- **Received:** 2026-04-15

## Verbatim text
> Team — quick one. Several of our biggest publishers have been asking for reader reviews on book pages, the way Amazon and SpringerOnline do it. Customers want to share their take and we want the social proof. Logged-in customers should be able to leave a star rating and a written review on any book. Reviews shouldn't go live immediately — we need a moderator to approve them first, otherwise we'll end up with spam and worse. Make it work like the rest of the site. Thanks. — Doug

---

## PO restatement
> Filled in by the Product Owner agent during intake. Every inference is marked with `[VERIFY]` until confirmed.

### Stated request (paraphrase in one sentence)
Allow logged-in customers to submit a star-rated written review of any book, and route the review through a moderator before it appears publicly.

### Inferred goal `[VERIFY]`
*Customer wants to share an opinion about a book they have read, so that other customers can use that opinion when deciding whether to buy.* — observable behaviour, not a UI choice.

### Inferred actor(s) `[VERIFY]`
- **Customer** — logged-in user submitting the review. `[VERIFY]`
- **Moderator** — bookstore staff member who approves or rejects pending reviews. `[VERIFY]` (Doug said "we need a moderator" — confirm whether this is a new role or an existing one.)

### Inferred scope
**In:**
- Submitting a written review with a 1–5 star rating from a book detail page.
- Putting the submitted review onto a "pending moderation" queue.

**Out:**
- The moderator's approval workflow itself (separate use case: *Moderate Customer Reviews*).
- Editing or deleting a review after submission.
- Showing reviews on the book detail page (separate use case: *Show Book Details*).
- Reviewer reputation, helpfulness votes, photo uploads — anything Amazon does that Doug did not explicitly ask for.

### Constraints / NFR seeds
| Category | Stated or inferred | Measurable target |
|---|---|---|
| Security | Logged-in customers only | All review submissions tied to an authenticated `Customer`. `[VERIFY]` |
| Compliance | Spam / abusive content cannot appear without moderator approval | 100% of submitted reviews enter pending state, never published state, on submit. `[VERIFY]` |
| Performance | "Make it work like the rest of the site" | Submit acknowledged within 2 s p95. `[VERIFY]` |
| Data integrity | Implicit: rating must be a real number of stars | Rating must be integer in `[1..5]`. `[VERIFY]` — derived from "star rating" wording. |
| Data integrity | Implicit: review text bounds | Min 10 chars, max 1 MB. `[VERIFY]` — derived from preventing empty/spam and abusive payloads. |

### Ambiguities — must clarify before extraction
- [x] Confirmed (offline, 2026-04-16): rating range is 1–5 stars, integer.
- [x] Confirmed: minimum review length 10 characters; maximum 1 MB; longer reviews rejected with an explanatory message.
- [x] Confirmed: if a customer is not logged in, send them through the existing Login flow then return them to the Write Review page with their draft preserved.
- [ ] Should a customer be allowed to leave more than one review per book? (Marked for v2.)
- [ ] Should the system notify the customer when their review is published? (Marked for v2.)

---

## Candidate artifacts

**Candidate REQs:**
- The system shall allow a logged-in Customer to submit a Customer Review consisting of a Book Rating (integer 1–5) and a Book Review text (10 chars to 1 MB) for a Book they are viewing. *(P0)*
- The system shall place every submitted Customer Review onto the Pending Reviews Queue and shall not publish it until a Moderator approves it. *(P0)*

**Candidate UC stubs:**

| UC title (noun-verb-noun) | Basic course outline |
|---|---|
| Customer writes Customer Review | Customer clicks Write Review on the Book Detail page → System checks login → System shows the Write Review page → Customer enters review text + star rating → System validates and adds to Pending Reviews Queue → System shows confirmation. |
| Moderator moderates Customer Reviews *(out of scope for this thread — separate UC)* | (handled in BOOK-413) |

**Candidate NFRs:**
- Performance: review submission acknowledged within 2 s p95 — feeds **BS-NFR-001**.
- Compliance: every submitted review must enter pending state before any public visibility — feeds **BS-NFR-002**.

---

## Status
- [x] **Ready** — open ambiguities resolved on 2026-04-16. Proceed to REQ + UC drafting.
- [ ] Blocked — pending clarification.
