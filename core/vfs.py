#!/usr/bin/env python3
"""
REVERS OS v3.0 — Виртуальная файловая система
"""

import os
import shutil
from core.utils import C_ERROR, C_SUCCESS, C_INFO, C_BRIGHT, C_DIM, C_RESET

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
VFS_DIR = os.path.join(DATA_DIR, "vfs")
os.makedirs(VFS_DIR, exist_ok=True)

current_vfs_path = "/"

def vfs_resolve(path):
    if path.startswith("/"):
        full = os.path.normpath(os.path.join(VFS_DIR, path.lstrip("/")))
    else:
        full = os.path.normpath(os.path.join(VFS_DIR, current_vfs_path.lstrip("/"), path))
    if not full.startswith(os.path.normpath(VFS_DIR)):
        return None
    return full

def cmd_ls(args):
    path = args[0] if args else "."
    real_path = vfs_resolve(path)
    if real_path is None or not os.path.exists(real_path):
        print(f"{C_ERROR}Путь не найден: {path}{C_RESET}")
        return
    try:
        items = sorted(os.listdir(real_path))
        for item in items:
            full = os.path.join(real_path, item)
            if os.path.isdir(full):
                print(f"{C_INFO}[DIR]{C_RESET}  {item}/")
            else:
                size = os.path.getsize(full)
                print(f"{C_BRIGHT}[FILE]{C_RESET} {item} ({size} bytes)")
    except PermissionError:
        print(f"{C_ERROR}Нет доступа к: {path}{C_RESET}")

def cmd_cd(args):
    global current_vfs_path
    if not args:
        current_vfs_path = "/"
        return
    path = args[0]
    real_path = vfs_resolve(path)
    if real_path is None or not os.path.exists(real_path) or not os.path.isdir(real_path):
        print(f"{C_ERROR}Директория не найдена: {path}{C_RESET}")
        return
    if path.startswith("/"):
        current_vfs_path = os.path.normpath(path)
    else:
        current_vfs_path = os.path.normpath(os.path.join(current_vfs_path, path))
    if not current_vfs_path.startswith("/"):
        current_vfs_path = "/" + current_vfs_path

def cmd_pwd(args):
    print(f"{C_BRIGHT}{current_vfs_path}{C_RESET}")

def cmd_mkdir(args):
    if not args:
        print(f"{C_ERROR}Использование: mkdir <имя>{C_RESET}")
        return
    real_path = vfs_resolve(args[0])
    if real_path is None:
        return
    try:
        os.makedirs(real_path, exist_ok=True)
        print(f"{C_SUCCESS}Создана директория: {args[0]}{C_RESET}")
    except Exception as e:
        print(f"{C_ERROR}Ошибка: {e}{C_RESET}")

def cmd_touch(args):
    if not args:
        print(f"{C_ERROR}Использование: touch <файл>{C_RESET}")
        return
    real_path = vfs_resolve(args[0])
    if real_path is None:
        return
    try:
        with open(real_path, 'a'):
            pass
        print(f"{C_SUCCESS}Файл создан/обновлён: {args[0]}{C_RESET}")
    except Exception as e:
        print(f"{C_ERROR}Ошибка: {e}{C_RESET}")

def cmd_cat(args):
    if not args:
        print(f"{C_ERROR}Использование: cat <файл>{C_RESET}")
        return
    real_path = vfs_resolve(args[0])
    if real_path is None or not os.path.exists(real_path):
        print(f"{C_ERROR}Файл не найден: {args[0]}{C_RESET}")
        return
    try:
        with open(real_path, 'r') as f:
            print(f.read())
    except Exception as e:
        print(f"{C_ERROR}Ошибка чтения: {e}{C_RESET}")

def cmd_rm(args):
    if not args:
        print(f"{C_ERROR}Использование: rm <файл/папка>{C_RESET}")
        return
    real_path = vfs_resolve(args[0])
    if real_path is None or not os.path.exists(real_path):
        print(f"{C_ERROR}Не найдено: {args[0]}{C_RESET}")
        return
    try:
        if os.path.isdir(real_path):
            shutil.rmtree(real_path)
            print(f"{C_SUCCESS}Директория удалена: {args[0]}{C_RESET}")
        else:
            os.remove(real_path)
            print(f"{C_SUCCESS}Файл удалён: {args[0]}{C_RESET}")
    except Exception as e:
        print(f"{C_ERROR}Ошибка удаления: {e}{C_RESET}")

def cmd_secure_del(args):
    """Безопасное удаление с перезаписью нулями"""
    if not args:
        print(f"{C_ERROR}Использование: secure-del <файл>{C_RESET}")
        return
    real_path = vfs_resolve(args[0])
    if real_path is None or not os.path.exists(real_path):
        print(f"{C_ERROR}Файл не найден: {args[0]}{C_RESET}")
        return
    if os.path.isdir(real_path):
        print(f"{C_ERROR}secure-del работает только с файлами.{C_RESET}")
        return
    try:
        size = os.path.getsize(real_path)
        with open(real_path, 'wb') as f:
            f.write(b'\x00' * size)
        os.remove(real_path)
        print(f"{C_SUCCESS}Файл безопасно удалён: {args[0]}{C_RESET}")
    except Exception as e:
        print(f"{C_ERROR}Ошибка: {e}{C_RESET}")
