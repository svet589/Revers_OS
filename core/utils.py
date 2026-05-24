#!/usr/bin/env python3
"""
REVERS OS v3.0 — Утилиты ядра
Баннер, цвета, анимации, прогресс-бар
"""

import os
import sys
import time
import platform
from colorama import Fore, Style, init

init(autoreset=True)

# ============================================
# ЦВЕТА
# ============================================
C_ERROR   = Fore.RED
C_SUCCESS = Fore.GREEN
C_WARNING = Fore.YELLOW
C_INFO    = Fore.CYAN
C_PROMPT  = Fore.MAGENTA
C_DIM     = Fore.LIGHTBLACK_EX
C_BRIGHT  = Fore.WHITE
C_RESET   = Style.RESET_ALL

THEMES = {
    "red":    {"prompt": Fore.RED,          "accent": Fore.LIGHTRED_EX,     "banner": Fore.RED},
    "green":  {"prompt": Fore.GREEN,        "accent": Fore.LIGHTGREEN_EX,   "banner": Fore.GREEN},
    "blue":   {"prompt": Fore.BLUE,         "accent": Fore.LIGHTCYAN_EX,    "banner": Fore.BLUE},
    "cyan":   {"prompt": Fore.CYAN,         "accent": Fore.LIGHTCYAN_EX,    "banner": Fore.CYAN},
    "purple": {"prompt": Fore.MAGENTA,      "accent": Fore.LIGHTMAGENTA_EX, "banner": Fore.MAGENTA},
    "matrix": {"prompt": Fore.GREEN,        "accent": Fore.LIGHTGREEN_EX,   "banner": Fore.GREEN},
}

current_theme = "red"

def set_theme(theme_name):
    global current_theme
    if theme_name in THEMES:
        current_theme = theme_name
        return True
    return False

def get_theme():
    return THEMES.get(current_theme, THEMES["red"])

# ============================================
# ЗВУК
# ============================================
def beep():
    sys.stdout.write('\a')
    sys.stdout.flush()

# ============================================
# МЕДЛЕННАЯ ПЕЧАТЬ
# ============================================
def slow_print(text, delay=0.015):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ============================================
# ПРОГРЕСС-БАР
# ============================================
def progress_bar(title="Загрузка", steps=None):
    if steps is None:
        steps = [
            ("CORE", "Инициализация ядра REVERS", 0.2),
            ("AUTH", "Загрузка модуля авторизации", 0.15),
            ("VFS", "Монтирование виртуальной ФС", 0.15),
            ("DB", "Подключение базы данных", 0.1),
            ("ENV", "Сканирование окружения", 0.15),
            ("NET", "Проверка сетевых интерфейсов", 0.1),
            ("TOOLS", "Индексация утилит", 0.2),
            ("DONE", "Система готова", 0.05),
        ]
    
    theme = get_theme()
    print(f"\n{theme['accent']}[SYSTEM] {title}...{C_RESET}\n")
    
    for tag, desc, delay in steps:
        sys.stdout.write(f"  {C_DIM}[{tag}]{C_RESET} {desc} ")
        sys.stdout.flush()
        for _ in range(3):
            time.sleep(0.08)
            sys.stdout.write(".")
            sys.stdout.flush()
        time.sleep(delay)
        sys.stdout.write(f" {C_SUCCESS}[OK]{C_RESET}\n")
        sys.stdout.flush()
    
    beep()
    print(f"\n{C_WARNING}[!] ДОСТУП РАЗРЕШЁН. ДОБРО ПОЖАЛОВАТЬ В REVERS OS.{C_RESET}")
    time.sleep(1.0)

def simple_progress(current, total, prefix="Прогресс", length=40):
    percent = int(current / total * 100)
    filled = int(length * current / total)
    bar = "█" * filled + "░" * (length - filled)
    sys.stdout.write(f"\r  {prefix}: |{bar}| {percent}% {current}/{total}")
    sys.stdout.flush()
    if current == total:
        print()

# ============================================
# БАННЕРЫ
# ============================================
def show_banner():
    theme = get_theme()
    art = f"""
{theme['banner']}
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀
    ⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀
    ⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀
    ⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿

{theme['accent']}                    ██████╗ ███████╗██╗   ██╗███████╗██████╗ ███████╗
                    ██╔══██╗██╔════╝██║   ██║██╔════╝██╔══██╗██╔════╝
                    ██████╔╝█████╗  ██║   ██║█████╗  ██████╔╝███████╗
                    ██╔══██╗██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║
                    ██║  ██║███████╗ ╚████╔╝ ███████╗██║  ██║███████║
                    ╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝
{C_RESET}
{C_WARNING}                    REVERS OS v3.0 — Эмулятор операционной системы
                    Разработчик: MRX | Группа REVERS{C_RESET}
"""
    print(art)

def show_mini_banner():
    theme = get_theme()
    art = f"""
{theme['accent']}  ██████╗ ███████╗██╗   ██╗███████╗██████╗ ███████╗
  ██╔══██╗██╔════╝██║   ██║██╔════╝██╔══██╗██╔════╝
  ██████╔╝█████╗  ██║   ██║█████╗  ██████╔╝███████╗
  ██╔══██╗██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║
  ██║  ██║███████╗ ╚████╔╝ ███████╗██║  ██║███████║
  ╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝
{C_RESET}
"""
    print(art)

# ============================================
# ОЧИСТКА ЭКРАНА
# ============================================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ============================================
# СИСТЕМНАЯ ИНФОРМАЦИЯ
# ============================================
def get_sys_info():
    return {
        "os": f"{platform.system()} {platform.release()}",
        "python": sys.version.split()[0],
        "hostname": platform.node(),
        "arch": platform.machine(),
    }

# ============================================
# ВАЛИДАЦИЯ ВВОДА
# ============================================
def confirm_action(message="Вы уверены? (y/n): "):
    while True:
        answer = input(f"{C_WARNING}{message}{C_RESET}").strip().lower()
        if answer in ['y', 'yes', 'д', 'да']:
            return True
        elif answer in ['n', 'no', 'н', 'нет']:
            return False

def select_option(options, prompt="Выберите опцию: "):
    for i, option in enumerate(options, 1):
        print(f"  {C_BRIGHT}{i}{C_RESET}. {option}")
    while True:
        try:
            choice = int(input(f"{C_INFO}{prompt}{C_RESET}"))
            if 1 <= choice <= len(options):
                return choice
            print(f"{C_ERROR}[!] Выберите число от 1 до {len(options)}{C_RESET}")
        except ValueError:
            print(f"{C_ERROR}[!] Введите число{C_RESET}")
