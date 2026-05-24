#!/usr/bin/env python3
"""
REVERS OS v3.0 — CipherForge
Шифрование и дешифрование текста
"""

import os
import base64
import binascii
import codecs
import urllib.parse
import json
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET, clear_screen

METHODS = [
    "Base64", "Hex", "ROT13", "URL-encoding",
    "Base32", "JSON escape", "Шифр Цезаря", "UTF-8 decimal",
    "XOR", "Revers"
]

def encode_text(text, method):
    if method == "Base64":
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    elif method == "Hex":
        return binascii.hexlify(text.encode('utf-8')).decode('utf-8')
    elif method == "ROT13":
        return codecs.encode(text, 'rot_13')
    elif method == "URL-encoding":
        return urllib.parse.quote(text)
    elif method == "Base32":
        return base64.b32encode(text.encode('utf-8')).decode('utf-8')
    elif method == "JSON escape":
        return json.dumps(text)[1:-1]
    elif method == "Шифр Цезаря":
        shift = 3
        result = []
        for c in text:
            if c.isupper():
                result.append(chr((ord(c) - 65 + shift) % 26 + 65))
            elif c.islower():
                result.append(chr((ord(c) - 97 + shift) % 26 + 97))
            else:
                result.append(c)
        return ''.join(result)
    elif method == "UTF-8 decimal":
        return ' '.join(str(b) for b in text.encode('utf-8'))
    elif method == "XOR":
        key = "REVERS"
        result = []
        for i, c in enumerate(text):
            result.append(chr(ord(c) ^ ord(key[i % len(key)])))
        return ''.join(result)
    elif method == "Revers":
        return text[::-1]
    return None

def decode_text(encoded, method):
    try:
        if method == "Base64":
            return base64.b64decode(encoded.encode('utf-8')).decode('utf-8')
        elif method == "Hex":
            return binascii.unhexlify(encoded.encode('utf-8')).decode('utf-8')
        elif method == "ROT13":
            return codecs.decode(encoded, 'rot_13')
        elif method == "URL-encoding":
            return urllib.parse.unquote(encoded)
        elif method == "Base32":
            return base64.b32decode(encoded.encode('utf-8')).decode('utf-8')
        elif method == "JSON escape":
            return encoded.encode('utf-8').decode('unicode_escape')
        elif method == "Шифр Цезаря":
            shift = -3
            result = []
            for c in encoded:
                if c.isupper():
                    result.append(chr((ord(c) - 65 + shift) % 26 + 65))
                elif c.islower():
                    result.append(chr((ord(c) - 97 + shift) % 26 + 97))
                else:
                    result.append(c)
            return ''.join(result)
        elif method == "UTF-8 decimal":
            return ''.join(chr(int(b)) for b in encoded.split())
        elif method == "XOR":
            key = "REVERS"
            result = []
            for i, c in enumerate(encoded):
                result.append(chr(ord(c) ^ ord(key[i % len(key)])))
            return ''.join(result)
        elif method == "Revers":
            return encoded[::-1]
    except:
        return None
    return None

def select_method(mode="encrypt"):
    print(f"\n{C_INFO}Методы:{C_RESET}")
    for i, m in enumerate(METHODS, 1):
        print(f"  {C_BRIGHT}{i}{C_RESET}. {m}")
    print(f"  {C_DIM}0. Назад{C_RESET}")
    
    while True:
        try:
            choice = int(input(f"\n{C_INFO}Выберите метод: {C_RESET}"))
            if choice == 0:
                return None
            if 1 <= choice <= len(METHODS):
                return METHODS[choice - 1]
        except ValueError:
            pass
        print(f"{C_ERROR}[!] Неверный выбор.{C_RESET}")

def get_input():
    print(f"\n{C_INFO}Источник:{C_RESET}")
    print(f"  1. Ввести текст вручную")
    print(f"  2. Загрузить из файла")
    print(f"  0. Назад")
    
    while True:
        choice = input(f"\n{C_INFO}Выбор: {C_RESET}").strip()
        if choice == "0":
            return None
        elif choice == "1":
            print(f"{C_INFO}Введите текст (пустая строка — конец):{C_RESET}")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            return "\n".join(lines)
        elif choice == "2":
            filepath = input(f"{C_INFO}Путь к файлу: {C_RESET}").strip()
            if os.path.exists(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        return f.read()
                except Exception as e:
                    print(f"{C_ERROR}[!] Ошибка чтения: {e}{C_RESET}")
            else:
                print(f"{C_ERROR}[!] Файл не найден.{C_RESET}")
        else:
            print(f"{C_ERROR}[!] Неверный выбор.{C_RESET}")

def run_cipher_forge(args):
    while True:
        clear_screen()
        print(f"\n{C_WARNING}╔══════════════════════════════════════════╗{C_RESET}")
        print(f"{C_WARNING}║         🔒 CIPHER FORGE v1.0             ║{C_RESET}")
        print(f"{C_WARNING}╠══════════════════════════════════════════╣{C_RESET}")
        print(f"{C_WARNING}║  1. Зашифровать                         ║{C_RESET}")
        print(f"{C_WARNING}║  2. Расшифровать                        ║{C_RESET}")
        print(f"{C_WARNING}║  0. Выход                               ║{C_RESET}")
        print(f"{C_WARNING}╚══════════════════════════════════════════╝{C_RESET}")
        
        choice = input(f"\n{C_INFO}Выберите действие: {C_RESET}").strip()
        
        if choice == "0":
            break
        
        elif choice == "1":
            method = select_method("encrypt")
            if not method:
                continue
            
            text = get_input()
            if text is None:
                continue
            
            result = encode_text(text, method)
            if result:
                print(f"\n{C_SUCCESS}[+] Результат ({method}):{C_RESET}")
                print(f"{C_BRIGHT}{result}{C_RESET}")
                
                save = input(f"\n{C_INFO}Сохранить в файл? (y/n): {C_RESET}").strip().lower()
                if save in ['y', 'yes', 'д', 'да']:
                    filename = f"encrypted_{method.lower().replace(' ', '_')}.txt"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(result)
                    print(f"{C_SUCCESS}Сохранено: {filename}{C_RESET}")
            else:
                print(f"{C_ERROR}[!] Ошибка шифрования.{C_RESET}")
            
            input(f"\n{C_DIM}Нажмите Enter...{C_RESET}")
        
        elif choice == "2":
            method = select_method("decrypt")
            if not method:
                continue
            
            text = get_input()
            if text is None:
                continue
            
            result = decode_text(text, method)
            if result:
                print(f"\n{C_SUCCESS}[+] Результат ({method}):{C_RESET}")
                print(f"{C_BRIGHT}{result}{C_RESET}")
                
                save = input(f"\n{C_INFO}Сохранить в файл? (y/n): {C_RESET}").strip().lower()
                if save in ['y', 'yes', 'д', 'да']:
                    filename = f"decrypted_{method.lower().replace(' ', '_')}.txt"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(result)
                    print(f"{C_SUCCESS}Сохранено: {filename}{C_RESET}")
            else:
                print(f"{C_ERROR}[!] Ошибка дешифрования. Проверьте метод.{C_RESET}")
            
            input(f"\n{C_DIM}Нажмите Enter...{C_RESET}")
