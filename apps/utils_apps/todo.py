#!/usr/bin/env python3
"""
REVERS OS v3.0 — Список задач
"""

import os
import json
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET, clear_screen
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
TODO_FILE = os.path.join(DATA_DIR, "todo.json")

def load_tasks():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TODO_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def run_todo(args):
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         📋 СПИСОК ЗАДАЧ{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    tasks = load_tasks()
    
    while True:
        # Показ задач
        if tasks:
            print(f"{C_INFO}Задачи:{C_RESET}")
            for i, task in enumerate(tasks, 1):
                status = f"{C_SUCCESS}[✓]{C_RESET}" if task.get("done") else f"{C_DIM}[ ]{C_RESET}"
                print(f"  {status} {C_BRIGHT}{i}{C_RESET}. {task['text']}")
        else:
            print(f"{C_DIM}Список пуст.{C_RESET}")
        
        print(f"\n{C_INFO}Команды:{C_RESET}")
        print(f"  {C_BRIGHT}a{C_RESET} — добавить задачу")
        print(f"  {C_BRIGHT}d N{C_RESET} — отметить как выполненную")
        print(f"  {C_BRIGHT}r N{C_RESET} — удалить задачу")
        print(f"  {C_BRIGHT}c{C_RESET} — очистить выполненные")
        print(f"  {C_DIM}q{C_RESET} — выход")
        
        cmd = input(f"\n{C_INFO}> {C_RESET}").strip().lower()
        
        if cmd == "q":
            break
        
        elif cmd == "a":
            text = input(f"{C_INFO}Текст задачи: {C_RESET}").strip()
            if text:
                tasks.append({"text": text, "done": False})
                save_tasks(tasks)
                print(f"{C_SUCCESS}Добавлено.{C_RESET}")
        
        elif cmd == "c":
            tasks = [t for t in tasks if not t["done"]]
            save_tasks(tasks)
            print(f"{C_SUCCESS}Выполненные задачи очищены.{C_RESET}")
        
        elif cmd.startswith("d "):
            try:
                idx = int(cmd.split()[1]) - 1
                if 0 <= idx < len(tasks):
                    tasks[idx]["done"] = True
                    save_tasks(tasks)
                    print(f"{C_SUCCESS}Отмечено как выполненное.{C_RESET}")
                else:
                    print(f"{C_ERROR}[!] Неверный номер.{C_RESET}")
            except (IndexError, ValueError):
                print(f"{C_ERROR}[!] Использование: d <номер>{C_RESET}")
        
        elif cmd.startswith("r "):
            try:
                idx = int(cmd.split()[1]) - 1
                if 0 <= idx < len(tasks):
                    removed = tasks.pop(idx)
                    save_tasks(tasks)
                    print(f"{C_SUCCESS}Удалено: {removed['text']}{C_RESET}")
                else:
                    print(f"{C_ERROR}[!] Неверный номер.{C_RESET}")
            except (IndexError, ValueError):
                print(f"{C_ERROR}[!] Использование: r <номер>{C_RESET}")
        
        else:
            print(f"{C_ERROR}[!] Неизвестная команда.{C_RESET}")
    
    print()
