---
description: "Run an ICONIX review on current changes. Checks code vs sequence diagrams, class model, and traceability."
---

Invoke the iconix-reviewer agent. Ask it to:

1. Run `git diff` (or inspect recent commits) to identify changed files under `src/` and `tests/`
2. For each changed file, locate its traceability comment (`UC-XXX | RB-XXX | SD-XXX`) and load the referenced artifacts
3. Check for drift: methods in code vs messages on the sequence diagram, classes in code vs the class model
4. Check NFR hints from `nfr-annotations/UC-XXX-nfr.md` for each touched UC
5. Produce a review report at `reviews/REVIEW-<today>-<scope>.md` with recommendation: BLOCK MERGE | REQUEST CHANGES | APPROVE WITH NOTES | APPROVE

Do not modify any code — review only.
