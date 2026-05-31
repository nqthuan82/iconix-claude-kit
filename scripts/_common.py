"""_common.py — shared stdlib helpers for the ICONIX `.claude/scripts/` toolset.

Single source of truth for the ID regex, config/prefix resolution, the checkpoint
selector, and the JSON / exit-code conventions every script uses. Keeping these here
means the ID-format rule and the prefix-resolution rule live in ONE place, not copied
across ids.py / promote.py / migration_preflight.py / router.py.

Design constraints (see BACKLOG.md "SDK Hybrid — Option B"):
- **Stdlib only.** No `pip`, no PyYAML. `iconix.config.yaml` is parsed with regex,
  exactly as the bash installer and `validate-traceability.sh` already do.
- **Honors `ICONIX_CONFIG_PATH`** so the scripts work from a service repo whose
  artifacts live in a separate meta-project checkout (multi-repo CI).
- Python 3.9+.
"""

import glob
import json
import os
import re
import sys
import tempfile

# ── Exit-code convention (shared by every script) ──────────────────────────
# 0 — success / READY
# 1 — gate failure: a deterministic check said "no" (corrupt checkpoint, NOT READY,
#     nothing eligible). The caller acts on this; it is NOT a crash.
# 2 — setup / IO error: file not found, unreadable, bad arguments. The caller should
#     surface stderr and fall back to the in-prompt logic.
EXIT_OK = 0
EXIT_GATE = 1
EXIT_IO = 2

# ── Traceability ID format: <PREFIX>-<TYPE>-<NNN> ──────────────────────────
# The chain is REQ → UC → RB → SD → CLS → TC (+ ADR). IDs are never reused.
# The regex tolerates BOTH the prefixed form (PRJ-UC-007) and the bare form
# (UC-007) — README examples and some legacy artifacts use the bare form.
ID_TYPES = ("REQ", "UC", "RB", "SD", "CLS", "TC", "ADR")
ID_RE = re.compile(r"(?:([A-Za-z][A-Za-z0-9]*)-)?(REQ|UC|RB|SD|CLS|TC|ADR)-(\d+)")

# `^\s*prefix:` deliberately does NOT match `work_item_prefix:` (the char before
# `prefix` is `_`, not whitespace), so this picks up only project.prefix — the same
# behaviour as the grep in validate-traceability.sh. `#` is excluded so a trailing
# `# comment` on the line is not captured.
_PREFIX_RE = re.compile(r"""^\s*prefix\s*:\s*["']?([^"'\n#]+)""", re.M)


# ── stdout / stderr helpers ────────────────────────────────────────────────
def emit(obj):
    """Print a JSON object to stdout (the script's machine-readable return value)."""
    json.dump(obj, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")


def die(message, code=EXIT_IO):
    """Print an error to stderr and exit with the given code."""
    sys.stderr.write(message.rstrip("\n") + "\n")
    raise SystemExit(code)


# ── JSON I/O (atomic write) ────────────────────────────────────────────────
def read_json(path):
    """Read and parse a JSON file. Raises FileNotFoundError / json.JSONDecodeError.

    Opens with utf-8-sig so a leading UTF-8 BOM (which stock Windows PowerShell
    tooling writes by default) is tolerated rather than misparsed as corruption.
    """
    with open(path, encoding="utf-8-sig") as fh:
        return json.load(fh)


# Tokens that mean "no value" across the scripts (case-insensitive). Shared so the
# null-coercion rule is defined once, not duplicated in checkpoint.py / migration_params.py.
_NULLISH = ("", "null", "none")


def is_nullish(value):
    """True when `value` represents an explicit null / empty (case-insensitive)."""
    return value is None or str(value).strip().lower() in _NULLISH


def write_json(path, obj):
    """Write `obj` as pretty JSON atomically (temp file + os.replace)."""
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


# ── Config resolution ──────────────────────────────────────────────────────
def find_config(start=None):
    """Resolve the path to iconix.config.yaml.

    Order: $ICONIX_CONFIG_PATH/iconix.config.yaml → walk up from `start`/cwd.
    Returns None if not found.
    """
    root = os.environ.get("ICONIX_CONFIG_PATH")
    if root:
        cand = os.path.join(root, "iconix.config.yaml")
        if os.path.isfile(cand):
            return cand
    directory = os.path.abspath(start or os.getcwd())
    while True:
        cand = os.path.join(directory, "iconix.config.yaml")
        if os.path.isfile(cand):
            return cand
        parent = os.path.dirname(directory)
        if parent == directory:
            return None
        directory = parent


def artifact_root(config_path=None):
    """Directory that contains the artifact folders (use-cases/, robustness/, …).

    With $ICONIX_CONFIG_PATH set that is the meta-project root; otherwise it is the
    directory holding iconix.config.yaml; otherwise the current working directory.
    """
    root = os.environ.get("ICONIX_CONFIG_PATH")
    if root:
        return os.path.abspath(root)
    if config_path:
        return os.path.dirname(os.path.abspath(config_path))
    cfg = find_config()
    return os.path.dirname(os.path.abspath(cfg)) if cfg else os.getcwd()


def get_prefix(config_path=None):
    """Read project.prefix from iconix.config.yaml. Returns '' when absent."""
    if config_path is None:
        config_path = find_config()
    if not config_path or not os.path.isfile(config_path):
        return ""
    with open(config_path, encoding="utf-8") as fh:
        match = _PREFIX_RE.search(fh.read())
    return match.group(1).strip() if match else ""


# ── Checkpoint selection ───────────────────────────────────────────────────
_CKPT_DATE_RE = re.compile(r"checkpoint-(\d{4}-\d{2}-\d{2})")


def latest_checkpoint(migration_dir="migration"):
    """Return the path of the most-recent migration/checkpoint-<date>.json.

    Tie-break (when two files share a date): newer mtime wins. Returns None if no
    checkpoint exists.
    """
    files = glob.glob(os.path.join(migration_dir, "checkpoint-*.json"))
    if not files:
        return None

    def sort_key(path):
        match = _CKPT_DATE_RE.search(os.path.basename(path))
        date = match.group(1) if match else ""
        return (date, os.path.getmtime(path))

    return max(files, key=sort_key)


# ── DRAFT vs permanent artifact discrimination ─────────────────────────────
def is_draft(path):
    """True when a filename marks a migration DRAFT (un-promoted) artifact.

    DRAFT artifacts carry `DRAFT` in the filename (UC-DRAFT-001-*.md,
    RB-DRAFT-*.puml, *-DRAFT.puml). Permanent artifacts never do. The class model
    is the one exception — class-model/class-model.puml keeps its name when a DRAFT
    and is discriminated by a header stamp, not the filename (callers handle that).
    """
    return "DRAFT" in os.path.basename(path).upper()
