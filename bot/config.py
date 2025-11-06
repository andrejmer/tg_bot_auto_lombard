"""
Конфигурация Telegram бота для автоломбарда
"""

import os
from typing import List


# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# URL веб-приложения
WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:1313")

# Путь к Hugo сайту
HUGO_SITE_PATH = os.getenv("HUGO_SITE_PATH", "../hugo-site")

# ID администраторов (кто может добавлять объявления)
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS: List[int] = []

if ADMIN_IDS_STR:
    try:
        ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(",") if id.strip()]
    except ValueError:
        print("⚠️ Ошибка при парсинге ADMIN_IDS. Проверьте .env файл")


# Настройки логирования
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# Проверка наличия администраторов
def is_admin(user_id: int) -> bool:
    """Проверяет, является ли пользователь администратором"""
    return user_id in ADMIN_IDS


# Информация для пользователей
def get_admin_info() -> str:
    """Возвращает информацию о настроенных администраторах"""
    if not ADMIN_IDS:
        return "⚠️ Администраторы не настроены. Добавьте ADMIN_IDS в .env файл"
    return f"✅ Настроено администраторов: {len(ADMIN_IDS)}"

