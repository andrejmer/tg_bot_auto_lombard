# Быстрый старт с Hugo для автоломбарда

## 🚀 Установка и настройка (5 минут)

### 1. Установка Hugo
```bash
# macOS
brew install hugo

# Проверка
hugo version
```

### 2. Создание проекта
```bash
# Создание нового сайта
hugo new site auto-lombard
cd auto-lombard

# Инициализация git
git init
```

### 3. Добавление темы для автомобилей
```bash
# Добавляем тему как submodule
git submodule add https://github.com/themefisher/bigspring-hugo themes/bigspring

# Или используем готовую автомобильную тему
git submodule add https://github.com/gethugothemes/automotive-hugo themes/automotive
```

## ⚙️ Конфигурация

### config.yaml
```yaml
baseURL: 'https://auto-lombard.ru'
languageCode: 'ru-RU'
title: 'Автоломбард - Каталог автомобилей'
theme: 'automotive'

params:
  # Основные настройки
  description: 'Лучшие автомобили в автоломбарде'
  author: 'Автоломбард'
  logo: '/images/logo.png'

  # Контакты
  phone: '+7 (999) 123-45-67'
  email: 'info@auto-lombard.ru'
  address: 'Москва, ул. Примерная, 123'

  # Telegram интеграция
  telegram_integration: true
  telegram_bot: '@your_bot'

  # Функции каталога
  filters:
    enabled: true
    brands: true
    price_range: true
    year_range: true
    mileage: true

  search:
    enabled: true
    placeholder: 'Найти автомобиль...'

  # SEO
  meta_keywords: 'автоломбард, купить автомобиль, б/у авто'
  google_analytics: 'G-XXXXXXXXXX'

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

# Языки
languages:
  ru:
    languageName: 'Русский'
    weight: 1
```

## 📁 Структура контента

### 1. Главная страница
```markdown
# content/_index.md
---
title: "Автоломбард - Лучшие автомобили"
description: "Большой выбор качественных автомобилей с пробегом"
hero:
  title: "Найдите свой идеальный автомобиль"
  subtitle: "Более 100 проверенных автомобилей в наличии"
  background: "/images/hero-bg.jpg"
  search_enabled: true

featured_cars:
  - "bmw-x5-2019"
  - "mercedes-e200-2020"
  - "audi-a6-2021"

benefits:
  - title: "Проверенное качество"
    description: "Все автомобили проходят техническую проверку"
    icon: "🔧"
  - title: "Честные цены"
    description: "Справедливая оценка без скрытых платежей"
    icon: "💰"
  - title: "Быстрое оформление"
    description: "Документы за 30 минут"
    icon: "⚡"
---

Добро пожаловать в наш автоломбард! Мы предлагаем большой выбор качественных автомобилей с пробегом по выгодным ценам.
```

### 2. Страницы автомобилей
```markdown
# content/cars/bmw-x5-2019.md
---
title: "BMW X5 2019"
date: 2024-01-15
brand: "BMW"
model: "X5"
year: 2019
price: 2500000
currency: "₽"
mileage: 75000
fuel: "Бензин"
transmission: "Автоматическая"
drive: "Полный"
engine_volume: "3.0"
engine_power: 249
color: "Черный"
condition: "Отличное"
vin: "WBA5A5C50FD123456"

# Изображения
images:
  - "/images/cars/bmw-x5-2019/main.jpg"
  - "/images/cars/bmw-x5-2019/interior.jpg"
  - "/images/cars/bmw-x5-2019/engine.jpg"

# Характеристики
features:
  - "Кожаный салон"
  - "Панорамная крыша"
  - "Система навигации"
  - "Пневмоподвеска"
  - "Камера заднего вида"

# Контакты
contact:
  manager: "Иван Петров"
  phone: "+7 (999) 123-45-67"
  telegram: "@manager_ivan"

# SEO
meta_description: "BMW X5 2019 в отличном состоянии. Цена 2,500,000 ₽. Один владелец, полная история обслуживания."
keywords: ["BMW X5", "2019", "автоломбард", "внедорожник"]

# Статус
status: "available" # available, sold, reserved
featured: true
---

Автомобиль в отличном состоянии. Один владелец, полная история обслуживания у официального дилера. Все ТО пройдены вовремя. Максимальная комплектация с пневмоподвеской и панорамной крышей.

## Технические характеристики

- **Двигатель:** 3.0L V6 Turbo
- **Мощность:** 249 л.с.
- **Крутящий момент:** 450 Нм
- **Разгон 0-100 км/ч:** 6.5 сек
- **Максимальная скорость:** 230 км/ч
- **Расход топлива:** 9.8 л/100км (смешанный)

## Комплектация

- Адаптивная пневматическая подвеска
- Полноценная кожаная отделка салона
- Панорамная стеклянная крыша
- Профессиональная навигационная система
- Камера заднего вида с динамическими линиями
- Парковочный ассистент
- Ксеноновые адаптивные фары
- Трехзонный автоматический климат-контроль
```

## 🎨 Шаблоны Hugo

### layouts/index.html (Главная)
```html
{{ define "main" }}
<section class="hero">
  <div class="container">
    <h1>{{ .Params.hero.title }}</h1>
    <p>{{ .Params.hero.subtitle }}</p>

    {{ if .Params.hero.search_enabled }}
    <div class="search-form">
      <input type="text" id="car-search" placeholder="Поиск автомобиля...">
      <select id="brand-filter">
        <option value="">Все марки</option>
        {{ range .Site.Data.brands }}
        <option value="{{ .slug }}">{{ .name }}</option>
        {{ end }}
      </select>
      <button type="submit">Найти</button>
    </div>
    {{ end }}
  </div>
</section>

<section class="featured-cars">
  <div class="container">
    <h2>Рекомендуемые автомобили</h2>
    <div class="cars-grid">
      {{ range .Params.featured_cars }}
        {{ with $.Site.GetPage (printf "/cars/%s" .) }}
          {{ partial "car-card.html" . }}
        {{ end }}
      {{ end }}
    </div>
  </div>
</section>

<section class="benefits">
  <div class="container">
    <h2>Наши преимущества</h2>
    <div class="benefits-grid">
      {{ range .Params.benefits }}
      <div class="benefit-card">
        <div class="icon">{{ .icon }}</div>
        <h3>{{ .title }}</h3>
        <p>{{ .description }}</p>
      </div>
      {{ end }}
    </div>
  </div>
</section>
{{ end }}
```

### layouts/cars/list.html (Каталог)
```html
{{ define "main" }}
<section class="catalog">
  <div class="container">
    <h1>Каталог автомобилей</h1>

    <!-- Фильтры -->
    <div class="filters">
      <div class="filter-group">
        <label>Марка:</label>
        <select id="brand-filter">
          <option value="">Все марки</option>
          {{ $brands := slice }}
          {{ range .Pages }}
            {{ $brands = $brands | append .Params.brand }}
          {{ end }}
          {{ range $brands | uniq }}
          <option value="{{ . }}">{{ . }}</option>
          {{ end }}
        </select>
      </div>

      <div class="filter-group">
        <label>Цена от:</label>
        <input type="number" id="price-min" placeholder="От">
      </div>

      <div class="filter-group">
        <label>Цена до:</label>
        <input type="number" id="price-max" placeholder="До">
      </div>

      <div class="filter-group">
        <label>Сортировка:</label>
        <select id="sort-by">
          <option value="date">По дате</option>
          <option value="price-asc">Цена: по возрастанию</option>
          <option value="price-desc">Цена: по убыванию</option>
          <option value="year">По году</option>
        </select>
      </div>
    </div>

    <!-- Результаты -->
    <div class="cars-grid" id="cars-container">
      {{ range .Pages }}
        {{ partial "car-card.html" . }}
      {{ end }}
    </div>

    <!-- Пагинация -->
    {{ template "_internal/pagination.html" . }}
  </div>
</section>
{{ end }}
```

### layouts/partials/car-card.html
```html
<div class="car-card"
     data-brand="{{ .Params.brand }}"
     data-price="{{ .Params.price }}"
     data-year="{{ .Params.year }}">

  <div class="car-image">
    {{ with index .Params.images 0 }}
    <img src="{{ . }}" alt="{{ $.Title }}" loading="lazy">
    {{ end }}

    {{ if .Params.featured }}
    <span class="featured-badge">Хит</span>
    {{ end }}
  </div>

  <div class="car-info">
    <h3><a href="{{ .Permalink }}">{{ .Title }}</a></h3>

    <div class="car-price">
      {{ .Params.price | printf "%s %s" (lang.FormatNumber 0 .) .Params.currency }}
    </div>

    <div class="car-details">
      <span>{{ .Params.year }} г.</span>
      <span>{{ .Params.mileage | lang.FormatNumber 0 }} км</span>
      <span>{{ .Params.engine_volume }}L</span>
    </div>

    <div class="car-features">
      {{ range first 3 .Params.features }}
      <span class="feature">{{ . }}</span>
      {{ end }}
    </div>

    <div class="car-actions">
      <a href="{{ .Permalink }}" class="btn btn-primary">Подробнее</a>
      <button class="btn btn-secondary" onclick="contactManager('{{ .Params.contact.phone }}')">
        Связаться
      </button>
    </div>
  </div>
</div>
```

## 📱 Telegram Web App интеграция

### layouts/partials/telegram-webapp.html
```html
{{ if .Site.Params.telegram_integration }}
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script>
// Инициализация Telegram Web App
window.Telegram.WebApp.ready();
window.Telegram.WebApp.expand();

// Применение темы Telegram
if (window.Telegram.WebApp.colorScheme === 'dark') {
  document.body.classList.add('telegram-dark');
}

// Главная кнопка для связи
function contactManager(phone) {
  if (window.Telegram && window.Telegram.WebApp) {
    window.Telegram.WebApp.openTelegramLink(`https://t.me/share/url?url=${encodeURIComponent(phone)}`);
  } else {
    window.location.href = `tel:${phone}`;
  }
}

// Кнопка назад
window.Telegram.WebApp.BackButton.onClick(() => {
  history.back();
});
</script>
{{ end }}
```

## 🚀 Команды для запуска

```bash
# Разработка
hugo server -D

# Сборка
hugo --minify

# Сборка для продакшна
hugo --minify --baseURL="https://auto-lombard.ru"
```

## ⏱️ Время разработки с Hugo

**День 1 (2-3 часа):**
- ✅ Установка Hugo и темы
- ✅ Базовая конфигурация
- ✅ Импорт данных автомобилей
- ✅ Первый рабочий прототип

**День 2 (4-5 часов):**
- ✅ Кастомизация дизайна
- ✅ Настройка фильтров
- ✅ Telegram интеграция

**Итого: 2 дня вместо 10!** 🎉

Хотите попробовать этот подход?
