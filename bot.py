import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from keyboards import *
from keyboards import (
    get_main_menu_keyboard,
    get_rarity_filter_keyboard,
    get_brawlers_by_rarity,
    get_back_keyboard,
    get_buffs_keyboard,
    get_star_powers_keyboard,
    get_gadgets_keyboard,
    get_hypercharge_keyboard,
    get_gears_keyboard,
    get_level_selection_keyboard
)
from calculations import calculate_upgrade, format_result
from brawlers_data import BRAWLERS, RARITY_EMOJI

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Состояния для диалога
class Form(StatesGroup):
    choosing_brawler = State()
    choosing_from_level = State()
    choosing_to_level = State()
    choosing_buffs = State()           # очки силы
    choosing_star_powers = State()     # пассивки
    choosing_gadgets = State()         # гаджеты
    choosing_hypercharge = State()     # гиперзаряд
    choosing_gears = State()           # гирсы

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 **Привет! Я Brawl Stars калькулятор!**\n\n"
        "Я помогу тебе рассчитать ресурсы для прокачки бойцов.\n"
        "Выбери действие:",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )

# Команда /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "❓ **Как пользоваться ботом:**\n\n"
        "1. Нажми 'Рассчитать прокачку'\n"
        "2. Выбери бойца\n"
        "3. Укажи уровни\n"
        "4. Получи результат!",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )

# Фильтр по редкости
@dp.callback_query(lambda c: c.data.startswith('rarity_'))
async def process_rarity_filter(callback: types.CallbackQuery, state: FSMContext):
    rarity = callback.data.replace('rarity_', '')
    
    if rarity == "all":
        keyboard = get_brawlers_by_rarity("all")
        await callback.message.edit_text(
            "📋 **Все бойцы:**",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    else:
        # Получаем русское название редкости
        rarity_names = {
            "starter": "Начальные",
            "rare": "Редкие",
            "super_rare": "Сверхредкие",
            "epic": "Эпические",
            "mythic": "Мифические",
            "legendary": "Легендарные",
            "ultra_legendary": "Ультралегендарные"
        }
        
        emoji = RARITY_EMOJI.get(rarity, "⚪")
        keyboard = get_brawlers_by_rarity(rarity)
        
        await callback.message.edit_text(
            f"{emoji} **{rarity_names.get(rarity, rarity)} бойцы:**",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    
    await state.set_state(Form.choosing_brawler)
    await callback.answer()

# Кнопка "Назад к редкости"
@dp.callback_query(lambda c: c.data == "back_to_rarity")
async def back_to_rarity(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🔍 **Выбери редкость бойца:**",
        reply_markup=get_rarity_filter_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

# Обновленный process_menu для раздела calculate
@dp.callback_query(lambda c: c.data.startswith('menu_'))
async def process_menu(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split('_')[1]
    
    if action == "calculate":
        await callback.message.edit_text(
            "🔍 **Выбери редкость бойца:**\n\n"
            "Можешь отфильтровать по редкости или посмотреть всех:",
            reply_markup=get_rarity_filter_keyboard(),
            parse_mode="Markdown"
        )
    
    elif action == "resources":
        await callback.message.edit_text(
            "💰 **Функция в разработке!**\n"
            "Скоро здесь можно будет сохранять свои ресурсы.",
            reply_markup=get_back_keyboard(),
            parse_mode="Markdown"
        )
    
    elif action == "progress":
        await callback.message.edit_text(
            "📈 **Функция в разработке!**\n"
            "Скоро здесь будет твой прогресс прокачки.",
            reply_markup=get_back_keyboard(),
            parse_mode="Markdown"
        )
    
    elif action == "help":
        await callback.message.edit_text(
            "❓ **Как пользоваться ботом:**\n\n"
            "1. Нажми 'Рассчитать прокачку'\n"
            "2. Выбери редкость или смотри всех\n"
            "3. Выбери бойца\n"
            "4. Укажи уровни\n"
            "5. Получи результат!\n\n"
            "Остальные функции скоро появятся!",
            reply_markup=get_back_keyboard(),
            parse_mode="Markdown"
        )
    
    await callback.answer()

# Выбор бойца
@dp.callback_query(lambda c: c.data.startswith('brawler_'))
async def process_brawler(callback: types.CallbackQuery, state: FSMContext):
    brawler = callback.data.replace('brawler_', '')
    
    # Сохраняем бойца в состояние
    await state.update_data(selected_brawler=brawler)
    
    # Создаем кнопки для выбора уровня (1-11)
    buttons = []
    row = []
    for level in range(1, 12):
        row.append(InlineKeyboardButton(text=str(level), callback_data=f"from_{level}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    # Добавляем кнопку "Назад"
    buttons.append([InlineKeyboardButton(text="🔙 Назад к выбору бойца", callback_data="back_to_brawlers")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(
        f"Выбран боец: **{brawler}**\n"
        f"Какой сейчас уровень?",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await state.set_state(Form.choosing_from_level)
    await callback.answer()

# Выбор текущего уровня
@dp.callback_query(lambda c: c.data.startswith('from_'))
async def process_from_level(callback: types.CallbackQuery, state: FSMContext):
    level = int(callback.data.replace('from_', ''))
    
    await state.update_data(from_level=level)
    
    # Получаем данные
    data = await state.get_data()
    
    # Проверяем, есть ли selected_brawler
    if 'selected_brawler' not in data:
        # Если нет - возвращаем к выбору
        await callback.message.edit_text(
            "❌ Ошибка! Пожалуйста, выбери бойца заново.",
            reply_markup=get_rarity_filter_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()
        await callback.answer()
        return
    
    brawler = data['selected_brawler']
    
    # Проверка на максимальный уровень
    if level == 11:
        await callback.message.edit_text(
            f"⚠️ **{brawler} уже на максимальном уровне!**\n\n"
            f"Текущий уровень: {level}\n"
            f"Максимальный уровень: 11\n\n"
            f"Прокачка не требуется. Может, прокачаешь другого бойца?",
            reply_markup=get_main_menu_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()
        await callback.answer()
        return
    
    # Создаем кнопки для выбора целевого уровня (только уровни выше текущего)
    buttons = []
    row = []
    for target_level in range(level + 1, 12):  # начинаем с level+1
        row.append(InlineKeyboardButton(text=str(target_level), callback_data=f"to_{target_level}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    # Добавляем кнопку "Назад"
    buttons.append([InlineKeyboardButton(text="🔙 Назад к выбору бойца", callback_data="back_to_brawlers")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(
        f"Боец: **{brawler}**\n"
        f"Текущий уровень: {level}\n\n"
        f"До какого уровня прокачать?",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await state.set_state(Form.choosing_to_level)
    await callback.answer()

# Выбор целевого уровня и расчет

@dp.callback_query(lambda c: c.data.startswith('to_'))
async def process_to_level(callback: types.CallbackQuery, state: FSMContext):
    to_level = int(callback.data.replace('to_', ''))
    
    data = await state.get_data()
    brawler = data.get('selected_brawler', '')
    from_level = data.get('from_level', 0)
    
    if not brawler or not from_level:
        await callback.message.edit_text(
            "❌ Ошибка! Пожалуйста, начни заново.",
            reply_markup=get_rarity_filter_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()
        await callback.answer()
        return
    
    # Проверка на максимальный уровень
    if from_level == 11:
        await callback.message.edit_text(
            f"⚠️ **{brawler} уже на максимальном уровне!**\n\n"
            f"Текущий уровень: {from_level}\n"
            f"Максимальный уровень: 11\n\n"
            f"Прокачка не требуется. Может, прокачаешь другого бойца?",
            reply_markup=get_main_menu_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()
        await callback.answer()
        return
    
    # Проверка на одинаковые уровни
    if from_level == to_level:
        await callback.message.edit_text(
            f"⚠️ **Ты выбрал одинаковые уровни!**\n\n"
            f"Боец: **{brawler}**\n"
            f"Текущий уровень: {from_level}\n"
            f"Целевой уровень: {to_level}\n\n"
            f"Выбери другой целевой уровень:",
            reply_markup=get_level_selection_keyboard(brawler, from_level),
            parse_mode="Markdown"
        )
        await callback.answer()
        return
    
    # Проверка на корректность уровней
    if to_level < from_level:
        await callback.message.edit_text(
            f"❌ **Ошибка!**\n\n"
            f"Целевой уровень ({to_level}) не может быть меньше текущего ({from_level}).\n\n"
            f"Выбери правильный целевой уровень:",
            reply_markup=get_level_selection_keyboard(brawler, from_level),
            parse_mode="Markdown"
        )
        await callback.answer()
        return
    
    # Если все проверки пройдены - переходим к выбору баффов
    await state.update_data(buffs=0)  # инициализируем
    await callback.message.edit_text(
        f"**{brawler}** {from_level} → {to_level}\n\n"
        f"Сколько баффов добавить?\n\n"
        f"(Баффы дают +2000 очков силы и +1000 монет каждый)",
        reply_markup=get_buffs_keyboard(brawler, from_level, to_level, 0),
        parse_mode="Markdown"
    )
    await state.set_state(Form.choosing_buffs)
    await callback.answer()

# Кнопка "Назад"
@dp.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "👋 **Главное меню**\n\n"
        "Выбери действие:",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

# Назад к выбору бойца
@dp.callback_query(lambda c: c.data == "back_to_brawlers")
async def back_to_brawlers(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "🔍 **Выбери редкость бойца:**",
        reply_markup=get_rarity_filter_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

# Выбор баффов
@dp.callback_query(lambda c: c.data.startswith('buffs_'))
async def process_buffs(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    action = data[1]  # plus, minus, done, reset
    brawler = data[2]
    from_level = int(data[3])
    to_level = int(data[4])
    
    state_data = await state.get_data()
    current_buffs = state_data.get('buffs', 0)
    
    if action == "done":
        # Переходим к выбору пассивок
        await callback.message.edit_text(
            f"**{brawler}** {from_level} → {to_level}\n"
            f"✅ Баффы: {current_buffs}\n\n"
            f"Сколько пассивок добавить?",
            reply_markup=get_star_powers_keyboard(brawler, from_level, to_level, 0),
            parse_mode="Markdown"
        )
        await state.set_state(Form.choosing_star_powers)
        await callback.answer()
        return
    
    elif action == "reset":
        current_buffs = 0
    
    elif action == "plus":
        if current_buffs < 3:
            current_buffs += 1
    
    elif action == "minus":
        if current_buffs > 0:
            current_buffs -= 1
    
    await state.update_data(buffs=current_buffs)
    
    await callback.message.edit_text(
        f"**{brawler}** {from_level} → {to_level}\n\n"
        f"Сколько баффов добавить?\n"
        f"(Баффы дают +2000 очков силы и +1000 монет каждый)",
        reply_markup=get_buffs_keyboard(brawler, from_level, to_level, current_buffs),
        parse_mode="Markdown"
    )
    await callback.answer()

# Выбор пассивок
@dp.callback_query(lambda c: c.data.startswith('sp_'))
async def process_star_powers(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    action = data[1]  # plus, minus, done, reset
    brawler = data[2]
    from_level = int(data[3])
    to_level = int(data[4])
    
    state_data = await state.get_data()
    current_sp = state_data.get('star_powers', 0)
    
    if action == "done":
        # Переходим к выбору гаджетов
        await callback.message.edit_text(
            f"**{brawler}** {from_level} → {to_level}\n"
            f"✅ Пассивки: {current_sp}\n\n"
            f"Сколько гаджетов добавить?",
            reply_markup=get_gadgets_keyboard(brawler, from_level, to_level, 0),
            parse_mode="Markdown"
        )
        await state.set_state(Form.choosing_gadgets)
        await callback.answer()
        return
    
    elif action == "reset":
        current_sp = 0
    
    elif action == "plus":
        if current_sp < 2:
            current_sp += 1
    
    elif action == "minus":
        if current_sp > 0:
            current_sp -= 1
    
    await state.update_data(star_powers=current_sp)
    
    await callback.message.edit_text(
        f"**{brawler}** {from_level} → {to_level}\n"
        f"✅ Пассивки: {current_sp}\n\n"
        f"Сколько пассивок добавить? (макс 2)",
        reply_markup=get_star_powers_keyboard(brawler, from_level, to_level, current_sp),
        parse_mode="Markdown"
    )
    await callback.answer()

# Выбор гаджетов
@dp.callback_query(lambda c: c.data.startswith('gadget_'))
async def process_gadgets(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    action = data[1]  # plus, minus, done, reset
    brawler = data[2]
    from_level = int(data[3])
    to_level = int(data[4])
    
    state_data = await state.get_data()
    current_gadgets = state_data.get('gadgets', 0)
    
    if action == "done":
        # Переходим к выбору гиперзаряда
        await callback.message.edit_text(
            f"**{brawler}** {from_level} → {to_level}\n"
            f"✅ Гаджеты: {current_gadgets}\n\n"
            f"Есть гиперзаряд?",
            reply_markup=get_hypercharge_keyboard(brawler, from_level, to_level, False),
            parse_mode="Markdown"
        )
        await state.set_state(Form.choosing_hypercharge)
        await callback.answer()
        return
    
    elif action == "reset":
        current_gadgets = 0
    
    elif action == "plus":
        if current_gadgets < 2:
            current_gadgets += 1
    
    elif action == "minus":
        if current_gadgets > 0:
            current_gadgets -= 1
    
    await state.update_data(gadgets=current_gadgets)
    
    await callback.message.edit_text(
        f"**{brawler}** {from_level} → {to_level}\n"
        f"✅ Гаджеты: {current_gadgets}\n\n"
        f"Сколько гаджетов добавить? (макс 2)",
        reply_markup=get_gadgets_keyboard(brawler, from_level, to_level, current_gadgets),
        parse_mode="Markdown"
    )
    await callback.answer()

# Выбор гиперзаряда
@dp.callback_query(lambda c: c.data.startswith('hyper_'))
async def process_hypercharge(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    action = data[1]  # yes, no или skip
    brawler = data[2]
    from_level = int(data[3])
    to_level = int(data[4])
    
    if action == "yes":
        hypercharge = True
    else:
        hypercharge = False
    
    await state.update_data(hypercharge=hypercharge)
    
    # Получаем данные о гирсах из состояния или создаем новые
    state_data = await state.get_data()
    current_gears = state_data.get('gears', {"common": 0, "epic": 0, "mythic": 0})
    
    # Переходим к выбору гирсов
    await callback.message.edit_text(
        f"**{brawler}** {from_level} → {to_level}\n"
        f"✅ Гиперзаряд: {'✅' if hypercharge else '❌'}\n\n"
        f"Выбери гирсы (нажимай на кнопки, чтобы добавить):",
        reply_markup=get_gears_keyboard(brawler, from_level, to_level, current_gears),
        parse_mode="Markdown"
    )
    await state.set_state(Form.choosing_gears)
    await callback.answer()

# Выбор гирсов
@dp.callback_query(lambda c: c.data.startswith('gear_'))
async def process_gears(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    action = data[1]  # plus, minus, done, reset, skip
    gear_type = data[2] if action in ["plus", "minus"] else None
    brawler = data[3] if action in ["plus", "minus"] else data[2]
    from_level = int(data[4] if action in ["plus", "minus"] else data[3])
    to_level = int(data[5] if action in ["plus", "minus"] else data[4])
    
    state_data = await state.get_data()
    current_gears = state_data.get('gears', {"common": 0, "epic": 0, "mythic": 0})
    
    if action == "done":
        # Завершаем выбор и считаем
        await calculate_final(callback, state, brawler, from_level, to_level, state_data)
        return
    
    elif action == "skip":
        # Пропускаем гирсы
        current_gears = {"common": 0, "epic": 0, "mythic": 0}
        await state.update_data(gears=current_gears)
        await calculate_final(callback, state, brawler, from_level, to_level, state_data)
        return
    
    elif action == "reset":
        # Сбрасываем все гирсы
        current_gears = {"common": 0, "epic": 0, "mythic": 0}
        await state.update_data(gears=current_gears)
        
    elif action == "plus":
        # Увеличиваем счетчик
        max_count = 1 if gear_type == "mythic" else 2  # мифические макс 1, остальные 2
        if current_gears[gear_type] < max_count:
            current_gears[gear_type] += 1
            await state.update_data(gears=current_gears)
    
    elif action == "minus":
        # Уменьшаем счетчик
        if current_gears[gear_type] > 0:
            current_gears[gear_type] -= 1
            await state.update_data(gears=current_gears)
    
    # Получаем доступные гирсы для красивого отображения
    from brawlers_data import get_available_gears
    available = get_available_gears(brawler)
    
    # Формируем текст с эмодзи
    gears_text = ""
    if "common" in available:
        gears_text += f"  ⚙️ Обычные: {current_gears['common']}/2\n"
    if "epic" in available:
        gears_text += f"  ⚡ Эпические: {current_gears['epic']}/2\n"
    if "mythic" in available:
        gears_text += f"  💫 Мифические: {current_gears['mythic']}/1\n"
    
    # Обновляем клавиатуру
    await callback.message.edit_text(
        f"**{brawler}** {from_level} → {to_level}\n"
        f"✅ Гирсы:\n{gears_text}\n"
        f"Используй кнопки + и - чтобы добавить или убрать гирсы:",
        reply_markup=get_gears_keyboard(brawler, from_level, to_level, current_gears),
        parse_mode="Markdown"
    )
    
    await callback.answer()

# Финальный расчет
async def calculate_final(callback, state, brawler, from_level, to_level, state_data):
    # Получаем все данные
    buffs = state_data.get('buffs', 0)
    star_powers = state_data.get('star_powers', 0)
    gadgets = state_data.get('gadgets', 0)  # ← здесь должно быть gadgets
    hypercharge = state_data.get('hypercharge', False)
    gears = state_data.get('gears', {"common": 0, "epic": 0, "mythic": 0})
    
    # Рассчитываем
    result = calculate_upgrade(
        brawler, from_level, to_level,
        buffs, star_powers, gadgets, hypercharge, gears
    )
    
    result_text = format_result(result)
    
    await callback.message.edit_text(
        result_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )
    
    await state.clear()
    await callback.answer()

# Игнорирование нажатий на информационные кнопки
@dp.callback_query(lambda c: c.data == "ignore")
async def ignore_callback(callback: types.CallbackQuery):
    await callback.answer()  # просто ничего не делаем

# Запуск бота
async def main():
    print("🤖 Бот запущен! Нажми Ctrl+C для остановки")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
    
"""
сколько ресурсов надо для прокачки каждого уровня

1 уровень - 0 очков сил + 0 монет
2 уровень - 20 очков сил + 20 монет
3 уровень - 30 очков сил + 35 монет
4 уровень - 50 очков сил + 75 монет
5 уровень - 80 очков сил + 140 монет
6 уровень - 130 очков сил + 290 монет
7 уровень - 210 очков сил + 480 монет
8 уровень - 340 очков сил + 800 монет
9 уровень - 550 очков сил + 1250 монет
10 уровень - 890 очков сил + 1875 монет 
11 уровень - 1440 очков сил + 2800 монет

Баффи (1 шт) = 2000 очков сил + 1000 монет
Баффи (2 шт) = 4000 очков сил + 2000 монет
Баффи (3 шт) = 6000 очков сил + 3000 монет

важно понимать, что баффи выпадают рандомно с автомата! 

1 пассивка на бойца - 2000 монет
2 пассивки на бойца - 4000 монет

1 гаджет на бойца - 1000 монет
2 гаджета на бойца - 2000 монет

гиперзаряд - 5000 монет

Обычные гирсы - 1000 монет (щит, скорость в кустах, урон, хп, зрение, перезарядка гаджета)
Эпические - 1500 монет 
мифические - 2000 монет

Список эпических гирсов

Брок (скорость перезарядки)

Эль Примо (зарядка супера)

Джесси (сила компаньона)

8-Бит (скорость перезарядки)

Рико (скорость перезарядки)

Пенни (сила компаньона)

Джеки (зарядка супера)

Нани (зарядка супера)

Эдгар (зарядка супера)

Грифф (скорость перезарядки)

Бонни (зарядка супера)

Белль (скорость перезарядки)

Эш (зарядка супера)

Лола (скорость перезарядки)

Тара (сила компаньона)

Мистер Пи (сила компаньона)

Спраут (зарядка супера)

Лу (зарядка супера)

Ева (скорость перезарядки)

Отис (зарядка супера)

Амбер (скорость перезарядки)



Список мифических снаряжений

тик (крепкая голова)

пэм (супертурель)

джин (длинная рука)

Ева (четверняшки)

Сэнди (Изнурительная буря)

Амбер (липкое масло)

"""