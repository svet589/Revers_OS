#!/usr/bin/env python3
"""
REVERS OS v3.0 — Traceroute
Трассировка маршрута с геолокацией
"""

import socket
import subprocess
import platform
import re
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

def run_traceroute(args):
    if not args:
        target = input(f"{C_INFO}Введите хост или IP: {C_RESET}").strip()
    else:
        target = args[0]
    
    if not target:
        print(f"{C_ERROR}[!] Цель не указана.{C_RESET}")
        return
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🛤️ TRACEROUTE: {target}{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    # Определяем команду
    if platform.system().lower() == "windows":
        cmd = ["tracert", "-d", "-h", "15", target]
    else:
        cmd = ["traceroute", "-m", "15", "-w", "2", target]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                line = line.strip()
                if line and not line.startswith("traceroute") and not line.startswith("Tracing"):
                    # Пытаемся найти IP в строке
                    ips = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
                    if ips:
                        ip = ips[0]
                        try:
                            hostname = socket.gethostbyaddr(ip)[0]
                            print(f"  {line} ({hostname})")
                        except:
                            print(f"  {line}")
                    else:
                        print(f"  {line}")
        else:
            print(f"{C_ERROR}[!] Ошибка выполнения.{C_RESET}")
            print(result.stderr)
    
    except FileNotFoundError:
        print(f"{C_ERROR}[!] traceroute не найден. Установите: apt install traceroute{C_RESET}")
    except Exception as e:
        print(f"{C_ERROR}[!] Ошибка: {e}{C_RESET}")
