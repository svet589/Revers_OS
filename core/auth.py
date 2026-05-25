#!/usr/bin/env python3
"""
REVERS OS v3.0 — Авторизация и управление пользователями
Полный фикс багов первого запуска
"""

import os
import json
import hashlib
import getpass
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_BRIGHT, C_RESET

# Пути
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
PASSWORD_FILE = os.path.join(DATA_DIR, "password.hash")  # Для миграции со старой версии

# Текущая сессия
current_user = None
current_role = None

# ============================================
# ХЕШИРОВАНИЕ
# ============================================
def hash_password(pwd):
    """SHA256 хеш пароля"""
    return hashlib.sha256(pwd.encode()).hexdigest()

# ============================================
# РАБОТА С ФАЙЛАМИ
# ============================================
def ensure_data_dir():
    """Создать папку data если её нет"""
    os.makedirs(DATA_DIR, exist_ok=True)

def init_users():
    """Совместимость со старым кодом"""
    ensure_data_dir()
    
def load_users():
    """Загрузить пользователей из файла"""
    ensure_data_dir()
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print(f"{C_ERROR}[!] Файл пользователей повреждён. Создаём новый.{C_RESET}")
            return {}
    return {}

def save_users(users):
    """Сохранить пользователей в файл"""
    ensure_data_dir()
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def is_first_launch():
    """Проверить, первый ли это запуск"""
    return not os.path.exists(USERS_FILE) or len(load_users()) == 0

# ============================================
# ПЕРВЫЙ ЗАПУСК — СОЗДАНИЕ АДМИНА
# ============================================
def first_launch_setup():
    """Создание учётной записи администратора при первом запуске"""
    print(f"\n{C_WARNING}╔══════════════════════════════════════════╗{C_RESET}")
    print(f"{C_WARNING}║       🔐 ПЕРВЫЙ ЗАПУСК ОБНАРУЖЕН        ║{C_RESET}")
    print(f"{C_WARNING}║  Создание учётной записи администратора  ║{C_RESET}")
    print(f"{C_WARNING}╚══════════════════════════════════════════╝{C_RESET}\n")
    
    while True:
        pwd = getpass.getpass("Придумайте пароль для admin: ")
        
        if len(pwd) < 4:
            print(f"{C_ERROR}[!] Пароль должен быть не короче 4 символов.{C_RESET}\n")
            continue
        
        pwd2 = getpass.getpass("Повторите пароль: ")
        
        if pwd != pwd2:
            print(f"{C_ERROR}[!] Пароли не совпадают. Попробуйте снова.{C_RESET}\n")
            continue
        
        # Сохраняем админа
        users = {
            "admin": {
                "password": hash_password(pwd),
                "role": "admin"
            }
        }
        save_users(users)
        
        print(f"\n{C_SUCCESS}╔══════════════════════════════════════════╗{C_RESET}")
        print(f"{C_SUCCESS}║  ✅ Администратор успешно создан!        ║{C_RESET}")
        print(f"{C_SUCCESS}║  Логин: admin                            ║{C_RESET}")
        print(f"{C_SUCCESS}║  ⚠️  НЕ ЗАБУДЬТЕ ПАРОЛЬ!                ║{C_RESET}")
        print(f"{C_SUCCESS}╚══════════════════════════════════════════╝{C_RESET}")
        
        input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
        return True

# ============================================
# МИГРАЦИЯ СО СТАРОЙ ВЕРСИИ
# ============================================
def migrate_from_old_version():
    """Миграция с password.hash на users.json"""
    if os.path.exists(PASSWORD_FILE):
        try:
            with open(PASSWORD_FILE, "r") as f:
                old_hash = f.read().strip()
            
            if old_hash:
                users = {"admin": {"password": old_hash, "role": "admin"}}
                save_users(users)
                os.remove(PASSWORD_FILE)
                print(f"{C_WARNING}[MIGRATION] Старый пароль перенесён в новую систему.{C_RESET}")
                return True
        except:
            pass
    return False

# ============================================
# АВТОРИЗАЦИЯ
# ============================================
def login():
    """Авторизация пользователя. Возвращает True при успехе."""
    global current_user, current_role
    
    ensure_data_dir()
    
    # Миграция со старой версии
    migrate_from_old_version()
    
    # Первый запуск — создаём админа
    if is_first_launch():
        first_launch_setup()
    
    # Загружаем пользователей
    users = load_users()
    
    if not users:
        print(f"{C_ERROR}[CRITICAL] Нет пользователей. Перезапустите систему.{C_RESET}")
        return False
    
    print(f"\n{C_INFO}╔══════════════════════════════════════════╗{C_RESET}")
    print(f"{C_INFO}║     🔒 ДОСТУП К REVERS OS v3.0           ║{C_RESET}")
    print(f"{C_INFO}║     Требуется авторизация                ║{C_RESET}")
    print(f"{C_INFO}╚══════════════════════════════════════════╝{C_RESET}\n")
    
    max_attempts = 3
    
    for attempt in range(max_attempts):
        username = input("Логин: ").strip()
        pwd = getpass.getpass("Пароль: ")
        
        # Проверяем существование пользователя
        if username not in users:
            left = max_attempts - attempt - 1
            if left > 0:
                print(f"{C_ERROR}[!] Пользователь '{username}' не найден. Осталось попыток: {left}{C_RESET}\n")
            else:
                print(f"{C_ERROR}[!] Пользователь '{username}' не найден.{C_RESET}")
            continue
        
        # Проверяем пароль
        hashed = hash_password(pwd)
        if hashed == users[username]["password"]:
            current_user = username
            current_role = users[username].get("role", "user")
            
            print(f"\n{C_SUCCESS}╔══════════════════════════════════════════╗{C_RESET}")
            print(f"{C_SUCCESS}║  ✅ ДОСТУП РАЗРЕШЁН                      ║{C_RESET}")
            print(f"{C_SUCCESS}║  Пользователь: {username:<27}║{C_RESET}")
            print(f"{C_SUCCESS}║  Роль: {current_role:<34}║{C_RESET}")
            print(f"{C_SUCCESS}╚══════════════════════════════════════════╝{C_RESET}\n")
            return True
        else:
            left = max_attempts - attempt - 1
            if left > 0:
                print(f"{C_ERROR}[!] Неверный пароль. Осталось попыток: {left}{C_RESET}\n")
            else:
                print(f"{C_ERROR}[!] Неверный пароль.{C_RESET}")
    
    # Исчерпаны попытки
    print(f"\n{C_ERROR}╔══════════════════════════════════════════╗{C_RESET}")
    print(f"{C_ERROR}║  ❌ ДОСТУП ЗАБЛОКИРОВАН                  ║{C_RESET}")
    print(f"{C_ERROR}║  Превышено количество попыток.           ║{C_RESET}")
    print(f"{C_ERROR}╚══════════════════════════════════════════╝{C_RESET}")
    return False

# ============================================
# ПРОВЕРКА ПРАВ
# ============================================
def check_perm(required_role="admin"):
    """Проверить, есть ли у текущего пользователя нужные права"""
    if current_role == "admin":
        return True
    if required_role == "admin" and current_role != "admin":
        print(f"{C_ERROR}[PERMISSION DENIED] Требуются права администратора.{C_RESET}")
        return False
    return True

# ============================================
# КОМАНДЫ УПРАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯМИ
# ============================================
def cmd_whoami(args=None):
    """Показать текущего пользователя"""
    if not current_user:
        print(f"{C_ERROR}[!] Сессия не активна.{C_RESET}")
        return
    print(f"\n{C_BRIGHT}Информация о сессии:{C_RESET}")
    print(f"  ├─ Пользователь: {current_user}")
    print(f"  └─ Роль: {current_role}")
    print()

def cmd_users(args=None):
    """Список всех пользователей (только для admin)"""
    if not check_perm("admin"):
        return
    
    users = load_users()
    if not users:
        print(f"{C_DIM}Нет зарегистрированных пользователей.{C_RESET}")
        return
    
    print(f"\n{C_WARNING}╔══════════════════════════════════════════╗{C_RESET}")
    print(f"{C_WARNING}║        👥 ПОЛЬЗОВАТЕЛИ СИСТЕМЫ           ║{C_RESET}")
    print(f"{C_WARNING}╚══════════════════════════════════════════╝{C_RESET}\n")
    
    for i, (name, data) in enumerate(users.items(), 1):
        role = data.get("role", "user")
        role_color = C_ERROR if role == "admin" else C_INFO
        print(f"  {C_BRIGHT}{i}.{C_RESET} {name} — {role_color}{role}{C_RESET}")
    print()

def cmd_useradd(args):
    """Добавить нового пользователя (только для admin)"""
    if not check_perm("admin"):
        return
    
    if not args:
        print(f"{C_ERROR}[!] Использование: useradd <имя> [роль: user/admin]{C_RESET}")
        print(f"{C_DIM}  Пример: useradd hacker{C_RESET}")
        print(f"{C_DIM}  Пример: useradd moderator admin{C_RESET}")
        return
    
    username = args[0].lower().strip()
    
    # Валидация имени
    if not username.isalnum():
        print(f"{C_ERROR}[!] Имя пользователя должно содержать только буквы и цифры.{C_RESET}")
        return
    
    if len(username) < 2:
        print(f"{C_ERROR}[!] Имя пользователя должно быть не короче 2 символов.{C_RESET}")
        return
    
    # Роль
    role = "user"
    if len(args) > 1:
        if args[1] in ["user", "admin"]:
            role = args[1]
        else:
            print(f"{C_ERROR}[!] Роль должна быть 'user' или 'admin'.{C_RESET}")
            return
    
    # Проверка существования
    users = load_users()
    if username in users:
        print(f"{C_ERROR}[!] Пользователь '{username}' уже существует.{C_RESET}")
        return
    
    # Пароль
    print(f"\n{C_INFO}Создание пользователя: {username} ({role}){C_RESET}")
    pwd = getpass.getpass("Пароль: ")
    
    if len(pwd) < 4:
        print(f"{C_ERROR}[!] Пароль должен быть не короче 4 символов.{C_RESET}")
        return
    
    pwd2 = getpass.getpass("Повторите пароль: ")
    
    if pwd != pwd2:
        print(f"{C_ERROR}[!] Пароли не совпадают.{C_RESET}")
        return
    
    # Сохраняем
    users[username] = {
        "password": hash_password(pwd),
        "role": role
    }
    save_users(users)
    
    print(f"\n{C_SUCCESS}✅ Пользователь '{username}' ({role}) успешно создан!{C_RESET}\n")

def cmd_userdel(args):
    """Удалить пользователя (только для admin)"""
    if not check_perm("admin"):
        return
    
    if not args:
        print(f"{C_ERROR}[!] Использование: userdel <имя>{C_RESET}")
        return
    
    username = args[0].lower().strip()
    
    # Нельзя удалить себя
    if username == current_user:
        print(f"{C_ERROR}[!] Нельзя удалить самого себя.{C_RESET}")
        return
    
    # Нельзя удалить встроенного админа (если он последний)
    users = load_users()
    
    if username not in users:
        print(f"{C_ERROR}[!] Пользователь '{username}' не найден.{C_RESET}")
        return
    
    # Проверка: не удаляем последнего админа
    if users[username]["role"] == "admin":
        admin_count = sum(1 for u in users.values() if u["role"] == "admin")
        if admin_count <= 1:
            print(f"{C_ERROR}[!] Нельзя удалить последнего администратора.{C_RESET}")
            return
    
    # Подтверждение
    print(f"{C_WARNING}Вы уверены, что хотите удалить пользователя '{username}'?{C_RESET}")
    confirm = input("Введите 'yes' для подтверждения: ").strip()
    
    if confirm.lower() != "yes":
        print(f"{C_DIM}Удаление отменено.{C_RESET}")
        return
    
    del users[username]
    save_users(users)
    print(f"{C_SUCCESS}✅ Пользователь '{username}' удалён.{C_RESET}\n")

# ============================================
# БЛОКИРОВКА СЕССИИ
# ============================================
def lock_session():
    """Заблокировать текущую сессию"""
    if not current_user:
        return False
    
    print(f"\n{C_WARNING}╔══════════════════════════════════════════╗{C_RESET}")
    print(f"{C_WARNING}║  🔒 СЕССИЯ ЗАБЛОКИРОВАНА                 ║{C_RESET}")
    print(f"{C_WARNING}║  Введите пароль для разблокировки        ║{C_RESET}")
    print(f"{C_WARNING}╚══════════════════════════════════════════╝{C_RESET}\n")
    
    users = load_users()
    
    for attempt in range(3):
        pwd = getpass.getpass("Пароль: ")
        
        if current_user in users:
            if hash_password(pwd) == users[current_user]["password"]:
                print(f"\n{C_SUCCESS}🔓 Сессия разблокирована. Добро пожаловать, {current_user}!{C_RESET}\n")
                return True
            else:
                left = 2 - attempt
                if left > 0:
                    print(f"{C_ERROR}[!] Неверный пароль. Осталось попыток: {left}{C_RESET}\n")
    
    print(f"\n{C_ERROR}[!] Превышено количество попыток. Сессия завершена.{C_RESET}")
    return False
