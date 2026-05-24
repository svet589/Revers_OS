#!/usr/bin/env python3
"""
REVERS OS v3.0 — База данных (история команд)
"""

import os
import sqlite3
from core.utils import C_DIM, C_BRIGHT, C_RESET

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
HISTORY_DB = os.path.join(DATA_DIR, "history.db")

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(HISTORY_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  command TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def add_to_history(cmd):
    conn = sqlite3.connect(HISTORY_DB)
    c = conn.cursor()
    c.execute("INSERT INTO history (command) VALUES (?)", (cmd,))
    conn.commit()
    conn.close()

def show_history(limit=20):
    conn = sqlite3.connect(HISTORY_DB)
    c = conn.cursor()
    c.execute("SELECT command, timestamp FROM history ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    for cmd, ts in rows:
        print(f"{C_DIM}{ts}{C_RESET} -> {C_BRIGHT}{cmd}{C_RESET}")
    conn.close()

def search_history(query):
    conn = sqlite3.connect(HISTORY_DB)
    c = conn.cursor()
    c.execute("SELECT command, timestamp FROM history WHERE command LIKE ? ORDER BY id DESC", (f"%{query}%",))
    rows = c.fetchall()
    if rows:
        print(f"{C_INFO}Результаты поиска по '{query}':{C_RESET}")
        for cmd, ts in rows:
            print(f"{C_DIM}{ts}{C_RESET} -> {C_BRIGHT}{cmd}{C_RESET}")
    else:
        print(f"{C_DIM}Ничего не найдено.{C_RESET}")
    conn.close()
