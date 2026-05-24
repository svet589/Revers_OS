#!/usr/bin/env python3
"""
REVERS OS v3.0 — Hash Cracker
Взлом хешей по словарю (MD5, SHA1, SHA256, SHA512)
"""

import hashlib
import os
import requests
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
WORDLIST_DIR = os.path.join(DATA_DIR, "wordlists")

HASH_TYPES = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}

# Вшитый топ-100 паролей для быстрой проверки
TOP_PASSWORDS = [
    "123456", "password", "123456789", "12345678", "12345", "1234567",
    "admin", "123123", "qwerty", "abc123", "letmein", "monkey", "111111",
    "password1", "qwerty123", "dragon", "1234", "iloveyou", "000000",
    "master", "sunshine", "flower", "football", "shadow", "michael",
    "ashley", "charlie", "superman", "lovely", "love", "sex", "secret",
    "hello", "freedom", "chocolate", "biteme", "654321", "654321",
    "passw0rd", "pass", "p@ssword", "p@ssw0rd", "qazwsx", "trustno1",
    "jordan", "jennifer", "hunter", "buster", "soccer", "batman",
    "andrew", "tigger", "joshua", "miller", "cheese", "pepper",
    "matthew", "access", "yankees", "thomas", "robert", "dallas",
    "banana", "lovers", "summer", "corona", "cookie", "starwars",
    "star", "qwerty1234", "1q2w3e4r", "zxcvbnm", "asdfgh", "fuck",
    "fuckyou", "fuckoff", "suckit", "test", "test123", "testing",
    "a123456", "1234567890", "0987654321", "qwertyuiop", "123321",
    "google", "mynoob", "zaq12wsx", "pokemon", "naruto", "hacker"
]

# Ссылки на словари
WORDLIST_URLS = {
    "top10k": {
        "url": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt",
        "size": "~100 KB",
        "desc": "10 тысяч популярных паролей"
    },
}

def download_wordlist(name):
    """Скачать словарь если его нет"""
    if name not in WORDLIST_URLS:
        return None
    
    os.makedirs(WORDLIST_DIR, exist_ok=True)
    filepath = os.path.join(WORDLIST_DIR, f"{name}.txt")
    
    if os.path.exists(filepath):
        return filepath
    
    info = WORDLIST_URLS[name]
    print(f"{C_INFO}[*] Скачивание {name} ({info['size']})...{C_RESET}")
    
    try:
        resp = requests.get(info["url"], timeout=120)
        resp.raise_for_status()
        
        with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
            f.write(resp.text)
        
        lines = sum(1 for _ in open(filepath, "r", errors="ignore"))
        print(f"{C_SUCCESS}[OK] Загружено {lines:,} паролей → {filepath}{C_RESET}")
        return filepath
    
    except Exception as e:
        print(f"{C_ERROR}[!] Ошибка скачивания: {e}{C_RESET}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return None

def detect_hash(hash_str):
    """Определение типа хеша по длине"""
    length = len(hash_str)
    if length == 32: return "md5"
    elif length == 40: return "sha1"
    elif length == 64: return "sha256"
    elif length == 128: return "sha512"
    return None

def crack_with_list(hash_str, words, hash_func):
    """Перебор по списку слов (для вшитого словаря)"""
    for word in words:
        if hash_func(word.encode()).hexdigest() == hash_str:
            return word
    return None

def crack_with_file(hash_str, wordlist, hash_func):
    """Перебор по файлу словаря"""
    if not os.path.exists(wordlist):
        return None, f"Файл не найден: {wordlist}"
    
    try:
        total = sum(1 for _ in open(wordlist, "r", errors="ignore"))
        checked = 0
        
        with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                word = line.strip()
                if hash_func(word.encode()).hexdigest() == hash_str:
                    return word, None
                
                checked += 1
                if checked % 10000 == 0:
                    percent = int(checked / total * 100)
                    sys.stdout.write(f"\r  Прогресс: {percent}% ({checked:,}/{total:,})")
                    sys.stdout.flush()
        
        print()  # Новая строка после прогресс-бара
        return None, "Пароль не найден"
    
    except Exception as e:
        return None, str(e)

def run_hash_crack(args):
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🔓 HASH CRACKER{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    print(f"{C_INFO}Поддерживаемые форматы: MD5, SHA1, SHA256, SHA512{C_RESET}\n")
    
    hash_str = input(f"{C_INFO}Хеш для взлома: {C_RESET}").strip()
    if not hash_str:
        print(f"{C_ERROR}[!] Хеш не указан.{C_RESET}")
        return
    
    # Автоопределение типа
    detected = detect_hash(hash_str)
    if detected:
        print(f"{C_DIM}Определён тип: {detected.upper()}{C_RESET}")
        use_auto = input(f"{C_INFO}Использовать? (Enter = да, n = выбрать другой): {C_RESET}").strip().lower()
        if use_auto in ['n', 'no', 'н', 'нет']:
            print(f"{C_DIM}Доступные: {', '.join(HASH_TYPES.keys())}{C_RESET}")
            hash_type = input(f"{C_INFO}Введите тип: {C_RESET}").strip().lower()
        else:
            hash_type = detected
    else:
        print(f"{C_DIM}Доступные: {', '.join(HASH_TYPES.keys())}{C_RESET}")
        hash_type = input(f"{C_INFO}Введите тип хеша: {C_RESET}").strip().lower()
    
    if hash_type not in HASH_TYPES:
        print(f"{C_ERROR}[!] Неподдерживаемый тип.{C_RESET}")
        return
    
    hash_func = HASH_TYPES[hash_type]
    
    # Выбор словаря
    print(f"\n{C_INFO}Словарь:{C_RESET}")
    print(f"  {C_BRIGHT}1{C_RESET}. Быстрая проверка (топ-100 паролей, мгновенно)")
    print(f"  {C_BRIGHT}2{C_RESET}. Скачать top10k (10 тыс паролей, {WORDLIST_URLS['top10k']['size']})")
    print(f"  {C_BRIGHT}3{C_RESET}. Указать свой файл словаря")
    print(f"  {C_DIM}0{C_RESET}. Отмена")
    
    wordlist_choice = input(f"\n{C_INFO}Выбор: {C_RESET}").strip()
    
    result = None
    error = None
    
    if wordlist_choice == "0":
        return
    
    elif wordlist_choice == "1":
        print(f"\n{C_INFO}[*] Быстрая проверка топ-100 паролей...{C_RESET}")
        result = crack_with_list(hash_str, TOP_PASSWORDS, hash_func)
        if not result:
            error = "Пароль не найден в топ-100"
    
    elif wordlist_choice == "2":
        wordlist = download_wordlist("top10k")
        if wordlist:
            print(f"\n{C_INFO}[*] Перебор по словарю top10k...{C_RESET}")
            result, error = crack_with_file(hash_str, wordlist, hash_func)
        else:
            error = "Не удалось загрузить словарь"
    
    elif wordlist_choice == "3":
        wordlist = input(f"{C_INFO}Путь к словарю: {C_RESET}").strip()
        if wordlist:
            print(f"\n{C_INFO}[*] Перебор по словарю...{C_RESET}")
            result, error = crack_with_file(hash_str, wordlist, hash_func)
        else:
            error = "Словарь не указан"
    
    else:
        error = "Неверный выбор"
    
    # Результат
    if error:
        print(f"\n{C_ERROR}[!] {error}{C_RESET}")
    elif result:
        print(f"\n{C_SUCCESS}╔══════════════════════════════════╗{C_RESET}")
        print(f"{C_SUCCESS}║  🎉 ПАРОЛЬ НАЙДЕН!              ║{C_RESET}")
        print(f"{C_SUCCESS}║  {result:<30} ║{C_RESET}")
        print(f"{C_SUCCESS}╚══════════════════════════════════╝{C_RESET}")
    
    print()
