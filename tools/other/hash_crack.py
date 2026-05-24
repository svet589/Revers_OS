#!/usr/bin/env python3
"""
REVERS OS v3.0 — Hash Cracker
Взлом хешей по словарю (MD5, SHA1, SHA256, SHA512)
"""

import hashlib
import os
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

HASH_TYPES = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}

def detect_hash(hash_str):
    """Определение типа хеша по длине"""
    length = len(hash_str)
    if length == 32:
        return "md5"
    elif length == 40:
        return "sha1"
    elif length == 64:
        return "sha256"
    elif length == 128:
        return "sha512"
    return None

def crack_hash(hash_str, wordlist, hash_type=None):
    """Перебор хеша по словарю"""
    if not hash_type:
        hash_type = detect_hash(hash_str)
        if not hash_type:
            return None, "Не удалось определить тип хеша"
    
    if hash_type not in HASH_TYPES:
        return None, f"Неподдерживаемый тип хеша: {hash_type}"
    
    hash_func = HASH_TYPES[hash_type]
    
    if not os.path.exists(wordlist):
        return None, f"Файл словаря не найден: {wordlist}"
    
    try:
        with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, 1):
                word = line.strip()
                if hash_func(word.encode()).hexdigest() == hash_str:
                    return word, None
    except Exception as e:
        return None, str(e)
    
    return None, "Пароль не найден в словаре"

def run_hash_crack(args):
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🔓 HASH CRACKER{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    print(f"{C_INFO}Поддерживаемые форматы: MD5, SHA1, SHA256, SHA512{C_RESET}\n")
    
    hash_str = input(f"{C_INFO}Хеш для взлома: {C_RESET}").strip()
    if not hash_str:
        print(f"{C_ERROR}[!] Хеш не указан.{C_RESET}")
        return
    
    # Автоопределение
    detected = detect_hash(hash_str)
    if detected:
        print(f"{C_DIM}Определён тип: {detected.upper()}{C_RESET}")
        
        use_auto = input(f"{C_INFO}Использовать этот тип? (y/n, Enter = да): {C_RESET}").strip().lower()
        if use_auto in ['n', 'no', 'н', 'нет']:
            print(f"{C_DIM}Доступные типы: {', '.join(HASH_TYPES.keys())}{C_RESET}")
            hash_type = input(f"{C_INFO}Введите тип: {C_RESET}").strip().lower()
        else:
            hash_type = detected
    else:
        print(f"{C_DIM}Доступные типы: {', '.join(HASH_TYPES.keys())}{C_RESET}")
        hash_type = input(f"{C_INFO}Введите тип хеша: {C_RESET}").strip().lower()
    
    wordlist = input(f"{C_INFO}Путь к словарю: {C_RESET}").strip()
    if not wordlist:
        print(f"{C_ERROR}[!] Словарь не указан.{C_RESET}")
        return
    
    print(f"\n{C_INFO}[*] Взлом хеша...{C_RESET}")
    
    result, error = crack_hash(hash_str, wordlist, hash_type)
    
    if error:
        print(f"{C_ERROR}[!] {error}{C_RESET}")
    elif result:
        print(f"\n{C_SUCCESS}╔══════════════════════════════════╗{C_RESET}")
        print(f"{C_SUCCESS}║  🎉 ПАРОЛЬ НАЙДЕН!              ║{C_RESET}")
        print(f"{C_SUCCESS}║  {result:<30} ║{C_RESET}")
        print(f"{C_SUCCESS}╚══════════════════════════════════╝{C_RESET}")
    else:
        print(f"\n{C_WARNING}[!] Пароль не найден в словаре.{C_RESET}")
    
    print()
