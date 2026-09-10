# -*- coding: utf-8 -*-
import uuid
from fastapi import FastAPI
from pydantic import BaseModel

from app.intent import classify
from app.retrieve import retrieve
from app.store import connect, init_db

init_db()
app = FastAPI(title="ecommerce-aftersales-agent-demo")


class TicketIn(BaseModel):
    query: str
    order_id: str | None = None


class ApproveIn(BaseModel):
    ticket_id: str


@app.get("/health")
def health():
    return {"status": "ok", "demo": True}


def lookup_order(order_id: str):
    conn = connect()
    row = conn.execute("SELECT * FROM orders WHERE order_id=?", (order_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


@app.post("/ticket")
def ticket(body: TicketIn):
    intent = classify(body.query)
    tid = "T" + uuid.uuid4().hex[:8]
    sources = []
    status = "answered"
    if intent == "human":
        answer = "该问题需要人工客服接手，Agent 不继续自动答复。"
        status = "handoff"
    elif intent == "order":
        oid = body.order_id or ""
        for token in body.query.replace("，", " ").split():
            if token.upper().startswith("A"):
                oid = token.upper()
        info = lookup_order(oid) if oid else None
        if not info:
            answer = "未查到订单。请提供订单号（示例 A1001）。订单状态不由模型编造。"
        else:
            answer = "订单 {order_id} 商品 {sku}，状态 {status}，物流：{logistics}。".format(**info)
            sources = ["orders 表（只读）"]
    elif intent == "refund":
        oid = body.order_id or ""
        for token in body.query.replace("，", " ").split():
            if token.upper().startswith("A"):
                oid = token.upper()
        info = lookup_order(oid) if oid else None
        hits = retrieve(body.query)
        sources = hits[:2]
        if not info:
            answer = "退款前必须命中真实订单。请提供订单号。退款不会自动执行。"
            status = "need_order"
        else:
            answer = (
                "已生成退款草稿：订单 {oid}，金额 {amount} 元。当前状态 needs_approval。"
                "请坐席审核后调用批准接口。政策依据见 sources。Agent 未执行退款。"
            ).format(oid=info["order_id"], amount=info["amount"])
            status = "needs_approval"
    else:
        hits = retrieve(body.query)
        sources = hits[:2]
        if not hits:
            answer = "知识库未覆盖该政策，请转人工，不要用通识编造规则。"
            status = "no_hit"
        else:
            answer = "根据内部售后政策：\n" + "\n---\n".join(hits[:2])

    conn = connect()
    conn.execute(
        "INSERT INTO tickets VALUES (?,?,?,?,?,?)",
        (tid, body.query, intent, status, answer, " | ".join(sources) if isinstance(sources, list) else str(sources)),
    )
    conn.commit()
    conn.close()
    return {"ticket_id": tid, "intent": intent, "status": status, "answer": answer, "sources": sources}


@app.post("/approve_refund")
def approve(body: ApproveIn):
    conn = connect()
    row = conn.execute("SELECT * FROM tickets WHERE ticket_id=?", (body.ticket_id,)).fetchone()
    if not row:
        conn.close()
        return {"ok": False, "error": "ticket not found"}
    if row["intent"] != "refund" or row["status"] != "needs_approval":
        conn.close()
        return {"ok": False, "error": "not a pending refund ticket"}
    conn.execute("UPDATE tickets SET status=? WHERE ticket_id=?", ("approved", body.ticket_id))
    conn.commit()
    conn.close()
    return {"ok": True, "ticket_id": body.ticket_id, "status": "approved", "note": "demo only, no real payout"}
