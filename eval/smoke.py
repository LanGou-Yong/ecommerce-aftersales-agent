# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)


def test_health():
    assert c.get("/health").json()["status"] == "ok"


def test_policy():
    r = c.post("/ticket", json={"query": "七天无理由运费谁出"}).json()
    assert r["intent"] == "policy"
    assert r["sources"]


def test_order():
    r = c.post("/ticket", json={"query": "A1001 物流到哪了", "order_id": "A1001"}).json()
    assert r["intent"] == "order"
    assert "深圳" in r["answer"]


def test_refund_hitl():
    r = c.post("/ticket", json={"query": "A1001 我要退款", "order_id": "A1001"}).json()
    assert r["status"] == "needs_approval"
    a = c.post("/approve_refund", json={"ticket_id": r["ticket_id"]}).json()
    assert a["ok"] is True


def test_no_auto_invent_order():
    r = c.post("/ticket", json={"query": "Z9999 到哪了", "order_id": "Z9999"}).json()
    assert "未查到" in r["answer"]


if __name__ == "__main__":
    test_health()
    test_policy()
    test_order()
    test_refund_hitl()
    test_no_auto_invent_order()
    print("SMOKE_OK")
