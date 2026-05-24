#!/usr/bin/env python3
"""
REVERS OS v3.0 — Часы
"""

import time
from datetime import datetime
from core.utils import C_ERROR, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET, clear_screen

def run_clock(args):
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🕐 ЧАСЫ{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    print(f"{C_DIM}Нажмите Ctrl+C для выхода.{C_RESET}\n")
    
    try:
        while True:
            clear_screen()
            now = datetime.now()
            
            print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
            print(f"{C_WARNING}         🕐 ЧАСЫ{C_RESET}")
            print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
            
            # Большие цифры времени
            time_str = now.strftime("%H:%M:%S")
            date_str = now.strftime("%d.%m.%Y")
            weekday = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"][now.weekday()]
            
            print(f"  {C_BRIGHT}{date_str} | {weekday}{C_RESET}\n")
            print(f"  {C_SUCCESS}╔══════════════════════╗{C_RESET}")
            print(f"  {C_SUCCESS}║     {time_str}      ║{C_RESET}")
            print(f"  {C_SUCCESS}╚══════════════════════╝{C_RESET}")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print(f"\n{C_DIM}Выход.{C_RESET}")
    
    print()
