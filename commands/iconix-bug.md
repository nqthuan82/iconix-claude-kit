---
description: "Triage a bug as Type 1 (code defect) or Type 2 (design defect). Reviewer-only — no fixes."
argument-hint: "<bug description, source path, or UC-ID>"
---

Invoke the iconix-reviewer agent in **bug-triage mode** with: $ARGUMENTS

For larger bugs with stack traces or extended reproduction steps, the user can fill in `docs/iconix/templates/bug-report-template.md`, save it under `bug-reports/BUG-<date>-<slug>.md`, and pass the saved path as $ARGUMENTS — the Reviewer treats the file like any other source pointer.

The Reviewer should follow its `# Bug triage` workflow (book Ch11 — *Code Review and Model Update*; Top 10 #1: "it's also a Model Update session, not just a Code Review").

1. Resolve $ARGUMENTS to the affected source file(s) and read their `Traceability:` comments to find UC-XXX and SD-XXX.
   - If $ARGUMENTS is a UC-ID, start there and find the implementing source files.
   - If $ARGUMENTS is a source path, read its traceability comment.
   - If $ARGUMENTS is a free-text description with no source pointer, ask the user for a file path or UC-ID before proceeding — do not guess.
2. Read the cited UC and SD; compare the code against the SD.
3. Classify the defect:
   - **Type 1 — Implementation bug** — code diverges from a correct SD. Design is right; code is wrong.
   - **Type 2 — Design bug** — code matches the SD but behaviour is still wrong. The SD/UC/RB describes the wrong thing.
4. Produce a review report at `reviews/REVIEW-<today>-bug-<slug>.md` with the agent's standard `## Bug triage` block: type, root artifact, affected UC, one-sentence rationale, recommended next step.
5. State the recommended next step explicitly:
   - **Type 1** → Developer bug-fix mode → Tester bug-verification mode (no ICONIX artifacts change; traceability chain stays intact)
   - **Type 2** → `/iconix-impact UC-XXX` → REQ change flow (full pipeline scoped to the blast radius)
6. If a recurring defect pattern surfaced during triage, append it to `reviews/review-checklist.md` (Ch11 Top 10 #6 — accumulate boilerplate checklists for future reviews).

Do not modify code or artifacts — triage only. The Type 1 fix and the Type 2 REQ change flow are separate, subsequent invocations the user runs after accepting the verdict.
