# Архитектура автоломбарда: Hugo + Telegram бот

## Обзор проекта

Разрабатываем платформу автоломбарда с использованием Hugo и интеграцией с Telegram:
- **Hugo-сайт**: Статический каталог автомобилей с фильтрами и поиском
- **Telegram бот**: Интеграция с веб-приложением через Web Apps API
- **Docker**: Контейнеризация всех компонентов

## ✅ Выбранный технологический стек

### Frontend: Hugo (Go)
- **Генератор**: Hugo v0.119+
- **Тема**: Automotive Hugo Theme (готовая)
- **Стилизация**: Tailwind CSS (встроенная в тему)
- **JavaScript**: Vanilla JS для интерактивности
- **Изображения**: WebP формат с lazy loading

### Backend & Infrastructure
- **Веб-сервер**: Nginx (статические файлы)
- **Данные**: JSON файлы + Hugo Data Files
- **Telegram Bot**: Python + aiogram
- **Контейнеризация**: Docker + Docker Compose
- **Сборка**: Hugo CLI

### Telegram Integration
- **Web Apps API**: Для встраивания сайта в бот
- **Bot API**: Для команд и навигации
- **Deep linking**: Прямые ссылки на автомобили

## Архитектура системы

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Telegram Bot  │────│   Hugo Website   │────│  Static Files   │
│                 │    │                  │    │                 │
│ - Web App кнопка│    │ - Автогенерация  │    │ - HTML/CSS/JS   │
│ - /start, /help │    │ - Фильтры        │    │ - Изображения   │
│ - Команды       │    │ - Поиск          │    │ - JSON данные   │
│ - Deep links    │    │ - Карточки авто  │    │ - Sitemap       │
└─────────────────┘    │ - SEO            │    └─────────────────┘
                       └──────────────────┘
                                │
                       ┌──────────────────┐
                       │   Hugo Build     │
                       │                  │
                       │ - Темы           │
                       │ - Шаблоны        │
                       │ - Контент        │
                       │ - Данные         │
                       └──────────────────┘
```

## Структура проекта Hugo

```
tg_bot_auto_lombard/
├── hugo-site/                    # Hugo сайт
│   ├── config.yaml              # Конфигурация Hugo
│   ├── content/                 # Контент
│   │   ├── _index.md           # Главная страница
│   │   ├── about.md            # О компании
│   │   ├── contact.md          # Контакты
│   │   └── cars/               # Автомобили
│   │       ├── _index.md       # Каталог
│   │       ├── bmw-x5-2019.md
│   │       └── mercedes-e200-2020.md
│   ├── data/                   # Данные
│   │   ├── cars.json          # База автомобилей
│   │   ├── brands.json        # Справочник марок
│   │   └── settings.json      # Настройки сайта
│   ├── static/                # Статические файлы
│   │   ├── images/
│   │   │   ├── cars/          # Фото автомобилей
│   │   │   ├── logo/          # Логотипы
│   │   │   └── icons/         # Иконки
│   │   ├── js/                # JavaScript
│   │   │   ├── search.js      # Поиск
│   │   │   ├── filters.js     # Фильтры
│   │   │   └── telegram.js    # Telegram Web App
│   │   └── css/               # Дополнительные стили
│   ├── layouts/               # Шаблоны (если кастомизация)
│   │   ├── _default/
│   │   ├── partials/
│   │   └── shortcodes/
│   ├── themes/                # Темы Hugo
│   │   └── automotive/        # Автомобильная тема
│   └── public/                # Готовый сайт (генерируется)
├── bot/                       # Telegram бот
│   ├── main.py               # Основной файл бота
│   ├── handlers/             # Обработчики команд
│   └── utils/               # Утилиты
├── docker/                   # Docker конфигурации
│   ├── hugo.Dockerfile      # Hugo сборка
│   ├── bot.Dockerfile       # Bot контейнер
│   └── nginx.Dockerfile     # Nginx контейнер
├── docker-compose.yml       # Оркестрация
└── docs/                    # Документация
```

## Структура данных

### Автомобиль в Hugo
```yaml
# content/cars/bmw-x5-2019.md
---
title: "BMW X5 2019"
date: 2024-01-15T00:00:00Z
draft: false

# Основная информация
brand: "BMW"
model: "X5"
year: 2019
price: 2500000
currency: "₽"
mileage: 75000

# Технические характеристики
engine:
  volume: "3.0"
  type: "Бензин"
  power: 249
transmission: "Автоматическая"
drive: "Полный"
body: "Внедорожник"
color: "Черный"
condition: "Отличное"

# Медиа
images:
  - "/images/cars/bmw-x5-2019/main.webp"
  - "/images/cars/bmw-x5-2019/interior.webp"
  - "/images/cars/bmw-x5-2019/engine.webp"

# Характеристики
features:
  - "Кожаный салон"
  - "Панорамная крыша"
  - "Система навигации"
  - "Пневмоподвеска"

# Контакты
contact:
  manager: "Иван Петров"
  phone: "+7 (999) 123-45-67"
  telegram: "@manager_ivan"

# SEO
description: "BMW X5 2019 в отличном состоянии. Цена 2,500,000 ₽"
keywords: ["BMW X5", "2019", "автоломбард", "внедорожник"]

# Статус
status: "available"
featured: true
---

Автомобиль в отличном состоянии...
```

## Функциональные возможности

### Hugo Website
1. **Автогенерация страниц**
   - Страницы автомобилей из Markdown файлов
   - Автоматический каталог с пагинацией
   - Генерация меню и навигации

2. **Фильтрация и поиск**
   ```go
   {{ range (where .Site.RegularPages "Params.brand" "BMW") }}
     {{ partial "car-card.html" . }}
   {{ end }}
   ```

3. **SEO оптимизация**
   - Автоматические meta-теги
   - Structured data для автомобилей
   - Sitemap генерация
   - RSS фиды

4. **Производительность**
   - Статические файлы
   - Минификация CSS/JS
   - Оптимизация изображений
   - CDN готовность

### Telegram Bot Integration
1. **Web App кнопка**
   ```python
   web_app = WebAppInfo(url="https://auto-lombard.ru")
   keyboard = ReplyKeyboardMarkup(
       keyboard=[[KeyboardButton(
           text="🚗 Каталог автомобилей", 
           web_app=web_app
       )]],
       resize_keyboard=True
   )
   ```

2. **Deep linking**
   ```python
   # Ссылка на конкретный автомобиль
   car_url = f"https://auto-lombard.ru/cars/bmw-x5-2019/"
   ```

3. **Telegram API интеграция**
   ```javascript
   // В Hugo теме
   window.Telegram.WebApp.ready();
   window.Telegram.WebApp.expand();
   ```

## Конфигурация Hugo

### config.yaml
```yaml
baseURL: 'https://auto-lombard.ru'
languageCode: 'ru-RU'
title: 'Автоломбард - Каталог автомобилей'
theme: 'automotive'

# Настройки сайта
params:
  description: 'Лучшие автомобили в автоломбарде'
  phone: '+7 (999) 123-45-67'
  email: 'info@auto-lombard.ru'
  address: 'Москва, ул. Примерная, 123'
  
  # Telegram
  telegram_integration: true
  telegram_bot: '@auto_lombard_bot'
  
  # Каталог
  cars_per_page: 12
  featured_cars_count: 6
  
  # SEO
  google_analytics: 'G-XXXXXXXXXX'

# Таксономии для фильтров
taxonomies:
  brand: 'brands'
  body_type: 'body_types'
  fuel_type: 'fuel_types'
  tag: 'tags'

# Форматы вывода
outputs:
  home: ["HTML", "RSS", "JSON"]
  section: ["HTML", "RSS"]

# Меню
menu:
  main:
    - name: 'Главная'
      url: '/'
      weight: 1
    - name: 'Каталог'
      url: '/cars/'
      weight: 2
    - name: 'О нас'
      url: '/about/'
      weight: 3
    - name: 'Контакты'
      url: '/contact/'
      weight: 4
```

## Преимущества Hugo для автоломбарда

### 1. Производительность
- ⚡ Сборка сайта за секунды
- 🚀 Lighthouse Score 95-100
- 📱 Perfect Mobile Performance
- 🔍 Отличное SEO

### 2. Удобство разработки
- 🎨 Готовые автомобильные темы
- 🔧 Простая кастомизация
- 📊 Автоматическая генерация страниц
- 🔄 Горячая перезагрузка при разработке

### 3. Масштабируемость
- 📈 Легко добавлять новые автомобили
- 🏗️ Модульная архитектура
- 🌐 CDN friendly
- 💾 Минимальные требования к серверу

### 4. Telegram интеграция
- 📱 Нативная поддержка Web Apps
- ⚡ Быстрая загрузка в Telegram
- 🔗 Deep linking на автомобили
- 📊 Аналитика переходов

## Обновленный план разработки

### День 1: Настройка Hugo (2-3 часа)
- ✅ Установка Hugo
- ✅ Выбор и установка темы
- ✅ Базовая конфигурация
- ✅ Импорт данных автомобилей

### День 2: Кастомизация (4-5 часов)
- ✅ Адаптация темы под бренд
- ✅ Настройка фильтров
- ✅ Telegram Web App интеграция
- ✅ Мобильная оптимизация

### День 3: Контент и оптимизация (2-3 часа)
- ✅ Добавление контента
- ✅ SEO настройки
- ✅ Тестирование производительности
- ✅ Финальные правки

**Итого: 3 дня вместо 10!** 🎉

## Следующие шаги

1. **Установка Hugo** - начинаем с базовой настройки
2. **Выбор темы** - находим подходящую автомобильную тему
3. **Импорт данных** - переносим наши данные об автомобилях
4. **Кастомизация** - адаптируем под наши нужды
5. **Telegram интеграция** - подключаем к боту

Готовы начинать?