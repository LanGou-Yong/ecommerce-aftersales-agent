# -*- coding: utf-8 -*-

def classify(query: str) -> str:
    q = query.replace(" ", "")
    if any(w in q for w in ["投诉", "报警", "律师", "曝光"]):
        return "human"
    if any(w in q for w in ["退款", "退货", "退钱", "退单"]):
        return "refund"
    if any(w in q for w in ["物流", "到哪", "订单", "签收", "快递"]):
        return "order"
    return "policy"
