#!/bin/bash
# Удобный скрипт запуска бота

echo "🚗 Telegram Bot Автоломбард"
echo "=========================="

# Проверяем .env
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "📝 Создайте файл .env из примера:"
    echo "cp .env.example .env"
    echo "Затем отредактируйте его."
    exit 1
fi

# Переходим в папку бота и запускаем
cd bot/
echo "🚀 Запуск Telegram бота..."
python run_bot.py
