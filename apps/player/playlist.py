#!/usr/bin/env python3
"""
REVERS OS v3.0 — Управление плейлистами
"""

import os
import json
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
PLAYLIST_DIR = os.path.join(DATA_DIR, "playlists")

def get_playlists():
    """Получить список плейлистов"""
    os.makedirs(PLAYLIST_DIR, exist_ok=True)
    return [f[:-5] for f in os.listdir(PLAYLIST_DIR) if f.endswith(".json")]

def load_playlist(name):
    """Загрузить плейлист"""
    filepath = os.path.join(PLAYLIST_DIR, f"{name}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return []

def save_playlist(name, tracks):
    """Сохранить плейлист"""
    os.makedirs(PLAYLIST_DIR, exist_ok=True)
    filepath = os.path.join(PLAYLIST_DIR, f"{name}.json")
    with open(filepath, "w") as f:
        json.dump(tracks, f, indent=2)

def delete_playlist(name):
    """Удалить плейлист"""
    filepath = os.path.join(PLAYLIST_DIR, f"{name}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
