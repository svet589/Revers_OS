#!/usr/bin/env python3
"""
REVERS OS v3.0 — KRAKEN OSINT
Цифровой профиль по email/телефону/username
"""

import os
import json
import sqlite3
import csv
import requests
import re
import subprocess
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

KRAKEN_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "db")
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

loaded_dbs = {}

def detect_format(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".json": return "json"
    elif ext == ".csv": return "csv"
    elif ext in [".db", ".sqlite", ".sqlite3"]: return "sqlite"
    return None

def load_json_db(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_csv_db(filepath):
    data = {}
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.get("username") or row.get("nick") or row.get("email") or str(len(data))
            data[key] = row
    return data

def load_sqlite_db(filepath):
    data = {}
    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in c.fetchall()]
    for table in tables:
        try:
            c.execute(f"SELECT * FROM {table}")
            rows = c.fetchall()
            cols = [desc[0] for desc in c.description]
            for row in rows:
                row_dict = dict(zip(cols, row))
                key = row_dict.get("username") or row_dict.get("nick") or row_dict.get("email") or str(row[0])
                data[key] = row_dict
        except:
            pass
    conn.close()
    return data

def search_in_data(target, data):
    target_lower = target.lower()
    results = {}
    for key, value in data.items():
        if isinstance(value, dict):
            if target_lower in str(key).lower():
                results[key] = value
            for subval in value.values():
                if target_lower in str(subval).lower():
                    results[key] = value
                    break
        elif isinstance(value, list):
            for item in value:
                if target_lower in str(item).lower():
                    results[key] = value
                    break
        else:
            if target_lower in str(value).lower() or target_lower in str(key).lower():
                results[key] = value
    return results

def check_hibp(email):
    breaches = []
    try:
        resp = requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
            headers={"User-Agent": "KRAKEN", "hibp-api-key": ""},
            timeout=10
        )
        if resp.status_code == 200:
            for b in resp.json():
                breaches.append({"name": b.get("Name", ""), "date": b.get("BreachDate", ""), "data": b.get("DataClasses", [])})
    except:
        pass
    return breaches

def check_emailrep(email):
    info = {}
    try:
        resp = requests.get(f"https://emailrep.io/{email}", headers={"User-Agent": "KRAKEN"}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            info["reputation"] = data.get("reputation", "unknown")
            info["suspicious"] = data.get("suspicious", False)
            info["details"] = data.get("details", {})
    except:
        pass
    return info

def check_whatsmyname(username):
    results = {}
    try:
        resp = requests.get(f"https://whatsmyname.app/?q={username}", headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            links = re.findall(r'https?://[^\s"\']+', resp.text)
            for link in links:
                if username.lower() in link.lower():
                    domain = re.findall(r'https?://(?:www\.)?([^/]+)', link)
                    if domain:
                        results[domain[0]] = link
    except:
        pass
    return results

def db_load(args):
    if not args:
        print(f"{C_ERROR}[X] Использование: kraken-db <путь>{C_RESET}")
        return
    filepath = args[0]
    if not os.path.exists(filepath):
        print(f"{C_ERROR}[X] Файл не найден: {filepath}{C_RESET}")
        return
    fmt = detect_format(filepath)
    if not fmt:
        print(f"{C_ERROR}[X] Неподдерживаемый формат. Используйте JSON, CSV, SQLite.{C_RESET}")
        return
    try:
        if fmt == "json": data = load_json_db(filepath)
        elif fmt == "csv": data = load_csv_db(filepath)
        elif fmt == "sqlite": data = load_sqlite_db(filepath)
        loaded_dbs[filepath] = data
        print(f"{C_SUCCESS}[OK] База загружена. Записей: {len(data)}{C_RESET}")
    except Exception as e:
        print(f"{C_ERROR}[X] Ошибка загрузки: {e}{C_RESET}")

def run_kraken(args):
    if not args:
        target = input(f"{C_INFO}Введите цель (email/телефон/username): {C_RESET}").strip()
    else:
        target = args[0]
    
    if not target:
        print(f"{C_ERROR}[X] Цель не указана.{C_RESET}")
        return
    
    if "@" in target:
        target_type = "email"
    elif target.replace("+", "").replace("-", "").replace(" ", "").isdigit():
        target_type = "phone"
    else:
        target_type = "username"
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🐙 KRAKEN OSINT{C_RESET}")
    print(f"{C_WARNING}         Тип: {target_type.upper()}{C_RESET}")
    print(f"{C_WARNING}         Цель: {C_BRIGHT}{target}{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    # Этап 1: Свои базы
    print(f"{C_INFO}[*] Поиск в загруженных базах...{C_RESET}")
    all_local = {}
    for filepath, data in loaded_dbs.items():
        found = search_in_data(target, data)
        if found:
            basename = os.path.basename(filepath)
            all_local[basename] = found
            print(f"  {C_SUCCESS}[+]{C_RESET} {basename}: найдено {len(found)} записей")
    if not all_local:
        print(f"  {C_DIM}[~] Загруженных баз нет. Используйте kraken-db для загрузки.{C_RESET}")
    
    # Этап 2: Онлайн
    print(f"\n{C_INFO}[*] Онлайн-источники...{C_RESET}")
    
    hibp_results = []
    emailrep_results = {}
    whatsmyname_results = {}
    
    if target_type == "email":
        hibp_results = check_hibp(target)
        print(f"  {C_SUCCESS}[+]{C_RESET} HIBP: {len(hibp_results)} утечек")
        emailrep_results = check_emailrep(target)
        print(f"  {C_SUCCESS}[+]{C_RESET} EmailRep: получен")
    
    if target_type in ["username", "email"]:
        whatsmyname_results = check_whatsmyname(target)
        print(f"  {C_SUCCESS}[+]{C_RESET} WhatsMyName: {len(whatsmyname_results)} ссылок")
    
    # Вывод отчёта
    print(f"\n{C_WARNING}═══════════════ ОТЧЁТ ═══════════════{C_RESET}")
    
    if all_local:
        print(f"\n{C_BRIGHT}[ЛОКАЛЬНЫЕ БАЗЫ]{C_RESET}")
        for basename, results in all_local.items():
            print(f"  {basename}: {len(results)} записей")
    
    if hibp_results:
        print(f"\n{C_BRIGHT}[УТЕЧКИ HIBP]{C_RESET}")
        for br in hibp_results:
            print(f"  ├─ {br['name']} ({br['date']})")
    
    if emailrep_results:
        print(f"\n{C_BRIGHT}[РЕПУТАЦИЯ EMAIL]{C_RESET}")
        print(f"  ├─ Репутация: {emailrep_results.get('reputation', '—')}")
        print(f"  ├─ Подозрительный: {emailrep_results.get('suspicious', '—')}")
    
    if whatsmyname_results:
        print(f"\n{C_BRIGHT}[WHATS MY NAME]{C_RESET}")
        for domain, url in list(whatsmyname_results.items())[:15]:
            print(f"  ├─ {domain}")
    
    if not any([all_local, hibp_results, emailrep_results, whatsmyname_results]):
        print(f"  {C_ERROR}[!] Ничего не найдено.{C_RESET}")
    
    print(f"\n{C_WARNING}═══════════════════════════════════════{C_RESET}\n")
