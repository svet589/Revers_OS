#!/usr/bin/env python3
"""
REVERS OS v3.0 — HTTP Headers Analyzer
"""

import requests
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

SECURITY_HEADERS = {
    "Strict-Transport-Security": "HSTS",
    "Content-Security-Policy": "CSP",
    "X-Frame-Options": "Защита от clickjacking",
    "X-Content-Type-Options": "Защита от MIME sniffing",
    "X-XSS-Protection": "Защита от XSS",
    "Referrer-Policy": "Политика реферера",
}

def run_http_headers(args):
    if not args:
        url = input(f"{C_INFO}Введите URL (https://example.com): {C_RESET}").strip()
    else:
        url = args[0]
    
    if not url.startswith("http"):
        url = "https://" + url
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🌐 HTTP HEADERS: {url}{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    try:
        resp = requests.get(url, timeout=10, allow_redirects=True)
        
        print(f"{C_BRIGHT}[Статус]{C_RESET} {resp.status_code} {resp.reason}")
        print(f"{C_BRIGHT}[Сервер]{C_RESET} {resp.headers.get('Server', 'N/A')}")
        print(f"{C_BRIGHT}[Технологии]{C_RESET} {resp.headers.get('X-Powered-By', 'N/A')}")
        
        print(f"\n{C_BRIGHT}[Заголовки]{C_RESET}")
        for key, value in resp.headers.items():
            print(f"  ├─ {key}: {value}")
        
        print(f"\n{C_BRIGHT}[Cookies]{C_RESET}")
        for cookie in resp.cookies:
            secure = "❌" if cookie.secure else "✔️"
            httponly = "HttpOnly" if cookie.has_nonstandard_attr('HttpOnly') else ""
            print(f"  ├─ {cookie.name}: {cookie.value[:50]} {secure} {httponly}")
        
        print(f"\n{C_WARNING}[Анализ безопасности]{C_RESET}")
        for header, desc in SECURITY_HEADERS.items():
            if header in resp.headers:
                print(f"  {C_SUCCESS}[✓]{C_RESET} {desc}")
            else:
                print(f"  {C_ERROR}[✗]{C_RESET} {desc} — отсутствует")
    
    except requests.exceptions.RequestException as e:
        print(f"{C_ERROR}[!] Ошибка запроса: {e}{C_RESET}")
