from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from brawlers_data import BRAWLERS, ALL_BRAWLERS
from calculations import GEAR_MAX

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
        [InlineKeyboardButton(text="👤 Шелли", callback_data="brawler_Шелли")],  # Шелли отдельно
        [InlineKeyboardButton(text="Редкие", callback_data="rarity_rare")],
        [InlineKeyboardButton(text="Сверхредкие", callback_data="rarity_super_rare")],
        [InlineKeyboardButton(text="Эпические", callback_data="rarity_epic")],
        [InlineKeyboardButton(text="Мифические", callback_data="rarity_mythic")],
        [InlineKeyboardButton(text="Легендарные", callback_data="rarity_legendary")],
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
                builder.button(text=brawler, callback_data=f"brawler_{brawler}")
    else:
        # Все бойцы с сортировкой по редкости
        rarity_order = {
            "common": 1,
            "rare": 2,
            "super_rare": 3,
            "epic": 4,
            "mythic": 5,
            "legendary": 6,
            "ultra_legendary": 7
        }
        
        sorted_brawlers = sorted(ALL_BRAWLERS, 
                               key=lambda x: rarity_order.get(BRAWLERS[x]["rarity"], 99))
        
        for brawler in sorted_brawlers:
            builder.button(text=brawler, callback_data=f"brawler_{brawler}")
    
    builder.adjust(2)
    
    rows = builder.export()
    rows.append([InlineKeyboardButton(text="🔙 Назад к редкости", callback_data="back_to_rarity")])
    
    return InlineKeyboardMarkup(inline_keyboard=rows)

def get_back_keyboard():
    """Кнопка 'Назад'"""
    buttons = [
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# === КЛАВИАТУРЫ ДЛЯ УЛУЧШЕНИЙ ===

def get_gadgets_keyboard(brawler: str, from_level: int, to_level: int, current: int = 0):
    """Клавиатура для выбора гаджетов"""
    buttons = [
        [
            InlineKeyboardButton(text="➖", callback_data=f"gadget_minus_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text=f"🎮 Гаджеты: {current}/2", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"gadget_plus_{brawler}_{from_level}_{to_level}")
        ],
        [
            InlineKeyboardButton(text="✅ Готово", callback_data=f"gadget_done_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text="❌ Сбросить", callback_data=f"gadget_reset_{brawler}_{from_level}_{to_level}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_star_powers_keyboard(brawler: str, from_level: int, to_level: int, current: int = 0):
    """Клавиатура для выбора пассивок"""
    buttons = [
        [
            InlineKeyboardButton(text="➖", callback_data=f"sp_minus_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text=f"⭐ Пассивки: {current}/2", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"sp_plus_{brawler}_{from_level}_{to_level}")
        ],
        [
            InlineKeyboardButton(text="✅ Готово", callback_data=f"sp_done_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text="❌ Сбросить", callback_data=f"sp_reset_{brawler}_{from_level}_{to_level}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_gears_keyboard(brawler: str, from_level: int, to_level: int, current_gears: dict = None):
    """Клавиатура для выбора гирсов"""
    from brawlers_data import get_available_gears
    
    if current_gears is None:
        current_gears = {"common": 0, "epic": 0, "mythic": 0}
    
    available = get_available_gears(brawler)
    buttons = []
    
    # Обычные гирсы - макс 6
    if "common" in available:
        buttons.append([
            InlineKeyboardButton(text="➖", callback_data=f"gear_minus_common_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text=f"⚙️ Обычные: {current_gears['common']}/6", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"gear_plus_common_{brawler}_{from_level}_{to_level}")
        ])
    
    # Эпические гирсы - макс 1
    if "epic" in available:
        buttons.append([
            InlineKeyboardButton(text="➖", callback_data=f"gear_minus_epic_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text=f"⚡ Эпические: {current_gears['epic']}/1", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"gear_plus_epic_{brawler}_{from_level}_{to_level}")
        ])
    
    # Мифические гирсы - макс 1
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

def get_hypercharge_keyboard(brawler: str, from_level: int, to_level: int):
    """Клавиатура для гиперзаряда"""
    buttons = [
        [
            InlineKeyboardButton(text="❌ Нет", callback_data=f"hyper_none_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text="✅ Уже есть", callback_data=f"hyper_has_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text="💰 Куплю", callback_data=f"hyper_buy_{brawler}_{from_level}_{to_level}")
        ],
        [
            InlineKeyboardButton(text="⏩ Далее", callback_data=f"hyper_done_{brawler}_{from_level}_{to_level}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_buffi_keyboard(brawler: str, from_level: int, to_level: int, 
                       gadget: int = 0, star: int = 0, hyper: int = 0):
    """Клавиатура для БАФФИ (макс 1 каждого вида)"""
    buttons = []
    
    # Гаджетный баффи (доступен с 7 уровня)
    if to_level >= 7:
        buttons.append([
            InlineKeyboardButton(text="➖", callback_data=f"buffi_gadget_minus_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text=f"🔧 Гаджетный БАФФИ: {gadget}/1", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"buffi_gadget_plus_{brawler}_{from_level}_{to_level}")
        ])
    
    # Звездный баффи (доступен с 9 уровня)
    if to_level >= 9:
        buttons.append([
            InlineKeyboardButton(text="➖", callback_data=f"buffi_star_minus_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text=f"✨ Звездный БАФФИ: {star}/1", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"buffi_star_plus_{brawler}_{from_level}_{to_level}")
        ])
    
    # Гиперзарядный баффи (доступен с 11 уровня)
    if to_level >= 11:
        buttons.append([
            InlineKeyboardButton(text="➖", callback_data=f"buffi_hyper_minus_{brawler}_{from_level}_{to_level}"),
            InlineKeyboardButton(text=f"🔥 Гиперзарядный БАФФИ: {hyper}/1", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"buffi_hyper_plus_{brawler}_{from_level}_{to_level}")
        ])
    
    # Кнопки управления
    buttons.append([
        InlineKeyboardButton(text="✅ Готово", callback_data=f"buffi_done_{brawler}_{from_level}_{to_level}"),
        InlineKeyboardButton(text="❌ Сбросить все", callback_data=f"buffi_reset_{brawler}_{from_level}_{to_level}")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_level_selection_keyboard(brawler: str, from_level: int):
    """Клавиатура для выбора целевого уровня"""
    buttons = []
    row = []
    
    for level in range(from_level + 1, 12):
        row.append(InlineKeyboardButton(text=str(level), callback_data=f"to_{level}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад к выбору бойца", callback_data="back_to_brawlers")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
