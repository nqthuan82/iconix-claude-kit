#!/usr/bin/env bash
# setup-branch-protection.sh — Configure GitHub branch protection for ICONIX CI gates.
#
# Run once after install to turn advisory CI checks into enforced merge gates.
# After running, PRs that fail the ICONIX traceability check cannot be merged.
#
# Prerequisites:
#   - gh CLI installed and authenticated (gh auth login)
#   - The ICONIX Validate workflow must have run at least once on a PR so that
#     GitHub registers the check name. If it hasn't run yet, push a test branch
#     first, then re-run this script.
#
# Usage:
#   bash .ci/scripts/setup-branch-protection.sh
#   bash .ci/scripts/setup-branch-protection.sh --dry-run
#   bash .ci/scripts/setup-branch-protection.sh --min-reviewers 2
#   bash .ci/scripts/setup-branch-protection.sh --also-branch develop   # gitflow
#   bash .ci/scripts/setup-branch-protection.sh --enforce-admins        # stricter
#
# To verify after running:
#   GitHub repo → Settings → Branches → main → Edit

set -euo pipefail

# ── Defaults ─────────────────────────────────────────────────────────────────
BRANCH="main"
EXTRA_BRANCH=""
MIN_REVIEWERS=1
ENFORCE_ADMINS=false
DRY_RUN=false

# The GitHub Actions job display name from .github/workflows/iconix-validate.yml.
# GitHub registers it as a required check context using this exact string.
# Run the helper command below if unsure:
#   gh api "repos/{owner}/{repo}/commits/$(git rev-parse HEAD)/check-runs" \
#     --jq ".check_runs[].name"
CHECK_NAME="Traceability gate"

# ── Argument parsing ──────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --branch)          BRANCH="$2"; shift 2 ;;
    --also-branch)     EXTRA_BRANCH="$2"; shift 2 ;;
    --min-reviewers)   MIN_REVIEWERS="$2"; shift 2 ;;
    --enforce-admins)  ENFORCE_ADMINS=true; shift ;;
    --dry-run)         DRY_RUN=true; shift ;;
    --check-name)      CHECK_NAME="$2"; shift 2 ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

# ── Auto-detect gitflow ───────────────────────────────────────────────────────
# If iconix.config.yaml declares branch_strategy: gitflow, also protect develop.
if [[ -z "$EXTRA_BRANCH" && -f "iconix.config.yaml" ]]; then
  if grep -qE 'branch_strategy:\s*"?gitflow"?' "iconix.config.yaml" 2>/dev/null; then
    EXTRA_BRANCH="develop"
    echo "  ℹ gitflow detected — will also protect '$EXTRA_BRANCH'"
  fi
fi

# ── Core function ─────────────────────────────────────────────────────────────
protect_branch() {
  local branch="$1"
  echo "→ Applying branch protection to '$branch' ..."

  local payload
  payload=$(cat <<JSON
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["$CHECK_NAME"]
  },
  "enforce_admins": $ENFORCE_ADMINS,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": $MIN_REVIEWERS
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
)

  if [[ "$DRY_RUN" == true ]]; then
    echo "  [dry-run] PUT repos/{owner}/{repo}/branches/${branch}/protection"
    echo "$payload" | sed 's/^/  /'
    return
  fi

  gh api \
    --method PUT \
    "repos/{owner}/{repo}/branches/${branch}/protection" \
    --input - <<< "$payload" \
    --silent

  echo "  ✓ '$branch' now enforces:"
  echo "    required check : '$CHECK_NAME' (strict — head must be up-to-date)"
  echo "    PR reviews      : min $MIN_REVIEWERS (stale reviews dismissed on push)"
  echo "    force pushes    : blocked"
  echo "    direct pushes   : blocked"
  echo "    enforce admins  : $ENFORCE_ADMINS"
}

# ── Main ──────────────────────────────────────────────────────────────────────
echo "ICONIX Branch Protection Setup — GitHub"
echo "========================================"
[[ "$DRY_RUN" == true ]] && echo "(dry-run mode — no changes will be made)"
echo ""

protect_branch "$BRANCH"
[[ -n "$EXTRA_BRANCH" ]] && protect_branch "$EXTRA_BRANCH"

echo ""
echo "Done. ICONIX CI gates are now enforced gates — PRs cannot merge if the"
echo "traceability check fails."
echo ""
if [[ "$DRY_RUN" != true ]]; then
  echo "Verify at: $(gh repo view --json url -q .url)/settings/branches"
  echo ""
  echo "Note: if '$CHECK_NAME' isn't recognised yet, push a PR branch to trigger"
  echo "the workflow, then re-run this script. GitHub must see the check at least once"
  echo "before it can be added as a required check."
fi
