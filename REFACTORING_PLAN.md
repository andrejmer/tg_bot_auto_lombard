# 🔧 План рефакторинга проекта

## 📂 Текущие проблемы:
- Много дублирующихся файлов
- Старые неиспользуемые скрипты
- Лишние конфигурации и документы
- Неорганизованная структура

## 🗑️ Файлы для удаления:

### Старые/дублирующиеся Python файлы:
- `main_clean.py` - старая версия
- `main_old.py` - старая версия
- `test_bot.py` - заменен на современные тесты
- `scripts/convert_cars_to_hugo.py` - больше не нужен
- `web/assets/data/cars.json` - старые данные
- `create_real_cars.py` - использовался только раз

### Лишние документы:
- `AGENTS.md` - не относится к проекту
- `ARCHITECTURE.md` - устарел
- `DEVELOPMENT_PLAN.md` - выполнен
- `TECHNICAL_SPECIFICATION.md` - устарел
- `TESTING_STRATEGY.md` - устарел
- `GITHUB_PAGES_SETUP.md` - общая инструкция
- `DEPLOY_TO_GITHUB.md` - инструкция выполнена

### Временные файлы:
- `car-template.md` - перенесем в инструменты
- `hugo-site/layouts/_default/models-data.json` - дубликат
- `hugo-site/public/` - генерируемая папка

## ✅ Файлы для сохранения:

### Основные компоненты:
- `main.py` - главный файл бота
- `bot_functions.py` - логика бота
- `run_bot.py` - запуск бота
- `requirements.txt` - зависимости бота

### Парсер Авито:
- `avito_parser.py` - основной парсер
- `run_parser.py` - запуск парсера
- `test_parser.py` - тесты парсера
- `requirements_parser.txt` - зависимости парсера
- `image_optimizer.py` - оптимизация изображений

### Инструменты:
- `add_cars.py` - ручное добавление автомобилей

### Документация:
- `AVITO_PARSER_SETUP.md` - инструкция по парсеру
- `TELEGRAM_SETUP.md` - инструкция по боту
- `README.md` - главная документация (создать)

### Hugo сайт:
- Вся папка `hugo-site/` (кроме `public/`)

## 🎯 Новая структура проекта:

```
tg_bot_auto_lombard/
├── README.md                   # Главная документация
├── .env.example               # Пример конфигурации
├── .gitignore                 # Git игнор
│
├── bot/                       # Telegram bot
│   ├── main.py               # Главный файл бота
│   ├── bot_functions.py      # Логика бота
│   ├── run_bot.py           # Запуск бота
│   └── requirements.txt     # Зависимости бота
│
├── parser/                   # Avito parser
│   ├── avito_parser.py      # Основной парсер
│   ├── run_parser.py        # Запуск парсера
│   ├── test_parser.py       # Тесты парсера
│   ├── image_optimizer.py   # Оптимизация изображений
│   └── requirements.txt     # Зависимости парсера
│
├── tools/                   # Утилиты
│   ├── add_cars.py         # Ручное добавление автомобилей
│   └── car_template.md     # Шаблон автомобиля
│
├── docs/                   # Документация
│   ├── AVITO_PARSER_SETUP.md
│   └── TELEGRAM_SETUP.md
│
├── hugo-site/             # Hugo website
│   ├── hugo.toml
│   ├── content/
│   ├── layouts/
│   ├── static/
│   └── ...
│
└── .github/              # GitHub Actions
    └── workflows/
        └── hugo.yml
```
