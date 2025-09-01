import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup

# Настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Получаем токен бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://localhost:8443")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен!")

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем клавиатуру с веб-приложением
def get_keyboard():
    web_app = WebAppInfo(url=WEB_APP_URL)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚗 Открыть каталог автомобилей", web_app=web_app)]],
        resize_keyboard=True
    )
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(f"Получена команда /start от пользователя {message.from_user.id}")
    try:
        await message.answer(
            "👋 Привет! Я бот автоломбарда.\n\n"
            "Нажми на кнопку ниже, чтобы посмотреть доступные автомобили:",
            reply_markup=get_keyboard()
        )
        logger.info(f"Отправлен ответ пользователю {message.from_user.id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке ответа: {e}")

@dp.message()
async def echo(message: Message):
    logger.info(f"Получено сообщение: {message.text} от пользователя {message.from_user.id}")
    try:
        await message.answer(
            "Используйте команду /start для начала работы с ботом",
            reply_markup=get_keyboard()
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке ответа: {e}")

async def main():
    logger.info("Запуск бота...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())