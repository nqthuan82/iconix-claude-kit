<!-- Default ICONIX PR template for Azure DevOps.
     Place phase-specific templates next to this file:
     - m1.md, m2.md, m3.md, implementation.md
     Azure DevOps loads these from `.azuredevops/pull_request_templates/`. -->

## Summary
<one sentence — what this PR delivers>

## Phase
- [ ] M1 — Requirements
- [ ] M2 — Preliminary Design
- [ ] M3 — Critical Design
- [ ] Implementation
- [ ] Bug fix — Type 1 (code-only)
- [ ] Bug fix — Type 2 (rejoins REQ change flow)

## Artifacts touched
<list UC/RB/SD/TC IDs>

## Traceability
<paste the chain, e.g. UC-017 → REQ-044 → RB-017 → SD-017 → TC-031>

## Reviewer checklist
- [ ] Phase tag in commit messages matches the artifacts in the diff
- [ ] No mixed-phase commits
- [ ] Every changed source file carries a `Traceability:` comment
- [ ] ICONIX traceability gate (build) is green
- [ ] If M2/M3, milestone gate (`/iconix-status`) reports ready

## Work item
AB#<N>   <!-- auto-link to Azure Boards work item; set git.work_item_prefix = "AB#" in iconix.config.yaml -->
