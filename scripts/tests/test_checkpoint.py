"""Tests for checkpoint.py — schema typing + Case-E corruption detection."""

import json
import os

import pytest

import checkpoint
import _common


def run(argv):
    """Invoke checkpoint.main, returning the exit code (SystemExit-safe)."""
    try:
        return checkpoint.main(argv)
    except SystemExit as exc:  # _common.die raises SystemExit
        return exc.code


# ── write: full schema + typing ────────────────────────────────────────────
def test_write_creates_full_schema(tmp_path):
    path = str(tmp_path / "migration" / "checkpoint-2026-05-30.json")
    run(["write", "--path", path,
         "--field", "run_date=2026-05-30",
         "--field", "mode=code-walking"])
    data = _common.read_json(path)
    # Every schema key present, defaults applied.
    assert set(data) == set(checkpoint.DEFAULTS)
    assert data["run_date"] == "2026-05-30"
    assert data["mode"] == "code-walking"
    assert data["phases_completed"] == ["infra"]
    assert data["next_phase"] == "structural"


def test_max_uc_coerced_to_int(tmp_path):
    """The bug this script fixes: max_uc must be a real int, not the string '20'."""
    path = str(tmp_path / "checkpoint-2026-05-30.json")
    run(["write", "--path", path, "--field", "max_uc=20"])
    data = _common.read_json(path)
    assert data["max_uc"] == 20
    assert isinstance(data["max_uc"], int)


def test_max_uc_absent_is_null(tmp_path):
    path = str(tmp_path / "checkpoint-2026-05-30.json")
    run(["write", "--path", path])
    assert _common.read_json(path)["max_uc"] is None


def test_max_uc_empty_is_null(tmp_path):
    path = str(tmp_path / "checkpoint-2026-05-30.json")
    run(["write", "--path", path, "--field", "max_uc="])
    assert _common.read_json(path)["max_uc"] is None


def test_entry_point_filter_comma_split(tmp_path):
    path = str(tmp_path / "checkpoint-2026-05-30.json")
    run(["write", "--path", path, "--field", "entry_point_filter=POST /orders, POST /payments"])
    assert _common.read_json(path)["entry_point_filter"] == ["POST /orders", "POST /payments"]


def test_entry_point_filter_json_array(tmp_path):
    path = str(tmp_path / "checkpoint-2026-05-30.json")
    run(["write", "--path", path, "--field", 'phases_completed=["infra","structural"]'])
    assert _common.read_json(path)["phases_completed"] == ["infra", "structural"]


def test_bool_and_int_fields(tmp_path):
    path = str(tmp_path / "checkpoint-2026-05-30.json")
    run(["write", "--path", path,
         "--field", "greenfield_coexistence=true",
         "--field", "entry_point_count=42"])
    data = _common.read_json(path)
    assert data["greenfield_coexistence"] is True
    assert data["entry_point_count"] == 42


# ── update: partial merge preserves phases_completed ───────────────────────
def test_update_preserves_phases(tmp_path):
    path = str(tmp_path / "checkpoint-2026-05-30.json")
    run(["write", "--path", path, "--field", 'phases_completed=["infra"]'])
    run(["update", "--path", path,
         "--field", "containers_surveyed=OrderService,PaymentService",
         "--field", "entry_point_count=12"])
    data = _common.read_json(path)
    assert data["phases_completed"] == ["infra"]  # untouched
    assert data["containers_surveyed"] == ["OrderService", "PaymentService"]
    assert data["entry_point_count"] == 12


def test_update_missing_file_is_io_error(tmp_path):
    assert run(["update", "--path", str(tmp_path / "nope.json"), "--field", "x=1"]) == _common.EXIT_IO


# ── read ───────────────────────────────────────────────────────────────────
def test_read_single_field(tmp_path, capsys):
    path = str(tmp_path / "checkpoint-2026-05-30.json")
    run(["write", "--path", path, "--field", "scope=OrderService"])
    capsys.readouterr()  # clear write output
    run(["read", "--path", path, "--field", "scope"])
    assert json.loads(capsys.readouterr().out.strip()) == "OrderService"


# ── validate: Case-E corruption + infra gate ───────────────────────────────
def test_validate_ok(tmp_path):
    path = str(tmp_path / "checkpoint-2026-05-30.json")
    run(["write", "--path", path,
         "--field", "containers_surveyed=OrderService",
         "--field", "entry_point_count=5"])
    assert run(["validate", "--path", path, "--phase", "infra"]) == _common.EXIT_OK


def test_validate_empty_object_fails(tmp_path):
    path = tmp_path / "checkpoint-2026-05-30.json"
    path.write_text("{}", encoding="utf-8")
    assert run(["validate", "--path", str(path)]) == _common.EXIT_GATE


def test_validate_missing_phases_is_corrupt(tmp_path):
    path = tmp_path / "checkpoint-2026-05-30.json"
    path.write_text(json.dumps({"run_date": "2026-05-30"}), encoding="utf-8")
    assert run(["validate", "--path", str(path)]) == _common.EXIT_GATE


def test_validate_corrupt_json(tmp_path):
    path = tmp_path / "checkpoint-2026-05-30.json"
    path.write_text("{not json", encoding="utf-8")
    assert run(["validate", "--path", str(path)]) == _common.EXIT_GATE


def test_validate_infra_gate_rejects_zero_entry_points(tmp_path):
    path = str(tmp_path / "checkpoint-2026-05-30.json")
    run(["write", "--path", path, "--field", "containers_surveyed=OrderService"])
    # entry_point_count defaults to 0 → infra gate must fail.
    assert run(["validate", "--path", path, "--phase", "infra"]) == _common.EXIT_GATE


def test_validate_infra_gate_rejects_empty_containers(tmp_path):
    path = str(tmp_path / "checkpoint-2026-05-30.json")
    run(["write", "--path", path, "--field", "entry_point_count=5"])
    assert run(["validate", "--path", path, "--phase", "infra"]) == _common.EXIT_GATE


# ── _common helpers exercised here (no separate test_common yet) ────────────
def test_latest_checkpoint_tiebreak(tmp_path, monkeypatch):
    mig = tmp_path / "migration"
    mig.mkdir()
    (mig / "checkpoint-2026-05-01.json").write_text("{}", encoding="utf-8")
    newer = mig / "checkpoint-2026-05-30.json"
    newer.write_text("{}", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert os.path.basename(_common.latest_checkpoint("migration")) == "checkpoint-2026-05-30.json"


def test_latest_checkpoint_none(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert _common.latest_checkpoint("migration") is None


# ── review fixes: non-dict JSON, invalid UTF-8, BOM, unknown key, case-null ──
def test_validate_non_dict_json_is_corrupt(tmp_path):
    path = tmp_path / "checkpoint-2026-05-30.json"
    path.write_text("[]", encoding="utf-8")  # valid JSON, not an object
    assert run(["validate", "--path", str(path)]) == _common.EXIT_GATE


def test_validate_invalid_utf8_is_corrupt(tmp_path):
    path = tmp_path / "checkpoint-2026-05-30.json"
    path.write_bytes(b'{\x80"}')  # garbled bytes — must classify corrupt, not crash
    assert run(["validate", "--path", str(path)]) == _common.EXIT_GATE


def test_bom_prefixed_valid_checkpoint_reads_ok(tmp_path):
    path = tmp_path / "checkpoint-2026-05-30.json"
    path.write_text('{"phases_completed":["infra"],"next_phase":"structural"}', encoding="utf-8-sig")
    assert run(["validate", "--path", str(path)]) == _common.EXIT_OK


def test_unknown_field_rejected(tmp_path):
    path = str(tmp_path / "checkpoint-2026-05-30.json")
    # typo'd key (missing underscore) must be rejected, not silently stored
    assert run(["write", "--path", path, "--field", "phasescompleted=infra"]) == _common.EXIT_IO


def test_nullish_case_insensitive(tmp_path):
    path = str(tmp_path / "checkpoint-2026-05-30.json")
    run(["write", "--path", path, "--field", "scope=NONE", "--field", "max_uc=Null"])
    data = _common.read_json(path)
    assert data["scope"] is None
    assert data["max_uc"] is None
