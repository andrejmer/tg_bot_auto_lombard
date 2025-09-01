#!/usr/bin/env python3
"""
Функции Telegram бота (отдельно от aiogram декораторов)
"""

import os
from typing import Dict, Any, Optional

# Конфигурация
WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:1313")

def get_start_message() -> Dict[str, Any]:
    """Возвращает данные для стартового сообщения"""

    text = """
🚗 **Добро пожаловать в Автоломбард!**

Мы предлагаем качественные автомобили с пробегом по выгодным ценам.

**Что вы можете сделать:**
• 🚗 Просмотреть каталог автомобилей
• 🔍 Найти автомобиль по параметрам
• 📱 Связаться с нашими менеджерами
• 💰 Узнать актуальные цены

**Нажмите кнопку ниже, чтобы открыть каталог!**
    """

    buttons = [
        {
            "text": "🚗 Открыть каталог автомобилей",
            "web_app_url": f"{WEBAPP_URL}/cars/"
        },
        {
            "text": "🏠 Главная страница",
            "web_app_url": WEBAPP_URL
        },
        {
            "text": "📞 Контакты",
            "callback_data": "contacts"
        },
        {
            "text": "ℹ️ О нас",
            "callback_data": "about"
        },
        {
            "text": "🔍 Помощь",
            "callback_data": "help"
        }
    ]

    return {
        "text": text,
        "buttons": buttons,
        "parse_mode": "Markdown"
    }

def get_catalog_message() -> Dict[str, Any]:
    """Возвращает данные для сообщения каталога"""

    text = """
🚗 **Каталог автомобилей**

В нашем каталоге представлены:
• BMW, Mercedes-Benz, Toyota, Audi
• Автомобили разных годов выпуска
• Различные ценовые категории
• Подробные характеристики и фото

**Удобные фильтры помогут найти идеальный автомобиль!**
    """

    buttons = [
        {
            "text": "🚗 Открыть каталог",
            "web_app_url": f"{WEBAPP_URL}/cars/"
        },
        {
            "text": "🏠 На главную",
            "web_app_url": WEBAPP_URL
        }
    ]

    return {
        "text": text,
        "buttons": buttons,
        "parse_mode": "Markdown"
    }

def get_search_message() -> Dict[str, Any]:
    """Возвращает данные для сообщения поиска"""

    text = """
🔍 **Поиск автомобилей**

Для поиска автомобиля напишите мне:
• Марку (например: BMW, Toyota)
• Модель (например: X5, Camry)
• Ценовой диапазон (например: до 2 млн)

**Или используйте расширенный поиск в каталоге!**
    """

    buttons = [
        {
            "text": "🔍 Расширенный поиск",
            "web_app_url": f"{WEBAPP_URL}/cars/"
        }
    ]

    return {
        "text": text,
        "buttons": buttons,
        "parse_mode": "Markdown"
    }

def get_callback_response(callback_data: str) -> Optional[Dict[str, Any]]:
    """Возвращает ответ на callback запрос"""

    if callback_data == "contacts":
        text = """
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

        buttons = [
            {
                "text": "📱 Написать менеджеру",
                "url": "https://t.me/manager_ivan"
            },
            {
                "text": "🚗 К каталогу",
                "web_app_url": f"{WEBAPP_URL}/cars/"
            }
        ]

    elif callback_data == "about":
        text = """
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

        buttons = [
            {
                "text": "🚗 Смотреть автомобили",
                "web_app_url": f"{WEBAPP_URL}/cars/"
            },
            {
                "text": "📞 Связаться с нами",
                "callback_data": "contacts"
            }
        ]

    elif callback_data == "help":
        text = """
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

        buttons = [
            {
                "text": "🚗 К каталогу",
                "web_app_url": f"{WEBAPP_URL}/cars/"
            },
            {
                "text": "🏠 На главную",
                "callback_data": "back_to_start"
            }
        ]

    else:
        return None

    return {
        "text": text,
        "buttons": buttons,
        "parse_mode": "Markdown"
    }

def search_by_text(query: str) -> Dict[str, Any]:
    """Поиск автомобилей по тексту"""

    query_lower = query.lower()

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
        if keyword in query_lower:
            found_brand = brand
            break

    if found_brand:
        search_url = f"{WEBAPP_URL}/cars/?brand={found_brand}"

        text = f"🔍 **Поиск: {found_brand}**\n\nНайдены автомобили марки {found_brand}.\nОткройте каталог для просмотра!"

        buttons = [
            {
                "text": f"🚗 Смотреть {found_brand}",
                "web_app_url": search_url
            },
            {
                "text": "🔍 Расширенный поиск",
                "web_app_url": f"{WEBAPP_URL}/cars/"
            }
        ]

    else:
        text = "🤔 Не могу найти автомобили по вашему запросу.\n\nПопробуйте использовать каталог с фильтрами или обратитесь к менеджеру!"

        buttons = [
            {
                "text": "🚗 Открыть каталог",
                "web_app_url": f"{WEBAPP_URL}/cars/"
            },
            {
                "text": "📞 Связаться с менеджером",
                "callback_data": "contacts"
            }
        ]

    return {
        "text": text,
        "buttons": buttons,
        "parse_mode": "Markdown"
    }

def get_menu_button_config() -> Dict[str, str]:
    """Возвращает конфигурацию кнопки меню"""
    return {
        "text": "🚗 Каталог авто",
        "web_app_url": f"{WEBAPP_URL}/cars/"
    }
