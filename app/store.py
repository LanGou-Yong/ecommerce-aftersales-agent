# -*- coding: utf-8 -*-
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "shop.db"


def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        sku TEXT,
        status TEXT,
        logistics TEXT,
        amount REAL
    )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS tickets (
        ticket_id TEXT PRIMARY KEY,
        query TEXT,
        intent TEXT,
        status TEXT,
        answer TEXT,
        sources TEXT
    )"""
    )
    n = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    if n == 0:
        conn.executemany(
            "INSERT INTO orders VALUES (?,?,?,?,?)",
            [
                ("A1001", "无线耳机", "shipped", "到达深圳转运中心", 199.0),
                ("A1002", "键盘", "delivered", "已签收", 329.0),
                ("A1003", "定制刻字杯", "delivered", "已签收", 59.0),
            ],
        )
    conn.commit()
    conn.close()
