#!/usr/bin/env python3
"""
REVERS OS v3.0 — Email Breach
Проверка email в утечках
"""

import requests
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

def check_hibp(email):
    breaches = []
    pastes = []
    
    try:
        # Проверка утечек
        resp = requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
            headers={"User-Agent": "REVERS-OSINT", "hibp-api-key": ""},
            timeout=10
        )
        if resp.status_code == 200:
            for b in resp.json():
                breaches.append({
                    "name": b.get("Name", ""),
                    "domain": b.get("Domain", ""),
                    "date": b.get("BreachDate", ""),
                    "data": b.get("DataClasses", []),
                    "count": b.get("PwnCount", 0)
                })
        
        # Проверка паст
        resp = requests.get(
            f"https://haveibeenpwned.com/api/v3/pasteaccount/{email}",
            headers={"User-Agent": "REVERS-OSINT", "hibp-api-key": ""},
            timeout=10
        )
        if resp.status_code == 200:
            for p in resp.json():
                pastes.append({
                    "source": p.get("Source", ""),
                    "id": p.get("Id", ""),
                    "date": p.get("Date", "")
                })
    except Exception as e:
        pass
    
    return breaches, pastes

def check_firefox_monitor(email):
    """Проверка через Firefox Monitor (публичная страница)"""
    try:
        resp = requests.get(
            f"https://monitor.firefox.com/api/v1/scan",
            params={"email": email},
            timeout=10
        )
        if resp.status_code == 200:
            return True
    except:
        pass
    return False

def run_email_breach(args):
    if not args:
        email = input(f"{C_INFO}Введите email для проверки: {C_RESET}").strip()
    else:
        email = args[0]
    
    if not email or "@" not in email:
        print(f"{C_ERROR}[!] Некорректный email.{C_RESET}")
        return
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         📧 EMAIL BREACH{C_RESET}")
    print(f"{C_WARNING}         Email: {C_BRIGHT}{email}{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    print(f"{C_INFO}[*] Проверка HIBP...{C_RESET}")
    breaches, pastes = check_hibp(email)
    
    if breaches:
        print(f"\n{C_ERROR}[УТЕЧКИ] Найдено {len(breaches)}:{C_RESET}\n")
        for b in breaches:
            print(f"  {C_BRIGHT}{b['name']}{C_RESET} ({b['domain']})")
            print(f"  ├─ Дата: {b['date']}")
            print(f"  ├─ Записей: {b['count']:,}")
            print(f"  └─ Данные: {', '.join(b['data'][:5])}")
            print()
    else:
        print(f"  {C_SUCCESS}Утечек не найдено.{C_RESET}")
    
    if pastes:
        print(f"\n{C_WARNING}[ПАСТЫ] Найдено {len(pastes)}:{C_RESET}\n")
        for p in pastes:
            print(f"  ├─ {p['source']} ({p['date']})")
        print()
    
    if not breaches and not pastes:
        print(f"\n{C_SUCCESS}Email чист. Утечек и паст не найдено.{C_RESET}")
    
    print()
