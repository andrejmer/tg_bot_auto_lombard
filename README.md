# 🚗 Telegram Bot Автоломбард

Полнофункциональный Telegram бот для автоломбарда с веб-каталогом автомобилей и автоматическим парсингом с Авито.

## 🎯 Возможности

- **Telegram Bot** с Web App интеграцией
- **Hugo сайт** с динамическими фильтрами
- **Парсер Авито** для автоматического обновления каталога
- **Адаптивный дизайн** для мобильных устройств
- **GitHub Pages** для бесплатного хостинга

## 🚀 Быстрый старт

### 1. Настройка Telegram бота
```bash
cd bot/
cp ../.env.example .env
# Отредактируйте .env и добавьте BOT_TOKEN
pip install -r requirements.txt
python run_bot.py
```

### 2. Запуск Hugo сайта (локально)
```bash
cd hugo-site/
hugo server --port 1313
```

### 3. Парсинг с Авито
```bash
cd parser/
pip install -r requirements.txt
python run_parser.py
```

## 📂 Структура проекта

```
tg_bot_auto_lombard/
├── bot/                    # Telegram bot
│   ├── main.py            # Основной файл бота
│   ├── bot_functions.py   # Логика бота
│   ├── run_bot.py         # Запуск бота
│   └── requirements.txt   # Зависимости
│
├── parser/                # Avito parser
│   ├── avito_parser.py    # Парсер с Selenium
│   ├── run_parser.py      # Интерактивный запуск
│   ├── test_parser.py     # Тесты парсера
│   ├── image_optimizer.py # Оптимизация изображений
│   └── requirements.txt   # Зависимости
│
├── tools/                 # Утилиты
│   ├── add_cars.py        # Ручное добавление авто
│   └── car_template.md    # Шаблон автомобиля
│
├── docs/                  # Документация
│   ├── AVITO_PARSER_SETUP.md
│   └── TELEGRAM_SETUP.md
│
├── hugo-site/             # Hugo website
│   ├── content/cars/      # Каталог автомобилей
│   ├── layouts/           # HTML шаблоны
│   ├── static/            # CSS, JS, изображения
│   └── hugo.toml          # Конфигурация Hugo
│
└── .github/workflows/     # GitHub Actions
    └── hugo.yml           # Автодеплой на GitHub Pages
```

## 🔧 Настройка

### Переменные окружения (.env)
```env
BOT_TOKEN=your_telegram_bot_token
WEBAPP_URL=https://yourusername.github.io/tg_bot_auto_lombard
```

### Требования
- Python 3.8+
- Hugo 0.120+
- Chrome + ChromeDriver (для парсера)

## 🎨 Особенности

### Динамические фильтры
- Автоматическая генерация списков марок и моделей
- Фильтрация по цене, году, типу кузова
- Адаптивный интерфейс для мобильных

### Парсер Авито
- Обход антиробота через Selenium
- Автоматическая загрузка изображений
- Создание Hugo-совместимых файлов
- Оптимизация изображений

### Telegram Integration
- Web App кнопка в боте
- Бесшовная интеграция с сайтом
- Мобильная оптимизация

## 📖 Подробная документация

- [Настройка Telegram бота](docs/TELEGRAM_SETUP.md)
- [Настройка парсера Авито](docs/AVITO_PARSER_SETUP.md)

## 🌐 Демо

- **Сайт**: https://andrejmer.github.io/tg_bot_auto_lombard
- **Telegram бот**: @auto_lombard_bot

## 📞 Контакты

- GitHub: [andrejmer](https://github.com/andrejmer)
- Telegram: @andrejmer

## 📄 Лицензия

MIT License
