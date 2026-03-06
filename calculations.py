# Стоимость прокачки уровней (накоплением)
LEVEL_COSTS = {
    1: {"power_points": 0, "coins": 0},
    2: {"power_points": 20, "coins": 20},
    3: {"power_points": 30, "coins": 35},
    4: {"power_points": 50, "coins": 75},
    5: {"power_points": 80, "coins": 140},
    6: {"power_points": 130, "coins": 290},
    7: {"power_points": 210, "coins": 480},
    8: {"power_points": 340, "coins": 800},
    9: {"power_points": 550, "coins": 1250},
    10: {"power_points": 890, "coins": 1875},
    11: {"power_points": 1440, "coins": 2800},
}

# Стоимость БАФФИ (каждый)
BUFFI_COST = {
    "power_points": 2000,
    "coins": 1000
}

# Стоимость пассивок (звездные силы)
STAR_POWER_COST = 2000  # за штуку

# Стоимость гаджетов
GADGET_COST = 1000  # за штуку

# Гиперзаряд
HYPERCHARGE_COST = 5000

# Стоимость гирсов
GEAR_COSTS = {
    "common": 1000,    # обычные - до 6 шт
    "epic": 1500,      # эпические - до 1 шт
    "mythic": 2000,    # мифические - до 1 шт
}

# Максимальное количество гирсов
GEAR_MAX = {
    "common": 6,
    "epic": 1,
    "mythic": 1
}

def calculate_upgrade(brawler: str, from_level: int, to_level: int, 
                     gadgets: int = 0, gears: dict = None, 
                     star_powers: int = 0, hypercharge: str = "none",
                     gadget_buffi: int = 0, star_buffi: int = 0, hyper_buffi: int = 0):
    """
    Расчет ресурсов для прокачки бойца
    hypercharge: "none" - нет, "has" - уже есть, "buy" - купит
    """
    if gears is None:
        gears = {"common": 0, "epic": 0, "mythic": 0}
    
    # Расчет уровней
    coins_needed = 0
    power_points_needed = 0
    
    for level in range(from_level + 1, to_level + 1):
        if level in LEVEL_COSTS:
            coins_needed += LEVEL_COSTS[level]["coins"]
            power_points_needed += LEVEL_COSTS[level]["power_points"]
    
    # Гаджеты (доступны с 7 уровня)
    coins_needed += gadgets * GADGET_COST
    
    # Пассивки (доступны с 9 уровня)
    coins_needed += star_powers * STAR_POWER_COST
    
    # Гиперзаряд
    if hypercharge == "buy":
        coins_needed += HYPERCHARGE_COST
    
    # Гирсы (доступны с 8 уровня)
    gears_coins = 0
    for gear_type, count in gears.items():
        if gear_type in GEAR_COSTS:
            gears_coins += GEAR_COSTS[gear_type] * count
    coins_needed += gears_coins
    
    # БАФФИ (три вида)
    total_buffi = gadget_buffi + star_buffi + hyper_buffi
    coins_needed += total_buffi * BUFFI_COST["coins"]
    power_points_needed += total_buffi * BUFFI_COST["power_points"]
    
    return {
        "brawler": brawler,
        "from_level": from_level,
        "to_level": to_level,
        "coins": coins_needed,
        "power_points": power_points_needed,
        "details": {
            "gadgets": gadgets,
            "star_powers": star_powers,
            "hypercharge": hypercharge,
            "gears": gears,
            "gadget_buffi": gadget_buffi,
            "star_buffi": star_buffi,
            "hyper_buffi": hyper_buffi
        }
    }

def format_result(result: dict) -> str:
    """Форматирование результата"""
    text = f"📊 **РЕЗУЛЬТАТ**\n\n"
    text += f"👤 **{result['brawler']}**\n"
    text += f"📈 {result['from_level']} → {result['to_level']}\n\n"
    
    text += f"💰 **Монеты:** {result['coins']:,}\n".replace(",", " ")
    text += f"💪 **Очки силы:** {result['power_points']:,}\n".replace(",", " ")
    
    details = result['details']
    text += "\n📋 **Детали:**\n"
    
    if details['gadgets'] > 0:
        text += f"• Гаджеты: {details['gadgets']} шт\n"
    if details['star_powers'] > 0:
        text += f"• Пассивки: {details['star_powers']} шт\n"
    if details['hypercharge'] == "buy":
        text += f"• Гиперзаряд: куплен\n"
    elif details['hypercharge'] == "has":
        text += f"• Гиперзаряд: уже есть\n"
    
    gears = details['gears']
    if gears.get('common', 0) > 0:
        text += f"• Обычные гирсы: {gears['common']} шт\n"
    if gears.get('epic', 0) > 0:
        text += f"• Эпические гирсы: {gears['epic']} шт\n"
    if gears.get('mythic', 0) > 0:
        text += f"• Мифические гирсы: {gears['mythic']} шт\n"
    
    if details['gadget_buffi'] > 0:
        text += f"• Гаджетный БАФФИ: {details['gadget_buffi']} шт\n"
    if details['star_buffi'] > 0:
        text += f"• Звездный БАФФИ: {details['star_buffi']} шт\n"
    if details['hyper_buffi'] > 0:
        text += f"• Гиперзарядный БАФФИ: {details['hyper_buffi']} шт\n"
    
    return text
