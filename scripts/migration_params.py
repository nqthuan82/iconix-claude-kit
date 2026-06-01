#!/usr/bin/env python3
"""migration_params.py — normalize & validate migration run parameters.

Replaces ONLY the deterministic normalize/validate half of the `# Scope and run
parameters` block in `iconix-migration-infra.md`. The natural-language detection half
(recognising `--scope`, `--max-uc`, `--entry-point` from a chat message) cannot move to
Python — that stays in the agent prompt. The agent detects the raw values, passes them
here, and trusts the normalized JSON, which it then feeds into `checkpoint.py write`.

Normalization rules (mirrors the infra prompt + Phase 1b path-param rule):
  - entry-point: split on ',', trim, drop empties; HTTP "<METHOD> /path" values get
    their `{placeholder}` path params canonicalised to `{param}` so
    `/orders/{id}` and `/orders/{orderId}` match. `class.method` values (no space) are
    left untouched.
  - max-uc: must be a positive integer (else exit 1).
  - precedence: when an entry-point filter is present it takes precedence over
    `--max-uc`, so max_uc is nulled and `precedence_applied` is set true.

Output JSON: {scope, max_uc, entry_point_filter, precedence_applied}.
Exit codes: 0 ok · 1 invalid --max-uc.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402

_PARAM_PLACEHOLDER = re.compile(r"\{[^}]*\}")


def _is_null(value):
    # Shared definition with checkpoint.py via _common, so a value like "NONE"/"Null"
    # normalizes to null identically on both sides of the params → checkpoint handoff.
    return _common.is_nullish(value)


def normalize_entry_point(name):
    """Trim one entry-point token and canonicalise HTTP path params to {param}."""
    name = name.strip()
    if " " in name:  # "<METHOD> /path/{id}" → "<METHOD> /path/{param}"
        name = _PARAM_PLACEHOLDER.sub("{param}", name)
    return name


def parse_entry_points(raw):
    """Comma-split, trim, drop empties, normalize each. Returns list or None."""
    if _is_null(raw):
        return None
    items = [normalize_entry_point(part) for part in str(raw).split(",")]
    items = [i for i in items if i]
    return items or None


def parse_max_uc(raw):
    """Positive int, or None when unset. Raises ValueError when invalid."""
    if _is_null(raw):
        return None
    text = str(raw).strip()
    if not re.fullmatch(r"\d+", text) or int(text) <= 0:
        raise ValueError(f"--max-uc must be a positive integer, got {raw!r}")
    return int(text)


def normalize(scope, max_uc_raw, entry_point_raw):
    """Return the normalized parameter dict. Raises ValueError on bad max_uc."""
    scope_val = None if _is_null(scope) else str(scope).strip()
    entry_points = parse_entry_points(entry_point_raw)
    max_uc = parse_max_uc(max_uc_raw)
    precedence_applied = False
    if entry_points:  # entry-point filter wins over the UC cap
        if max_uc is not None:
            precedence_applied = True
        max_uc = None
    return {
        "scope": scope_val,
        "max_uc": max_uc,
        "entry_point_filter": entry_points,
        "precedence_applied": precedence_applied,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Normalize ICONIX migration run parameters")
    parser.add_argument("--scope", default="")
    parser.add_argument("--max-uc", dest="max_uc", default="")
    parser.add_argument("--entry-point", dest="entry_point", default="")
    args = parser.parse_args(argv)
    try:
        result = normalize(args.scope, args.max_uc, args.entry_point)
    except ValueError as exc:
        _common.die(f"migration_params: {exc}", _common.EXIT_GATE)
    _common.emit(result)
    return _common.EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
