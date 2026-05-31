#!/usr/bin/env python3
"""migration_promoted.py — list entry points already covered by a promoted robustness diagram.

Replaces the already-promoted entry-point check in `iconix-migration-semantic.md`
Phase 5. It greps the **permanent** robustness diagrams (`<PREFIX>-RB-*.puml`, excluding
any file with `DRAFT` in its name), extracts their boundary node names, and — when an
entry-point filter is supplied — reports which targets are already covered so the
semantic agent does not re-draft a UC for them.

Fuzzy (substring) name matches are returned in `ambiguous[]` for the agent to confirm,
NOT auto-skipped — auto-skipping a fuzzy match could silently drop a real entry point.

  --robustness-dir robustness/ [--prefix PRJ | --config iconix.config.yaml]
                              [--entry-points "POST /orders,OrderController.Place"]
    → JSON {
        already_promoted: [{entry_point, uc_id, boundary_name, rb_file}],
        ambiguous:        [{entry_point, candidate, uc_id, rb_file}],
        skip_count: N,
        promoted_boundaries: [{uc_id, boundary_name, rb_file}]   # when no filter given
      }

Exit codes: 0 ok · 2 IO error.
"""

import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402
import migration_params  # noqa: E402

_BOUNDARY_RE = re.compile(r'^\s*boundary\s+"([^"]+)"', re.MULTILINE)
_BOUNDARY_BARE_RE = re.compile(r'^\s*boundary\s+([A-Za-z_]\w*)\s*$', re.MULTILINE)
# UC id cited in the RB header comment, e.g. `' Traceability: ... UC-017 ...`
_UC_IN_TEXT_RE = re.compile(r"(?:[A-Za-z][A-Za-z0-9]*-)?UC-\d+")


def _casefold_norm(name):
    """Normalize an entry-point/boundary name for comparison (path-params + casefold)."""
    return migration_params.normalize_entry_point(name).casefold()


def permanent_rb_files(robustness_dir, prefix):
    """Permanent (non-DRAFT) robustness diagrams for this prefix."""
    if prefix:
        pattern = os.path.join(robustness_dir, f"{prefix}-RB-*.puml")
        files = glob.glob(pattern)
    else:
        files = [p for p in glob.glob(os.path.join(robustness_dir, "*RB-*.puml"))]
    return sorted(p for p in files if not _common.is_draft(p))


def extract_boundaries(text):
    names = _BOUNDARY_RE.findall(text)
    names += _BOUNDARY_BARE_RE.findall(text)
    # de-dup preserving order
    seen, out = set(), []
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def extract_uc_id(text, fallback):
    """The diagram's own UC id (header Traceability comment or note-bottom `UC:`), else fallback.

    `<<...>>` stereotype contents are dropped first, so a reused-page reference like
    `boundary "X" as P <<from PRJ-UC-099 Title>>` does not get mistaken for this RB's UC.
    """
    cleaned = re.sub(r"<<[^>]*>>", "", text)
    match = _UC_IN_TEXT_RE.search(cleaned)
    return match.group(0) if match else fallback


def scan(robustness_dir, prefix, entry_points):
    promoted_boundaries = []
    for rb in permanent_rb_files(robustness_dir, prefix):
        try:
            with open(rb, encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        except OSError:
            continue
        slug = os.path.basename(rb)
        uc_id = extract_uc_id(text, slug)
        rel = os.path.relpath(rb).replace("\\", "/")
        for boundary in extract_boundaries(text):
            promoted_boundaries.append({"uc_id": uc_id, "boundary_name": boundary, "rb_file": rel})

    result = {
        "already_promoted": [],
        "ambiguous": [],
        "skip_count": 0,
        "promoted_boundaries": promoted_boundaries,
    }

    if not entry_points:
        return result

    norm_boundaries = [(b, _casefold_norm(b["boundary_name"])) for b in promoted_boundaries]
    for ep in entry_points:
        ep_norm = _casefold_norm(ep)
        exact = next((b for b, bn in norm_boundaries if bn == ep_norm), None)
        if exact:
            result["already_promoted"].append({
                "entry_point": ep, "uc_id": exact["uc_id"],
                "boundary_name": exact["boundary_name"], "rb_file": exact["rb_file"],
            })
            continue
        fuzzy = next((b for b, bn in norm_boundaries
                      if ep_norm and (ep_norm in bn or bn in ep_norm)), None)
        if fuzzy:
            result["ambiguous"].append({
                "entry_point": ep, "candidate": fuzzy["boundary_name"],
                "uc_id": fuzzy["uc_id"], "rb_file": fuzzy["rb_file"],
            })
    result["skip_count"] = len(result["already_promoted"])
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="ICONIX already-promoted entry-point check")
    parser.add_argument("--robustness-dir", default="robustness")
    parser.add_argument("--prefix", default=None)
    parser.add_argument("--config", default=None)
    parser.add_argument("--entry-points", dest="entry_points", default="")
    args = parser.parse_args(argv)

    prefix = args.prefix if args.prefix is not None else _common.get_prefix(args.config)
    entry_points = migration_params.parse_entry_points(args.entry_points) or []
    _common.emit(scan(args.robustness_dir, prefix, entry_points))
    return _common.EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
