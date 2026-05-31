#!/usr/bin/env python3
"""promote.py — promote reviewed migration DRAFTs to permanent ICONIX IDs.

Replaces the 5-step DRAFT-promotion algorithm in `iconix-traceability.md` /
`/iconix-promote`. It scans DRAFT artifacts, gates on unresolved `[VERIFY]` markers,
assigns permanent IDs (via ids.py, highest + 1), renames files, rewrites internal IDs
and cross-references, preserves `Source-container:` annotations verbatim, and appends
the registry.

The single most load-bearing detail: the `[VERIFY]` gate counts on the regex
``\\[VERIFY`` (open-bracket + VERIFY, NO closing-bracket requirement) so it catches
`[VERIFY]`, `[VERIFY:HIGH]`, and `[VERIFY — note]`. A literal `[VERIFY]` match would
miss the severity-tagged forms and promote a dirty draft.

  --args "$ARGUMENTS" [--config iconix.config.yaml] [--dry-run]
    → JSON {promoted, promoted_noid, skipped_verify, skipped_already,
            multi_container, dry_run}

Exit codes: 0 some/all promoted · 1 nothing eligible · 2 IO error.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402
import ids  # noqa: E402

# Open-bracket + VERIFY — matches [VERIFY], [VERIFY:HIGH], [VERIFY — note]. Load-bearing.
VERIFY_RE = re.compile(r"\[VERIFY")

_ID_DRAFT_RE = re.compile(r"^(UC|RB|SD)-DRAFT-(\d+)-(.+)\.(md|puml)$", re.IGNORECASE)
_ID_DRAFT_FOLDERS = {"UC": "use-cases", "RB": "robustness", "SD": "sequence"}
_DRAFT_GLOBS = (
    "use-cases/UC-DRAFT-*.md",
    "robustness/RB-DRAFT-*.puml",
    "sequence/SD-DRAFT-*.puml",
    "domain-model/domain-model-DRAFT.puml",
    "use-case-packages/*-DRAFT.puml",
)


def _is_comment(line):
    stripped = line.lstrip()
    return stripped.startswith(("'", "#", "<!--", "//"))


def count_verify(text):
    return len(VERIFY_RE.findall(text))


def strip_draft_stamp(text):
    """Drop header comment lines carrying the DRAFT stamp (first 8 lines only).

    Must run AFTER ID rewriting, so a `' Traceability: UC-DRAFT-001` line has already
    become `' Traceability: PRJ-UC-001` and is no longer mistaken for a stamp. The
    `Source-container:` line never contains 'DRAFT', so it survives verbatim.
    """
    out = []
    for index, line in enumerate(text.splitlines(keepends=True)):
        # Never strip the Source-container annotation, even if a container name contains
        # the substring "DRAFT" (e.g. `DRAFTService`) — it is the Developer's multi-repo
        # routing signal and must survive promotion verbatim.
        if "Source-container:" in line:
            out.append(line)
            continue
        if index < 8 and _is_comment(line) and "DRAFT" in line.upper():
            continue
        out.append(line)
    return "".join(out)


def apply_mappings(text, mappings):
    """Rewrite every old DRAFT id → new permanent id with a digit-safe boundary.

    `(?!\\d)` stops `UC-DRAFT-1` from matching inside `UC-DRAFT-10`.
    """
    for old, new in mappings.items():
        text = re.sub(re.escape(old) + r"(?!\d)", new, text)
    return text


def classify(path):
    """Return a dict describing how to promote a draft file, or None to ignore."""
    name = os.path.basename(path)
    match = _ID_DRAFT_RE.match(name)
    if match:
        typ = match.group(1).upper()
        slug = match.group(3)
        ext = match.group(4)
        return {"kind": "id", "type": typ, "slug": slug, "ext": ext,
                "old_id": f"{typ}-DRAFT-{match.group(2)}", "path": path}
    if name == "class-model.puml":
        # Discover() only feeds this in when it carries a DRAFT header stamp. The name
        # never changes on promotion — only the stamp is removed.
        return {"kind": "noid", "slug": "class-model", "path": path, "new_name": "class-model.puml"}
    if name == "domain-model-DRAFT.puml" or name.endswith("-DRAFT.puml"):
        return {"kind": "noid", "slug": _slug_from(name), "path": path,
                "new_name": name.replace("-DRAFT", "")}
    return None


def _slug_from(name):
    base = re.sub(r"\.(md|puml)$", "", name, flags=re.IGNORECASE)
    return base.replace("-DRAFT", "")


def discover(root, slug_filter):
    import glob
    found = []
    for pattern in _DRAFT_GLOBS:
        found += glob.glob(os.path.join(root, pattern))
    class_model = os.path.join(root, "class-model", "class-model.puml")
    if os.path.isfile(class_model):
        with open(class_model, encoding="utf-8", errors="ignore") as fh:
            head = "".join(fh.readline() for _ in range(6))
        if "DRAFT" in head.upper():
            found.append(class_model)
    found = sorted(set(found))
    if slug_filter and slug_filter.lower() not in ("all", ""):
        found = [p for p in found if slug_filter.lower() in os.path.basename(p).lower()]
    return found


def _source_containers(text):
    match = re.search(r"Source-container:\s*(.+)", text)
    if not match:
        return []
    value = match.group(1).split("-->")[0].strip()
    return [c.strip() for c in value.split(",") if c.strip()]


def promote(args_str, config_path, dry_run):
    root = _common.artifact_root(config_path)
    prefix = _common.get_prefix(config_path)
    registry = os.path.join(root, "ids.registry.md")
    promoted_slugs = {r["slug"] for r in ids.read_rows(registry) if r["slug"]}

    slug_filter = (args_str or "").strip()
    candidates = []
    for path in discover(root, slug_filter):
        info = classify(path)
        if not info:
            continue
        with open(path, encoding="utf-8", errors="ignore") as fh:
            info["text"] = fh.read()
        candidates.append(info)

    result = {"promoted": [], "promoted_noid": [], "skipped_verify": [],
              "skipped_already": [], "multi_container": [], "dry_run": dry_run}

    eligible = []
    for info in candidates:
        rel = os.path.relpath(info["path"], root).replace("\\", "/")
        vcount = count_verify(info["text"])
        if vcount > 0:
            result["skipped_verify"].append({"file": rel, "count": vcount})
            continue
        if info["slug"] in promoted_slugs:
            result["skipped_already"].append({"file": rel, "slug": info["slug"]})
            continue
        eligible.append(info)

    # Assign IDs to ID-bearing drafts, sorted by filename within each type for a
    # reproducible allocation order.
    highest = ids.scan_registry(registry)
    counters = dict(highest)
    mappings = {}
    id_targets = sorted([e for e in eligible if e["kind"] == "id"],
                        key=lambda e: (e["type"], os.path.basename(e["path"])))
    for info in id_targets:
        typ = info["type"]
        counters[typ] = counters.get(typ, 0) + 1
        new_id = ids.format_id(prefix, typ, counters[typ])
        info["new_id"] = new_id
        mappings[info["old_id"]] = new_id
        folder = _ID_DRAFT_FOLDERS[typ]
        info["new_path"] = os.path.join(root, folder, f"{new_id}-{info['slug']}.{info['ext']}")

    # Rewrite + rename eligible files.
    for info in eligible:
        new_text = strip_draft_stamp(apply_mappings(info["text"], mappings))
        if info["kind"] == "id":
            new_path = info["new_path"]
            rel_new = os.path.relpath(new_path, root).replace("\\", "/")
            rel_old = os.path.relpath(info["path"], root).replace("\\", "/")
            if not dry_run:
                with open(new_path, "w", encoding="utf-8") as fh:
                    fh.write(new_text)
                if os.path.abspath(new_path) != os.path.abspath(info["path"]):
                    os.remove(info["path"])
                ids.main(["append", "--registry", registry,
                          "--row", f"{info['new_id']}|{info['slug']}|{rel_new}|promoted from {info['old_id']}"])
            result["promoted"].append({"draft": rel_old, "new_id": info["new_id"], "new_path": rel_new})
            for container_list in [_source_containers(new_text)]:
                if len(container_list) > 1:
                    result["multi_container"].append({"new_id": info["new_id"], "containers": container_list})
        else:  # noid: class-model keeps its name; others drop -DRAFT
            name = os.path.basename(info["path"])
            if name == "class-model.puml":
                new_path = info["path"]
            else:
                new_path = os.path.join(os.path.dirname(info["path"]), info["new_name"])
            rel_new = os.path.relpath(new_path, root).replace("\\", "/")
            rel_old = os.path.relpath(info["path"], root).replace("\\", "/")
            if not dry_run:
                with open(new_path, "w", encoding="utf-8") as fh:
                    fh.write(new_text)
                if os.path.abspath(new_path) != os.path.abspath(info["path"]):
                    os.remove(info["path"])
            result["promoted_noid"].append({"draft": rel_old, "new_path": rel_new})

    # Cross-reference update in DRAFT files that were NOT promoted (skipped), so a
    # reference to a now-promoted sibling resolves to its new ID.
    if mappings and not dry_run:
        eligible_paths = {os.path.abspath(e["path"]) for e in eligible}
        import glob
        for pattern in _DRAFT_GLOBS:
            for path in glob.glob(os.path.join(root, pattern)):
                if os.path.abspath(path) in eligible_paths:
                    continue
                with open(path, encoding="utf-8", errors="ignore") as fh:
                    text = fh.read()
                updated = apply_mappings(text, mappings)
                if updated != text:
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(updated)

    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Promote ICONIX migration DRAFTs")
    parser.add_argument("--args", default="", help="the raw $ARGUMENTS (slug filter or 'all')")
    parser.add_argument("--config", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    config_path = args.config or _common.find_config()
    result = promote(args.args, config_path, args.dry_run)
    _common.emit(result)
    if not result["promoted"] and not result["promoted_noid"]:
        return _common.EXIT_GATE  # nothing eligible
    return _common.EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
