"""Tests for ids.py — highest+1 allocation, never-reuse, prefixed + bare forms."""

import json
import os

import ids
import _common


def run(argv):
    try:
        return ids.main(argv)
    except SystemExit as exc:
        return exc.code


REG_PREFIXED = """# ID Registry

| ID | Slug | Path | Note |
|---|---|---|---|
| PRJ-UC-006 | cart | use-cases/PRJ-UC-006-cart.md | promoted from UC-DRAFT-002 |
| PRJ-RB-003 | cart | robustness/PRJ-RB-003-cart.puml | promoted from RB-DRAFT-001 |
"""

REG_GAP = """| ID | Slug | Path | Note |
|---|---|---|---|
| PRJ-UC-001 | a | use-cases/PRJ-UC-001-a.md | x |
| PRJ-UC-005 | b | use-cases/PRJ-UC-005-b.md | x |
"""

CONFIG_PRJ = 'project:\n  name: "Demo"\n  prefix: "PRJ"\n'


def write(path, text):
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_empty_registry_starts_at_001(tmp_path, capsys):
    reg = str(tmp_path / "ids.registry.md")  # does not exist
    cfg = write(tmp_path / "iconix.config.yaml", CONFIG_PRJ)
    run(["next", "--type", "UC", "--registry", reg, "--config", cfg])
    out = json.loads(capsys.readouterr().out)
    assert out["UC"] == "PRJ-UC-001"


def test_highest_plus_one_per_type(tmp_path, capsys):
    reg = write(tmp_path / "ids.registry.md", REG_PREFIXED)
    cfg = write(tmp_path / "iconix.config.yaml", CONFIG_PRJ)
    run(["next", "--type", "UC", "--type", "RB", "--registry", reg, "--config", cfg])
    out = json.loads(capsys.readouterr().out)
    assert out == {"UC": "PRJ-UC-007", "RB": "PRJ-RB-004"}


def test_no_gap_fill(tmp_path, capsys):
    reg = write(tmp_path / "ids.registry.md", REG_GAP)
    cfg = write(tmp_path / "iconix.config.yaml", CONFIG_PRJ)
    run(["next", "--type", "UC", "--registry", reg, "--config", cfg])
    out = json.loads(capsys.readouterr().out)
    assert out["UC"] == "PRJ-UC-006"  # 5+1, not the missing 002


def test_bare_ids_recognized(tmp_path, capsys):
    reg = write(tmp_path / "ids.registry.md",
                "| ID | Slug |\n|---|---|\n| UC-003 | x |\n| RB-002 | y |\n")
    cfg = write(tmp_path / "iconix.config.yaml", CONFIG_PRJ)
    run(["next", "--type", "UC", "--registry", reg, "--config", cfg])
    out = json.loads(capsys.readouterr().out)
    assert out["UC"] == "PRJ-UC-004"


def test_id_in_note_not_miscounted(tmp_path, capsys):
    # A real-looking ID inside the Note column must NOT bump the counter.
    reg = write(tmp_path / "ids.registry.md",
                "| ID | Slug | Path | Note |\n|---|---|---|---|\n"
                "| PRJ-UC-002 | a | p | see PRJ-UC-099 for history |\n")
    cfg = write(tmp_path / "iconix.config.yaml", CONFIG_PRJ)
    run(["next", "--type", "UC", "--registry", reg, "--config", cfg])
    out = json.loads(capsys.readouterr().out)
    assert out["UC"] == "PRJ-UC-003"  # 2+1, NOT 100


def test_uc_draft_not_counted(tmp_path, capsys):
    # UC-DRAFT-001 must not parse as UC-001.
    reg = write(tmp_path / "ids.registry.md",
                "| ID | Slug |\n|---|---|\n| UC-DRAFT-007 | x |\n")
    cfg = write(tmp_path / "iconix.config.yaml", CONFIG_PRJ)
    run(["next", "--type", "UC", "--registry", reg, "--config", cfg])
    out = json.loads(capsys.readouterr().out)
    assert out["UC"] == "PRJ-UC-001"


def test_no_prefix_yields_bare_id(tmp_path, capsys):
    reg = str(tmp_path / "ids.registry.md")
    cfg = write(tmp_path / "iconix.config.yaml", 'project:\n  name: "Demo"\n')
    run(["next", "--type", "UC", "--registry", reg, "--config", cfg])
    out = json.loads(capsys.readouterr().out)
    assert out["UC"] == "UC-001"


def test_work_item_prefix_not_mistaken_for_prefix(tmp_path, capsys):
    # `work_item_prefix:` must not be picked up as project.prefix.
    cfg_text = 'project:\n  prefix: "RGS"\ngit:\n  work_item_prefix: "AB#"\n'
    reg = str(tmp_path / "ids.registry.md")
    cfg = write(tmp_path / "iconix.config.yaml", cfg_text)
    run(["next", "--type", "UC", "--registry", reg, "--config", cfg])
    out = json.loads(capsys.readouterr().out)
    assert out["UC"] == "RGS-UC-001"


def test_append_creates_file_with_header(tmp_path):
    reg = tmp_path / "ids.registry.md"
    run(["append", "--registry", str(reg),
         "--row", "PRJ-UC-001|checkout|use-cases/PRJ-UC-001-checkout.md|promoted"])
    text = reg.read_text(encoding="utf-8")
    assert "| ID | Slug | Path | Note |" in text
    assert "| PRJ-UC-001 | checkout | use-cases/PRJ-UC-001-checkout.md | promoted |" in text


def test_append_then_next_sees_new_id(tmp_path, capsys):
    reg = tmp_path / "ids.registry.md"
    cfg = write(tmp_path / "iconix.config.yaml", CONFIG_PRJ)
    run(["append", "--registry", str(reg), "--row", "PRJ-UC-009|x|p|n"])
    capsys.readouterr()
    run(["next", "--type", "UC", "--registry", str(reg), "--config", cfg])
    out = json.loads(capsys.readouterr().out)
    assert out["UC"] == "PRJ-UC-010"


def test_unknown_type_errors(tmp_path):
    cfg = write(tmp_path / "iconix.config.yaml", CONFIG_PRJ)
    assert run(["next", "--type", "WIDGET", "--config", cfg]) == _common.EXIT_IO


# ── review fix: scan ID column only, aligned with read_rows ─────────────────
def test_blank_id_column_row_ignored(tmp_path, capsys):
    # ID column empty; an ID in a later cell must NOT be counted.
    reg = write(tmp_path / "ids.registry.md",
                "| ID | Slug | Path | Note |\n|---|---|---|---|\n|  | PRJ-UC-099 | uc/orphan.md | x |\n")
    cfg = write(tmp_path / "iconix.config.yaml", CONFIG_PRJ)
    run(["next", "--type", "UC", "--registry", reg, "--config", cfg])
    assert json.loads(capsys.readouterr().out)["UC"] == "PRJ-UC-001"


def test_id_only_note_cell_ignored(tmp_path, capsys):
    reg = write(tmp_path / "ids.registry.md",
                "| ID | Slug | Path | Note |\n|---|---|---|---|\n|  |  |  | UC-042 |\n")
    cfg = write(tmp_path / "iconix.config.yaml", CONFIG_PRJ)
    run(["next", "--type", "UC", "--registry", reg, "--config", cfg])
    assert json.loads(capsys.readouterr().out)["UC"] == "PRJ-UC-001"


def test_scan_and_read_rows_agree(tmp_path):
    reg = write(tmp_path / "ids.registry.md",
                "| ID | Slug | Path | Note |\n|---|---|---|---|\n"
                "| PRJ-UC-003 | a | p | x |\n|  | PRJ-UC-099 | q | y |\n")
    highest = ids.scan_registry(reg)
    rows = ids.read_rows(reg)
    # both see only the well-formed row (UC-003); the blank-ID row is ignored by both
    assert highest.get("UC") == 3
    assert [r["id"] for r in rows] == ["PRJ-UC-003"]
