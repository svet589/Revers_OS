#!/usr/bin/env python3
"""
REVERS OS v3.0 — Авторизация и управление пользователями
"""

import os
import json
import hashlib
import getpass
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_BRIGHT, C_RESET

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
PASSWORD_FILE = os.path.join(DATA_DIR, "password.hash")

current_user = None
current_role = None

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def init_users():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        default_users = {
            "admin": {
                "password": hash_password("admin"),
                "role": "admin"
            }
        }
        with open(USERS_FILE, "w") as f:
            json.dump(default_users, f, indent=2)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def is_first_launch():
    return not os.path.exists(USERS_FILE)

def first_launch_setup():
    print(f"\n{C_WARNING}[FIRST LAUNCH DETECTED]{C_RESET}")
    print("Создание учётной записи администратора.\n")
    while True:
        pwd = getpass.getpass("Придумайте пароль admin: ")
        if len(pwd) < 4:
            print(f"{C_ERROR}Пароль должен быть не короче 4 символов.{C_RESET}\n")
            continue
        pwd2 = getpass.getpass("Повторите пароль: ")
        if pwd == pwd2:
            users = {"admin": {"password": hash_password(pwd), "role": "admin"}}
            save_users(users)
            print(f"\n{C_WARNING}[!] Пароль сохранён. НЕ ЗАБУДЬТЕ ЕГО!{C_RESET}")
            input("\nНажмите Enter, чтобы продолжить...")
            return True
        else:
            print(f"{C_ERROR}Пароли не совпадают.{C_RESET}\n")

def login():
    global current_user, current_role
    
    # Миграция со старого формата
    if os.path.exists(PASSWORD_FILE) and not os.path.exists(USERS_FILE):
        with open(PASSWORD_FILE, "r") as f:
            old_hash = f.read().strip()
        users = {"admin": {"password": old_hash, "role": "admin"}}
        save_users(users)
        os.remove(PASSWORD_FILE)
    
    if is_first_launch():
        first_launch_setup()
    
    print(f"\n{C_INFO}[SYSTEM] Доступ к REVERS OS требует авторизации.{C_RESET}\n")
    
    for attempt in range(3):
        username = input("Логин: ").strip()
        pwd = getpass.getpass("Пароль: ")
        
        users = load_users()
        if username in users:
            if hash_password(pwd) == users[username]["password"]:
                current_user = username
                current_role = users[username]["role"]
                print(f"{C_SUCCESS}[ACCESS GRANTED] Добро пожаловать, {username} ({current_role}){C_RESET}\n")
                return True
            else:
                left = 2 - attempt
                print(f"{C_ERROR}[ACCESS DENIED] Неверный пароль. Осталось попыток: {left}{C_RESET}\n")
        else:
            left = 2 - attempt
            print(f"{C_ERROR}[ACCESS DENIED] Пользователь не найден. Осталось попыток: {left}{C_RESET}\n")
    
    print(f"{C_ERROR}[SYSTEM] Превышено количество попыток. Выход.{C_RESET}")
    return False

def check_perm(required_role="admin"):
    if current_role == "admin":
        return True
    if required_role == "admin" and current_role != "admin":
        print(f"{C_ERROR}[PERMISSION DENIED] Требуются права администратора.{C_RESET}")
        return False
    return True

def cmd_useradd(args):
    if not check_perm("admin"):
        return
    if len(args) < 1:
        print(f"{C_ERROR}Использование: useradd <имя> [роль: user/admin]{C_RESET}")
        return
    username = args[0]
    role = args[1] if len(args) > 1 else "user"
    if role not in ["user", "admin"]:
        print(f"{C_ERROR}Роль должна быть user или admin{C_RESET}")
        return
    users = load_users()
    if username in users:
        print(f"{C_ERROR}Пользователь {username} уже существует.{C_RESET}")
        return
    pwd = getpass.getpass(f"Пароль для {username}: ")
    users[username] = {"password": hash_password(pwd), "role": role}
    save_users(users)
    print(f"{C_SUCCESS}Пользователь {username} ({role}) создан.{C_RESET}")

def cmd_userdel(args):
    if not check_perm("admin"):
        return
    if not args:
        print(f"{C_ERROR}Использование: userdel <имя>{C_RESET}")
        return
    username = args[0]
    if username == "admin":
        print(f"{C_ERROR}Нельзя удалить встроенного администратора.{C_RESET}")
        return
    users = load_users()
    if username not in users:
        print(f"{C_ERROR}Пользователь не найден.{C_RESET}")
        return
    del users[username]
    save_users(users)
    print(f"{C_SUCCESS}Пользователь {username} удалён.{C_RESET}")

def cmd_whoami(args):
    print(f"{C_BRIGHT}Пользователь:{C_RESET} {current_user}")
    print(f"{C_BRIGHT}Роль:{C_RESET} {current_role}")

def cmd_users(args):
    if not check_perm("admin"):
        return
    users = load_users()
    print(f"\n{C_WARNING}=== ПОЛЬЗОВАТЕЛИ ==={C_RESET}")
    for name, data in users.items():
        print(f"  {C_BRIGHT}{name}{C_RESET} — роль: {data['role']}")

def lock_session():
    """Блокировка сессии"""
    print(f"{C_INFO}[LOCK] Сессия заблокирована. Введите пароль для разблокировки.{C_RESET}")
    pwd = getpass.getpass("Пароль: ")
    users = load_users()
    if current_user in users and hash_password(pwd) == users[current_user]["password"]:
        print(f"{C_SUCCESS}[UNLOCK] Сессия разблокирована.{C_RESET}")
        return True
    print(f"{C_ERROR}[LOCK] Неверный пароль. Сессия заблокирована.{C_RESET}")
    return False
