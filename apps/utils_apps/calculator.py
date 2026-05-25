#!/usr/bin/env python3
"""
REVERS OS v3.0 — Калькулятор
"""

import math
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET, clear_screen
def run_calculator(args):
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🔢 КАЛЬКУЛЯТОР{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    print(f"{C_DIM}Операции: + - * / ** % sqrt sin cos tan log ln{C_RESET}")
    print(f"{C_DIM}Константы: pi e{C_RESET}")
    print(f"{C_DIM}Выход: q или exit{C_RESET}\n")
    
    # Контекст для eval
    context = {
        "pi": math.pi,
        "e": math.e,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log10,
        "ln": math.log,
        "abs": abs,
        "round": round,
        "pow": pow,
    }
    
    while True:
        try:
            expr = input(f"{C_INFO}>>> {C_RESET}").strip()
            
            if expr.lower() in ['q', 'exit', 'quit', 'выход']:
                break
            
            if not expr:
                continue
            
            result = eval(expr, {"__builtins__": {}}, context)
            
            if isinstance(result, float):
                print(f"  {C_SUCCESS}{result:.10g}{C_RESET}")
            else:
                print(f"  {C_SUCCESS}{result}{C_RESET}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"  {C_ERROR}Ошибка: {e}{C_RESET}")
    
    print()
