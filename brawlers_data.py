# Словарь с редкостью бойцов (только rarity, color больше не нужен)
BRAWLERS = {
    # Шелли отдельно
    "Шелли": {"rarity": "common"},
    
    # Rare (редкие)
    "Нита": {"rarity": "rare", "epic_gear": True},
    "Кольт": {"rarity": "rare", "epic_gear": True},
    "Булл": {"rarity": "rare"},
    "Брок": {"rarity": "rare", "epic_gear": True},
    "Эль Примо": {"rarity": "rare", "epic_gear": True},
    "Барли": {"rarity": "rare"},
    "Поко": {"rarity": "rare"},
    "Роза": {"rarity": "rare"},
    
    # Super Rare (сверхредкие)
    "Джесси": {"rarity": "super_rare", "epic_gear": True},
    "Динамайк": {"rarity": "super_rare"},
    "Тик": {"rarity": "super_rare", "mythic_gear": True},
    "8-Бит": {"rarity": "super_rare", "epic_gear": True},
    "Рико": {"rarity": "super_rare", "epic_gear": True},
    "Дэррил": {"rarity": "super_rare"},
    "Пенни": {"rarity": "super_rare", "epic_gear": True},
    "Карл": {"rarity": "super_rare"},
    "Джеки": {"rarity": "super_rare", "epic_gear": True},
    "Гас": {"rarity": "super_rare"},
    
    # Epic (эпические)
    "Бо": {"rarity": "epic"},
    "Эмз": {"rarity": "epic"},
    "Сту": {"rarity": "epic"},
    "Пайпер": {"rarity": "epic"},
    "Пэм": {"rarity": "epic", "mythic_gear": True},
    "Фрэнк": {"rarity": "epic"},
    "Биби": {"rarity": "epic"},
    "Беа": {"rarity": "epic"},
    "Нани": {"rarity": "epic", "epic_gear": True},
    "Эдгар": {"rarity": "epic", "epic_gear": True},
    "Грифф": {"rarity": "epic", "epic_gear": True},
    "Гром": {"rarity": "epic"},
    "Бонни": {"rarity": "epic", "epic_gear": True},
    "Гейл": {"rarity": "epic"},
    "Колетт": {"rarity": "epic"},
    "Белль": {"rarity": "epic", "epic_gear": True},
    "Эш": {"rarity": "epic", "epic_gear": True},
    "Лола": {"rarity": "epic", "epic_gear": True},
    "Сэм": {"rarity": "epic"},
    "Мэнди": {"rarity": "epic"},
    "Мэйси": {"rarity": "epic"},
    "Хэнк": {"rarity": "epic"},
    "Перл": {"rarity": "epic"},
    "Ларри и Лори": {"rarity": "epic"},
    "Анджело": {"rarity": "epic"},
    "Берри": {"rarity": "epic"},
    "Шейд": {"rarity": "epic"},
    "Мэпл": {"rarity": "epic"},
    "Транк": {"rarity": "epic"},
    
    # Mythic (мифические)
    "Мортис": {"rarity": "mythic"},
    "Тара": {"rarity": "mythic", "epic_gear": True},
    "Джин": {"rarity": "mythic", "mythic_gear": True},
    "Макс": {"rarity": "mythic"},
    "Мистер П": {"rarity": "mythic", "epic_gear": True},
    "Спраут": {"rarity": "mythic", "epic_gear": True},
    "Байрон": {"rarity": "mythic"},
    "Сквик": {"rarity": "mythic"},
    "Лу": {"rarity": "mythic", "epic_gear": True},
    "Гавс": {"rarity": "mythic"},
    "Базз": {"rarity": "mythic"},
    "Фэнг": {"rarity": "mythic"},
    "Ева": {"rarity": "mythic", "epic_gear": True, "mythic_gear": True},
    "Джанет": {"rarity": "mythic"},
    "Отис": {"rarity": "mythic", "epic_gear": True},
    "Бастер": {"rarity": "mythic"},
    "Грей": {"rarity": "mythic"},
    "Р-Т": {"rarity": "mythic"},
    "Виллоу": {"rarity": "mythic"},
    "Даг": {"rarity": "mythic"},
    "Чак": {"rarity": "mythic"},
    "Чарли": {"rarity": "mythic"},
    "Мико": {"rarity": "mythic"},
    "Мелоди": {"rarity": "mythic"},
    "Лили": {"rarity": "mythic"},
    "Клэнси": {"rarity": "mythic"},
    "Мо": {"rarity": "mythic"},
    "Джуджу": {"rarity": "mythic"},
    "Олли": {"rarity": "mythic"},
    "Луми": {"rarity": "mythic"},
    "Финкс": {"rarity": "mythic"},
    "Джэ Ён": {"rarity": "mythic"},
    "Алли": {"rarity": "mythic"},
    "Глоуберт": {"rarity": "mythic"},
    "Джиджи": {"rarity": "mythic"},
    "Мина": {"rarity": "mythic"},
    "Зигги": {"rarity": "mythic"},
    
    # Legendary (легендарные)
    "Спайк": {"rarity": "legendary"},
    "Ворон": {"rarity": "legendary"},
    "Леон": {"rarity": "legendary"},
    "Сэнди": {"rarity": "legendary", "mythic_gear": True},
    "Амбер": {"rarity": "legendary", "epic_gear": True, "mythic_gear": True},
    "Мэг": {"rarity": "legendary"},
    "Вольт": {"rarity": "legendary"},
    "Честер": {"rarity": "legendary"},
    "Корделиус": {"rarity": "legendary"},
    "Кит": {"rarity": "legendary"},
    "Драко": {"rarity": "legendary"},
    "Кэндзи": {"rarity": "legendary"},
    "Пирс": {"rarity": "legendary"},
    
    # Ultralegendary (ультралегендарные)
    "Кадзэ": {"rarity": "ultra_legendary"},
    "Сириус": {"rarity": "ultra_legendary"},
}

# Для удобства - список всех бойцов
ALL_BRAWLERS = list(BRAWLERS.keys())

GEAR_MAX = {
    "common": 6,
    "epic": 1,
    "mythic": 1
}

RARITY_EMOJI = {
    "ultra_legendary": "⭐",
}

# Стоимость гирсов (для calculations.py)
GEAR_COSTS = {
    "common": 1000,
    "epic": 1500,
    "mythic": 2000,
}

# Функция для проверки доступности гирсов
def get_available_gears(brawler: str):
    """Возвращает список доступных гирсов для бойца"""
    available = ["common"]  # обычные есть у всех
    
    brawler_data = BRAWLERS.get(brawler, {})
    if brawler_data.get("epic_gear"):
        available.append("epic")
    if brawler_data.get("mythic_gear"):
        available.append("mythic")
    
    return available

""" 
Шелли (начальный)

редкие:
нита, кольт, булл, брок, эль примо, барли, поко, роза

сверхредкие:
джесси, динамайк, тик, 8-бит, рико, дэррил, пенни, карл, джеки, гас

эпические:
бо, эмз, сту, пайпер, пэм, фрэнк, биби, беа, нани, эдгар, грифф, гром, бонни, гейл,
колетт, белль, эш, лола, сэм, мэнди, мэйси, хэнк, перл, Ларри и Лори, анджело, Берри,
шейд, мипл, транк

мифические;
мортис, тара, джин, макс, мистер пи, спраут, байрон, скуик, лу, гавс, базз, фэнг,
ева, джанет, отис, бастер, грей, р-т, виллоу, даг, чак, чарли, мико, мелоди, 
лили, клэнси, мо, джуджу, олли, луми, финкс, джэ ён, алли, глоуберт, джиджи, мина, зигги

легендарные:

спайк, ворон, леон, сэнди, амбер, мэг, вольт, честер, корделиус, кит, драко, кэндзи, пирс

ультралегендарные:
кадзэ
сириус

"""
