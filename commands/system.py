#!/usr/bin/env python3
"""
REVERS OS v3.0 — Системные команды
"""

import os
import sys
from core.utils import (
    C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET,
    clear_screen, show_banner, show_mini_banner, get_sys_info
)
from core.auth import current_user, current_role, cmd_whoami, cmd_users, cmd_useradd, cmd_userdel, lock_session
from core.database import show_history, search_history

def cmd_help(args):
    help_text = f"""
{C_WARNING}================================================
              REVERS OS v3.0
================================================{C_RESET}

{C_INFO}Системные команды:{C_RESET}
  {C_BRIGHT}help{C_RESET}        - показать эту справку
  {C_BRIGHT}clear{C_RESET}       - очистить экран
  {C_BRIGHT}exit{C_RESET}        - выйти из REVERS OS
  {C_BRIGHT}lock{C_RESET}        - заблокировать сессию
  {C_BRIGHT}whoami{C_RESET}      - текущий пользователь
  {C_BRIGHT}users{C_RESET}       - список пользователей (admin)
  {C_BRIGHT}useradd{C_RESET}     - добавить пользователя (admin)
  {C_BRIGHT}userdel{C_RESET}     - удалить пользователя (admin)
  {C_BRIGHT}theme{C_RESET}       - сменить тему оформления
  {C_BRIGHT}alias{C_RESET}       - управление алиасами

{C_INFO}Файловые команды:{C_RESET}
  {C_BRIGHT}ls{C_RESET}          - список файлов
  {C_BRIGHT}cd{C_RESET}          - сменить директорию
  {C_BRIGHT}pwd{C_RESET}         - текущая директория
  {C_BRIGHT}mkdir{C_RESET}       - создать директорию
  {C_BRIGHT}touch{C_RESET}       - создать файл
  {C_BRIGHT}cat{C_RESET}         - просмотр файла
  {C_BRIGHT}rm{C_RESET}          - удалить файл/папку
  {C_BRIGHT}secure-del{C_RESET}  - безопасное удаление

{C_INFO}Приложения:{C_RESET}
  {C_BRIGHT}calc{C_RESET}        - калькулятор
  {C_BRIGHT}clock{C_RESET}       - часы
  {C_BRIGHT}timer{C_RESET}       - таймер
  {C_BRIGHT}stopwatch{C_RESET}   - секундомер
  {C_BRIGHT}alarm{C_RESET}       - будильник
  {C_BRIGHT}todo{C_RESET}        - список задач
  {C_BRIGHT}notes{C_RESET}       - заметки
  {C_BRIGHT}weather{C_RESET}     - погода
  {C_BRIGHT}qr{C_RESET}          - генератор QR-кодов
  {C_BRIGHT}player{C_RESET}      - аудиоплеер

{C_INFO}Пентест:{C_RESET}
  {C_BRIGHT}tools{C_RESET}       - меню пентест-утилит (21 шт.)
  {C_BRIGHT}export{C_RESET}      - экспорт результатов
  {C_BRIGHT}share{C_RESET}       - HTTP-сервер для файла
  {C_BRIGHT}vault{C_RESET}       - шифрованное хранилище

{C_INFO}Прочее:{C_RESET}
  {C_BRIGHT}history{C_RESET}     - история команд
  {C_BRIGHT}history search{C_RESET} - поиск по истории
  {C_BRIGHT}env{C_RESET}         - информация о системе

{C_DIM}Разработчик: MRX | Группа REVERS{C_RESET}
"""
    print(help_text)

def cmd_clear(args):
    clear_screen()
    show_mini_banner()

def cmd_exit(args):
    print(f"{C_WARNING}[SYSTEM] Завершение работы REVERS OS...{C_RESET}")
    sys.exit(0)

def cmd_lock(args):
    if lock_session():
        return
    else:
        cmd_exit([])

def cmd_history(args):
    if args and args[0] == "search":
        if len(args) > 1:
            search_history(args[1])
        else:
            print(f"{C_ERROR}Использование: history search <запрос>{C_RESET}")
    else:
        show_history()

def cmd_env(args):
    info = get_sys_info()
    print(f"{C_BRIGHT}OS:{C_RESET} {info['os']}")
    print(f"{C_BRIGHT}Python:{C_RESET} {info['python']}")
    print(f"{C_BRIGHT}Hostname:{C_RESET} {info['hostname']}")
    print(f"{C_BRIGHT}Arch:{C_RESET} {info['arch']}")
