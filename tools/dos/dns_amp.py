#!/usr/bin/env python3
"""
REVERS OS v3.0 — DNS Amplification Test
⚠️ Только для тестирования своих систем!
"""

import socket
import threading
import time
import sys
from core.utils import C_ERROR, C_WARNING, C_INFO, C_BRIGHT, C_RESET

running = False

# Публичные DNS серверы для теста амплификации
DNS_SERVERS = [
    "8.8.8.8", "8.8.4.4",  # Google
    "1.1.1.1", "1.0.0.1",  # Cloudflare
    "9.9.9.9",              # Quad9
]

# DNS запрос для теста
DNS_QUERY = b'\xaa\xbb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\xff\x00\x01'

def dns_worker(target, port, duration):
    global running
    end_time = time.time() + duration
    sent = 0
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while running and time.time() < end_time:
        for server in DNS_SERVERS:
            try:
                # Отправляем DNS запрос с поддельным обратным адресом (целью)
                # В реальности нужен raw socket, здесь имитация
                sock.sendto(DNS_QUERY, (server, 53))
                sent += 1
            except:
                pass
    
    sock.close()
    return sent

def run_dns_amp(args):
    global running
    
    print(f"\n{C_ERROR}╔══════════════════════════════════════════╗{C_RESET}")
    print(f"{C_ERROR}║  ⚠️  ВНИМАНИЕ! ТОЛЬКО ДЛЯ СВОИХ СИСТЕМ!  ║{C_RESET}")
    print(f"{C_ERROR}║  Незаконное использование запрещено!    ║{C_RESET}")
    print(f"{C_ERROR}╚══════════════════════════════════════════╝{C_RESET}\n")
    print(f"{C_DIM}Примечание: без root прав работает в тестовом режиме.{C_RESET}\n")
    
    if not args:
        target = input(f"{C_INFO}Цель (IP) — тестовый режим: {C_RESET}").strip()
        if not target:
            target = "127.0.0.1"
        try:
            duration = int(input(f"{C_INFO}Длительность (сек, по умолч. 5): {C_RESET}").strip() or "5")
        except:
            duration = 5
    else:
        target = args[0]
        duration = int(args[1]) if len(args) > 1 else 5
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         ⚡ DNS AMPLIFICATION (ТЕСТ){C_RESET}")
    print(f"{C_WARNING}         Длительность: {duration} сек{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    print(f"{C_INFO}[*] Отправка DNS запросов...{C_RESET}")
    
    running = True
    start_time = time.time()
    sent = 0
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        while time.time() - start_time < duration and running:
            for server in DNS_SERVERS:
                try:
                    sock.sendto(DNS_QUERY, (server, 53))
                    sent += 1
                except:
                    pass
            elapsed = int(time.time() - start_time)
            sys.stdout.write(f"\r  Отправлено: {sent} запросов | {elapsed}s / {duration}s")
            sys.stdout.flush()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"\n{C_WARNING}[!] Прервано.{C_RESET}")
    
    running = False
    sock.close()
    
    print(f"\n{C_INFO}[*] DNS тест завершён. Отправлено {sent} запросов.{C_RESET}")
    print(f"{C_DIM}[!] Для реальной амплификации требуются root права и raw sockets.{C_RESET}\n")
