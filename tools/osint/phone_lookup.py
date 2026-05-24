#!/usr/bin/env python3
"""
REVERS OS v3.0 — Phone Lookup
Информация о телефонном номере
"""

import re
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

# База кодов стран (выборочно)
COUNTRY_CODES = {
    "7": "Россия / Казахстан",
    "1": "США / Канада",
    "44": "Великобритания",
    "49": "Германия",
    "33": "Франция",
    "39": "Италия",
    "34": "Испания",
    "380": "Украина",
    "375": "Беларусь",
    "86": "Китай",
    "81": "Япония",
    "82": "Южная Корея",
    "91": "Индия",
    "55": "Бразилия",
    "52": "Мексика",
    "48": "Польша",
    "90": "Турция",
    "31": "Нидерланды",
    "46": "Швеция",
    "47": "Норвегия",
    "45": "Дания",
    "358": "Финляндия",
    "420": "Чехия",
    "36": "Венгрия",
    "40": "Румыния",
    "359": "Болгария",
    "30": "Греция",
    "351": "Португалия",
    "32": "Бельгия",
    "41": "Швейцария",
    "43": "Австрия",
    "972": "Израиль",
    "971": "ОАЭ",
    "966": "Саудовская Аравия",
    "20": "Египет",
    "27": "ЮАР",
    "61": "Австралия",
    "64": "Новая Зеландия",
}

MOBILE_CODES_RU = {
    "900": "Tele2", "901": "Tele2", "902": "Tele2", "903": "Tele2",
    "904": "Tele2", "905": "Tele2", "906": "Tele2", "908": "Tele2",
    "910": "МТС", "911": "МТС", "912": "МТС", "913": "МТС", "914": "МТС",
    "915": "МТС", "916": "МТС", "917": "МТС", "918": "МТС", "919": "МТС",
    "920": "МегаФон", "921": "МегаФон", "922": "МегаФон", "923": "МегаФон",
    "924": "МегаФон", "925": "МегаФон", "926": "МегаФон", "927": "МегаФон",
    "928": "МегаФон", "929": "МегаФон",
    "960": "Билайн", "961": "Билайн", "962": "Билайн", "963": "Билайн",
    "964": "Билайн", "965": "Билайн", "966": "Билайн", "967": "Билайн",
    "968": "Билайн", "969": "Билайн",
    "999": "Yota", "997": "Yota", "996": "Yota",
}

def parse_phone(phone):
    """Очистка и парсинг номера"""
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    if not cleaned.isdigit():
        return None
    if len(cleaned) < 7:
        return None
    return cleaned

def get_country(code):
    for prefix in sorted(COUNTRY_CODES.keys(), key=len, reverse=True):
        if code.startswith(prefix):
            return COUNTRY_CODES[prefix]
    return "Неизвестно"

def get_operator_ru(code):
    if len(code) >= 3:
        prefix = code[:3]
        return MOBILE_CODES_RU.get(prefix, "Неизвестный оператор")
    return "Неизвестно"

def run_phone_lookup(args):
    if not args:
        phone = input(f"{C_INFO}Введите номер телефона: {C_RESET}").strip()
    else:
        phone = args[0]
    
    cleaned = parse_phone(phone)
    if not cleaned:
        print(f"{C_ERROR}[!] Некорректный номер.{C_RESET}")
        return
    
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         📞 PHONE LOOKUP{C_RESET}")
    print(f"{C_WARNING}         Номер: {C_BRIGHT}+{cleaned}{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    print(f"{C_BRIGHT}[Основная информация]{C_RESET}")
    print(f"  ├─ Номер: +{cleaned}")
    print(f"  ├─ Длина: {len(cleaned)} цифр")
    
    # Определение страны
    country = get_country(cleaned)
    print(f"  └─ Страна: {country}")
    
    # Для РФ — оператор
    if cleaned.startswith("7") or cleaned.startswith("8"):
        local = cleaned.lstrip("78")
        if len(local) >= 10:
            operator = get_operator_ru(local)
            region_code = local[:3]
            print(f"\n{C_BRIGHT}[Россия — детали]{C_RESET}")
            print(f"  ├─ Оператор: {operator}")
            print(f"  ├─ Код региона: {region_code}")
            print(f"  └─ Номер: {local[3:]}")
    
    # Тип номера
    if cleaned.startswith("8") or cleaned.startswith("79"):
        print(f"\n{C_BRIGHT}[Тип]{C_RESET}")
        print(f"  └─ Вероятно мобильный номер")
    
    print()
