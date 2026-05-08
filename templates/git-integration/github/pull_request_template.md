<!-- Default ICONIX PR template. For phase-specific templates, append
     ?template=m1.md, ?template=m2.md, ?template=m3.md, or
     ?template=implementation.md to the PR-create URL. -->

## Summary
<one sentence — what this PR delivers>

## Phase
- [ ] M1 — Requirements (REQs, UCs, glossary, initial domain model)
- [ ] M2 — Preliminary Design (RBs, refined domain model, container mapping, ADRs)
- [ ] M3 — Critical Design (SDs, class model, TCs, test plan)
- [ ] Implementation (code + tests)
- [ ] Bug fix — Type 1 (code-only)
- [ ] Bug fix — Type 2 (rejoins REQ change flow)

## Artifacts touched
<list the UC/RB/SD/TC IDs this PR adds or modifies>

## Traceability
<paste the relevant chain, e.g. UC-017 → REQ-044 → RB-017 → SD-017 → TC-031>

## Reviewer checklist
- [ ] Phase tag in commit messages matches the artifacts in the diff
- [ ] No mixed-phase commits (e.g., `[UC-017] M2:` should not include `src/` changes)
- [ ] Every changed source file carries a `Traceability:` comment
- [ ] ICONIX traceability gate (CI) is green
- [ ] If this is M2/M3, the matching milestone gate (`/iconix-status`) reports ready

## Work item / issue
<#NN or AB#NN — optional, see iconix.config.yaml git.work_item_prefix>
