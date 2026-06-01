#!/usr/bin/env python3
"""migration_preflight.py — deterministic idempotency checks for the migration infra agent.

Replaces the mechanical detection in `iconix-migration-infra.md` Steps 0–4 (and the
detection half of Step 4b). It only *detects and reports* — every human decision stays
in the agent prompt: the Step 0a greenfield STOP, the Step 4b continue/cancel gate, and
any --force override are the agent's to make from these booleans.

  --args "$ARGUMENTS" [--config iconix.config.yaml] [--migration-dir migration]
    → JSON {
        greenfield_detected, greenfield_files, allow_greenfield, abort_greenfield,
        last_run_date, promoted_artifacts, human_edited_drafts, safe_to_regenerate,
        nothing_left_to_migrate,
        domain_glossary_exists, schema_files_present, schema_files_sample,
        scope, db_readiness_warning
      }

Exit codes: 0 ok · 2 IO error. (Detection is advisory; the agent acts on the booleans.)
"""

import argparse
import datetime
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402
import ids  # noqa: E402

# Folders scanned for greenfield (non-DRAFT) collisions. In a clean migration target
# these are empty, so ANY non-DRAFT artifact here signals greenfield coexistence.
_GREENFIELD_GLOBS = ("use-cases/*.md", "robustness/*.puml", "sequence/*.puml")

# Migration DRAFT outputs (Step 3 / safe-to-regenerate set).
_DRAFT_GLOBS = (
    "use-cases/UC-DRAFT-*.md",
    "robustness/RB-DRAFT-*.puml",
    "sequence/SD-DRAFT-*.puml",
    "domain-model/domain-model-DRAFT.puml",
    "use-case-packages/*-DRAFT.puml",
)

# Files a human may have hand-edited since the last run (Step 3 list).
_HUMAN_EDIT_GLOBS = (
    "docs/architecture/system-architecture.md",
    "docs/architecture/package-map.md",
    "migration/coverage-gaps.md",
    "class-model/class-model.puml",
    "sequence/SD-DRAFT-*.puml",
    "robustness/RB-DRAFT-*.puml",
    "domain-model/domain-model-DRAFT.puml",
    "use-cases/UC-DRAFT-*.md",
    "use-case-packages/*-DRAFT.puml",
)

_SKIP_DIRS = {".git", "node_modules", "bin", "obj", "dist", "build", ".venv", "venv",
              "__pycache__", "target", ".claude", "migration"}
_DRAFT_SLUG_RE = re.compile(r"(?:UC|RB|SD)-DRAFT-\d+-(.+?)\.(?:md|puml)$", re.IGNORECASE)
_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _glob(root, pattern):
    return sorted(glob.glob(os.path.join(root, pattern)))


def _rel(root, paths):
    return [os.path.relpath(p, root).replace("\\", "/") for p in paths]


def _has_draft_stamp(path):
    """True if a file's header (first ~6 lines) carries a DRAFT stamp."""
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            head = "".join(fh.readline() for _ in range(6))
    except OSError:
        return False
    return "DRAFT" in head.upper()


def _mtime_date(path):
    return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()


_GF_SLUG_RE = re.compile(r"(?:[A-Za-z][A-Za-z0-9]*-)?(?:UC|RB|SD)-\d+-(.+)\.(?:md|puml)$", re.IGNORECASE)


def _greenfield_slug(path):
    match = _GF_SLUG_RE.search(os.path.basename(path))
    return match.group(1) if match else None


def detect_greenfield(root, promoted_paths=frozenset(), promoted_slugs=frozenset(), prior_run=False):
    """Non-DRAFT artifacts that would collide with a migration run.

    Excludes the migration's OWN promoted outputs so a 2nd+ migrate→promote cycle is not
    blocked: an ID-bearing artifact already in the registry (matched by path or slug) is
    not a collision, and — when a prior migration run is detected — neither are the no-ID
    migration artifacts (class-model.puml, use-case-packages) that the registry can't
    track. On a truly fresh target (no prior run, empty registry) any non-DRAFT artifact
    is still flagged, so hand-authored greenfield work is caught as before.
    """
    found = []
    for pattern in _GREENFIELD_GLOBS:
        for p in _glob(root, pattern):
            if _common.is_draft(p):
                continue
            rel = os.path.relpath(p, root).replace("\\", "/")
            if rel in promoted_paths:
                continue
            slug = _greenfield_slug(p)
            if slug and slug in promoted_slugs:
                continue
            found.append(p)
    if not prior_run:
        found += [p for p in _glob(root, "use-case-packages/*.puml") if not p.endswith("-DRAFT.puml")]
        class_model = os.path.join(root, "class-model", "class-model.puml")
        if os.path.isfile(class_model) and not _has_draft_stamp(class_model):
            found.append(class_model)
    return sorted(set(found))


def latest_run_date(migration_dir):
    dates = []
    for pattern in ("checkpoint-*.json", "survey-*.md"):
        for path in glob.glob(os.path.join(migration_dir, pattern)):
            match = _DATE_RE.search(os.path.basename(path))
            if match:
                dates.append(match.group(1))
    return max(dates) if dates else None


def draft_slug(path):
    match = _DRAFT_SLUG_RE.search(os.path.basename(path))
    return match.group(1) if match else None


def find_schema_files(root, cap=50):
    """Bounded recursive scan for DB schema files (Step 4b signal)."""
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
        low_dir = dirpath.lower()
        for name in filenames:
            low = name.lower()
            is_schema = (
                low.endswith((".sql", ".sqlproj"))
                or low == "schema.prisma"
                or (low.endswith(".py") and "alembic" in low_dir and "versions" in low_dir)
                or (low.endswith(".rb") and "migrate" in low_dir)
            )
            if is_schema:
                found.append(os.path.relpath(os.path.join(dirpath, name), root).replace("\\", "/"))
                if len(found) >= cap:
                    return found
    return found


def parse_scope(args_str):
    match = re.search(r"--scope\s+(\"[^\"]+\"|'[^']+'|\S+)", args_str or "")
    if not match:
        return None
    return match.group(1).strip("\"'")


def run_preflight(args_str, config_path, migration_dir):
    root = _common.artifact_root(config_path)
    allow_greenfield = "--allow-greenfield" in (args_str or "")
    scope = parse_scope(args_str)

    last_run = latest_run_date(migration_dir)
    registry = os.path.join(root, "ids.registry.md")
    promoted = ids.read_rows(registry)
    promoted_slugs = {row["slug"] for row in promoted if row["slug"]}
    promoted_paths = {row["path"].replace("\\", "/").strip().lstrip("./")
                      for row in promoted if row["path"]}

    # Greenfield-collision detection excludes the migration's own promoted outputs; a
    # prior run (any checkpoint/survey present) means non-DRAFT artifacts are this
    # migration's work, not hand-authored greenfield to abort on.
    greenfield = detect_greenfield(root, promoted_paths, promoted_slugs, prior_run=last_run is not None)

    drafts = []
    for pattern in _DRAFT_GLOBS:
        drafts += _glob(root, pattern)
    class_model = os.path.join(root, "class-model", "class-model.puml")
    if os.path.isfile(class_model) and _has_draft_stamp(class_model):
        drafts.append(class_model)
    drafts = sorted(set(drafts))

    # Human-edited: existing files whose mtime *date* is later than the last-run date.
    # Date granularity is deliberate: the checkpoint filename records the run's START
    # date, and the run's own drafts are written later the same day — comparing full
    # timestamps against the checkpoint would false-flag every freshly generated draft as
    # "edited". The known limitation is that a human edit made later on the SAME calendar
    # day as the run is not flagged; the agent's continue/cancel gate and `--force` are
    # the backstop for that narrow window.
    human_edited = []
    if last_run:
        seen = set()
        for pattern in _HUMAN_EDIT_GLOBS:
            for path in _glob(root, pattern):
                if path in seen or not os.path.isfile(path):
                    continue
                seen.add(path)
                if _mtime_date(path) > last_run:
                    human_edited.append(path)

    human_edited_set = set(human_edited)
    safe = [
        p for p in drafts
        if p not in human_edited_set and (draft_slug(p) not in promoted_slugs)
    ]
    nothing_left = bool(drafts) and not safe

    # Step 4b — database-container readiness (detection only; the warning's
    # continue/cancel gate stays in the agent prompt).
    glossary_exists = os.path.isfile(os.path.join(root, "migration", "domain-glossary.md"))
    schema_sample = find_schema_files(root) if scope else []
    schema_present = bool(schema_sample)
    db_warning = bool(scope) and schema_present and not glossary_exists

    return {
        "greenfield_detected": bool(greenfield),
        "greenfield_files": _rel(root, greenfield),
        "allow_greenfield": allow_greenfield,
        "abort_greenfield": bool(greenfield) and not allow_greenfield,
        "last_run_date": last_run,
        "promoted_artifacts": [{"id": r["id"], "slug": r["slug"]} for r in promoted],
        "human_edited_drafts": _rel(root, human_edited),
        "safe_to_regenerate": _rel(root, safe),
        "nothing_left_to_migrate": nothing_left,
        "domain_glossary_exists": glossary_exists,
        "schema_files_present": schema_present,
        "schema_files_sample": schema_sample,
        "scope": scope,
        "db_readiness_warning": db_warning,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="ICONIX migration pre-flight detection")
    parser.add_argument("--args", default="", help="the raw $ARGUMENTS string")
    parser.add_argument("--config", default=None)
    parser.add_argument("--migration-dir", default="migration")
    args = parser.parse_args(argv)
    config_path = args.config or _common.find_config()
    _common.emit(run_preflight(args.args, config_path, args.migration_dir))
    return _common.EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
