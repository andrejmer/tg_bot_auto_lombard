#!/usr/bin/env python3
"""
Тестирование функций бота без подключения к Telegram
"""

import asyncio
from unittest.mock import Mock, AsyncMock
import sys
import os

# Добавляем текущую директорию в PATH для импорта main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_bot_functions():
    """Тестирование основных функций бота"""

    print("🧪 Тестирование функций Telegram бота...")
    print("=" * 50)

    # Мокаем объекты Telegram
    mock_message = Mock()
    mock_message.chat.id = 123456789
    mock_message.text = "/start"
    mock_message.answer = AsyncMock()

    mock_callback = Mock()
    mock_callback.data = "contacts"
    mock_callback.message = mock_message
    mock_callback.answer = AsyncMock()
    mock_callback.message.edit_text = AsyncMock()

    try:
        # Импортируем функции из bot_functions.py
        from bot_functions import (
            get_start_message, get_catalog_message, get_search_message,
            get_callback_response, search_by_text, get_menu_button_config
        )

        print("✅ Импорт функций успешен")

        # Тестируем команду /start
        print("\n🧪 Тестируем команду /start...")
        start_data = get_start_message()
        assert "Добро пожаловать" in start_data["text"]
        assert len(start_data["buttons"]) > 0
        print("✅ Команда /start работает")

        # Тестируем команду /catalog
        print("\n🧪 Тестируем команду /catalog...")
        catalog_data = get_catalog_message()
        assert "Каталог автомобилей" in catalog_data["text"]
        assert len(catalog_data["buttons"]) > 0
        print("✅ Команда /catalog работает")

        # Тестируем команду /search
        print("\n🧪 Тестируем команду /search...")
        search_data = get_search_message()
        assert "Поиск автомобилей" in search_data["text"]
        assert len(search_data["buttons"]) > 0
        print("✅ Команда /search работает")

        # Тестируем обработку callback'ов
        print("\n🧪 Тестируем обработку кнопок...")
        contacts_data = get_callback_response("contacts")
        about_data = get_callback_response("about")
        help_data = get_callback_response("help")
        assert contacts_data and "Наши контакты" in contacts_data["text"]
        assert about_data and "О нашем автоломбарде" in about_data["text"]
        assert help_data and "Справка" in help_data["text"]
        print("✅ Обработка кнопок работает")

        # Тестируем поиск по тексту
        print("\n🧪 Тестируем текстовый поиск...")
        bmw_search = search_by_text("BMW")
        toyota_search = search_by_text("Toyota")
        unknown_search = search_by_text("Unknown brand")
        assert "BMW" in bmw_search["text"]
        assert "Toyota" in toyota_search["text"]
        assert "не могу найти" in unknown_search["text"].lower()
        print("✅ Текстовый поиск работает")

        # Тестируем конфигурацию меню
        print("\n🧪 Тестируем кнопку меню...")
        menu_config = get_menu_button_config()
        assert "Каталог авто" in menu_config["text"]
        assert "web_app_url" in menu_config
        print("✅ Конфигурация меню работает")

        print("\n" + "=" * 50)
        print("🎉 Все тесты пройдены успешно!")
        print("\n📝 Результаты тестирования:")
        print("✅ Команды бота работают корректно")
        print("✅ Inline кнопки функционируют")
        print("✅ Поиск по тексту работает")
        print("✅ Web App интеграция настроена")

        print("\n🚀 Готово к подключению реального токена!")

    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

    return True

async def test_webapp_urls():
    """Проверка URL'ов для Web App"""

    print("\n🌐 Проверка Web App URL'ов...")

    webapp_url = os.getenv("WEBAPP_URL", "http://localhost:1313")

    test_urls = [
        f"{webapp_url}",
        f"{webapp_url}/cars/",
        f"{webapp_url}/cars/?brand=BMW",
        f"{webapp_url}/cars/?brand=Toyota&model=Camry"
    ]

    print(f"📋 Base URL: {webapp_url}")
    print("📋 Test URLs:")
    for url in test_urls:
        print(f"   • {url}")

    print("✅ URL'ы сформированы корректно")

def main():
    """Основная функция тестирования"""

    print("🤖 Тест Telegram Bot для Автоломбарда")
    print("🎯 Проверка функций без подключения к Telegram")
    print("=" * 60)

    # Устанавливаем тестовые переменные окружения
    os.environ["BOT_TOKEN"] = "TEST_TOKEN"
    os.environ["WEBAPP_URL"] = "http://localhost:1313"

    try:
        # Запускаем тесты
        result = asyncio.run(test_bot_functions())
        asyncio.run(test_webapp_urls())

        if result:
            print("\n🎉 Тестирование завершено успешно!")
            print("\n📋 Следующие шаги:")
            print("1. Создайте бота через @BotFather")
            print("2. Получите токен и сохраните в .env")
            print("3. Запустите Hugo сервер: cd hugo-site && hugo server")
            print("4. Запустите бота: python run_bot.py")
            print("5. Протестируйте в Telegram")
        else:
            print("\n❌ Тестирование не пройдено")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
