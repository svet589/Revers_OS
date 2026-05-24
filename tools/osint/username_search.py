#!/usr/bin/env python3
"""
REVERS OS v3.0 — Username Search
Поиск username по соцсетям и сервисам
"""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Twitter/X": "https://x.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Reddit": "https://www.reddit.com/user/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Steam": "https://steamcommunity.com/id/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Medium": "https://medium.com/@{}",
    "VK": "https://vk.com/{}",
    "Telegram": "https://t.me/{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "Flickr": "https://www.flickr.com/people/{}",
    "Patreon": "https://www.patreon.com/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "About.me": "https://about.me/{}",
    "Keybase": "https://keybase.io/{}",
    "Bitbucket": "https://bitbucket.org/{}/",
    "GitLab": "https://gitlab.com/{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "Lobste.rs": "https://lobste.rs/u/{}",
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "Chess.com": "https://www.chess.com/member/{}",
    "FortniteTracker": "https://fortnitetracker.com/profile/all/{}",
}

def check_platform(name, url_template, username, timeout=5):
    try:
        url = url_template.format(username)
        resp = requests.get(url, timeout=timeout, allow_redirects=True, 
                           headers={"User-Agent": "Mozilla/5.0"})
        # Если страница существует (не 404 и не редирект на главную)
        if resp.status_code == 200 and len(resp.text) > 100:
            return (name, url, True)
        return (name, url, False)
    except:
        return (name, url, None)

def run_username_search(args):
    if not args:
        username = input(f"{C_INFO}Введите username для поиска: {C_RESET}").strip()
    else:
        username = args[0]
    
    if not username:
        print(f"{C_ERROR}[!] Username не указан.{C_RESET}")
        return
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🔍 USERNAME SEARCH{C_RESET}")
    print(f"{C_WARNING}         Цель: {C_BRIGHT}{username}{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    print(f"{C_INFO}[*] Проверка {len(PLATFORMS)} платформ...{C_RESET}\n")
    
    found = []
    not_found = []
    errors = []
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_platform, name, url, username): name 
                   for name, url in PLATFORMS.items()}
        done = 0
        for future in as_completed(futures):
            name, url, exists = future.result()
            done += 1
            
            if exists:
                found.append((name, url))
                print(f"  {C_SUCCESS}[+]{C_RESET} {name}: {url}")
            elif exists is False:
                not_found.append(name)
            else:
                errors.append(name)
            
            # Прогресс
            percent = int(done / len(PLATFORMS) * 100)
            sys.stdout.write(f"\r  Прогресс: {percent}% ({done}/{len(PLATFORMS)})")
            sys.stdout.flush()
    
    print(f"\n\n{C_WARNING}═══════════════ РЕЗУЛЬТАТЫ ═══════════════{C_RESET}")
    print(f"  {C_SUCCESS}Найдено: {len(found)}{C_RESET}")
    print(f"  {C_ERROR}Не найдено: {len(not_found)}{C_RESET}")
    print(f"  {C_DIM}Ошибки: {len(errors)}{C_RESET}")
    
    if found:
        print(f"\n{C_BRIGHT}Найденные профили:{C_RESET}")
        for name, url in found:
            print(f"  ├─ {name}: {url}")
    
    print()
