#!/usr/bin/env python3
"""
REVERS OS v3.0 — Конфигурация, алиасы, темы
"""

import os
import json
from core.utils import C_SUCCESS, C_ERROR, C_INFO, C_BRIGHT, C_WARNING, C_RESET, set_theme, get_theme, THEMES

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

def load_config():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    else:
        config = {"theme": "red", "aliases": {}}
        save_config(config)
    # Применить тему
    if "theme" in config:
        set_theme(config["theme"])
    return config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def cmd_theme(args):
    if not args:
        print(f"{C_INFO}Доступные темы: {', '.join(THEMES.keys())}{C_RESET}")
        print(f"{C_INFO}Текущая тема: {get_theme()}{C_RESET}")
        return
    theme = args[0]
    if theme not in THEMES:
        print(f"{C_ERROR}Тема не найдена. Доступные: {', '.join(THEMES.keys())}{C_RESET}")
        return
    config = load_config()
    config["theme"] = theme
    save_config(config)
    set_theme(theme)
    print(f"{C_SUCCESS}Тема изменена на {theme}.{C_RESET}")

def cmd_alias(args):
    config = load_config()
    aliases = config.get("aliases", {})
    
    if not args:
        if aliases:
            print(f"{C_INFO}Алиасы:{C_RESET}")
            for alias, cmd in aliases.items():
                print(f"  {C_BRIGHT}{alias}{C_RESET} -> {cmd}")
        else:
            print(f"{C_DIM}Алиасы не настроены.{C_RESET}")
        return
    
    if args[0] == "set":
        if len(args) < 3:
            print(f"{C_ERROR}Использование: alias set <имя> <команда>{C_RESET}")
            return
        alias_name = args[1]
        alias_cmd = " ".join(args[2:])
        aliases[alias_name] = alias_cmd
        config["aliases"] = aliases
        save_config(config)
        print(f"{C_SUCCESS}Алиас создан: {alias_name} -> {alias_cmd}{C_RESET}")
    
    elif args[0] == "remove":
        if len(args) < 2:
            print(f"{C_ERROR}Использование: alias remove <имя>{C_RESET}")
            return
        alias_name = args[1]
        if alias_name in aliases:
            del aliases[alias_name]
            config["aliases"] = aliases
            save_config(config)
            print(f"{C_SUCCESS}Алиас удалён: {alias_name}{C_RESET}")
        else:
            print(f"{C_ERROR}Алиас не найден: {alias_name}{C_RESET}")
    
    else:
        print(f"{C_ERROR}Использование: alias [set|remove] <имя> [команда]{C_RESET}")
