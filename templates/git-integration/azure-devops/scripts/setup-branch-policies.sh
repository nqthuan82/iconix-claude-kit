#!/usr/bin/env bash
# setup-branch-policies.sh — Configure Azure DevOps branch policies for ICONIX CI gates.
#
# Run once after install to wire the ICONIX pipeline as a required build policy
# and to set a minimum reviewer count on the main branch.
# After running, PRs that fail the ICONIX traceability pipeline cannot be completed.
#
# Prerequisites:
#   - az CLI installed and logged in (az login)
#   - Azure DevOps extension: az extension add --name azure-devops
#   - The ICONIX pipeline already created from azure-pipelines-iconix-validate.yml
#     (Pipelines → New pipeline → YAML → select the yml file)
#
# Usage:
#   bash .ci/scripts/setup-branch-policies.sh \
#     --org https://dev.azure.com/myorg \
#     --project MyProject \
#     --repo MyRepo
#
#   # Preview without making changes:
#   bash .ci/scripts/setup-branch-policies.sh --dry-run \
#     --org https://dev.azure.com/myorg --project MyProject --repo MyRepo
#
#   # Custom options:
#   bash .ci/scripts/setup-branch-policies.sh \
#     --org https://dev.azure.com/myorg --project MyProject --repo MyRepo \
#     --branch main --min-reviewers 2
#
# To verify after running:
#   Azure DevOps → Project Settings → Repositories → <repo> → Policies → Branches → main

set -euo pipefail

# ── Defaults ─────────────────────────────────────────────────────────────────
ORG_URL=""
PROJECT=""
REPO=""
BRANCH="main"
MIN_REVIEWERS=1
DRY_RUN=false
PIPELINE_NAME="ICONIX Validate"

# ── Argument parsing ──────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --org)             ORG_URL="$2"; shift 2 ;;
    --project)         PROJECT="$2"; shift 2 ;;
    --repo)            REPO="$2"; shift 2 ;;
    --branch)          BRANCH="$2"; shift 2 ;;
    --min-reviewers)   MIN_REVIEWERS="$2"; shift 2 ;;
    --pipeline-name)   PIPELINE_NAME="$2"; shift 2 ;;
    --dry-run)         DRY_RUN=true; shift ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

# Validate required arguments
for arg_name in ORG_URL PROJECT REPO; do
  if [[ -z "${!arg_name}" ]]; then
    flag="--$(echo "$arg_name" | tr '[:upper:]' '[:lower:]' | tr '_' '-')"
    echo "ERROR: $flag is required" >&2
    echo "Run with --help for usage." >&2
    exit 1
  fi
done

# ── Main ──────────────────────────────────────────────────────────────────────
echo "ICONIX Branch Policy Setup — Azure DevOps"
echo "=========================================="
[[ "$DRY_RUN" == true ]] && echo "(dry-run mode — no changes will be made)"
echo ""
echo "  Org:      $ORG_URL"
echo "  Project:  $PROJECT"
echo "  Repo:     $REPO"
echo "  Branch:   $BRANCH"
echo ""

# Resolve repository ID
echo "→ Resolving repository ID ..."
REPO_ID=$(az repos show \
  --org "$ORG_URL" --project "$PROJECT" \
  --repository "$REPO" \
  --query "id" -o tsv)
echo "  ✓ Repo ID: $REPO_ID"

# Resolve build definition ID for the ICONIX pipeline
echo "→ Looking up '$PIPELINE_NAME' pipeline ..."
BUILD_DEF_ID=$(az pipelines build definition list \
  --org "$ORG_URL" --project "$PROJECT" \
  --name "$PIPELINE_NAME" \
  --query "[0].id" -o tsv 2>/dev/null || true)

if [[ -z "$BUILD_DEF_ID" ]]; then
  echo "" >&2
  echo "ERROR: Pipeline '$PIPELINE_NAME' not found in project '$PROJECT'." >&2
  echo "" >&2
  echo "Create it first:" >&2
  echo "  Azure DevOps → Pipelines → New pipeline → YAML" >&2
  echo "  Select the file: azure-pipelines-iconix-validate.yml" >&2
  echo "  Save and run it once, then re-run this script." >&2
  exit 1
fi
echo "  ✓ Pipeline ID: $BUILD_DEF_ID"

if [[ "$DRY_RUN" == true ]]; then
  echo ""
  echo "[dry-run] would create:"
  echo "  1. Build policy: pipeline '$PIPELINE_NAME' (ID $BUILD_DEF_ID) required on '$BRANCH'"
  echo "  2. Approver count policy: min $MIN_REVIEWERS reviewer(s) on '$BRANCH'"
  echo ""
  echo "Re-run without --dry-run to apply."
  exit 0
fi

# 1. Build validation policy: require ICONIX pipeline to pass before PR completion
echo "→ Creating build validation policy ..."
az repos policy build create \
  --org "$ORG_URL" --project "$PROJECT" \
  --blocking true \
  --branch "$BRANCH" \
  --build-definition-id "$BUILD_DEF_ID" \
  --display-name "ICONIX Validate — required" \
  --enabled true \
  --queue-on-source-update-only false \
  --manual-queue-only false \
  --valid-duration 0 \
  --repository-id "$REPO_ID" \
  --output none
echo "  ✓ Build policy: '$PIPELINE_NAME' required on '$BRANCH'"

# 2. Minimum reviewer count
echo "→ Creating reviewer count policy ..."
az repos policy approver-count create \
  --org "$ORG_URL" --project "$PROJECT" \
  --blocking true \
  --branch "$BRANCH" \
  --minimum-approver-count "$MIN_REVIEWERS" \
  --creator-vote-counts false \
  --allow-downvotes false \
  --reset-on-source-push true \
  --repository-id "$REPO_ID" \
  --output none
echo "  ✓ Reviewer policy: min $MIN_REVIEWERS reviewer(s) on '$BRANCH' (resets on push)"

echo ""
echo "Done. ICONIX CI gates are now enforced gates — PRs cannot be completed if"
echo "the traceability pipeline fails."
echo ""
echo "Verify at: $ORG_URL/$PROJECT/_settings/repositories?_a=policies&repoId=$REPO_ID&refName=refs/heads/$BRANCH"
