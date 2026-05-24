#!/usr/bin/env python3
"""
REVERS OS v3.0 — IP Intelligence
Геолокация и информация об IP
"""

import requests
import socket
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

def get_ip_info(ip):
    """Получить информацию об IP через ip-api.com (бесплатно)"""
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719&lang=ru", timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None

def check_tor(ip):
    """Проверка Tor exit node"""
    try:
        reversed_ip = ".".join(reversed(ip.split(".")))
        resp = requests.get(f"https://check.torproject.org/cgi-bin/TorBulkExitList.py?ip=1.1.1.1", timeout=5)
        return False  # Упрощённо, полная проверка требует загрузки всего списка
    except:
        return None

def run_ip_intel(args):
    if not args:
        target = input(f"{C_INFO}Введите IP-адрес (или Enter для своего): {C_RESET}").strip()
        if not target:
            try:
                target = requests.get("https://api.ipify.org", timeout=5).text
            except:
                target = socket.gethostbyname(socket.gethostname())
    else:
        target = args[0]
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🌍 IP INTELLIGENCE{C_RESET}")
    print(f"{C_WARNING}         IP: {C_BRIGHT}{target}{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    info = get_ip_info(target)
    
    if info and info.get("status") == "success":
        print(f"{C_BRIGHT}[Геолокация]{C_RESET}")
        print(f"  ├─ Страна: {info.get('country', '—')} ({info.get('countryCode', '—')})")
        print(f"  ├─ Регион: {info.get('regionName', '—')}")
        print(f"  ├─ Город: {info.get('city', '—')}")
        print(f"  ├─ ZIP: {info.get('zip', '—')}")
        print(f"  └─ Координаты: {info.get('lat', '—')}, {info.get('lon', '—')}")
        
        print(f"\n{C_BRIGHT}[Провайдер]{C_RESET}")
        print(f"  ├─ Провайдер: {info.get('isp', '—')}")
        print(f"  ├─ Организация: {info.get('org', '—')}")
        print(f"  └─ AS: {info.get('as', '—')}")
        
        print(f"\n{C_BRIGHT}[Другое]{C_RESET}")
        print(f"  ├─ Часовой пояс: {info.get('timezone', '—')}")
        print(f"  └─ Мобильный/Прокси/Хостинг: ", end="")
        flags = []
        if info.get('mobile'): flags.append("📱 Мобильный")
        if info.get('proxy'): flags.append("🔒 Прокси")
        if info.get('hosting'): flags.append("🖥 Хостинг")
        print(", ".join(flags) if flags else "Нет")
        
        # Карта (ссылка)
        lat, lon = info.get('lat'), info.get('lon')
        if lat and lon:
            print(f"\n{C_DIM}Карта: https://www.google.com/maps?q={lat},{lon}{C_RESET}")
    else:
        print(f"{C_ERROR}[!] Не удалось получить информацию об IP.{C_RESET}")
    
    print()
