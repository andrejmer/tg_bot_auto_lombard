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
