#!/usr/bin/env python3
"""
Telegram Bot для Автоломбарда
Версия с возможностью добавления объявлений через FSM
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    WebAppInfo,
    MenuButtonWebApp
)

# Импортируем наши модули
try:
    from config import BOT_TOKEN, WEBAPP_URL, is_admin, ADMIN_IDS, get_admin_info, HUGO_SITE_PATH
    from states import CarCreationStates
    from car_manager import CarManager
    from car_brands import CAR_BRANDS  # Локальный справочник марок и моделей
    from bot_functions import (
        get_start_message, get_catalog_message, get_search_message,
        get_callback_response, search_by_text, get_menu_button_config,
        get_admin_start_message, get_admin_help_message,
        FUEL_TYPES, TRANSMISSIONS, DRIVE_TYPES, BODY_TYPES, CONDITIONS
    )
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что все файлы находятся в одной папке")
    sys.exit(1)


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота
if BOT_TOKEN and BOT_TOKEN != "YOUR_BOT_TOKEN_HERE":
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    car_manager = CarManager(hugo_site_path=HUGO_SITE_PATH)
else:
    logger.error("BOT_TOKEN не установлен! Проверьте .env файл")
    sys.exit(1)


def create_keyboard_from_buttons(buttons_data):
    """Создает Telegram клавиатуру из данных кнопок"""
    keyboard = []

    for button in buttons_data:
        button_row = []

        if "web_app_url" in button:
            telegram_button = InlineKeyboardButton(
                text=button["text"],
                web_app=WebAppInfo(url=button["web_app_url"])
            )
        elif "callback_data" in button:
            telegram_button = InlineKeyboardButton(
                text=button["text"],
                callback_data=button["callback_data"]
            )
        elif "url" in button:
            telegram_button = InlineKeyboardButton(
                text=button["text"],
                url=button["url"]
            )
        else:
            continue

        button_row.append(telegram_button)
        keyboard.append(button_row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_selection_keyboard(options: list, row_width: int = 2):
    """Создает клавиатуру для выбора опций"""
    keyboard = []
    row = []

    for option in options:
        row.append(KeyboardButton(text=option))
        if len(row) >= row_width:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    # Добавляем кнопку отмены
    keyboard.append([KeyboardButton(text="❌ Отменить")])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def create_inline_keyboard(items: list, callback_prefix: str, row_width: int = 2, add_manual: bool = True):
    """Создает inline клавиатуру для выбора из списка"""
    keyboard = []
    row = []

    for item in items:
        button = InlineKeyboardButton(
            text=item,
            callback_data=f"{callback_prefix}:{item}"
        )
        row.append(button)
        if len(row) >= row_width:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    # Добавляем кнопку "Ввести вручную"
    if add_manual:
        keyboard.append([InlineKeyboardButton(
            text="✍️ Ввести вручную",
            callback_data=f"{callback_prefix}:manual"
        )])

    # Добавляем кнопку отмены
    keyboard.append([InlineKeyboardButton(
        text="❌ Отменить",
        callback_data="cancel_add_car"
    )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# ========== КОМАНДЫ ==========

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Команда /start - приветствие и главное меню"""

    # Настраиваем Web App кнопку в меню
    menu_config = get_menu_button_config()
    webapp_button = MenuButtonWebApp(
        text=menu_config["text"],
        web_app=WebAppInfo(url=menu_config["web_app_url"])
    )

    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=webapp_button
    )

    # Проверяем, является ли пользователь администратором
    if is_admin(message.from_user.id):
        message_data = get_admin_start_message(message.from_user.id)
    else:
        message_data = get_start_message()

    keyboard = create_keyboard_from_buttons(message_data["buttons"])

    await message.answer(
        message_data["text"],
        reply_markup=keyboard,
        parse_mode=message_data["parse_mode"]
    )


@dp.message(Command("catalog"))
async def cmd_catalog(message: types.Message):
    """Команда /catalog - открытие каталога"""

    message_data = get_catalog_message()
    keyboard = create_keyboard_from_buttons(message_data["buttons"])

    await message.answer(
        message_data["text"],
        reply_markup=keyboard,
        parse_mode=message_data["parse_mode"]
    )


@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    """Команда /search - быстрый поиск"""

    message_data = get_search_message()
    keyboard = create_keyboard_from_buttons(message_data["buttons"])

    await message.answer(
        message_data["text"],
        reply_markup=keyboard,
        parse_mode=message_data["parse_mode"]
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Команда /help - справка"""

    if is_admin(message.from_user.id):
        message_data = get_admin_help_message()
        keyboard = create_keyboard_from_buttons(message_data["buttons"])
        await message.answer(
            message_data["text"],
            reply_markup=keyboard,
            parse_mode=message_data["parse_mode"]
        )
    else:
        callback_data = get_callback_response("help")
        keyboard = create_keyboard_from_buttons(callback_data["buttons"])
        await message.answer(
            callback_data["text"],
            reply_markup=keyboard,
            parse_mode=callback_data["parse_mode"]
        )


@dp.message(Command("add_car"))
async def cmd_add_car(message: types.Message, state: FSMContext):
    """Команда /add_car - начало процесса добавления автомобиля (только для админов)"""

    if not is_admin(message.from_user.id):
        await message.answer(
            "⛔️ У вас нет доступа к этой команде.\n\n"
            "Эта функция доступна только администраторам.",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    await state.set_state(CarCreationStates.brand)

    # Создаем inline кнопки с марками (загружаются из API или кеша)
    brands = await get_all_brands()
    keyboard = create_inline_keyboard(brands, "brand", row_width=2)

    await message.answer(
        "➕ **Добавление нового автомобиля**\n\n"
        "🚗 Выберите марку автомобиля из списка или введите вручную:",
        parse_mode="Markdown",
        reply_markup=keyboard
    )


# ========== FSM ОБРАБОТЧИКИ ДЛЯ СОЗДАНИЯ ОБЪЯВЛЕНИЯ ==========

@dp.message(CarCreationStates.brand)
async def process_brand(message: types.Message, state: FSMContext):
    """Обработка ввода марки"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    brand_input = message.text.strip()

    # Добавляем марку в справочник, если её там нет
    if brand_input not in CAR_BRANDS:
        CAR_BRANDS[brand_input] = []
        logger.info(f"Добавлена новая марка: {brand_input}")

    await state.update_data(brand=brand_input)
    await state.set_state(CarCreationStates.model)

    await message.answer(
        f"✅ Марка: **{brand_input}**\n\n"
        f"📝 Введите модель автомобиля (например: X5, Camry, E-класс):",
        parse_mode="Markdown"
    )


@dp.message(CarCreationStates.model)
async def process_model(message: types.Message, state: FSMContext):
    """Обработка ввода модели"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    model_input = message.text.strip()

    # Получаем марку из состояния
    data = await state.get_data()
    brand = data.get('brand', '')

    # Принимаем любую модель (Dadata API не поддерживает справочник моделей)
    await state.update_data(model=model_input)
    await state.set_state(CarCreationStates.year)

    await message.answer(
        f"✅ Марка: **{brand}**\n"
        f"✅ Модель: **{model_input}**\n\n"
        f"📅 Введите год выпуска (например: 2020):",
        parse_mode="Markdown"
    )


@dp.message(CarCreationStates.year)
async def process_year(message: types.Message, state: FSMContext):
    """Обработка ввода года"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    try:
        year = int(message.text.strip())
        if year < 1990 or year > datetime.now().year + 1:
            await message.answer("❌ Некорректный год. Введите год от 1990 до текущего:")
            return
    except ValueError:
        await message.answer("❌ Введите год числом (например: 2020):")
        return

    await state.update_data(year=year)
    await state.set_state(CarCreationStates.price)

    await message.answer(
        "💰 Введите цену в рублях (например: 2500000):",
        parse_mode="Markdown"
    )


@dp.message(CarCreationStates.price)
async def process_price(message: types.Message, state: FSMContext):
    """Обработка ввода цены"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    try:
        price = int(message.text.strip().replace(" ", "").replace(",", ""))
        if price <= 0:
            await message.answer("❌ Цена должна быть положительным числом:")
            return
    except ValueError:
        await message.answer("❌ Введите цену числом (например: 2500000):")
        return

    await state.update_data(price=price)
    await state.set_state(CarCreationStates.mileage)

    await message.answer(
        "🛣 Введите пробег в километрах (например: 85000):",
        parse_mode="Markdown"
    )


@dp.message(CarCreationStates.mileage)
async def process_mileage(message: types.Message, state: FSMContext):
    """Обработка ввода пробега"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    try:
        mileage = int(message.text.strip().replace(" ", "").replace(",", ""))
        if mileage < 0:
            await message.answer("❌ Пробег не может быть отрицательным:")
            return
    except ValueError:
        await message.answer("❌ Введите пробег числом (например: 85000):")
        return

    await state.update_data(mileage=mileage)
    await state.set_state(CarCreationStates.engine_volume)

    await message.answer(
        "⚙️ Введите объем двигателя в литрах (например: 2.0):",
        parse_mode="Markdown"
    )


@dp.message(CarCreationStates.engine_volume)
async def process_engine_volume(message: types.Message, state: FSMContext):
    """Обработка ввода объема двигателя"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    try:
        engine_volume = float(message.text.strip().replace(",", "."))
        if engine_volume <= 0 or engine_volume > 10:
            await message.answer("❌ Введите корректный объем двигателя (0.5 - 10.0):")
            return
    except ValueError:
        await message.answer("❌ Введите объем двигателя числом (например: 2.0):")
        return

    await state.update_data(engine_volume=engine_volume)
    await state.set_state(CarCreationStates.fuel_type)

    keyboard = create_selection_keyboard(FUEL_TYPES, row_width=3)
    await message.answer(
        "⛽️ Выберите тип топлива:",
        reply_markup=keyboard
    )


@dp.message(CarCreationStates.fuel_type)
async def process_fuel_type(message: types.Message, state: FSMContext):
    """Обработка выбора типа топлива"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    if message.text not in FUEL_TYPES:
        await message.answer("❌ Пожалуйста, выберите тип топлива из предложенных вариантов:")
        return

    await state.update_data(fuel_type=message.text)
    await state.set_state(CarCreationStates.transmission)

    keyboard = create_selection_keyboard(TRANSMISSIONS, row_width=3)
    await message.answer(
        "🔧 Выберите коробку передач:",
        reply_markup=keyboard
    )


@dp.message(CarCreationStates.transmission)
async def process_transmission(message: types.Message, state: FSMContext):
    """Обработка выбора коробки передач"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    if message.text not in TRANSMISSIONS:
        await message.answer("❌ Пожалуйста, выберите коробку передач из предложенных вариантов:")
        return

    await state.update_data(transmission=message.text)
    await state.set_state(CarCreationStates.drive_type)

    keyboard = create_selection_keyboard(DRIVE_TYPES, row_width=3)
    await message.answer(
        "🔄 Выберите тип привода:",
        reply_markup=keyboard
    )


@dp.message(CarCreationStates.drive_type)
async def process_drive_type(message: types.Message, state: FSMContext):
    """Обработка выбора типа привода"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    if message.text not in DRIVE_TYPES:
        await message.answer("❌ Пожалуйста, выберите тип привода из предложенных вариантов:")
        return

    await state.update_data(drive_type=message.text)
    await state.set_state(CarCreationStates.body_type)

    keyboard = create_selection_keyboard(BODY_TYPES, row_width=2)
    await message.answer(
        "🚗 Выберите тип кузова:",
        reply_markup=keyboard
    )


@dp.message(CarCreationStates.body_type)
async def process_body_type(message: types.Message, state: FSMContext):
    """Обработка выбора типа кузова"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    if message.text not in BODY_TYPES:
        await message.answer("❌ Пожалуйста, выберите тип кузова из предложенных вариантов:")
        return

    await state.update_data(body_type=message.text)
    await state.set_state(CarCreationStates.condition)

    keyboard = create_selection_keyboard(CONDITIONS, row_width=2)
    await message.answer(
        "✨ Выберите состояние автомобиля:",
        reply_markup=keyboard
    )


@dp.message(CarCreationStates.condition)
async def process_condition(message: types.Message, state: FSMContext):
    """Обработка выбора состояния"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    if message.text not in CONDITIONS:
        await message.answer("❌ Пожалуйста, выберите состояние из предложенных вариантов:")
        return

    await state.update_data(condition=message.text)
    await state.set_state(CarCreationStates.color)

    await message.answer(
        "🎨 Введите цвет автомобиля (например: Черный, Белый, Серебристый):",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(CarCreationStates.color)
async def process_color(message: types.Message, state: FSMContext):
    """Обработка ввода цвета"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    await state.update_data(color=message.text.strip())
    await state.set_state(CarCreationStates.description)

    await message.answer(
        "📝 **Детальное описание автомобиля**\n\n"
        "Укажите важную информацию для покупателя:\n"
        "• Техническое состояние (двигатель, коробка, подвеска)\n"
        "• Недостатки если есть (стуки, течи, царапины)\n"
        "• Последнее ТО и что делали\n"
        "• Состояние салона\n"
        "• Комплектация и опции\n"
        "• История владения\n\n"
        "**Пример:**\n"
        "_Стучит спереди справа, мотор коробка все ок. Последнее ТО 2300 км назад - менял шрузы, катушку. "
        "Салон в идеальном состоянии, небольшая потертость на сиденье водителя._",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(CarCreationStates.description)
async def process_description(message: types.Message, state: FSMContext):
    """Обработка ввода описания"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    await state.update_data(description=message.text.strip())
    await state.set_state(CarCreationStates.photos)

    # Устанавливаем счетчик фотографий
    await state.update_data(images=[])

    await message.answer(
        "📸 Загрузите фотографии автомобиля (до 10 шт):\n\n"
        "Отправляйте фото по одному.\n"
        "Когда загрузите все фото, напишите 'Готово'",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="✅ Готово")], [KeyboardButton(text="❌ Отменить")]],
            resize_keyboard=True
        )
    )


@dp.message(CarCreationStates.photos, F.photo)
async def process_photo(message: types.Message, state: FSMContext):
    """Обработка загрузки фотографий"""

    try:
        data = await state.get_data()
        images = data.get('images', [])

        if len(images) >= 10:
            await message.answer("❌ Можно загрузить максимум 10 фотографий. Напишите 'Готово' для продолжения.")
            return

        # Получаем файл фото
        photo = message.photo[-1]  # Берем самое большое фото
        file = await bot.get_file(photo.file_id)

        # Генерируем имя файла
        brand = data.get('brand', 'car').lower().replace(' ', '-')
        model = data.get('model', 'model').lower().replace(' ', '-')
        year = data.get('year', 2024)
        filename = f"{brand}-{model}-{year}-{len(images)}.jpg"

        # Скачиваем и сохраняем фото
        file_path = car_manager.images_path / filename
        await bot.download_file(file.file_path, file_path)

        # Добавляем путь к изображению
        image_path = f"images/cars/{filename}"
        images.append(image_path)

        await state.update_data(images=images)

        await message.answer(
            f"✅ Фото {len(images)}/10 загружено.\n"
            f"Загрузите ещё или напишите 'Готово'"
        )
    except Exception as e:
        logger.error(f"Ошибка при загрузке фото: {e}")
        await message.answer(
            f"❌ Ошибка при загрузке фото. Попробуйте еще раз или напишите 'Готово' для продолжения без этого фото."
        )


@dp.message(CarCreationStates.photos, F.text)
async def process_photos_done(message: types.Message, state: FSMContext):
    """Завершение загрузки фотографий"""

    if message.text == "❌ Отменить":
        await state.clear()
        await message.answer("❌ Добавление автомобиля отменено", reply_markup=ReplyKeyboardRemove())
        return

    if message.text != "✅ Готово":
        await message.answer("📸 Пожалуйста, загрузите фото или напишите 'Готово'")
        return

    data = await state.get_data()
    images = data.get('images', [])

    if not images:
        await message.answer("❌ Необходимо загрузить хотя бы одну фотографию!")
        return

    # Устанавливаем значения по умолчанию для необязательных полей
    await state.update_data(
        vin="Не указан",
        owners_count=1,
        pts_original=True,
        exchange_possible=True,
        credit_available=True
    )

    await state.set_state(CarCreationStates.confirm)

    # Показываем предпросмотр
    car_data = await state.get_data()
    summary = car_manager.format_car_summary(car_data)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Опубликовать", callback_data="confirm_car"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_car")
        ]
    ])

    await message.answer(
        "📋 **Проверьте данные автомобиля:**\n" + summary,
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        "Всё верно?",
        reply_markup=keyboard
    )


# ========== CALLBACK ОБРАБОТЧИКИ ==========

@dp.callback_query(F.data == "admin_add_car")
async def callback_admin_add_car(callback: types.CallbackQuery, state: FSMContext):
    """Начало добавления автомобиля через callback"""

    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ У вас нет доступа к этой функции", show_alert=True)
        return

    await state.set_state(CarCreationStates.brand)

    # Создаем inline кнопки с марками из справочника
    brands = sorted(CAR_BRANDS.keys())
    keyboard = create_inline_keyboard(brands, "brand", row_width=2)

    await callback.message.answer(
        "➕ **Добавление нового автомобиля**\n\n"
        "🚗 Выберите марку автомобиля из списка или введите вручную:",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("brand:"), CarCreationStates.brand)
async def callback_brand_selected(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора марки через inline кнопку"""

    brand = callback.data.split(":", 1)[1]

    if brand == "manual":
        # Пользователь хочет ввести марку вручную
        await callback.message.edit_text(
            "📝 Введите марку автомобиля вручную:",
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    # Сохраняем выбранную марку
    await state.update_data(brand=brand)
    await state.set_state(CarCreationStates.model)

    # Получаем модели для выбранной марки
    models = CAR_BRANDS.get(brand, [])
    keyboard = create_inline_keyboard(models, "model", row_width=2)

    await callback.message.edit_text(
        f"✅ Марка: **{brand}**\n\n"
        f"🚗 Выберите модель автомобиля:",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("model:"), CarCreationStates.model)
async def callback_model_selected(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора модели через inline кнопку"""

    model = callback.data.split(":", 1)[1]

    if model == "manual":
        # Пользователь хочет ввести модель вручную
        data = await state.get_data()
        brand = data.get('brand', '')
        await callback.message.edit_text(
            f"✅ Марка: **{brand}**\n\n"
            f"📝 Введите модель автомобиля вручную:",
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    # Сохраняем выбранную модель
    await state.update_data(model=model)
    await state.set_state(CarCreationStates.year)

    data = await state.get_data()
    brand = data.get('brand', '')

    await callback.message.edit_text(
        f"✅ Марка: **{brand}**\n"
        f"✅ Модель: **{model}**\n\n"
        f"📅 Введите год выпуска (например: 2020):",
        parse_mode="Markdown"
    )
    await callback.answer()


@dp.callback_query(F.data == "cancel_add_car")
async def callback_cancel_add_car(callback: types.CallbackQuery, state: FSMContext):
    """Отмена создания объявления через inline кнопку"""

    await state.clear()
    await callback.message.edit_text("❌ Добавление автомобиля отменено")
    await callback.answer()


@dp.callback_query(F.data == "confirm_car")
async def callback_confirm_car(callback: types.CallbackQuery, state: FSMContext):
    """Подтверждение создания объявления"""

    await callback.message.edit_text("⏳ Создаю объявление...")

    try:
        # Получаем данные
        car_data = await state.get_data()

        # Создаем объявление
        filepath = await car_manager.create_car_listing(car_data)

        # Очищаем состояние
        await state.clear()

        await callback.message.edit_text(
            f"✅ **Объявление успешно создано!**\n\n"
            f"Файл: `{Path(filepath).name}`\n\n"
            f"Автомобиль появится на сайте после следующего деплоя.\n"
            f"Для немедленного появления выполните `hugo` в папке hugo-site.",
            parse_mode="Markdown"
        )

    except Exception as e:
        logger.error(f"Ошибка при создании объявления: {e}")
        await callback.message.edit_text(
            f"❌ Ошибка при создании объявления:\n{str(e)}"
        )
        await state.clear()

    await callback.answer()


@dp.callback_query(F.data == "cancel_car")
async def callback_cancel_car(callback: types.CallbackQuery, state: FSMContext):
    """Отмена создания объявления"""

    await state.clear()
    await callback.message.edit_text("❌ Создание объявления отменено")
    await callback.answer()


@dp.callback_query(F.data == "admin_stats")
async def callback_admin_stats(callback: types.CallbackQuery):
    """Показать статистику (заглушка)"""

    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ У вас нет доступа к этой функции", show_alert=True)
        return

    # Подсчитываем количество объявлений
    content_path = Path(HUGO_SITE_PATH) / "content" / "cars"
    car_files = list(content_path.glob("*.md"))
    # Исключаем _index.md
    car_count = len([f for f in car_files if f.name != "_index.md"])

    await callback.message.edit_text(
        f"📊 **Статистика:**\n\n"
        f"🚗 Автомобилей в каталоге: {car_count}\n"
        f"👤 Администраторов: {len(ADMIN_IDS)}\n"
        f"🌐 Сайт: {WEBAPP_URL}",
        parse_mode="Markdown"
    )
    await callback.answer()


@dp.callback_query(F.data == "back_to_start")
async def callback_back_to_start(callback: types.CallbackQuery):
    """Возврат к стартовому сообщению"""

    if is_admin(callback.from_user.id):
        message_data = get_admin_start_message(callback.from_user.id)
    else:
            message_data = get_start_message()

            keyboard = create_keyboard_from_buttons(message_data["buttons"])

            await callback.message.edit_text(
                message_data["text"],
                reply_markup=keyboard,
                parse_mode=message_data["parse_mode"]
            )
    await callback.answer()


@dp.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    """Обработка остальных callback'ов"""

    response_data = get_callback_response(callback.data)

    if response_data:
        keyboard = create_keyboard_from_buttons(response_data["buttons"])

        await callback.message.edit_text(
            response_data["text"],
            reply_markup=keyboard,
            parse_mode=response_data["parse_mode"]
        )

    await callback.answer()


# ========== ОБРАБОТЧИК ТЕКСТОВЫХ СООБЩЕНИЙ ==========

@dp.message(F.text, StateFilter(None))
async def handle_text_messages(message: types.Message):
    """Обработка текстовых сообщений вне FSM (поиск)"""

    search_data = search_by_text(message.text)
    keyboard = create_keyboard_from_buttons(search_data["buttons"])

    await message.answer(
        search_data["text"],
        reply_markup=keyboard,
        parse_mode=search_data["parse_mode"]
    )


# ========== ГЛАВНАЯ ФУНКЦИЯ ==========

async def main():
    """Основная функция запуска бота"""

    logger.info("=" * 50)
    logger.info("🚗 Запуск Telegram бота Автоломбарда")
    logger.info("=" * 50)
    logger.info(f"Web App URL: {WEBAPP_URL}")
    logger.info(f"Hugo Site Path: {HUGO_SITE_PATH}")
    logger.info(get_admin_info())
    logger.info("=" * 50)

    # Запускаем polling
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
