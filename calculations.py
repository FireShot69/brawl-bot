# Стоимость прокачки уровней (накоплением) - тратятся ОЧКИ СИЛЫ и МОНЕТЫ
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

# Стоимость БАФФОВ (отдельные улучшения) - тратятся ОЧКИ СИЛЫ и МОНЕТЫ
BUFF_COSTS = {
    1: {"power_points": 2000, "coins": 1000},  # первый бафф
    2: {"power_points": 4000, "coins": 2000},  # второй бафф
    3: {"power_points": 6000, "coins": 3000},  # третий бафф
}

# Стоимость пассивок (звездные силы) - только МОНЕТЫ
STAR_POWER_COST = 2000  # за штуку

# Стоимость гаджетов - только МОНЕТЫ
GADGET_COST = 1000  # за штуку

# Гиперзаряд - только МОНЕТЫ
HYPERCHARGE_COST = 5000

# Стоимость гирсов - только МОНЕТЫ
GEAR_COSTS = {
    "common": 1000,    # обычные
    "epic": 1500,      # эпические
    "mythic": 2000,    # мифические
}

def calculate_upgrade(brawler: str, from_level: int, to_level: int, 
                     buffs: int = 0, star_powers: int = 0, 
                     gadgets: int = 0, hypercharge: bool = False,
                     gears: dict = None):
    """
    Расчет ресурсов для прокачки бойца
    """
    if gears is None:
        gears = {"common": 0, "epic": 0, "mythic": 0}
    
    # 1. РАСЧЕТ УРОВНЕЙ (очки силы + монеты)
    coins_needed = 0
    power_points_needed = 0
    
    for level in range(from_level + 1, to_level + 1):
        if level in LEVEL_COSTS:
            coins_needed += LEVEL_COSTS[level]["coins"]
            power_points_needed += LEVEL_COSTS[level]["power_points"]
    
    # 2. РАСЧЕТ БАФФОВ (очки силы + монеты)
    buffs_power_points = 0
    buffs_coins = 0
    if buffs > 0:
        for i in range(1, buffs + 1):
            if i in BUFF_COSTS:
                buffs_coins += BUFF_COSTS[i]["coins"]
                buffs_power_points += BUFF_COSTS[i]["power_points"]
    
    # 3. РАСЧЕТ ПАССИВОК (только монеты)
    star_powers_coins = star_powers * STAR_POWER_COST
    
    # 4. РАСЧЕТ ГАДЖЕТОВ (только монеты)
    gadgets_coins = gadgets * GADGET_COST
    
    # 5. ГИПЕРЗАРЯД (только монеты)
    hypercharge_coins = HYPERCHARGE_COST if hypercharge else 0
    
    # 6. РАСЧЕТ ГИРСОВ (только монеты)
    gears_coins = 0
    for gear_type, count in gears.items():
        if gear_type in GEAR_COSTS:
            gears_coins += GEAR_COSTS[gear_type] * count
    
    # Суммируем всё
    total_coins = coins_needed + buffs_coins + star_powers_coins + gadgets_coins + hypercharge_coins + gears_coins
    total_power_points = power_points_needed + buffs_power_points
    
    return {
        "brawler": brawler,
        "from_level": from_level,
        "to_level": to_level,
        "coins": total_coins,
        "power_points": total_power_points,
        # Детализация для уровней
        "levels": {
            "coins": coins_needed,
            "power_points": power_points_needed
        },
        # Детализация для баффов
        "buffs": {
            "count": buffs,
            "coins": buffs_coins,
            "power_points": buffs_power_points
        },
        # Остальные улучшения
        "star_powers": star_powers,
        "gadgets": gadgets,
        "hypercharge": hypercharge,
        "gears": gears,
    }

def format_result(result: dict) -> str:
    """Форматирование результата для вывода"""
    text = f"📊 **РЕЗУЛЬТАТ РАСЧЕТА**\n\n"
    text += f"👤 Боец: **{result['brawler']}**\n"
    text += f"📈 Прокачка: {result['from_level']} → {result['to_level']} уровень\n\n"
    
    text += f"💰 **ВСЕГО МОНЕТ:** {result['coins']:,}\n".replace(",", " ")
    text += f"💪 **ВСЕГО ОЧКОВ СИЛЫ:** {result['power_points']:,}\n".replace(",", " ")
    
    text += "\n📋 **ДЕТАЛИ:**\n"
    
    # Уровни
    text += f"• Уровни: {result['levels']['coins']:,} монет + {result['levels']['power_points']:,} очков силы\n".replace(",", " ")
    
    # Баффы
    if result['buffs']['count'] > 0:
        text += f"• Баффы ({result['buffs']['count']} шт): {result['buffs']['coins']:,} монет + {result['buffs']['power_points']:,} очков силы\n".replace(",", " ")
    
    # Пассивки
    if result['star_powers'] > 0:
        text += f"• Пассивки: {result['star_powers'] * STAR_POWER_COST:,} монет\n".replace(",", " ")
    
    # Гаджеты
    if result['gadgets'] > 0:
        text += f"• Гаджеты: {result['gadgets'] * GADGET_COST:,} монет\n".replace(",", " ")
    
    # Гиперзаряд
    if result['hypercharge']:
        text += f"• Гиперзаряд: {HYPERCHARGE_COST:,} монет\n".replace(",", " ")
    
    # Гирсы
    gears = result['gears']
    if gears.get('common', 0) > 0:
        text += f"• Обычные гирсы: {gears['common'] * GEAR_COSTS['common']:,} монет\n".replace(",", " ")
    if gears.get('epic', 0) > 0:
        text += f"• Эпические гирсы: {gears['epic'] * GEAR_COSTS['epic']:,} монет\n".replace(",", " ")
    if gears.get('mythic', 0) > 0:
        text += f"• Мифические гирсы: {gears['mythic'] * GEAR_COSTS['mythic']:,} монет\n".replace(",", " ")
    
    return text