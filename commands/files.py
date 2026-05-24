#!/usr/bin/env python3
"""
REVERS OS v3.0 — Файловые команды
"""

from core.vfs import (
    cmd_ls, cmd_cd, cmd_pwd, cmd_mkdir,
    cmd_touch, cmd_cat, cmd_rm, cmd_secure_del
)

# Все функции уже реализованы в core/vfs.py
# Этот модуль просто ре-экспортирует их
