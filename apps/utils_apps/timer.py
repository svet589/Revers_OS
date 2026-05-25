#!/usr/bin/env python3
"""
REVERS OS v3.0 — Таймер обратного отсчёта
"""

import time
import sys
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET, clear_screen
def run_timer(args):
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         ⏱️ ТАЙМЕР{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    if args:
        try:
            seconds = int(args[0]) if args[0].isdigit() else None
        except:
            seconds = None
    else:
        try:
            minutes = input(f"{C_INFO}Введите время (минуты:секунды, например 1:30): {C_RESET}").strip()
            if ":" in minutes:
                m, s = minutes.split(":")
                seconds = int(m) * 60 + int(s)
            else:
                seconds = int(minutes)
        except:
            print(f"{C_ERROR}[!] Неверный формат.{C_RESET}")
            return
    
    if not seconds or seconds <= 0:
        print(f"{C_ERROR}[!] Время должно быть больше 0.{C_RESET}")
        return
    
    total = seconds
    
    print(f"{C_INFO}Таймер на {seconds} сек. Нажмите Ctrl+C для отмены.{C_RESET}\n")
    
    try:
        while seconds > 0:
            clear_screen()
            mins, secs = divmod(seconds, 60)
            
            # Прогресс-бар
            progress = int((total - seconds) / total * 30)
            bar = "█" * progress + "░" * (30 - progress)
            
            print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
            print(f"{C_WARNING}         ⏱️ ТАЙМЕР{C_RESET}")
            print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
            print(f"  {C_BRIGHT}{mins:02d}:{secs:02d}{C_RESET}")
            print(f"  [{bar}]")
            print(f"\n  {C_DIM}Осталось: {seconds} сек{C_RESET}")
            
            time.sleep(1)
            seconds -= 1
        
        # Таймер закончился
        clear_screen()
        print(f"\n{C_SUCCESS}  ══════════════════════════════════════════{C_RESET}")
        print(f"{C_SUCCESS}         ⏰ ВРЕМЯ ВЫШЛО!{C_RESET}")
        print(f"{C_SUCCESS}  ══════════════════════════════════════════{C_RESET}\n")
        
        # Звуковой сигнал
        for _ in range(3):
            sys.stdout.write('\a')
            sys.stdout.flush()
            time.sleep(0.3)
    
    except KeyboardInterrupt:
        print(f"\n{C_WARNING}Таймер отменён.{C_RESET}")
    
    print()
