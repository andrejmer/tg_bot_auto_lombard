#!/usr/bin/env python3
"""
Telegram Bot для Автоломбарда
Интеграция с Hugo каталогом автомобилей
"""

import asyncio
import logging
import os
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
    MenuButtonWebApp
)

# Импортируем функции бота
from bot_functions import (
    get_start_message, get_catalog_message, get_search_message,
    get_callback_response, search_by_text, get_menu_button_config
)


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:1313")

# Инициализация бота (только если токен валидный)
if BOT_TOKEN and BOT_TOKEN != "YOUR_BOT_TOKEN_HERE" and not BOT_TOKEN.startswith("TEST_"):
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
else:
    bot = None
    dp = None


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


if dp:  # Только если dispatcher инициализирован
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

        # Получаем данные сообщения
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


    @dp.callback_query()
    async def handle_callbacks(callback: types.CallbackQuery):
        """Обработка нажатий на inline кнопки"""

        if callback.data == "back_to_start":
            # Возврат к стартовому сообщению
            message_data = get_start_message()
            keyboard = create_keyboard_from_buttons(message_data["buttons"])

            await callback.message.edit_text(
                message_data["text"],
                reply_markup=keyboard,
                parse_mode=message_data["parse_mode"]
            )
        else:
            # Обрабатываем остальные callback'ы
            response_data = get_callback_response(callback.data)

            if response_data:
                keyboard = create_keyboard_from_buttons(response_data["buttons"])

                await callback.message.edit_text(
                    response_data["text"],
                    reply_markup=keyboard,
                    parse_mode=response_data["parse_mode"]
                )

        await callback.answer()


    @dp.message()
    async def handle_text_messages(message: types.Message):
        """Обработка текстовых сообщений (поиск)"""

        search_data = search_by_text(message.text)
        keyboard = create_keyboard_from_buttons(search_data["buttons"])

        await message.answer(
            search_data["text"],
            reply_markup=keyboard,
            parse_mode=search_data["parse_mode"]
        )


async def main():
    """Основная функция запуска бота"""

    if not bot or not dp:
        logger.error("Бот не инициализирован! Проверьте BOT_TOKEN в .env файле")
        return

    logger.info("Запуск Telegram бота...")
    logger.info(f"Web App URL: {WEBAPP_URL}")

    # Запускаем polling
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
📞 **Наши контакты**

**Телефон:** +7 (999) 123-45-67
**Email:** info@autolombard.ru
**Адрес:** г. Москва, ул. Примерная, 123

**Режим работы:**
Пн-Пт: 9:00 - 20:00
Сб-Вс: 10:00 - 18:00

**Менеджеры:**
👨‍💼 Иван Петров - @manager_ivan
👨‍💼 Сергей Сидоров - @manager_sergey
        """

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📱 Написать менеджеру",
                    url="https://t.me/manager_ivan"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚗 К каталогу",
                    web_app=WebAppInfo(url=f"{WEBAPP_URL}/cars/")
                )
            ]
        ])

        await callback.message.edit_text(
            contacts_text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    elif callback.data == "about":
        about_text = """
ℹ️ **О нашем автоломбарде**

**Мы предлагаем:**
• Качественные автомобили с пробегом
• Честные цены без переплат
• Полную проверку истории автомобиля
• Гарантию юридической чистоты
• Помощь в оформлении документов

**Наши преимущества:**
✅ Опыт работы более 10 лет
✅ Более 500 довольных клиентов
✅ Все автомобили проверены
✅ Flexible payment options
✅ Профессиональная консультация
        """

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚗 Смотреть автомобили",
                    web_app=WebAppInfo(url=f"{WEBAPP_URL}/cars/")
                )
            ],
            [
                InlineKeyboardButton(
                    text="📞 Связаться с нами",
                    callback_data="contacts"
                )
            ]
        ])

        await callback.message.edit_text(
            about_text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    elif callback.data == "help":
        help_text = """
🔍 **Справка по использованию бота**

**Основные команды:**
/start - Главное меню
/catalog - Открыть каталог автомобилей
/search - Поиск автомобилей
/help - Эта справка

**Как искать автомобили:**
1. Нажмите "🚗 Открыть каталог"
2. Используйте фильтры по марке, цене, году
3. Просматривайте подробную информацию
4. Связывайтесь с менеджерами

**Нужна помощь?**
Напишите @manager_ivan - поможем подобрать автомобиль!
        """

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚗 К каталогу",
                    web_app=WebAppInfo(url=f"{WEBAPP_URL}/cars/")
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 На главную",
                    callback_data="back_to_start"
                )
            ]
        ])

        await callback.message.edit_text(
            help_text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    elif callback.data == "back_to_start":
        # Возврат к стартовому сообщению
        await cmd_start(callback.message)

    await callback.answer()


@dp.message()
async def handle_text_messages(message: types.Message):
    """Обработка текстовых сообщений (поиск)"""

    text = message.text.lower()

    # Простая логика поиска по ключевым словам
    search_results = []

    # Поиск по маркам
    brands = {
        'bmw': 'BMW',
        'mercedes': 'Mercedes-Benz',
        'мерседес': 'Mercedes-Benz',
        'toyota': 'Toyota',
        'тойота': 'Toyota',
        'audi': 'Audi',
        'ауди': 'Audi',
        'volkswagen': 'Volkswagen',
        'фольксваген': 'Volkswagen',
        'hyundai': 'Hyundai',
        'хендай': 'Hyundai'
    }

    found_brand = None
    for keyword, brand in brands.items():
        if keyword in text:
            found_brand = brand
            break

    if found_brand:
        search_url = f"{WEBAPP_URL}/cars/?brand={found_brand}"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🚗 Смотреть {found_brand}",
                    web_app=WebAppInfo(url=search_url)
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Расширенный поиск",
                    web_app=WebAppInfo(url=f"{WEBAPP_URL}/cars/")
                )
            ]
        ])

        await message.answer(
            f"🔍 **Поиск: {found_brand}**\n\nНайдены автомобили марки {found_brand}.\nОткройте каталог для просмотра!",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    else:
        # Если ничего не найдено
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚗 Открыть каталог",
                    web_app=WebAppInfo(url=f"{WEBAPP_URL}/cars/")
                )
            ],
            [
                InlineKeyboardButton(
                    text="📞 Связаться с менеджером",
                    callback_data="contacts"
                )
            ]
        ])

        await message.answer(
            "🤔 Не могу найти автомобили по вашему запросу.\n\nПопробуйте использовать каталог с фильтрами или обратитесь к менеджеру!",
            reply_markup=keyboard
        )


async def main():
    """Основная функция запуска бота"""

    logger.info("Запуск Telegram бота...")
    logger.info(f"Web App URL: {WEBAPP_URL}")

    # Запускаем polling
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())