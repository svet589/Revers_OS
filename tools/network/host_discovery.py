#!/usr/bin/env python3
"""
REVERS OS v3.0 — Host Discovery
Поиск живых хостов в локальной сети
"""

import os
import subprocess
import platform
import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET, simple_progress

def ping_host(ip):
    """Пинг одного хоста"""
    param = "-n 1 -w 500" if platform.system().lower() == "windows" else "-c 1 -W 1"
    try:
        result = subprocess.run(
            f"ping {param} {ip}",
            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=2
        )
        return (ip, result.returncode == 0)
    except:
        return (ip, False)

def get_local_network():
    """Получить локальную сеть"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
        return local_ip, str(network)
    except:
        return None, None

def run_host_discovery(args):
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🔍 HOST DISCOVERY{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    local_ip, network = get_local_network()
    if not local_ip:
        print(f"{C_ERROR}[!] Не удалось определить локальную сеть.{C_RESET}")
        return
    
    print(f"{C_INFO}Локальный IP: {C_BRIGHT}{local_ip}{C_RESET}")
    print(f"{C_INFO}Сеть: {C_BRIGHT}{network}{C_RESET}")
    print(f"{C_DIM}Сканирование...{C_RESET}\n")
    
    hosts = list(ipaddress.IPv4Network(network).hosts())
    alive = []
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(ping_host, str(ip)): ip for ip in hosts}
        done = 0
        for future in as_completed(futures):
            ip, is_alive = future.result()
            done += 1
            if is_alive:
                alive.append(ip)
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    hostname = "N/A"
                print(f"  {C_SUCCESS}[ALIVE]{C_RESET} {ip} ({hostname})")
            simple_progress(done, len(hosts), "Прогресс", 30)
    
    print(f"\n{C_INFO}Найдено хостов: {C_BRIGHT}{len(alive)}{C_RESET}")
