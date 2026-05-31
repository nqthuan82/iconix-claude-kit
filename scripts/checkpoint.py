#!/usr/bin/env python3
"""checkpoint.py — read / write / update / validate the migration checkpoint JSON.

The migration pipeline (infra → structural → semantic) hands state off through
`migration/checkpoint-<date>.json`. This script is the single authority for that
file's schema and typing, replacing the literal JSON block in
`iconix-migration-infra.md` Step 5.

Two correctness fixes over the prompt-authored version it replaces:
  1. **`max_uc` is a real int|null**, not the quoted string `"<N or null>"` the
     template showed — downstream comparisons (`>= max_uc`) were comparing against a
     string.
  2. **Case-E corruption is detected deterministically** (`validate`): missing or
     non-array `phases_completed`, or unparseable JSON, exit 1 so the router can tell
     the user to delete and restart rather than silently proceeding.

Subcommands
  write    --path P [--field k=v ...]      build a full checkpoint (defaults + overrides)
  read     --path P [--field k]            print the whole JSON, or one field's value
  update   --path P [--field k=v ...]      merge overrides into an existing checkpoint
                                           (every unspecified field, incl. phases_completed,
                                           is preserved verbatim)
  validate --path P [--phase infra]        structural validity; with --phase infra also
                                           asserts the infra-complete gate conditions

Exit codes: 0 ok · 1 schema violation / corrupt · 2 IO error.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402


# Full schema with defaults. `write` starts from this and applies --field overrides.
DEFAULTS = {
    "run_date": "",
    "mode": "",
    "scope": None,
    "max_uc": None,
    "entry_point_filter": None,
    "greenfield_coexistence": False,
    "greenfield_files": [],
    "phases_completed": ["infra"],
    "containers_surveyed": [],
    "entry_point_count": 0,
    "next_phase": "structural",
}

ARRAY_FIELDS = {"entry_point_filter", "greenfield_files", "phases_completed", "containers_surveyed"}
INT_FIELDS = {"entry_point_count"}
INT_OR_NULL_FIELDS = {"max_uc"}
BOOL_FIELDS = {"greenfield_coexistence"}
# Fields that accept an explicit null (empty / "null" → None rather than 0 / []).
NULLABLE_FIELDS = {"scope", "max_uc", "entry_point_filter"}


def coerce(key, raw):
    """Coerce a `--field key=value` string to the typed value the schema expects."""
    if key in NULLABLE_FIELDS and _common.is_nullish(raw):
        return None
    if key in BOOL_FIELDS:
        return str(raw).strip().lower() in ("true", "1", "yes", "on")
    if key in INT_FIELDS or key in INT_OR_NULL_FIELDS:
        if _common.is_nullish(raw):
            return None if key in INT_OR_NULL_FIELDS else 0
        try:
            return int(str(raw).strip())
        except ValueError:
            _common.die(f"checkpoint: field '{key}' expects an integer, got {raw!r}", _common.EXIT_IO)
    if key in ARRAY_FIELDS:
        if _common.is_nullish(raw):
            return None if key == "entry_point_filter" else []
        text = str(raw).strip()
        if text.startswith("["):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                _common.die(f"checkpoint: field '{key}' looks like JSON but did not parse: {raw!r}", _common.EXIT_IO)
        return [part.strip() for part in text.split(",") if part.strip()]
    # Plain string fields (run_date, mode, scope-when-set, next_phase).
    return raw


def parse_fields(pairs):
    """Turn ['k=v', ...] into a coerced {k: value} dict.

    Rejects unknown keys: a typo like `phasescompleted=` would otherwise be stored as a
    junk field while the real `phases_completed` stayed unchanged — a silent no-op that
    leaves the operator believing they advanced a phase.
    """
    out = {}
    for pair in pairs or []:
        if "=" not in pair:
            _common.die(f"checkpoint: --field expects key=value, got {pair!r}", _common.EXIT_IO)
        key, raw = pair.split("=", 1)
        key = key.strip()
        if key not in DEFAULTS:
            _common.die(
                f"checkpoint: unknown field '{key}' (known: {', '.join(sorted(DEFAULTS))})",
                _common.EXIT_IO,
            )
        out[key] = coerce(key, raw)
    return out


def load_and_classify(path):
    """Load a checkpoint and classify it. Shared by `validate` and router.py so the
    two agree on what "corrupt" means.

    Returns (data_or_None, status) with status in {"ok", "corrupt", "missing"}.
    A checkpoint is corrupt (Case E in iconix-migration.md) when the JSON is
    unparseable OR `phases_completed` is absent / not a list.
    """
    if not os.path.isfile(path):
        return None, "missing"
    try:
        data = _common.read_json(path)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        # Unparseable JSON, garbled (non-UTF-8) bytes, or an unreadable file are all
        # "corrupt" for routing purposes — never a crash (router promises exit 0).
        return None, "corrupt"
    # Valid JSON that is not an object (e.g. a top-level array or scalar) has no
    # phases_completed and is corrupt; guard before calling .get to avoid AttributeError.
    if not isinstance(data, dict) or not isinstance(data.get("phases_completed"), list):
        return None, "corrupt"
    return data, "ok"


def cmd_write(args):
    data = dict(DEFAULTS)
    data.update(parse_fields(args.field))
    _common.write_json(args.path, data)
    _common.emit(data)
    return _common.EXIT_OK


def cmd_read(args):
    try:
        data = _common.read_json(args.path)
    except FileNotFoundError:
        _common.die(f"checkpoint: file not found: {args.path}", _common.EXIT_IO)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        _common.die(f"checkpoint: corrupt JSON in {args.path}: {exc}", _common.EXIT_GATE)
    if args.field:
        key = args.field[0] if isinstance(args.field, list) else args.field
        if key not in data:
            _common.die(f"checkpoint: no such field '{key}' in {args.path}", _common.EXIT_IO)
        sys.stdout.write(json.dumps(data[key], ensure_ascii=False) + "\n")
    else:
        _common.emit(data)
    return _common.EXIT_OK


def cmd_update(args):
    try:
        data = _common.read_json(args.path)
    except FileNotFoundError:
        _common.die(f"checkpoint: cannot update missing file: {args.path}", _common.EXIT_IO)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        _common.die(f"checkpoint: refusing to update corrupt JSON in {args.path}: {exc}", _common.EXIT_GATE)
    data.update(parse_fields(args.field))  # only specified fields change
    _common.write_json(args.path, data)
    _common.emit(data)
    return _common.EXIT_OK


def cmd_validate(args):
    issues = []
    data, status = load_and_classify(args.path)
    if status == "missing":
        _common.die(f"checkpoint: file not found: {args.path}", _common.EXIT_IO)
    if status == "corrupt":
        # Case E (iconix-migration.md): unparseable JSON or phases_completed missing/non-list.
        _common.emit({"valid": False, "corrupt": True,
                      "issues": ["invalid JSON or phases_completed missing / not a list"]})
        return _common.EXIT_GATE

    if args.phase == "infra":
        if data.get("next_phase") != "structural":
            issues.append("next_phase must be 'structural' after infra")
        if not data.get("containers_surveyed"):
            issues.append("containers_surveyed must be a non-empty list after infra")
        ep = data.get("entry_point_count")
        if not isinstance(ep, int) or ep <= 0:
            issues.append("entry_point_count must be an integer > 0 after infra")

    if issues:
        _common.emit({"valid": False, "corrupt": False, "issues": issues})
        return _common.EXIT_GATE
    _common.emit({"valid": True, "corrupt": False, "issues": []})
    return _common.EXIT_OK


def build_parser():
    parser = argparse.ArgumentParser(description="ICONIX migration checkpoint manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p_write = sub.add_parser("write", help="create a full checkpoint")
    p_write.add_argument("--path", required=True)
    p_write.add_argument("--field", action="append", default=[], metavar="k=v")
    p_write.set_defaults(func=cmd_write)

    p_read = sub.add_parser("read", help="print a checkpoint (or one field)")
    p_read.add_argument("--path", required=True)
    p_read.add_argument("--field", action="append", default=[], metavar="k")
    p_read.set_defaults(func=cmd_read)

    p_update = sub.add_parser("update", help="merge fields into an existing checkpoint")
    p_update.add_argument("--path", required=True)
    p_update.add_argument("--field", action="append", default=[], metavar="k=v")
    p_update.set_defaults(func=cmd_update)

    p_validate = sub.add_parser("validate", help="validate checkpoint structure / gate")
    p_validate.add_argument("--path", required=True)
    p_validate.add_argument("--phase", choices=["infra"], default=None)
    p_validate.set_defaults(func=cmd_validate)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
