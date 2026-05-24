#!/usr/bin/env python3
"""
REVERS OS v3.0 — Image Metadata
Извлечение EXIF/GPS из изображений
"""

import os
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

def extract_exif(filepath):
    """Извлечение EXIF данных"""
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS
        
        img = Image.open(filepath)
        exif_data = img._getexif()
        
        if not exif_data:
            return None
        
        result = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "GPSInfo":
                gps_data = {}
                for gps_tag_id in value:
                    gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    gps_data[gps_tag] = value[gps_tag_id]
                result["GPSInfo"] = gps_data
            else:
                result[tag] = str(value)[:100]
        
        return result
    except ImportError:
        return "PIL_NOT_INSTALLED"
    except Exception as e:
        return str(e)

def convert_to_degrees(value):
    """Конвертация GPS координат в градусы"""
    if not value or not isinstance(value, (tuple, list)) or len(value) < 3:
        return None
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

def run_image_meta(args):
    if not args:
        filepath = input(f"{C_INFO}Укажите путь к изображению: {C_RESET}").strip()
    else:
        filepath = args[0]
    
    if not os.path.exists(filepath):
        print(f"{C_ERROR}[!] Файл не найден: {filepath}{C_RESET}")
        return
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🖼️ IMAGE METADATA{C_RESET}")
    print(f"{C_WARNING}         Файл: {C_BRIGHT}{os.path.basename(filepath)}{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    # Размер файла
    size = os.path.getsize(filepath)
    print(f"{C_BRIGHT}[Файл]{C_RESET}")
    print(f"  ├─ Размер: {size:,} байт")
    print(f"  └─ Тип: {os.path.splitext(filepath)[1].upper()}")
    
    # EXIF
    exif = extract_exif(filepath)
    if exif == "PIL_NOT_INSTALLED":
        print(f"\n{C_ERROR}[!] Pillow не установлен. pip install Pillow{C_RESET}")
    elif exif is None:
        print(f"\n{C_DIM}[~] EXIF данные не найдены.{C_RESET}")
    elif isinstance(exif, str):
        print(f"\n{C_ERROR}[!] Ошибка чтения EXIF: {exif}{C_RESET}")
    else:
        print(f"\n{C_BRIGHT}[EXIF Данные]{C_RESET}")
        for tag, value in exif.items():
            if tag != "GPSInfo":
                print(f"  ├─ {tag}: {value}")
        
        # GPS
        if "GPSInfo" in exif:
            gps = exif["GPSInfo"]
            print(f"\n{C_BRIGHT}[📍 GPS Координаты]{C_RESET}")
            
            lat = convert_to_degrees(gps.get("GPSLatitude"))
            lat_ref = gps.get("GPSLatitudeRef", "N")
            lon = convert_to_degrees(gps.get("GPSLongitude"))
            lon_ref = gps.get("GPSLongitudeRef", "E")
            
            if lat and lon:
                lat = lat if lat_ref == "N" else -lat
                lon = lon if lon_ref == "E" else -lon
                print(f"  ├─ Широта: {lat:.6f}")
                print(f"  ├─ Долгота: {lon:.6f}")
                print(f"  └─ Карта: https://www.google.com/maps?q={lat},{lon}")
    
    print()
