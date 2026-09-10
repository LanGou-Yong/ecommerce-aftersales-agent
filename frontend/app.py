# -*- coding: utf-8 -*-
import os
import httpx
import streamlit as st

API = os.environ.get("API_BASE", "http://127.0.0.1:8011")
st.set_page_config(page_title="售后工单 Demo", layout="wide")
st.title("电商售后工单助手（脱敏 Demo）")
try:
    ok = httpx.get(API + "/health", timeout=2).json().get("status") == "ok"
except Exception:
    ok = False
st.sidebar.write("后端服务在线" if ok else "后端未启动")
q = st.text_input("坐席/用户问题", "七天无理由怎么退？运费谁出？")
oid = st.text_input("订单号（查单/退款用）", "A1001")
if st.button("提交工单") and q.strip():
    r = httpx.post(API + "/ticket", json={"query": q, "order_id": oid or None}, timeout=10)
    st.session_state["last"] = r.json()
    st.json(st.session_state["last"])
last = st.session_state.get("last")
if last and last.get("status") == "needs_approval":
    if st.button("人工批准退款（演示）"):
        r = httpx.post(API + "/approve_refund", json={"ticket_id": last["ticket_id"]}, timeout=10)
        st.json(r.json())
