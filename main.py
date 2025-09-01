import asyncio
import logging
import os
from typing import List, Dict
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto,
    CallbackQuery
)

# Настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Получаем токен бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен!")

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Примеры автомобилей (в реальном приложении это должно быть в базе данных)
CARS = [
    {
        "id": "1",
        "brand": "BMW",
        "model": "X5",
        "year": 2019,
        "price": 2500000,
        "mileage": 75000,
        "engine": "3.0L",
        "power": 249,
        "image_url": "https://images.unsplash.com/photo-1550355291-bbee04a92027",
        "description": "Отличное состояние, один владелец, полная история обслуживания."
    },
    {
        "id": "2",
        "brand": "Mercedes-Benz",
        "model": "E200",
        "year": 2020,
        "price": 3100000,
        "mileage": 45000,
        "engine": "2.0L",
        "power": 197,
        "image_url": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341",
        "description": "Идеальное состояние, максимальная комплектация."
    },
    {
        "id": "3",
        "brand": "Audi",
        "model": "A6",
        "year": 2021,
        "price": 4200000,
        "mileage": 25000,
        "engine": "2.0L",
        "power": 245,
        "image_url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d",
        "description": "На гарантии, все ТО у официального дилера."
    }
]

def get_car_keyboard(car_id: str, is_first: bool, is_last: bool) -> InlineKeyboardMarkup:
    """Создает клавиатуру для карточки автомобиля"""
    keyboard = []

    # Кнопки навигации
    nav_buttons = []
    if not is_first:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Предыдущий", callback_data=f"prev_{car_id}"))
    if not is_last:
        nav_buttons.append(InlineKeyboardButton(text="Следующий ➡️", callback_data=f"next_{car_id}"))
    if nav_buttons:
        keyboard.append(nav_buttons)

    # Кнопка для получения подробной информации
    keyboard.append([InlineKeyboardButton(
        text="📋 Подробная информация",
        callback_data=f"info_{car_id}"
    )])

    # Кнопка для связи
    keyboard.append([InlineKeyboardButton(
        text="📞 Связаться с менеджером",
        callback_data=f"contact_{car_id}"
    )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def format_car_caption(car: Dict) -> str:
    """Форматирует описание автомобиля"""
    return (
        f"🚗 {car['brand']} {car['model']} {car['year']}\n\n"
        f"💰 Цена: {car['price']:,} ₽\n"
        f"🛣 Пробег: {car['mileage']:,} км\n"
        f"⚙️ Двигатель: {car['engine']} ({car['power']} л.с.)"
    )

async def show_car(message: Message | CallbackQuery, car_index: int = 0) -> None:
    """Показывает карточку автомобиля"""
    car = CARS[car_index]
    is_first = car_index == 0
    is_last = car_index == len(CARS) - 1

    caption = format_car_caption(car)
    keyboard = get_car_keyboard(car["id"], is_first, is_last)

    if isinstance(message, CallbackQuery):
        await message.message.edit_media(
            media=InputMediaPhoto(media=car["image_url"], caption=caption),
            reply_markup=keyboard
        )
    else:
        await message.answer_photo(
            photo=car["image_url"],
            caption=caption,
            reply_markup=keyboard
        )

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    logger.info(f"Получена команда /start от пользователя {message.from_user.id}")
    try:
        await message.answer(
            "👋 Привет! Я бот автоломбарда.\n\n"
            "Здесь вы можете посмотреть доступные автомобили и получить подробную информацию о них."
        )
        await show_car(message)
        logger.info(f"Отправлен ответ пользователю {message.from_user.id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке ответа: {e}")

@dp.callback_query(lambda c: c.data.startswith(('next_', 'prev_')))
async def process_navigation(callback_query: CallbackQuery):
    """Обработчик кнопок навигации"""
    action, car_id = callback_query.data.split('_')
    current_index = next(i for i, car in enumerate(CARS) if car["id"] == car_id)

    if action == 'next':
        next_index = current_index + 1
    else:
        next_index = current_index - 1

    await show_car(callback_query, next_index)
    await callback_query.answer()

@dp.callback_query(lambda c: c.data.startswith('info_'))
async def process_info(callback_query: CallbackQuery):
    """Обработчик кнопки информации"""
    car_id = callback_query.data.split('_')[1]
    car = next(car for car in CARS if car["id"] == car_id)

    info_text = (
        f"📋 Подробная информация о {car['brand']} {car['model']}\n\n"
        f"🚗 Год выпуска: {car['year']}\n"
        f"💰 Цена: {car['price']:,} ₽\n"
        f"🛣 Пробег: {car['mileage']:,} км\n"
        f"⚙️ Двигатель: {car['engine']}\n"
        f"💪 Мощность: {car['power']} л.с.\n\n"
        f"📝 Описание:\n{car['description']}"
    )

    await callback_query.answer()
    await callback_query.message.reply(info_text)

@dp.callback_query(lambda c: c.data.startswith('contact_'))
async def process_contact(callback_query: CallbackQuery):
    """Обработчик кнопки связи с менеджером"""
    await callback_query.answer()
    await callback_query.message.reply(
        "📞 Для связи с менеджером:\n"
        "- Телефон: +7 (XXX) XXX-XX-XX\n"
        "- Telegram: @manager_username\n\n"
        "Режим работы: ПН-ВС с 9:00 до 21:00"
    )

async def main():
    logger.info("Запуск бота...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())