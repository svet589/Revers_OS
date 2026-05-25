#!/usr/bin/env python3
"""
REVERS OS v3.0 — Будильник
"""

import time
import sys
import threading
from datetime import datetime
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET, clear_screen

def alarm_worker(alarm_time):
    global alarm_triggered
    while not alarm_triggered:
        now = datetime.now().strftime("%H:%M")
        if now == alarm_time:
            alarm_triggered = True
            print(f"\n\n{C_ERROR}╔══════════════════════════════════════════╗{C_RESET}")
            print(f"{C_ERROR}║  ⏰ БУДИЛЬНИК! {alarm_time}              ║{C_RESET}")
            print(f"{C_ERROR}╚══════════════════════════════════════════╝{C_RESET}\n")
            for _ in range(5):
                sys.stdout.write('\a')
                sys.stdout.flush()
                time.sleep(0.5)
            break
        time.sleep(10)

def run_alarm(args):
    global alarm_triggered
    alarm_triggered = False
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         ⏰ БУДИЛЬНИК{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    alarm_time = input(f"{C_INFO}Введите время (ЧЧ:ММ, например 07:30): {C_RESET}").strip()
    
    try:
        datetime.strptime(alarm_time, "%H:%M")
    except ValueError:
        print(f"{C_ERROR}[!] Неверный формат. Используйте ЧЧ:ММ{C_RESET}")
        return
    
    print(f"{C_SUCCESS}Будильник установлен на {alarm_time}{C_RESET}")
    print(f"{C_DIM}Нажмите Enter для отмены...{C_RESET}")
    
    # Запуск в фоне
    t = threading.Thread(target=alarm_worker, args=(alarm_time,), daemon=True)
    t.start()
    
    input()
    alarm_triggered = True
    print(f"{C_WARNING}Будильник отменён.{C_RESET}\n")
