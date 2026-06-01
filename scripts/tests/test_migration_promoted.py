"""Tests for migration_promoted.py — permanent-RB boundary scan + match classes."""

import migration_promoted as mpr

RB_CHECKOUT = """' PRJ-RB-001 checkout
' Traceability: PRJ-UC-001
@startuml
actor User
boundary "POST /orders" as B1
control PlaceOrderController as C1
entity Order as E1
@enduml
"""

RB_ORDERS_PARAM = """' PRJ-RB-002 view-order
' Traceability: PRJ-UC-002
@startuml
boundary "GET /orders/{orderId}" as B1
control OrderController as C1
@enduml
"""

RB_DRAFT = """' RB-DRAFT-003 search
@startuml
boundary "GET /search" as B1
@enduml
"""


def setup_rb(tmp_path):
    rb = tmp_path / "robustness"
    rb.mkdir()
    (rb / "PRJ-RB-001-checkout.puml").write_text(RB_CHECKOUT, encoding="utf-8")
    (rb / "PRJ-RB-002-view-order.puml").write_text(RB_ORDERS_PARAM, encoding="utf-8")
    (rb / "RB-DRAFT-003-search.puml").write_text(RB_DRAFT, encoding="utf-8")
    return str(rb)


def test_permanent_only_excludes_draft(tmp_path):
    rb = setup_rb(tmp_path)
    r = mpr.scan(rb, "PRJ", [])
    boundaries = {b["boundary_name"] for b in r["promoted_boundaries"]}
    assert "POST /orders" in boundaries
    assert "GET /orders/{param}" not in boundaries  # raw form stored, not normalized
    assert "GET /search" not in boundaries  # DRAFT excluded


def test_exact_match_already_promoted(tmp_path):
    rb = setup_rb(tmp_path)
    r = mpr.scan(rb, "PRJ", ["POST /orders"])
    assert r["skip_count"] == 1
    assert r["already_promoted"][0]["uc_id"] == "PRJ-UC-001"
    assert r["already_promoted"][0]["entry_point"] == "POST /orders"


def test_path_param_normalized_match(tmp_path):
    rb = setup_rb(tmp_path)
    # entry point uses {id}; boundary uses {orderId} → both normalize to {param}
    r = mpr.scan(rb, "PRJ", ["GET /orders/{id}"])
    assert r["skip_count"] == 1
    assert r["already_promoted"][0]["uc_id"] == "PRJ-UC-002"


def test_fuzzy_match_is_ambiguous_not_skipped(tmp_path):
    rb = setup_rb(tmp_path)
    # "OrderController.PlaceOrder" contains boundary token? boundary is "GET /orders/{param}"
    # Use a class.method that substring-matches a control-derived... here we target the
    # boundary "POST /orders" partial: "/orders" appears in the entry point string.
    r = mpr.scan(rb, "PRJ", ["POST /orders/extra"])
    assert r["skip_count"] == 0
    assert any(a["entry_point"] == "POST /orders/extra" for a in r["ambiguous"])


def test_unmatched_entry_point_neither(tmp_path):
    rb = setup_rb(tmp_path)
    r = mpr.scan(rb, "PRJ", ["DELETE /accounts"])
    assert r["skip_count"] == 0
    assert r["ambiguous"] == []


def test_no_filter_returns_all_boundaries(tmp_path):
    rb = setup_rb(tmp_path)
    r = mpr.scan(rb, "PRJ", [])
    assert r["skip_count"] == 0
    assert len(r["promoted_boundaries"]) == 2  # two permanent RBs, one boundary each


def test_uc_id_falls_back_to_filename(tmp_path):
    rb = tmp_path / "robustness"
    rb.mkdir()
    (rb / "PRJ-RB-009-no-header.puml").write_text(
        "@startuml\nboundary \"POST /thing\" as B1\n@enduml\n", encoding="utf-8")
    r = mpr.scan(str(rb), "PRJ", ["POST /thing"])
    assert r["already_promoted"][0]["uc_id"] == "PRJ-RB-009-no-header.puml"


# ── review fix: reused-page <<from UC-XXX>> stereotype is not this RB's UC ───
def test_reused_page_stereotype_not_mistaken_for_uc(tmp_path):
    rb = tmp_path / "robustness"
    rb.mkdir()
    content = ("@startuml\n"
               'boundary "Login" as P <<from PRJ-UC-099 Login>>\n'
               'boundary "POST /thing" as B1\n'
               "note bottom\nUC: PRJ-UC-005\nend note\n@enduml\n")
    (rb / "PRJ-RB-005-thing.puml").write_text(content, encoding="utf-8")
    r = mpr.scan(str(rb), "PRJ", ["POST /thing"])
    assert r["already_promoted"][0]["uc_id"] == "PRJ-UC-005"  # not PRJ-UC-099
