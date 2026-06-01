#!/usr/bin/env python3
"""router.py — deterministic routing for the ICONIX migration pipeline.

This slice implements `--migration-route` only: it reads the most-recent
`migration/checkpoint-<date>.json` and maps `phases_completed` to the next sub-agent,
replacing the Case A–E ladder in `iconix-migration.md`. The general orchestrator
routing (`--next` / `--preflight` / `--phase9-next`) is deferred to a later slice.

  --migration-route [--migration-dir migration] [--path CHECKPOINT]
      → {"next": "infra"|"structural"|"semantic"|"complete"|"corrupt",
         "case": "A".."E",
         "checkpoint": <path or null>,
         "phases_completed": [...]}

Routing is advisory, so the exit code is **always 0** — the agent reads `next` and
dispatches. A corrupt checkpoint is reported as `next: "corrupt"` (Case E), not a crash.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402
import checkpoint  # noqa: E402


def route_migration(migration_dir="migration", path=None):
    """Map checkpoint state → next migration sub-agent (Cases A–E)."""
    ckpt = path or _common.latest_checkpoint(migration_dir)
    if not ckpt:
        return {"next": "infra", "case": "A", "checkpoint": None, "phases_completed": []}

    data, status = checkpoint.load_and_classify(ckpt)
    if status == "missing":
        # An explicit --path that does not exist behaves like "no checkpoint".
        return {"next": "infra", "case": "A", "checkpoint": None, "phases_completed": []}
    if status == "corrupt":
        return {"next": "corrupt", "case": "E", "checkpoint": ckpt, "phases_completed": []}

    phases = data.get("phases_completed", [])
    if "semantic" in phases:
        nxt, case = "complete", "D"
    elif "structural" in phases:
        nxt, case = "semantic", "C"
    elif "infra" in phases:
        nxt, case = "structural", "B"
    else:
        # Valid JSON, list present but empty — nothing has completed; restart infra.
        nxt, case = "infra", "A"
    return {"next": nxt, "case": case, "checkpoint": ckpt, "phases_completed": phases}


def main(argv=None):
    parser = argparse.ArgumentParser(description="ICONIX pipeline router")
    parser.add_argument("--migration-route", action="store_true",
                        help="route the migration pipeline from the checkpoint")
    parser.add_argument("--migration-dir", default="migration")
    parser.add_argument("--path", default=None, help="explicit checkpoint path (overrides latest)")
    args = parser.parse_args(argv)

    if not args.migration_route:
        _common.die("router: this build supports only --migration-route", _common.EXIT_IO)

    _common.emit(route_migration(args.migration_dir, args.path))
    return _common.EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
