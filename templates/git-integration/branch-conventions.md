# ICONIX Git Branch Conventions

Provider-agnostic branch naming used by `iconix-git` and `/iconix-pr`. These work the same on GitHub, Azure DevOps, GitLab, Bitbucket, or any plain git host.

## Branch types

| Pattern | Purpose | Lifetime | Merges to |
|---|---|---|---|
| `feature/UC-<id>-<slug>` | One per use case, all phases | Bootstrap → release | `main` (via milestone PRs) |
| `arch/<scope>` | Cross-UC architecture work | One iteration | `main` |
| `bugfix/T1-<slug>` | **Type 1** — code drift; no artifacts change | Short | `main` |
| `bugfix/T2-UC-<id>-<slug>` | **Type 2** — design defect; rejoins REQ change flow | Same as feature | `main` |
| `hotfix/T1-<slug>` | Emergency Type 1 against a release | Very short | `main` and `release/*` |
| `release/<version>` | Release prep / stabilization | Cuts → tag | `main` |

`<id>` is the artifact ID without prefix (e.g., `UC-017` → `017`). `<slug>` is a kebab-case 2-5 word summary (e.g., `place-bet-negative-balance`).

## Examples

```
feature/UC-017-place-bet
arch/payment-provider-abstraction
bugfix/T1-bet-controller-status-code
bugfix/T2-UC-017-balance-validation
hotfix/T1-jackpot-payout-overflow
release/2.4.0
```

## When to create which

- **Starting a new use case?** → `feature/UC-<id>-<slug>`. Created at M1 entry; lives until the Implementation PR merges.
- **Reviewer triages a Type 1 bug?** → `bugfix/T1-<slug>`. No artifact files in this branch — code only.
- **Reviewer triages a Type 2 bug?** → `bugfix/T2-UC-<id>-<slug>`. This branch will accumulate REQ/UC/RB/SD/TC changes through the scoped REQ change flow, then code.
- **Architect doing cross-UC work?** → `arch/<scope>`. PRs to `main`; downstream UCs rebase or merge from `main` once landed.
- **Emergency fix in production?** → `hotfix/T1-<slug>`. Cherry-pick or merge into both `main` and the active `release/*` branch.

## Strategy options (configurable)

`iconix.config.yaml` `git.branch_strategy` selects:

- `trunk` (default) — all branches above merge directly to `main`. Releases are tag-based (`release/2.4.0` is short-lived, used only for stabilization).
- `gitflow` — adds a permanent `develop` branch; `feature/*` and `arch/*` merge to `develop`; `release/*` merges to both `main` and `develop`; `hotfix/*` merges to both. Use only if your org has strict release-train requirements.

The kit's automation defaults to **trunk**.
