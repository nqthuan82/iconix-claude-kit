# ICONIX Commit Message Conventions

Provider-neutral commit format. Works the same on any git host.

## Format

```
[<artifact-id>] <phase>: <imperative summary>

<optional body — what changed and *why*; reference past decisions where relevant>

[Traceability: <upstream IDs>]    ← optional footer, when commit touches a single UC
[<work-item-prefix><N>]           ← optional, see "Work-item linking" below
```

- `<artifact-id>` — the primary artifact this commit serves (e.g., `UC-017`, `REQ-044`, `BUG-T1`, `BUG-T2-UC-017`, `ARCH`).
- `<phase>` — one of `M1` (requirements), `M2` (preliminary design), `M3` (critical design), `Impl` (implementation), `Fix`, `Doc`, `Refactor`, `Chore`.
- `<imperative summary>` — one line, ≤72 chars, present tense imperative ("add", not "added"; "fix", not "fixed").

## Examples

```
[UC-017] M1: draft place-bet use case and link REQ-044

Two-column flow with three alternate courses (insufficient balance,
duplicate bet ID, ledger write timeout).

Traceability: UC-017 → REQ-044, REQ-051

AB#3421
```

```
[UC-017] M2: robustness diagram + container mapping

[ARCH] M2: extract PaymentProvider interface

[UC-017] M3: sequence diagram + 6 test cases

[UC-017] Impl: PlaceBetController + service layer

[BUG-T1] Fix: BetController returns 400 on negative balance

Code drifted from SD-017 step 5 (the validation arrow was missing
the early-return). No artifact changes.

#42
```

## Phase tag rules

| Tag | When | What's in the diff |
|---|---|---|
| `M1` | Product Owner phase | `requirements/`, `use-cases/`, `glossary.md`, `domain-model/` (initial) |
| `M2` | Analyst + Architect phase | `robustness/`, `domain-model/` (refined), `container-mapping/`, `adrs/`, `nfr-annotations/` |
| `M3` | Developer + Tester phase (design) | `sequence/`, `class-model/`, `test-cases/`, `features/`, `test-plan/`, `test-matrices/` |
| `Impl` | Implementation phase | `src/`, `tests/` (added or changed); files must carry `Traceability:` comments |
| `Fix` | Bug fix | After Reviewer triage. T1 = `src/` only; T2 = scoped artifacts + `src/` |
| `Doc` | Documentation | Generated user/dev/API docs; `README.md`, `CHANGELOG.md` |
| `Refactor` | Methodology-neutral cleanup | Code restructure with no behaviour change; no artifact changes |
| `Chore` | Build, deps, infra | `iconix.config.yaml` tweaks, dependency bumps, formatting |

## Don't mix phases in one commit

A commit tagged `[UC-017] M2: ...` should not contain code changes; that would belong to a separate `[UC-017] Impl: ...` commit. The Reviewer surfaces mixed-phase commits as drift.

## Work-item linking (optional)

Set `git.work_item_prefix` in `iconix.config.yaml`:

| Provider | Prefix | Example |
|---|---|---|
| GitHub | `#` | `#42` (auto-links to issue 42) |
| Azure DevOps | `AB#` | `AB#3421` (auto-links to Azure Boards work item 3421) |
| GitLab | `#` (issue), `!` (MR) | `#101` |
| Bitbucket | none / `[]` | implicit via branch name |

When set, `iconix-git` adds the work-item ref as a footer line on commits and includes it in PR descriptions. Empty string disables linking entirely (kit default).

## Squashing strategy

Phase PRs (M1/M2/M3) **squash** to one commit per phase per UC. The squash commit message follows the format above. The Implementation PR can squash or preserve individual `[UC-017] Impl: ...` commits, depending on team preference (`git.impl_squash` config; default: preserve).

This keeps `git log` readable: one line per phase per UC, plus implementation history.
