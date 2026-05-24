#!/usr/bin/env python3
"""
REVERS OS v3.0 — Аудиоплеер
"""

import os
import time
import threading
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET
from apps.player.playlist import get_playlists, load_playlist, save_playlist, delete_playlist

class AudioPlayer:
    def __init__(self):
        self.playing = False
        self.paused = False
        self.current_track = None
        self.current_index = 0
        self.playlist = []
        self.thread = None
    
    def play_file(self, filepath):
        """Воспроизвести файл"""
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            self.playing = True
            self.paused = False
            return True
        except ImportError:
            return "PYGAME_NOT_FOUND"
        except Exception as e:
            return str(e)
    
    def pause_resume(self):
        """Пауза/продолжить"""
        try:
            import pygame
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                return "resumed"
            else:
                pygame.mixer.music.pause()
                self.paused = True
                return "paused"
        except:
            return None
    
    def stop(self):
        """Остановить"""
        try:
            import pygame
            pygame.mixer.music.stop()
            self.playing = False
            self.paused = False
            return True
        except:
            return None
    
    def next_track(self):
        """Следующий трек"""
        if self.playlist and self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            self.current_track = self.playlist[self.current_index]
            self.play_file(self.current_track)
            return self.current_track
        return None
    
    def prev_track(self):
        """Предыдущий трек"""
        if self.playlist and self.current_index > 0:
            self.current_index -= 1
            self.current_track = self.playlist[self.current_index]
            self.play_file(self.current_track)
            return self.current_track
        return None
    
    def get_status(self):
        """Статус плеера"""
        if not self.playing:
            return "Остановлен"
        elif self.paused:
            return "Пауза"
        else:
            return "Воспроизведение"

_player = AudioPlayer()

def run_player(args):
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🎵 AUDIO PLAYER{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    # Проверка pygame
    try:
        import pygame
    except ImportError:
        print(f"{C_ERROR}[!] Pygame не установлен. pip install pygame{C_RESET}")
        return
    
    while True:
        print(f"\n{C_INFO}Меню плеера:{C_RESET}")
        print(f"  {C_BRIGHT}1{C_RESET}. Воспроизвести файл")
        print(f"  {C_BRIGHT}2{C_RESET}. Плейлисты")
        print(f"  {C_BRIGHT}3{C_RESET}. Управление (пауза/стоп/след/пред)")
        print(f"  {C_DIM}0{C_RESET}. Выход")
        
        if _player.current_track:
            status = _player.get_status()
            track_name = os.path.basename(_player.current_track)
            print(f"\n  {C_DIM}Статус: {status} | Трек: {track_name}{C_RESET}")
        
        choice = input(f"\n{C_INFO}Выбор: {C_RESET}").strip()
        
        if choice == "0":
            _player.stop()
            break
        
        elif choice == "1":
            filepath = input(f"{C_INFO}Путь к аудиофайлу (.mp3/.wav): {C_RESET}").strip()
            if os.path.exists(filepath):
                result = _player.play_file(filepath)
                if result == True:
                    _player.current_track = filepath
                    _player.playlist = [filepath]
                    _player.current_index = 0
                    print(f"{C_SUCCESS}Воспроизведение: {os.path.basename(filepath)}{C_RESET}")
                elif result == "PYGAME_NOT_FOUND":
                    print(f"{C_ERROR}[!] Pygame не установлен.{C_RESET}")
                else:
                    print(f"{C_ERROR}[!] Ошибка: {result}{C_RESET}")
            else:
                print(f"{C_ERROR}[!] Файл не найден.{C_RESET}")
        
        elif choice == "2":
            while True:
                playlists = get_playlists()
                print(f"\n{C_INFO}Плейлисты:{C_RESET}")
                for i, pl in enumerate(playlists, 1):
                    tracks = load_playlist(pl)
                    print(f"  {C_BRIGHT}{i}{C_RESET}. {pl} ({len(tracks)} треков)")
                print(f"  {C_BRIGHT}n{C_RESET}. Создать новый")
                print(f"  {C_DIM}0{C_RESET}. Назад")
                
                pl_choice = input(f"\n{C_INFO}Выбор: {C_RESET}").strip()
                
                if pl_choice == "0":
                    break
                elif pl_choice == "n":
                    name = input(f"{C_INFO}Название плейлиста: {C_RESET}").strip()
                    if name:
                        save_playlist(name, [])
                        print(f"{C_SUCCESS}Плейлист создан: {name}{C_RESET}")
                        # Добавление треков
                        print(f"{C_INFO}Добавьте треки (пустая строка — конец):{C_RESET}")
                        tracks = []
                        while True:
                            track = input("  > ").strip()
                            if not track:
                                break
                            if os.path.exists(track):
                                tracks.append(track)
                                print(f"    {C_SUCCESS}Добавлен{C_RESET}")
                            else:
                                print(f"    {C_ERROR}Файл не найден{C_RESET}")
                        save_playlist(name, tracks)
                        print(f"{C_SUCCESS}Плейлист сохранён ({len(tracks)} треков){C_RESET}")
                else:
                    try:
                        idx = int(pl_choice) - 1
                        if 0 <= idx < len(playlists):
                            name = playlists[idx]
                            tracks = load_playlist(name)
                            if tracks:
                                _player.playlist = tracks
                                _player.current_index = 0
                                _player.current_track = tracks[0]
                                _player.play_file(tracks[0])
                                print(f"{C_SUCCESS}Воспроизведение плейлиста: {name}{C_RESET}")
                            else:
                                print(f"{C_ERROR}Плейлист пуст.{C_RESET}")
                        else:
                            print(f"{C_ERROR}[!] Неверный номер.{C_RESET}")
                    except ValueError:
                        print(f"{C_ERROR}[!] Неверный ввод.{C_RESET}")
        
        elif choice == "3":
            if not _player.playing:
                print(f"{C_DIM}Плеер не запущен.{C_RESET}")
                continue
            
            print(f"\n{C_INFO}Управление:{C_RESET}")
            print(f"  {C_BRIGHT}p{C_RESET} — пауза/продолжить")
            print(f"  {C_BRIGHT}s{C_RESET} — стоп")
            print(f"  {C_BRIGHT}n{C_RESET} — следующий трек")
            print(f"  {C_BRIGHT}b{C_RESET} — предыдущий трек")
            
            ctrl = input(f"\n{C_INFO}Команда: {C_RESET}").strip().lower()
            
            if ctrl == "p":
                result = _player.pause_resume()
                print(f"{C_INFO}{'Пауза' if result == 'paused' else 'Продолжено'}{C_RESET}")
            elif ctrl == "s":
                _player.stop()
                print(f"{C_INFO}Остановлено{C_RESET}")
            elif ctrl == "n":
                track = _player.next_track()
                if track:
                    print(f"{C_SUCCESS}Следующий: {os.path.basename(track)}{C_RESET}")
                else:
                    print(f"{C_DIM}Конец плейлиста.{C_RESET}")
            elif ctrl == "b":
                track = _player.prev_track()
                if track:
                    print(f"{C_SUCCESS}Предыдущий: {os.path.basename(track)}{C_RESET}")
                else:
                    print(f"{C_DIM}Начало плейлиста.{C_RESET}")
        
        else:
            print(f"{C_ERROR}[!] Неверный выбор.{C_RESET}")
    
    print()
