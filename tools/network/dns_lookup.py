#!/usr/bin/env python3
"""
REVERS OS v3.0 — DNS Lookup
Полная DNS-разведка
"""

import socket
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

def dns_query(domain, record_type):
    """Запрос DNS записи"""
    try:
        if record_type == "A":
            result = socket.gethostbyname_ex(domain)
            return result[2]
        elif record_type == "MX":
            try:
                import dns.resolver
                answers = dns.resolver.resolve(domain, 'MX')
                return [f"{r.preference} {r.exchange}" for r in answers]
            except:
                return []
        elif record_type == "NS":
            try:
                import dns.resolver
                answers = dns.resolver.resolve(domain, 'NS')
                return [str(r) for r in answers]
            except:
                return []
        elif record_type == "TXT":
            try:
                import dns.resolver
                answers = dns.resolver.resolve(domain, 'TXT')
                return [str(r) for r in answers]
            except:
                return []
        else:
            return []
    except Exception as e:
        return [f"Ошибка: {e}"]

def run_dns_lookup(args):
    if not args:
        target = input(f"{C_INFO}Введите домен: {C_RESET}").strip()
    else:
        target = args[0]
    
    if not target:
        print(f"{C_ERROR}[!] Домен не указан.{C_RESET}")
        return
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🌐 DNS LOOKUP: {target}{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    # A записи
    a_records = dns_query(target, "A")
    print(f"{C_BRIGHT}[A Записи]{C_RESET}")
    for r in a_records:
        print(f"  ├─ {r}")
    
    # MX записи
    mx_records = dns_query(target, "MX")
    if mx_records:
        print(f"\n{C_BRIGHT}[MX Записи]{C_RESET}")
        for r in mx_records:
            print(f"  ├─ {r}")
    
    # NS записи
    ns_records = dns_query(target, "NS")
    if ns_records:
        print(f"\n{C_BRIGHT}[NS Записи]{C_RESET}")
        for r in ns_records:
            print(f"  ├─ {r}")
    
    # TXT записи
    txt_records = dns_query(target, "TXT")
    if txt_records:
        print(f"\n{C_BRIGHT}[TXT Записи]{C_RESET}")
        for r in txt_records:
            print(f"  ├─ {r[:100]}")
    
    # Обратный DNS
    try:
        ip = socket.gethostbyname(target)
        try:
            reverse = socket.gethostbyaddr(ip)[0]
            print(f"\n{C_BRIGHT}[Reverse DNS]{C_RESET}")
            print(f"  ├─ {reverse}")
        except:
            pass
    except:
        pass
    
    print()
