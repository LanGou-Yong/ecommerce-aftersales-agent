# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / "data" / "policies.md").read_text(encoding="utf-8")
CHUNKS = [c.strip() for c in TEXT.split("## ") if c.strip()]


def retrieve(query: str, k: int = 2):
    q = set(query)
    scored = []
    for ch in CHUNKS:
        overlap = len(q & set(ch)) / max(len(q), 1)
        bonus = sum(1 for w in ["七天", "无理由", "运费", "质量", "退款", "时效"] if w in query and w in ch)
        scored.append((overlap + bonus, ch))
    scored.sort(reverse=True)
    return [c for s, c in scored[:k] if s > 0]
