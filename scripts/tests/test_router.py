"""Tests for router.py --migration-route — Cases A–E from checkpoint state."""

import json

import router
import _common


def run(argv):
    try:
        return router.main(argv)
    except SystemExit as exc:
        return exc.code


def write_ckpt(tmp_path, phases, name="checkpoint-2026-05-30.json"):
    mig = tmp_path / "migration"
    mig.mkdir(exist_ok=True)
    path = mig / name
    path.write_text(json.dumps({"phases_completed": phases}), encoding="utf-8")
    return str(path)


def test_case_a_no_checkpoint(tmp_path):
    r = router.route_migration(str(tmp_path / "migration"))
    assert r["next"] == "infra" and r["case"] == "A"


def test_case_b_infra_only(tmp_path):
    write_ckpt(tmp_path, ["infra"])
    r = router.route_migration(str(tmp_path / "migration"))
    assert r["next"] == "structural" and r["case"] == "B"


def test_case_c_infra_structural(tmp_path):
    write_ckpt(tmp_path, ["infra", "structural"])
    r = router.route_migration(str(tmp_path / "migration"))
    assert r["next"] == "semantic" and r["case"] == "C"


def test_case_d_all_three(tmp_path):
    write_ckpt(tmp_path, ["infra", "structural", "semantic"])
    r = router.route_migration(str(tmp_path / "migration"))
    assert r["next"] == "complete" and r["case"] == "D"


def test_case_e_corrupt_json(tmp_path):
    mig = tmp_path / "migration"
    mig.mkdir()
    (mig / "checkpoint-2026-05-30.json").write_text("{not json", encoding="utf-8")
    r = router.route_migration(str(mig))
    assert r["next"] == "corrupt" and r["case"] == "E"


def test_case_e_missing_phases(tmp_path):
    mig = tmp_path / "migration"
    mig.mkdir()
    (mig / "checkpoint-2026-05-30.json").write_text('{"run_date":"x"}', encoding="utf-8")
    r = router.route_migration(str(mig))
    assert r["next"] == "corrupt"


def test_latest_wins_over_older(tmp_path):
    write_ckpt(tmp_path, ["infra"], "checkpoint-2026-05-01.json")
    write_ckpt(tmp_path, ["infra", "structural", "semantic"], "checkpoint-2026-05-30.json")
    r = router.route_migration(str(tmp_path / "migration"))
    assert r["next"] == "complete"  # newest dated file selected


def test_explicit_missing_path_is_case_a(tmp_path):
    r = router.route_migration(str(tmp_path / "migration"), path=str(tmp_path / "nope.json"))
    assert r["next"] == "infra" and r["case"] == "A"


def test_route_always_exit_0(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert run(["--migration-route"]) == _common.EXIT_OK
    assert json.loads(capsys.readouterr().out)["next"] == "infra"


def test_requires_migration_route_flag():
    assert run([]) == _common.EXIT_IO


# ── review fix: valid-but-non-object JSON routes to corrupt, never crashes ───
def test_non_dict_json_is_corrupt(tmp_path):
    mig = tmp_path / "migration"
    mig.mkdir()
    (mig / "checkpoint-2026-05-30.json").write_text("[]", encoding="utf-8")
    r = router.route_migration(str(mig))
    assert r["next"] == "corrupt" and r["case"] == "E"


def test_invalid_utf8_is_corrupt(tmp_path):
    mig = tmp_path / "migration"
    mig.mkdir()
    (mig / "checkpoint-2026-05-30.json").write_bytes(b'{\x80"}')
    r = router.route_migration(str(mig))
    assert r["next"] == "corrupt"
