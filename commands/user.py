#!/usr/bin/env python3
"""
REVERS OS v3.0 — Пользовательские команды
"""

import os
import json
import http.server
import socketserver
import threading
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET
from core.vfs import vfs_resolve

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
NOTES_DIR = os.path.join(DATA_DIR, "notes")
VAULT_DIR = os.path.join(DATA_DIR, "vault")
EXPORTS_DIR = os.path.join(DATA_DIR, "exports")

# ============================================
# ЗАМЕТКИ
# ============================================
def cmd_notes(args):
    os.makedirs(NOTES_DIR, exist_ok=True)
    notes_file = os.path.join(NOTES_DIR, "notes.txt")
    
    if not args:
        if os.path.exists(notes_file):
            with open(notes_file, "r") as f:
                content = f.read()
            if content:
                print(f"{C_INFO}Заметки:{C_RESET}\n{content}")
            else:
                print(f"{C_DIM}Заметок нет.{C_RESET}")
        else:
            print(f"{C_DIM}Заметок нет.{C_RESET}")
        return
    
    action = args[0]
    if action == "add":
        print(f"{C_INFO}Введите заметку (Enter для сохранения, пустая строка — выход):{C_RESET}")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        if lines:
            with open(notes_file, "a") as f:
                f.write("\n".join(lines) + "\n")
            print(f"{C_SUCCESS}Заметка добавлена.{C_RESET}")
    elif action == "clear":
        if os.path.exists(notes_file):
            os.remove(notes_file)
        print(f"{C_SUCCESS}Заметки очищены.{C_RESET}")
    else:
        print(f"{C_ERROR}Использование: notes [add|clear]{C_RESET}")

# ============================================
# ЭКСПОРТ
# ============================================
def cmd_export(args):
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    if not args:
        print(f"{C_ERROR}Использование: export <данные> [файл]{C_RESET}")
        print(f"{C_DIM}  Экспорт сохраняется в data/exports/{C_RESET}")
        return
    
    data = " ".join(args)
    filename = f"export_{len(os.listdir(EXPORTS_DIR)) + 1}.txt"
    
    filepath = os.path.join(EXPORTS_DIR, filename)
    with open(filepath, "w") as f:
        f.write(data)
    print(f"{C_SUCCESS}Экспортировано в {filepath}{C_RESET}")

# ============================================
# HTTP SHARE
# ============================================
def cmd_share(args):
    if not args:
        print(f"{C_ERROR}Использование: share <файл> [порт]{C_RESET}")
        return
    
    filepath = args[0]
    if not os.path.exists(filepath):
        real_path = vfs_resolve(filepath)
        if real_path and os.path.exists(real_path):
            filepath = real_path
        else:
            print(f"{C_ERROR}Файл не найден: {args[0]}{C_RESET}")
            return
    
    port = int(args[1]) if len(args) > 1 else 8080
    directory = os.path.dirname(os.path.abspath(filepath))
    
    print(f"{C_INFO}[SHARE] HTTP-сервер запущен на порту {port}{C_RESET}")
    print(f"{C_INFO}[SHARE] Файл: {os.path.basename(filepath)}{C_RESET}")
    print(f"{C_WARNING}[SHARE] Нажмите Ctrl+C для остановки{C_RESET}")
    
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{C_WARNING}[SHARE] Сервер остановлен.{C_RESET}")

# ============================================
# VAULT (Шифрованное хранилище)
# ============================================
def cmd_vault(args):
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        print(f"{C_ERROR}[VAULT] Требуется cryptography. Установите: pip install cryptography{C_RESET}")
        return
    
    os.makedirs(VAULT_DIR, exist_ok=True)
    key_file = os.path.join(VAULT_DIR, ".key")
    
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
        print(f"{C_SUCCESS}[VAULT] Хранилище инициализировано.{C_RESET}")
    
    with open(key_file, "rb") as f:
        key = f.read()
    fernet = Fernet(key)
    
    if not args:
        files = [f for f in os.listdir(VAULT_DIR) if f.endswith(".enc")]
        if files:
            print(f"{C_INFO}[VAULT] Файлы в хранилище:{C_RESET}")
            for f in files:
                print(f"  {C_BRIGHT}{f[:-4]}{C_RESET}")
        else:
            print(f"{C_DIM}[VAULT] Хранилище пусто.{C_RESET}")
        return
    
    action = args[0]
    if action == "add" and len(args) > 1:
        filepath = args[1]
        if not os.path.exists(filepath):
            print(f"{C_ERROR}[VAULT] Файл не найден.{C_RESET}")
            return
        with open(filepath, "rb") as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        vault_file = os.path.join(VAULT_DIR, os.path.basename(filepath) + ".enc")
        with open(vault_file, "wb") as f:
            f.write(encrypted)
        print(f"{C_SUCCESS}[VAULT] Файл добавлен в хранилище.{C_RESET}")
    
    elif action == "get" and len(args) > 1:
        vault_file = os.path.join(VAULT_DIR, args[1] + ".enc")
        if not os.path.exists(vault_file):
            print(f"{C_ERROR}[VAULT] Файл не найден в хранилище.{C_RESET}")
            return
        with open(vault_file, "rb") as f:
            encrypted = f.read()
        decrypted = fernet.decrypt(encrypted)
        out_file = args[2] if len(args) > 2 else args[1]
        with open(out_file, "wb") as f:
            f.write(decrypted)
        print(f"{C_SUCCESS}[VAULT] Файл извлечён: {out_file}{C_RESET}")
    
    elif action == "delete" and len(args) > 1:
        vault_file = os.path.join(VAULT_DIR, args[1] + ".enc")
        if os.path.exists(vault_file):
            os.remove(vault_file)
            print(f"{C_SUCCESS}[VAULT] Файл удалён из хранилища.{C_RESET}")
        else:
            print(f"{C_ERROR}[VAULT] Файл не найден.{C_RESET}")
    
    else:
        print(f"{C_ERROR}[VAULT] Использование:{C_RESET}")
        print(f"  vault              - список файлов")
        print(f"  vault add <файл>   - добавить в хранилище")
        print(f"  vault get <файл>   - извлечь из хранилища")
        print(f"  vault delete <файл> - удалить из хранилища")
