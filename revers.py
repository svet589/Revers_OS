#!/usr/bin/env python3
"""
REVERS OS v3.0 — Эмулятор операционной системы
Разработчик: MRX | Группа REVERS
"""

import sys
import os

# Добавляем корень в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.utils import (
    C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET, C_PROMPT,
    clear_screen, show_banner, show_mini_banner, progress_bar,
    set_theme, get_theme
)
from core.auth import init_users, login, current_user, current_role, cmd_whoami, cmd_users, cmd_useradd, cmd_userdel
from core.database import init_db, add_to_history
from core.config import load_config, cmd_theme, cmd_alias
from core.vfs import current_vfs_path

# Системные команды
from commands.system import cmd_help, cmd_clear, cmd_exit, cmd_lock, cmd_history, cmd_env
from commands.files import cmd_ls, cmd_cd, cmd_pwd, cmd_mkdir, cmd_touch, cmd_cat, cmd_rm, cmd_secure_del
from commands.user import cmd_notes, cmd_export, cmd_share, cmd_vault

# Приложения
from apps.player.audio import run_player
from apps.utils_apps.calculator import run_calculator
from apps.utils_apps.clock import run_clock
from apps.utils_apps.timer import run_timer
from apps.utils_apps.stopwatch import run_stopwatch
from apps.utils_apps.alarm import run_alarm
from apps.utils_apps.todo import run_todo

# Утилиты
from tools.menu import tools_menu

def execute_command(cmd):
    """Обработчик команд"""
    if not cmd:
        return
    
    # Проверка алиасов
    config = load_config()
    aliases = config.get("aliases", {})
    if cmd in aliases:
        cmd = aliases[cmd]
    
    parts = cmd.split()
    command = parts[0]
    args = parts[1:]
    
    # Системные команды
    if command == "help":
        cmd_help(args)
    elif command == "clear":
        cmd_clear(args)
    elif command == "exit":
        cmd_exit(args)
    elif command == "lock":
        cmd_lock(args)
    elif command == "whoami":
        cmd_whoami(args)
    elif command == "users":
        cmd_users(args)
    elif command == "useradd":
        cmd_useradd(args)
    elif command == "userdel":
        cmd_userdel(args)
    elif command == "theme":
        cmd_theme(args)
    elif command == "alias":
        cmd_alias(args)
    elif command == "history":
        cmd_history(args)
    elif command == "env":
        cmd_env(args)
    
    # Файловые команды
    elif command == "ls":
        cmd_ls(args)
    elif command == "cd":
        cmd_cd(args)
    elif command == "pwd":
        cmd_pwd(args)
    elif command == "mkdir":
        cmd_mkdir(args)
    elif command == "touch":
        cmd_touch(args)
    elif command == "cat":
        cmd_cat(args)
    elif command == "rm":
        cmd_rm(args)
    elif command == "secure-del":
        cmd_secure_del(args)
    
    # Пользовательские команды
    elif command == "notes":
        cmd_notes(args)
    elif command == "export":
        cmd_export(args)
    elif command == "share":
        cmd_share(args)
    elif command == "vault":
        cmd_vault(args)
    
    # Приложения
    elif command == "player":
        run_player(args)
    elif command == "calc":
        run_calculator(args)
    elif command == "clock":
        run_clock(args)
    elif command == "timer":
        run_timer(args)
    elif command == "stopwatch":
        run_stopwatch(args)
    elif command == "alarm":
        run_alarm(args)
    elif command == "todo":
        run_todo(args)
    
    # Пентест-утилиты
    elif command == "tools":
        tools_menu()
    
    # Погода (заглушка)
    elif command == "weather":
        city = args[0] if args else input(f"{C_INFO}Введите город: {C_RESET}").strip()
        if city:
            try:
                import requests
                resp = requests.get(f"https://wttr.in/{city}?format=3&lang=ru", timeout=5)
                print(f"\n{C_BRIGHT}Погода:{C_RESET} {resp.text}")
            except:
                print(f"{C_ERROR}[!] Не удалось получить погоду.{C_RESET}")
        print()
    
    # QR-код
    elif command == "qr":
        text = " ".join(args) if args else input(f"{C_INFO}Текст для QR-кода: {C_RESET}").strip()
        if text:
            try:
                import qrcode
                qr = qrcode.QRCode()
                qr.add_data(text)
                qr.make()
                qr.print_ascii()
                print(f"{C_SUCCESS}QR-код сгенерирован.{C_RESET}")
            except ImportError:
                print(f"{C_ERROR}[!] Установите: pip install qrcode{C_RESET}")
        print()
    
    else:
        print(f"{C_ERROR}[!] Неизвестная команда: {command}{C_RESET}")
        print(f"{C_DIM}Введите 'help' для списка команд.{C_RESET}")

def main():
    """Главная функция"""
    # Инициализация
    init_users()
    init_db()
    config = load_config()
    
    # Авторизация
    if not login():
        sys.exit(1)
    
    # Заставка
    clear_screen()
    progress_bar()
    show_banner()
    print(f"{C_DIM}Введите 'help' для списка команд.{C_RESET}\n")
    
    # Главный цикл
    while True:
        try:
            theme = get_theme()
            prompt_color = theme["prompt"]
            
            cmd = input(f"\n{prompt_color}{current_user}@revers:{current_vfs_path}>{C_RESET} ").strip()
            
            if cmd:
                add_to_history(cmd)
            
            execute_command(cmd)
        
        except KeyboardInterrupt:
            print(f"\n{C_WARNING}[SYSTEM] Прерывание. Для выхода введите 'exit'{C_RESET}")
        
        except Exception as e:
            print(f"{C_ERROR}[ERROR] {e}{C_RESET}")

if __name__ == "__main__":
    main()
