#!/usr/bin/env bash
# PostToolUse hook (matcher: Write|Edit) for the iconix-kit repository.
#
# Fires after every Write/Edit. Inspects tool_input.file_path; if the path
# touches the kit's user-facing surface (agents/*.md, commands/*.md,
# templates/, iconix-init / iconix-init.ps1, iconix-state-machine.puml),
# prints a stderr reminder to re-check README counts, the README
# "## Project layout" section, and the state machine diagram.
#
# The hook NEVER blocks — it always exits 0. It's a maintainer reminder,
# not a gate (CI in .github/workflows/validate.yml is the gate).
#
# Reference: CLAUDE.md "## Keeping README and state machine in sync".

# Read stdin JSON; tolerate empty input
input=$(cat 2>/dev/null || true)
[ -z "$input" ] && exit 0

# Extract tool_input.file_path without depending on jq.
# Grep the first "file_path": "..." pair, then strip the wrapping.
path=$(
  printf '%s' "$input" \
    | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' \
    | head -1 \
    | sed -E 's/^"file_path"[[:space:]]*:[[:space:]]*"//; s/"$//'
)

[ -z "$path" ] && exit 0

# Normalize Windows backslashes so a single set of patterns covers both
# `agents/foo.md` (POSIX) and `agents\foo.md` (Windows abs paths).
# JSON encodes a single `\` as `\\`, so the captured string here has `\\`
# wherever the OS has `\`. Convert any `\` we see back to `/`.
norm=$(printf '%s' "$path" | tr '\\' '/')

matched=0
case "$norm" in
  */agents/*.md|agents/*.md) matched=1 ;;
  */commands/*.md|commands/*.md) matched=1 ;;
  */templates/*|templates/*) matched=1 ;;
  */iconix-init|iconix-init) matched=1 ;;
  */iconix-init.ps1|iconix-init.ps1) matched=1 ;;
  */iconix-state-machine.puml|iconix-state-machine.puml) matched=1 ;;
esac

if [ "$matched" -eq 1 ]; then
  {
    printf '\n[iconix-kit reminder] User-facing surface touched: %s\n' "$path"
    printf '  Per CLAUDE.md "Keeping README and state machine in sync", verify:\n'
    printf '    1. README.md agent / command counts and examples.\n'
    printf '    2. README.md "## Project layout" section reflects every directory the kit creates.\n'
    printf '    3. iconix-state-machine.puml states / transitions / M1-M3 gates / agent labels.\n'
    printf '  Apply fixes in the same change rather than deferring.\n\n'
  } >&2
fi

exit 0
