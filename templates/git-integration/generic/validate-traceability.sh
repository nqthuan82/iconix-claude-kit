#!/usr/bin/env bash
# validate-traceability.sh — provider-agnostic ICONIX traceability gate.
#
# Run this in any CI (GitHub Actions, Azure Pipelines, GitLab CI,
# Bitbucket Pipelines, plain Jenkins, etc.) as a merge-gate check.
#
# What it checks:
#   1. Every changed file under src/ and tests/ has a `Traceability:` comment.
#   2. Every cited UC-XXX / RB-XXX / SD-XXX / REQ-XXX / TC-XXX ID exists in the
#      corresponding artifact folder.
#   3. No file references an ID that's been deleted or renamed.
#   4. Every changed container-mapping/*.md file has a non-empty "Effective stack"
#      column on every data row (M2 blocker per Traceability check #16).
#
# Usage:
#   validate-traceability.sh [<base-ref>] [<head-ref>]
#
#   Defaults: base = origin/main, head = HEAD.
#   Override via env: ICONIX_BASE_REF, ICONIX_HEAD_REF.
#   ICONIX_CONFIG_PATH: root of the ICONIX meta-project (default: current dir).
#     Set in service repo CI when iconix.config.yaml and artifact folders live
#     in a separate meta-project checkout:
#       env:
#         ICONIX_CONFIG_PATH: path/to/meta-project
#
# Exit codes:
#   0 — all checks pass
#   1 — one or more violations (printed to stderr)
#   2 — usage / setup error

set -euo pipefail

BASE_REF="${1:-${ICONIX_BASE_REF:-origin/main}}"
HEAD_REF="${2:-${ICONIX_HEAD_REF:-HEAD}}"

# Root of the ICONIX meta-project (iconix.config.yaml + artifact folders).
# Default: current directory (single-repo or running inside the meta-project).
# In a service repo CI, set ICONIX_CONFIG_PATH to the meta-project checkout root.
ARTIFACT_ROOT="${ICONIX_CONFIG_PATH:-.}"

# Resolve the kit-prefix from iconix.config.yaml (if present)
PREFIX=""
if [[ -f "${ARTIFACT_ROOT}/iconix.config.yaml" ]]; then
  PREFIX="$(grep -E '^\s*prefix:' "${ARTIFACT_ROOT}/iconix.config.yaml" | head -1 | sed -E 's/.*prefix:\s*"?([^"]*)"?.*/\1/' || echo "")"
fi
ID_RE='[A-Z][A-Z0-9]*-(REQ|UC|RB|SD|CLS|TC|ADR)-[0-9]+'
if [[ -n "${PREFIX}" ]]; then
  ID_RE="${PREFIX}-(REQ|UC|RB|SD|CLS|TC|ADR)-[0-9]+"
fi

violations=0

# Make sure the base ref exists locally
if ! git rev-parse --verify "${BASE_REF}" >/dev/null 2>&1; then
  echo "ERROR: base ref '${BASE_REF}' not found. Fetch the remote first or pass a different base." >&2
  exit 2
fi

CHANGED_FILES="$(git diff --name-only --diff-filter=AM "${BASE_REF}...${HEAD_REF}" -- 'src/**' 'tests/**' 2>/dev/null || true)"

if [[ -z "${CHANGED_FILES}" ]]; then
  echo "validate-traceability: no source or test files changed against ${BASE_REF}; skipping."
  exit 0
fi

# ── Check 1: every changed file has a Traceability comment ─────────────
echo "validate-traceability: checking ${BASE_REF}...${HEAD_REF}"

while IFS= read -r f; do
  [[ -z "$f" || ! -f "$f" ]] && continue

  # Look for `Traceability:` in the first 30 lines (any comment style)
  if ! head -n 30 "$f" | grep -q -E '(Traceability|@traceability)\s*[:|=]'; then
    echo "MISSING_TRACE: ${f} has no \`Traceability:\` comment in its first 30 lines" >&2
    violations=$((violations + 1))
    continue
  fi

  # ── Check 2: cited IDs exist as artifacts ─────────────────────────────
  cited_ids="$(head -n 30 "$f" | grep -oE "${ID_RE}" | sort -u || true)"
  while IFS= read -r id; do
    [[ -z "$id" ]] && continue
    # Strip prefix to get TYPE-NNN
    type_id="$(echo "$id" | sed -E "s/^[A-Z][A-Z0-9]*-//")"
    type="$(echo "$type_id" | cut -d'-' -f1)"

    case "$type" in
      REQ) folder="requirements" ; pattern="${id}.md" ;;
      UC)  folder="use-cases"    ; pattern="${id}-*.md" ;;
      RB)  folder="robustness"   ; pattern="${id}-*.puml" ;;
      SD)  folder="sequence"     ; pattern="${id}-*.puml" ;;
      CLS) continue ;;  # CLS is a class-model node, not a file
      TC)  folder="test-cases"   ; pattern="${id}-*.md" ;;
      ADR) folder="adrs"         ; pattern="${id}-*.md" ;;
      *)   continue ;;
    esac

    if [[ -d "${ARTIFACT_ROOT}/${folder}" ]]; then
      # shellcheck disable=SC2086
      matches="$(find "${ARTIFACT_ROOT}/${folder}" -maxdepth 2 -name "${pattern}" 2>/dev/null | head -1)"
      if [[ -z "$matches" ]]; then
        echo "BROKEN_TRACE: ${f} cites ${id} but no artifact found at ${ARTIFACT_ROOT}/${folder}/${pattern}" >&2
        violations=$((violations + 1))
      fi
    fi
  done <<< "$cited_ids"

done <<< "${CHANGED_FILES}"

# ── Check 3: changed container-mapping files have Effective stack filled ─
CHANGED_MAPS="$(git diff --name-only --diff-filter=AM "${BASE_REF}...${HEAD_REF}" -- 'container-mapping/*.md' 2>/dev/null || true)"

while IFS= read -r f; do
  [[ -z "$f" || ! -f "$f" ]] && continue

  if ! grep -q "Effective stack" "$f"; then
    echo "MISSING_STACK_COL: ${f} has no 'Effective stack' column — regenerate from templates/container-mapping-template.md" >&2
    violations=$((violations + 1))
    continue
  fi

  # Check each table data row for a blank Effective stack cell (column 2).
  # Rows starting with | that are not the header or separator are data rows.
  while IFS= read -r row; do
    col2="$(echo "$row" | cut -d'|' -f3 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    # Skip header row and separator row (all dashes/colons)
    [[ "$col2" == "Effective stack" || "$col2" =~ ^[-:]+$ ]] && continue
    if [[ -z "$col2" ]]; then
      echo "BLANK_STACK: ${f} has a blank 'Effective stack' cell — Architect must resolve per Stack resolution rule" >&2
      violations=$((violations + 1))
    fi
  done < <(grep '^|' "$f")

done <<< "${CHANGED_MAPS}"

# ── Summary ─────────────────────────────────────────────────────────────
if [[ "$violations" -eq 0 ]]; then
  echo "validate-traceability: OK ($(echo "${CHANGED_FILES}" | wc -l | tr -d ' ') files checked)"
  exit 0
else
  echo ""
  echo "validate-traceability: ${violations} violation(s) — fix before merging." >&2
  echo "Each source/test file under src/ or tests/ must carry a Traceability comment" >&2
  echo "citing valid UC/RB/SD/REQ/TC/ADR IDs. See:" >&2
  echo "  docs/iconix/templates/branch-conventions.md" >&2
  echo "  agents/iconix-traceability.md (kit)" >&2
  exit 1
fi
