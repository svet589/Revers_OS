#!/usr/bin/env python3
"""
REVERS OS v3.0 — Social Media Scraper
Быстрый сбор инфы из открытых источников
"""

import requests
import re
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

def scrape_telegram(username):
    """Парсинг публичной инфы Telegram"""
    info = {}
    try:
        resp = requests.get(f"https://t.me/{username}", headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            # Имя и описание
            title = re.findall(r'<meta property="og:title" content="([^"]+)"', resp.text)
            desc = re.findall(r'<meta property="og:description" content="([^"]+)"', resp.text)
            image = re.findall(r'<meta property="og:image" content="([^"]+)"', resp.text)
            info["title"] = title[0] if title else None
            info["description"] = desc[0] if desc else None
            info["image"] = image[0] if image else None
            info["exists"] = True
        else:
            info["exists"] = False
    except:
        info["exists"] = None
    return info

def scrape_instagram(username):
    """Парсинг публичной инфы Instagram (базовый)"""
    info = {}
    try:
        resp = requests.get(f"https://www.instagram.com/{username}/?__a=1", 
                           headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            user = data.get("graphql", {}).get("user", {})
            info["username"] = user.get("username")
            info["full_name"] = user.get("full_name")
            info["bio"] = user.get("biography")
            info["followers"] = user.get("edge_followed_by", {}).get("count", 0)
            info["following"] = user.get("edge_follow", {}).get("count", 0)
            info["posts"] = user.get("edge_owner_to_timeline_media", {}).get("count", 0)
            info["is_private"] = user.get("is_private", False)
            info["exists"] = True
        else:
            info["exists"] = False
    except:
        info["exists"] = None
    return info

def run_social_scraper(args):
    if not args:
        target = input(f"{C_INFO}Введите username или ссылку: {C_RESET}").strip()
    else:
        target = args[0]
    
    # Очистка username от URL
    username = target.replace("https://", "").replace("http://", "").replace("t.me/", "").replace("instagram.com/", "").strip("/")
    
    if not username:
        print(f"{C_ERROR}[!] Username не указан.{C_RESET}")
        return
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         📱 SOCIAL MEDIA SCRAPER{C_RESET}")
    print(f"{C_WARNING}         Цель: {C_BRIGHT}{username}{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    # Telegram
    print(f"{C_INFO}[*] Проверка Telegram...{C_RESET}")
    tg = scrape_telegram(username)
    if tg.get("exists"):
        print(f"  {C_SUCCESS}[+]{C_RESET} Telegram: @{username}")
        if tg.get("title"): print(f"  ├─ Имя: {tg['title']}")
        if tg.get("description"): print(f"  └─ Описание: {tg['description'][:200]}")
    elif tg.get("exists") is False:
        print(f"  {C_ERROR}[-]{C_RESET} Telegram: не найден")
    
    # Instagram
    print(f"\n{C_INFO}[*] Проверка Instagram...{C_RESET}")
    ig = scrape_instagram(username)
    if ig.get("exists"):
        print(f"  {C_SUCCESS}[+]{C_RESET} Instagram: @{username}")
        if ig.get("full_name"): print(f"  ├─ Имя: {ig['full_name']}")
        if ig.get("bio"): print(f"  ├─ Bio: {ig['bio'][:200]}")
        if ig.get("followers"): print(f"  ├─ Подписчиков: {ig['followers']:,}")
        if ig.get("following"): print(f"  ├─ Подписок: {ig['following']:,}")
        if ig.get("posts"): print(f"  ├─ Постов: {ig['posts']:,}")
        print(f"  └─ Приватный: {'Да 🔒' if ig.get('is_private') else 'Нет 🔓'}")
    elif ig.get("exists") is False:
        print(f"  {C_ERROR}[-]{C_RESET} Instagram: не найден")
    
    print()
