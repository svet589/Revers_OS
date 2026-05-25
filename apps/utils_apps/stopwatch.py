#!/usr/bin/env python3
"""
REVERS OS v3.0 — Секундомер
"""

import time
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET, clear_screen
def run_stopwatch(args):
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         ⏱️ СЕКУНДОМЕР{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    print(f"{C_INFO}Управление:{C_RESET}")
    print(f"  Enter — старт/пауза")
    print(f"  r — сброс")
    print(f"  q — выход\n")
    
    running = False
    start_time = 0
    elapsed = 0
    
    while True:
        try:
            cmd = input(f"{C_INFO}Секундомер > {C_RESET}").strip().lower()
            
            if cmd == "q":
                break
            
            elif cmd == "r":
                running = False
                elapsed = 0
                clear_screen()
                print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
                print(f"{C_WARNING}         ⏱️ СЕКУНДОМЕР{C_RESET}")
                print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
                print(f"  {C_BRIGHT}00:00.0{C_RESET}")
                print(f"  {C_DIM}Сброшен{C_RESET}")
            
            elif cmd == "":
                if not running:
                    running = True
                    start_time = time.time() - elapsed
                    print(f"  {C_SUCCESS}Старт!{C_RESET}")
                    
                    # Режим отсчёта
                    try:
                        while True:
                            clear_screen()
                            elapsed = time.time() - start_time
                            mins, secs = divmod(int(elapsed), 60)
                            millis = int((elapsed - int(elapsed)) * 10)
                            
                            print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
                            print(f"{C_WARNING}         ⏱️ СЕКУНДОМЕР (идет){C_RESET}")
                            print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
                            print(f"  {C_BRIGHT}{mins:02d}:{secs:02d}.{millis}{C_RESET}")
                            print(f"\n  {C_DIM}Нажмите Enter для паузы{C_RESET}")
                            
                            time.sleep(0.1)
                    except KeyboardInterrupt:
                        pass
                else:
                    running = False
                    elapsed = time.time() - start_time
                    mins, secs = divmod(int(elapsed), 60)
                    millis = int((elapsed - int(elapsed)) * 10)
                    print(f"  {C_WARNING}Пауза: {mins:02d}:{secs:02d}.{millis}{C_RESET}")
            
            else:
                print(f"  {C_ERROR}Неизвестная команда.{C_RESET}")
        
        except KeyboardInterrupt:
            break
    
    print()
