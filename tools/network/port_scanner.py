#!/usr/bin/env python3
"""
REVERS OS v3.0 — Port Scanner
Многопоточный сканер портов
"""

import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET, simple_progress

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 111: "RPC", 135: "RPC", 139: "NetBIOS",
    143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
    1723: "PPTP", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    5900: "VNC", 6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    27017: "MongoDB", 4444: "Metasploit", 1337: "Waste", 31337: "Back Orifice"
}

def scan_port(ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return (port, result == 0)
    except:
        return (port, False)

def run_port_scanner(args):
    if not args:
        target = input(f"{C_INFO}Введите IP или хост: {C_RESET}").strip()
    else:
        target = args[0]
    
    if not target:
        print(f"{C_ERROR}[!] Цель не указана.{C_RESET}")
        return
    
    try:
        ip = socket.gethostbyname(target)
    except:
        print(f"{C_ERROR}[!] Не удалось разрешить хост: {target}{C_RESET}")
        return
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🔍 PORT SCANNER{C_RESET}")
    print(f"{C_WARNING}         Цель: {target} ({ip}){C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    ports = list(COMMON_PORTS.keys())
    results = []
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in ports}
        done = 0
        for future in as_completed(futures):
            port, is_open = future.result()
            done += 1
            if is_open:
                service = COMMON_PORTS.get(port, "unknown")
                results.append((port, service))
                print(f"  {C_SUCCESS}[OPEN]{C_RESET} {port}/tcp ({service})")
            simple_progress(done, len(ports), "Прогресс", 30)
    
    elapsed = time.time() - start_time
    
    print(f"\n{C_INFO}Открыто портов: {C_BRIGHT}{len(results)}{C_RESET}")
    print(f"{C_DIM}Время: {elapsed:.1f} сек{C_RESET}\n")
