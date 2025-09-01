#!/usr/bin/env python3
"""
Скрипт для запуска Telegram бота
"""

import os
import sys
from dotenv import load_dotenv

def main():
    """Запуск бота с загрузкой конфигурации"""

    # Загружаем переменные окружения из корня проекта
    if os.path.exists('../.env'):
        load_dotenv('../.env')
        print("✅ Загружен .env файл")
    elif os.path.exists('.env'):
        load_dotenv('.env')
        print("✅ Загружен локальный .env файл")
    else:
        print("⚠️  .env файл не найден, используем переменные окружения")

    # Проверяем BOT_TOKEN
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token or bot_token == "YOUR_BOT_TOKEN_HERE":
        print("❌ BOT_TOKEN не установлен!")
        print("\n📝 Создайте файл .env со следующим содержимым:")
        print("BOT_TOKEN=ваш_токен_от_@BotFather")
        print("WEBAPP_URL=http://localhost:1313")
        sys.exit(1)

    webapp_url = os.getenv("WEBAPP_URL", "http://localhost:1313")

    print("🚀 Запуск Telegram бота...")
    print(f"🌐 Web App URL: {webapp_url}")
    print(f"🤖 Bot Token: {bot_token[:10]}...")
    print(f"\n💡 Убедитесь, что Hugo сервер запущен на {webapp_url}")
    print("   Для запуска Hugo: cd ../hugo-site && hugo server")
    print("\n🛑 Для остановки бота нажмите Ctrl+C")
    print("-" * 50)

    # Импортируем и запускаем основной модуль
    try:
        from main import main as bot_main
        import asyncio
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
