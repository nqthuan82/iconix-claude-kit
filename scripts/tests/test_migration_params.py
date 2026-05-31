"""Tests for migration_params.py — normalize, path-param canonicalisation, precedence."""

import json

import migration_params as mp
import _common


def run(argv):
    try:
        return mp.main(argv)
    except SystemExit as exc:
        return exc.code


def test_entry_points_split_and_trim(capsys):
    run(["--entry-point", "POST /orders, OrderController.Place"])
    out = json.loads(capsys.readouterr().out)
    assert out["entry_point_filter"] == ["POST /orders", "OrderController.Place"]


def test_path_param_canonicalised():
    r = mp.normalize("", "", "POST /orders/{orderId}")
    assert r["entry_point_filter"] == ["POST /orders/{param}"]


def test_class_method_untouched():
    r = mp.normalize("", "", "OrderController.PlaceOrder")
    assert r["entry_point_filter"] == ["OrderController.PlaceOrder"]


def test_precedence_nulls_max_uc(capsys):
    run(["--max-uc", "20", "--entry-point", "POST /orders"])
    out = json.loads(capsys.readouterr().out)
    assert out["max_uc"] is None
    assert out["precedence_applied"] is True


def test_max_uc_alone_kept():
    r = mp.normalize("OrderService", "20", "")
    assert r["max_uc"] == 20
    assert r["scope"] == "OrderService"
    assert r["precedence_applied"] is False


def test_invalid_max_uc_exits_1():
    assert run(["--max-uc", "-1"]) == _common.EXIT_GATE
    assert run(["--max-uc", "abc"]) == _common.EXIT_GATE
    assert run(["--max-uc", "0"]) == _common.EXIT_GATE


def test_all_empty_is_null(capsys):
    run([])
    out = json.loads(capsys.readouterr().out)
    assert out == {"scope": None, "max_uc": None, "entry_point_filter": None, "precedence_applied": False}


def test_empty_entry_points_dropped():
    r = mp.normalize("", "", "POST /orders, ,  ,")
    assert r["entry_point_filter"] == ["POST /orders"]


def test_precedence_false_when_no_max_uc(capsys):
    # entry-point present but no max_uc → max_uc null, but precedence_applied stays false
    run(["--entry-point", "POST /orders"])
    out = json.loads(capsys.readouterr().out)
    assert out["max_uc"] is None
    assert out["precedence_applied"] is False
