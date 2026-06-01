#!/usr/bin/env python3
"""ids.py — allocate permanent ICONIX IDs from ids.registry.md (never reuse).

Replaces the model-driven "read the registry, find the highest ID, add one" step in
`iconix-traceability.md` and is imported by `promote.py` to batch-allocate IDs for a
run of DRAFT promotions.

ID format: `<PREFIX>-<TYPE>-<NNN>` (TYPE ∈ REQ/UC/RB/SD/CLS/TC/ADR), zero-padded to 3
digits, PREFIX from `project.prefix` in iconix.config.yaml. Allocation is **highest + 1
per type** — gaps left by deleted IDs are never refilled, so a retired ID is never
reissued.

Subcommands
  next   --type UC [--type RB ...] [--registry P] [--config P]
             → JSON {"UC": "PRJ-UC-007", "RB": "PRJ-RB-004", ...}
  append --registry P --row 'ID|slug|path|note'
             → append one ledger row, creating the file + header if absent

Exit codes: 0 ok · 2 IO / parse error.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402

REGISTRY_HEADER = (
    "# ID Registry\n"
    "\n"
    "Canonical ledger of issued ICONIX IDs. IDs are **never reused**, even after a\n"
    "deletion — allocation is always highest-seen + 1 per type. Maintained by the\n"
    "Traceability agent and `.claude/scripts/ids.py` / `promote.py`.\n"
    "\n"
    "| ID | Slug | Path | Note |\n"
    "|---|---|---|---|\n"
)


def scan_registry(registry_path):
    """Return {TYPE: highest_int_seen} parsed from the registry's ID column.

    Only the ID column of pipe-table rows is inspected (via a full-cell match), so an
    ID appearing in a free-text Note cell — e.g. "promoted from UC-DRAFT-001" — is not
    miscounted. A missing registry yields an empty map (everything starts at 001).
    """
    highest = {}
    if not registry_path or not os.path.isfile(registry_path):
        return highest
    with open(registry_path, encoding="utf-8-sig") as fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.split("|")]
            body = cells[1:]  # drop the empty cell before the leading pipe
            # Read the ID *column* (first cell), matching read_rows — NOT the first
            # non-empty cell, which on a blank-ID row would wrongly match a slug/note.
            id_cell = body[0] if body else ""
            match = _common.ID_RE.fullmatch(id_cell)
            if not match:
                continue
            typ = match.group(2).upper()
            num = int(match.group(3))
            if num > highest.get(typ, 0):
                highest[typ] = num
    return highest


def read_rows(registry_path):
    """Return [{'id','slug','path','note'}] for each valid ledger row.

    Used by promote.py / migration_preflight.py to know which slugs are already
    promoted. Rows whose first non-empty cell is not a valid ID are skipped (headers,
    separators).
    """
    rows = []
    if not registry_path or not os.path.isfile(registry_path):
        return rows
    with open(registry_path, encoding="utf-8-sig") as fh:
        for line in fh:
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.split("|")]
            cells = [c for c in cells]  # keep positions; leading/trailing '' from split
            body = cells[1:]  # drop the empty cell before the first pipe
            if not body or not _common.ID_RE.fullmatch(body[0]):
                continue
            rows.append({
                "id": body[0],
                "slug": body[1] if len(body) > 1 else "",
                "path": body[2] if len(body) > 2 else "",
                "note": body[3] if len(body) > 3 else "",
            })
    return rows


def format_id(prefix, typ, number):
    """`PRJ-UC-007` (or `UC-007` when the project has no prefix)."""
    body = f"{typ.upper()}-{number:03d}"
    return f"{prefix}-{body}" if prefix else body


def next_ids(types, registry_path, prefix):
    """Allocate one id per requested type as a {TYPE: id} dict (highest + 1)."""
    highest = scan_registry(registry_path)
    out = {}
    for typ in types:
        key = typ.upper()
        out[key] = format_id(prefix, key, highest.get(key, 0) + 1)
    return out


def cmd_next(args):
    registry = args.registry or os.path.join(_common.artifact_root(args.config), "ids.registry.md")
    prefix = _common.get_prefix(args.config)
    types = []
    for typ in args.type:
        key = typ.upper()
        if key not in _common.ID_TYPES:
            _common.die(f"ids: unknown type '{typ}' (expected one of {', '.join(_common.ID_TYPES)})")
        if key not in types:
            types.append(key)
    _common.emit(next_ids(types, registry, prefix))
    return _common.EXIT_OK


def cmd_append(args):
    parts = [p.strip() for p in args.row.split("|")]
    while len(parts) < 4:
        parts.append("")
    ident, slug, path, note = parts[0], parts[1], parts[2], parts[3]
    if not ident:
        _common.die("ids: --row must start with an ID (ID|slug|path|note)")
    new_file = not os.path.isfile(args.registry)
    os.makedirs(os.path.dirname(os.path.abspath(args.registry)) or ".", exist_ok=True)
    with open(args.registry, "a", encoding="utf-8") as fh:
        if new_file:
            fh.write(REGISTRY_HEADER)
        fh.write(f"| {ident} | {slug} | {path} | {note} |\n")
    _common.emit({"appended": ident, "registry": args.registry, "created": new_file})
    return _common.EXIT_OK


def build_parser():
    parser = argparse.ArgumentParser(description="ICONIX ID allocator")
    sub = parser.add_subparsers(dest="command", required=True)

    p_next = sub.add_parser("next", help="allocate the next ID per type")
    p_next.add_argument("--type", action="append", required=True, metavar="TYPE")
    p_next.add_argument("--registry", default=None)
    p_next.add_argument("--config", default=None)
    p_next.set_defaults(func=cmd_next)

    p_append = sub.add_parser("append", help="append a ledger row")
    p_append.add_argument("--registry", required=True)
    p_append.add_argument("--row", required=True, metavar="ID|slug|path|note")
    p_append.set_defaults(func=cmd_append)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
