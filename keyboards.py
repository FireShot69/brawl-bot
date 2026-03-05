from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from brawlers_data import BRAWLERS, ALL_BRAWLERS, RARITY_EMOJI

def get_main_menu_keyboard():
    """Главное меню"""
    buttons = [
        [InlineKeyboardButton(text="📊 Рассчитать прокачку", callback_data="menu_calculate")],
        [InlineKeyboardButton(text="💰 Мои ресурсы", callback_data="menu_resources")],
        [InlineKeyboardButton(text="📈 Мой прогресс", callback_data="menu_progress")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="menu_help")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_rarity_filter_keyboard():
    """Клавиатура с фильтром по редкости"""
    buttons = [
        [InlineKeyboardButton(text="⬜ Начальные (Starter)", callback_data="rarity_starter")],
        [InlineKeyboardButton(text="🟩 Редкие (Rare)", callback_data="rarity_rare")],
        [InlineKeyboardButton(text="🟦 Сверхредкие (Super Rare)", callback_data="rarity_super_rare")],
        [InlineKeyboardButton(text="🟪 Эпические (Epic)", callback_data="rarity_epic")],
        [InlineKeyboardButton(text="🟥 Мифические (Mythic)", callback_data="rarity_mythic")],
        [InlineKeyboardButton(text="🟨 Легендарные (Legendary)", callback_data="rarity_legendary")],
        [InlineKeyboardButton(text="⭐ Ультралегендарные", callback_data="rarity_ultra_legendary")],
        [InlineKeyboardButton(text="📋 Все бойцы", callback_data="rarity_all")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_brawlers_by_rarity(rarity: str = None):
    """Клавиатура с бойцами определенной редкости"""
    builder = InlineKeyboardBuilder()
    
    if rarity and rarity != "all":
        # Фильтруем по редкости
        for brawler in ALL_BRAWLERS:
            if BRAWLERS[brawler]["rarity"] == rarity:
                emoji = RARITY_EMOJI.get(BRAWLERS[brawler]["rarity"], "⚪")
                builder.button(text=f"{emoji} {brawler}", callback_data=f"brawler_{brawler}")
    else:
        # Все бойцы с сортировкой по редкости
        rarity_order = {
            "starter": 1,
            "rare": 2,
            "super_rare": 3,
            "epic": 4,
            "mythic": 5,
            "legendary": 6,
            "ultra_legendary": 7
        }
        
        sorted_brawlers = sorted(ALL_BRAWLERS, 
                               key=lambda x: rarity_order[BRAWLERS[x]["rarity"]])
        
        for brawler in sorted_brawlers:
            emoji = RARITY_EMOJI.get(BRAWLERS[brawler]["rarity"], "⚪")
            builder.button(text=f"{emoji} {brawler}", callback_data=f"brawler_{brawler}")
    
    builder.adjust(2)  # по 2 кнопки в ряд
    
    # Добавляем кнопку "Назад к фильтрам"
    rows = builder.export()
    rows.append([InlineKeyboardButton(text="🔙 Назад к редкости", callback_data="back_to_rarity")])
    
    return InlineKeyboardMarkup(inline_keyboard=rows)

def get_back_keyboard():
    """Кнопка 'Назад'"""
    buttons = [
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# === НОВЫЕ ФУНКЦИИ ДЛЯ УЛУЧШЕНИЙ ===

def get_buffs_keyboard(brawler: str, from_level: int, to_level: int, current_buffs: int = 0):
    """Клавиатура для выбора баффов с кнопками + и -"""
    buttons = [
        [
            InlineKeyboardButton(text="➖", callback_data=f"buffs_minus_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text=f"📊 Баффы: {current_buffs}/3", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"buffs_plus_{brawler}_{from_level}_{to_level}")
        ],
        [
            InlineKeyboardButton(text="✅ Готово", callback_data=f"buffs_done_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text="❌ Сбросить", callback_data=f"buffs_reset_{brawler}_{from_level}_{to_level}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_star_powers_keyboard(brawler: str, from_level: int, to_level: int, current_sp: int = 0):
    """Клавиатура для выбора пассивок с кнопками + и -"""
    buttons = [
        [
            InlineKeyboardButton(text="➖", callback_data=f"sp_minus_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text=f"⭐ Пассивки: {current_sp}/2", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"sp_plus_{brawler}_{from_level}_{to_level}")
        ],
        [
            InlineKeyboardButton(text="✅ Готово", callback_data=f"sp_done_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text="❌ Сбросить", callback_data=f"sp_reset_{brawler}_{from_level}_{to_level}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_gadgets_keyboard(brawler: str, from_level: int, to_level: int, current_gadgets: int = 0):
    """Клавиатура для выбора гаджетов с кнопками + и -"""
    buttons = [
        [
            InlineKeyboardButton(text="➖", callback_data=f"gadget_minus_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text=f"🎮 Гаджеты: {current_gadgets}/2", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"gadget_plus_{brawler}_{from_level}_{to_level}")
        ],
        [
            InlineKeyboardButton(text="✅ Готово", callback_data=f"gadget_done_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text="❌ Сбросить", callback_data=f"gadget_reset_{brawler}_{from_level}_{to_level}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_hypercharge_keyboard(brawler: str, from_level: int, to_level: int, current_hc: bool = False):
    """Клавиатура для выбора гиперзаряда с кнопками да/нет"""
    status = "✅ Есть" if current_hc else "❌ Нет"
    buttons = [
        [
            InlineKeyboardButton(text="✅ Да", callback_data=f"hyper_yes_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text="❌ Нет", callback_data=f"hyper_no_{brawler}_{from_level}_{to_level}")
        ],
        [
            InlineKeyboardButton(text=f"Текущий: {status}", callback_data="ignore"),
            InlineKeyboardButton(text="✅ Готово", callback_data=f"hyper_done_{brawler}_{from_level}_{to_level}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_gears_keyboard(brawler: str, from_level: int, to_level: int, current_gears: dict = None):
    """Клавиатура для выбора гирсов с кнопками + и -"""
    from brawlers_data import get_available_gears
    
    if current_gears is None:
        current_gears = {"common": 0, "epic": 0, "mythic": 0}
    
    available = get_available_gears(brawler)
    buttons = []
    
    # Обычные гирсы (есть у всех) - макс 2
    if "common" in available:
        buttons.append([
            InlineKeyboardButton(text="➖", callback_data=f"gear_minus_common_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text=f"⚙️ Обычные: {current_gears['common']}/2", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"gear_plus_common_{brawler}_{from_level}_{to_level}")
        ])
    
    # Эпические гирсы (если доступны) - макс 2
    if "epic" in available:
        buttons.append([
            InlineKeyboardButton(text="➖", callback_data=f"gear_minus_epic_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text=f"⚡ Эпические: {current_gears['epic']}/2", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"gear_plus_epic_{brawler}_{from_level}_{to_level}")
        ])
    
    # Мифические гирсы (если доступны) - макс 1
    if "mythic" in available:
        buttons.append([
            InlineKeyboardButton(text="➖", callback_data=f"gear_minus_mythic_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text=f"💫 Мифические: {current_gears['mythic']}/1", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"gear_plus_mythic_{brawler}_{from_level}_{to_level}")
        ])
    
    # Кнопки управления
    buttons.append([
        InlineKeyboardButton(text="✅ Готово", callback_data=f"gear_done_{brawler}_{from_level}_{to_level}"),
        InlineKeyboardButton(text="❌ Сбросить", callback_data=f"gear_reset_{brawler}_{from_level}_{to_level}")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_level_selection_keyboard(brawler: str, from_level: int):
    """Клавиатура для выбора целевого уровня"""
    buttons = []
    row = []
    
    # Создаем кнопки только для уровней выше текущего
    for level in range(from_level + 1, 12):
        row.append(InlineKeyboardButton(text=str(level), callback_data=f"to_{level}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    # Добавляем кнопку "Назад"
    buttons.append([InlineKeyboardButton(text="🔙 Назад к выбору бойца", callback_data="back_to_brawlers")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)