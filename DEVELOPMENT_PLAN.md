# План разработки Hugo Автоломбард

## ✅ Окончательный выбор: Hugo

### Почему Hugo идеален для автоломбарда:
- ⚡ **Скорость разработки**: 3 дня вместо 10
- 🎨 **Готовые темы**: Automotive Hugo Theme
- 🚀 **Производительность**: Lighthouse Score 95-100
- 📱 **Telegram готовность**: Нативная поддержка Web Apps
- 🔍 **SEO из коробки**: Автоматические метатеги и структурированные данные
- 💰 **Экономия времени**: 70% меньше кода

## Финальная архитектура

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Telegram Bot  │────│   Hugo Website   │────│  Static Files   │
│                 │    │                  │    │                 │
│ - Web App кнопка│    │ - Автогенерация  │    │ - HTML/CSS/JS   │
│ - Deep links    │    │ - Фильтры        │    │ - Изображения   │
│ - Команды       │    │ - Поиск          │    │ - JSON API      │
│ - aiogram       │    │ - SEO            │    │ - Sitemap       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                       ┌──────────────────┐
                       │   Hugo Build     │
                       │                  │
                       │ - Markdown→HTML  │
                       │ - Data→Pages     │
                       │ - Themes         │
                       │ - Минификация    │
                       └──────────────────┘
```

## Структура Hugo проекта

```
tg_bot_auto_lombard/
├── hugo-site/                    # Hugo сайт
│   ├── config.yaml              # Конфигурация
│   ├── content/                 # Контент
│   │   ├── _index.md           # Главная
│   │   ├── about.md            # О нас
│   │   ├── contact.md          # Контакты
│   │   └── cars/               # Автомобили
│   │       ├── _index.md       # Каталог
│   │       ├── bmw-x5-2019.md
│   │       └── mercedes-e200.md
│   ├── data/                   # Данные
│   │   ├── cars.json          # База автомобилей
│   │   ├── brands.json        # Справочник марок
│   │   └── settings.json      # Настройки
│   ├── static/                # Статика
│   │   ├── images/cars/       # Фото автомобилей
│   │   ├── js/                # JavaScript
│   │   └── css/               # Доп. стили
│   ├── themes/                # Темы
│   │   └── automotive/        # Автомобильная тема
│   └── public/                # Готовый сайт
├── bot/                       # Telegram бот
│   └── main.py               # aiogram бот
├── docker-compose.yml        # Оркестрация
└── docs/                     # Документация
```

## 📅 Детальный план: 3 дня

### 🏗️ День 1: Настройка Hugo (3-4 часа)

#### Утро (1.5-2 часа): Установка и базовая настройка
```bash
# 1. Установка Hugo
brew install hugo

# 2. Создание проекта
hugo new site hugo-site
cd hugo-site

# 3. Установка темы
git submodule add https://github.com/themefisher/automotive-hugo themes/automotive
echo 'theme = "automotive"' >> config.yaml

# 4. Базовая конфигурация
```

**Результат**: Рабочий Hugo сайт с темой

#### День (1.5-2 часа): Импорт данных и контента
```bash
# 1. Конвертация JSON данных в Markdown
python scripts/convert_cars_to_markdown.py

# 2. Настройка конфигурации
# config.yaml - основные параметры

# 3. Создание базового контента
hugo new _index.md
hugo new about.md
hugo new contact.md
hugo new cars/_index.md
```

**Результат**: Структура сайта с данными автомобилей

#### Контрольная точка Дня 1
- ✅ Hugo установлен и работает
- ✅ Тема подключена
- ✅ Данные автомобилей импортированы
- ✅ Базовые страницы созданы
- ✅ Сайт собирается без ошибок

---

### 🎨 День 2: Кастомизация и функциональность (4-5 часов)

#### Утро (2-2.5 часа): Адаптация темы
```bash
# 1. Кастомизация стилей
# assets/css/custom.css

# 2. Настройка логотипа и брендинга
# static/images/logo.png

# 3. Конфигурация меню и навигации
# config.yaml - menu section

# 4. Настройка главной страницы
# content/_index.md + data/homepage.yml
```

#### День (1.5-2 часа): Фильтры и поиск
```javascript
// static/js/catalog.js
class CarCatalog {
  // Реализация фильтрации
  // Интеграция с Hugo данными
  // Поиск через Fuse.js
}
```

#### Вечер (1 час): Telegram интеграция
```html
<!-- layouts/partials/telegram-webapp.html -->
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script>
window.Telegram.WebApp.ready();
// Адаптация темы
// Навигация
// Haptic feedback
</script>
```

#### Контрольная точка Дня 2
- ✅ Тема адаптирована под бренд
- ✅ Фильтры работают
- ✅ Поиск функционирует
- ✅ Telegram Web App интегрирован
- ✅ Мобильная версия оптимизирована

---

### 🚀 День 3: Финализация и деплой (2-3 часа)

#### Утро (1-1.5 часа): SEO и оптимизация
```yaml
# config.yaml
minify:
  tdewolff:
    html:
      keepWhitespace: false

# Настройка Schema.org
# Open Graph метатеги
# Sitemap генерация
```

#### День (1-1.5 часа): Docker и деплой
```dockerfile
# Dockerfile.hugo
FROM hugomods/hugo:exts as builder
# ...сборка Hugo

FROM nginx:alpine
# ...финальный образ
```

```yaml
# docker-compose.yml
services:
  hugo-build:
    build: ./docker/hugo.Dockerfile
  web:
    image: nginx:alpine
  bot:
    build: ./docker/bot.Dockerfile
```

#### Контрольная точка Дня 3
- ✅ SEO настроено
- ✅ Производительность оптимизирована
- ✅ Docker контейнеры готовы
- ✅ Все тестируется корректно

---

## 🛠 Конкретные файлы для создания

### 1. Конфигурация Hugo
```yaml
# hugo-site/config.yaml
baseURL: 'https://auto-lombard.ru'
languageCode: 'ru-RU'
title: 'Автоломбард - Каталог автомобилей'
theme: 'automotive'

params:
  company_name: 'Автоломбард'
  phone: '+7 (999) 123-45-67'
  email: 'info@auto-lombard.ru'
  address: 'Москва, ул. Примерная, 123'
  
  telegram_integration: true
  telegram_bot: '@auto_lombard_bot'
  
  cars_per_page: 12
  featured_cars_count: 6

taxonomies:
  brand: 'brands'
  body_type: 'body_types'
  fuel_type: 'fuel_types'

menu:
  main:
    - name: 'Главная'
      url: '/'
    - name: 'Каталог'  
      url: '/cars/'
    - name: 'О нас'
      url: '/about/'
    - name: 'Контакты'
      url: '/contact/'
```

### 2. Пример автомобиля
```markdown
# hugo-site/content/cars/bmw-x5-2019.md
---
title: "BMW X5 2019"
date: 2024-01-15T00:00:00Z
draft: false

brand: "BMW"
model: "X5"
year: 2019
price: 2500000
currency: "₽"
mileage: 75000

engine:
  volume: "3.0"
  type: "Бензин"
  power: 249
transmission: "Автоматическая"
drive: "Полный"
body: "Внедорожник"
color: "Черный"
condition: "Отличное"

images:
  - "/images/cars/bmw-x5-2019/main.webp"
  - "/images/cars/bmw-x5-2019/interior.webp"

features:
  - "Кожаный салон"
  - "Панорамная крыша"
  - "Система навигации"

contact:
  manager: "Иван Петров"
  phone: "+7 (999) 123-45-67"
  telegram: "@manager_ivan"

description: "BMW X5 2019 в отличном состоянии"
keywords: ["BMW X5", "2019", "автоломбард"]

status: "available"
featured: true

brands: ["BMW"]
body_types: ["Внедорожник"]
fuel_types: ["Бензин"]
---

Автомобиль в отличном состоянии...
```

### 3. Telegram Bot
```python
# bot/main.py
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://auto-lombard.ru")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_webapp_keyboard():
    web_app = WebAppInfo(url=WEB_APP_URL)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(
            text="🚗 Открыть каталог автомобилей", 
            web_app=web_app
        )]],
        resize_keyboard=True
    )
    return keyboard

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в автоломбард!\n\n"
        "Нажмите кнопку ниже, чтобы посмотреть доступные автомобили:",
        reply_markup=get_webapp_keyboard()
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "🤖 Команды бота:\n\n"
        "/start - Главное меню\n"
        "/catalog - Открыть каталог\n"
        "/contact - Контакты\n"
        "/help - Эта справка"
    )

@dp.message(Command("catalog"))
async def catalog_command(message: types.Message):
    await message.answer(
        "🚗 Открываю каталог автомобилей...",
        reply_markup=get_webapp_keyboard()
    )

@dp.message(Command("contact"))
async def contact_command(message: types.Message):
    await message.answer(
        "📞 Наши контакты:\n\n"
        "☎️ Телефон: +7 (999) 123-45-67\n"
        "📧 Email: info@auto-lombard.ru\n"
        "📍 Адрес: Москва, ул. Примерная, 123\n\n"
        "🕐 Режим работы: ПН-ВС с 9:00 до 21:00"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

### 4. Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  hugo-build:
    build:
      context: .
      dockerfile: docker/hugo.Dockerfile
    volumes:
      - hugo-site:/site

  web:
    image: nginx:alpine
    volumes:
      - hugo-site:/usr/share/nginx/html:ro
      - ./docker/nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - hugo-build

  bot:
    build:
      context: .
      dockerfile: docker/bot.Dockerfile
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - WEB_APP_URL=https://auto-lombard.ru
    restart: unless-stopped

volumes:
  hugo-site:
```

## 🎯 Критерии качества

### Hugo Website
- ✅ Lighthouse Score > 95
- ✅ Сборка < 5 секунд
- ✅ Все страницы автогенерированы
- ✅ SEO метатеги на всех страницах
- ✅ Адаптивный дизайн

### Telegram Integration
- ✅ Web App открывается в боте
- ✅ Тема адаптируется автоматически
- ✅ Haptic feedback работает
- ✅ Навигация интуитивная

### Функциональность
- ✅ Фильтры работают без перезагрузки
- ✅ Поиск находит релевантные результаты
- ✅ Изображения в WebP формате
- ✅ Lazy loading реализован

## 🚀 Инструменты для быстрого старта

### Скрипт конвертации данных
```python
# scripts/convert_cars_to_markdown.py
import json
import os
from datetime import datetime

def convert_cars_to_hugo():
    with open('web/assets/data/cars.json', 'r', encoding='utf-8') as f:
        cars = json.load(f)
    
    os.makedirs('hugo-site/content/cars', exist_ok=True)
    
    for car in cars:
        filename = f"{car['brand'].lower()}-{car['model'].lower()}-{car['year']}.md"
        filename = filename.replace(' ', '-')
        
        content = f"""---
title: "{car['brand']} {car['model']} {car['year']}"
date: {car['created_at']}
draft: false

brand: "{car['brand']}"
model: "{car['model']}"
year: {car['year']}
price: {car['price']}
currency: "{car['currency']}"
mileage: {car['mileage']}

engine:
  volume: "{car['engine']['volume']}"
  type: "{car['engine']['type']}"
  power: {car['engine']['power']}
transmission: "{car['transmission']}"
drive: "{car['drive']}"
body: "{car['body']}"
color: "{car['color']}"
condition: "{car['condition']}"

images:
{chr(10).join(f'  - "{img}"' for img in car['images'])}

features:
{chr(10).join(f'  - "{feature}"' for feature in car['features'])}

contact:
  manager: "{car['contacts']['manager']}"
  phone: "{car['contacts']['phone']}"
  telegram: "{car['contacts']['telegram']}"

description: "{car['description'][:150]}..."
keywords: ["{car['brand']}", "{car['year']}", "автоломбард"]

status: "{car['status']}"
featured: {'true' if car.get('featured') else 'false'}

brands: ["{car['brand']}"]
body_types: ["{car['body']}"]
fuel_types: ["{car['engine']['type']}"]
---

{car['description']}
"""
        
        with open(f'hugo-site/content/cars/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    convert_cars_to_hugo()
    print("✅ Автомобили конвертированы в Hugo формат!")
```

## ✅ Готовы начинать?

**Преимущества Hugo подхода:**
- 🔥 **3 дня** вместо 10
- 🎨 **Готовая тема** для автомобилей
- ⚡ **Мгновенная** загрузка сайта
- 📱 **Perfect** Telegram интеграция
- 🔍 **Автоматическое** SEO
- 💰 **70% экономии** времени

Начинаем с Дня 1?