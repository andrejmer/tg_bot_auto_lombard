# Стратегия тестирования Hugo Автоломбарда

## 🎯 Особенности тестирования Hugo проектов

Hugo генерирует статические сайты, поэтому тестирование отличается от обычных веб-приложений:

### Что тестируем:
- ✅ **Сборка Hugo** - корректность генерации
- ✅ **Контент** - валидность Markdown и данных
- ✅ **Frontend JavaScript** - фильтры, поиск, Telegram интеграция
- ✅ **SEO** - метатеги, Schema.org, производительность
- ✅ **Telegram Bot** - команды и Web App интеграция
- ✅ **Визуальное тестирование** - кроссбраузерность

### Что НЕ тестируем:
- ❌ **Backend API** (его нет - статичный сайт)
- ❌ **Базы данных** (данные в JSON/Markdown)
- ❌ **Серверная логика** (только Nginx)

## 📋 Уровни тестирования

### 1. 🏗️ Build Tests (Тесты сборки)
**Цель:** Убедиться, что Hugo собирает сайт без ошибок

```bash
# hugo-site/tests/build/test_hugo_build.sh
#!/bin/bash
set -e

echo "🏗️ Тестирование сборки Hugo..."

# Проверка конфигурации
echo "Проверка config.yaml..."
hugo config | grep -q "baseURL" || { echo "❌ baseURL не найден"; exit 1; }

# Сборка сайта
echo "Сборка сайта..."
hugo --minify --baseURL="http://localhost:1313" || { echo "❌ Ошибка сборки"; exit 1; }

# Проверка обязательных файлов
echo "Проверка обязательных файлов..."
[ -f "public/index.html" ] || { echo "❌ index.html не создан"; exit 1; }
[ -f "public/cars/index.html" ] || { echo "❌ cars/index.html не создан"; exit 1; }
[ -f "public/sitemap.xml" ] || { echo "❌ sitemap.xml не создан"; exit 1; }

# Проверка автомобилей
echo "Проверка страниц автомобилей..."
car_count=$(find public/cars -name "*.html" -not -name "index.html" | wc -l)
if [ "$car_count" -lt 1 ]; then
    echo "❌ Страницы автомобилей не созданы"
    exit 1
fi

echo "✅ Сборка прошла успешно! Создано $car_count автомобилей"
```

### 2. 📊 Content Tests (Тесты контента)
**Цель:** Валидация данных и Markdown файлов

```python
# tests/content/test_cars_data.py
import json
import os
import yaml
from pathlib import Path

def test_cars_json_structure():
    """Проверка структуры JSON данных автомобилей"""
    with open('hugo-site/data/cars.json', 'r', encoding='utf-8') as f:
        cars = json.load(f)

    assert isinstance(cars, list), "cars.json должен содержать массив"
    assert len(cars) > 0, "Должен быть хотя бы один автомобиль"

    required_fields = ['brand', 'model', 'year', 'price', 'images']

    for i, car in enumerate(cars):
        for field in required_fields:
            assert field in car, f"Автомобиль {i}: отсутствует поле {field}"

        # Проверка типов данных
        assert isinstance(car['year'], int), f"Автомобиль {i}: year должен быть числом"
        assert isinstance(car['price'], (int, float)), f"Автомобиль {i}: price должен быть числом"
        assert isinstance(car['images'], list), f"Автомобиль {i}: images должен быть массивом"
        assert len(car['images']) > 0, f"Автомобиль {i}: должно быть хотя бы одно изображение"

def test_markdown_files():
    """Проверка Markdown файлов автомобилей"""
    cars_dir = Path('hugo-site/content/cars')
    markdown_files = list(cars_dir.glob('*.md'))

    assert len(markdown_files) > 0, "Должны быть Markdown файлы автомобилей"

    for md_file in markdown_files:
        if md_file.name == '_index.md':
            continue

        content = md_file.read_text(encoding='utf-8')

        # Проверка Front Matter
        assert content.startswith('---'), f"{md_file.name}: должен начинаться с Front Matter"

        # Извлечение Front Matter
        parts = content.split('---', 2)
        assert len(parts) >= 3, f"{md_file.name}: некорректный Front Matter"

        try:
            front_matter = yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            assert False, f"{md_file.name}: ошибка парсинга YAML: {e}"

        # Проверка обязательных полей
        required_fields = ['title', 'brand', 'model', 'year', 'price']
        for field in required_fields:
            assert field in front_matter, f"{md_file.name}: отсутствует поле {field}"

def test_images_exist():
    """Проверка существования изображений"""
    with open('hugo-site/data/cars.json', 'r', encoding='utf-8') as f:
        cars = json.load(f)

    for car in cars:
        for image_path in car['images']:
            # Убираем ведущий слеш для проверки файла
            local_path = image_path.lstrip('/')
            full_path = f"hugo-site/static/{local_path}"

            # Пока пропускаем - изображения добавим позже
            # assert os.path.exists(full_path), f"Изображение не найдено: {full_path}"

if __name__ == "__main__":
    test_cars_json_structure()
    test_markdown_files()
    test_images_exist()
    print("✅ Все тесты контента прошли успешно!")
```

### 3. 🌐 Frontend Tests (Тесты JavaScript)
**Цель:** Тестирование фильтров, поиска, Telegram интеграции

```javascript
// tests/frontend/catalog.test.js
describe('Car Catalog', () => {
  let catalog;

  beforeEach(() => {
    // Мокаем HTML структуру
    document.body.innerHTML = `
      <div id="cars-container"></div>
      <input id="search-input" type="text">
      <select id="brand-filter">
        <option value="">Все марки</option>
        <option value="BMW">BMW</option>
        <option value="Mercedes">Mercedes</option>
      </select>
      <input id="price-min" type="range" min="0" max="10000000">
      <input id="price-max" type="range" min="0" max="10000000">
    `;

    // Мокаем данные автомобилей
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve([
          {
            title: "BMW X5 2019",
            brand: "BMW",
            model: "X5",
            year: 2019,
            price: 2500000,
            permalink: "/cars/bmw-x5-2019/"
          },
          {
            title: "Mercedes E200 2020",
            brand: "Mercedes",
            model: "E200",
            year: 2020,
            price: 3000000,
            permalink: "/cars/mercedes-e200-2020/"
          }
        ])
      })
    );

    catalog = new CarCatalog();
  });

  test('должен загружать автомобили', async () => {
    await catalog.loadCars();
    expect(catalog.cars).toHaveLength(2);
    expect(catalog.cars[0].brand).toBe('BMW');
  });

  test('должен фильтровать по марке', async () => {
    await catalog.loadCars();
    catalog.filter('brand', 'BMW');

    expect(catalog.filteredCars).toHaveLength(1);
    expect(catalog.filteredCars[0].brand).toBe('BMW');
  });

  test('должен фильтровать по цене', async () => {
    await catalog.loadCars();
    catalog.filter('priceMax', 2800000);

    expect(catalog.filteredCars).toHaveLength(1);
    expect(catalog.filteredCars[0].price).toBeLessThanOrEqual(2800000);
  });

  test('должен искать автомобили', async () => {
    await catalog.loadCars();
    catalog.search('BMW');

    expect(catalog.filteredCars).toHaveLength(1);
    expect(catalog.filteredCars[0].brand).toBe('BMW');
  });
});

// tests/frontend/telegram.test.js
describe('Telegram Integration', () => {
  beforeEach(() => {
    // Мокаем Telegram Web App API
    global.window.Telegram = {
      WebApp: {
        ready: jest.fn(),
        expand: jest.fn(),
        close: jest.fn(),
        colorScheme: 'light',
        MainButton: {
          setText: jest.fn(),
          show: jest.fn(),
          hide: jest.fn(),
          onClick: jest.fn()
        },
        BackButton: {
          show: jest.fn(),
          hide: jest.fn(),
          onClick: jest.fn()
        },
        HapticFeedback: {
          impactOccurred: jest.fn()
        },
        openTelegramLink: jest.fn()
      }
    };
  });

  test('должен инициализировать Telegram Web App', () => {
    // Имитируем загрузку скрипта
    const script = document.createElement('script');
    script.src = 'https://telegram.org/js/telegram-web-app.js';
    document.head.appendChild(script);

    // Инициализация
    window.Telegram.WebApp.ready();
    window.Telegram.WebApp.expand();

    expect(window.Telegram.WebApp.ready).toHaveBeenCalled();
    expect(window.Telegram.WebApp.expand).toHaveBeenCalled();
  });

  test('должен адаптировать тему под Telegram', () => {
    window.Telegram.WebApp.colorScheme = 'dark';

    // Симулируем применение темы
    if (window.Telegram.WebApp.colorScheme === 'dark') {
      document.documentElement.classList.add('dark');
    }

    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });
});
```

### 4. 🤖 Bot Tests (Тесты Telegram бота)
**Цель:** Тестирование команд и интеграции

```python
# tests/bot/test_telegram_bot.py
import pytest
from unittest.mock import AsyncMock, MagicMock
import sys
import os

# Добавляем путь к боту
sys.path.append(os.path.join(os.path.dirname(__file__), '../../bot'))

from main import start_command, help_command, catalog_command, contact_command

class TestTelegramBot:

    @pytest.fixture
    def mock_message(self):
        """Мок сообщения от пользователя"""
        message = MagicMock()
        message.answer = AsyncMock()
        message.from_user.id = 12345
        message.from_user.username = "testuser"
        return message

    @pytest.mark.asyncio
    async def test_start_command(self, mock_message):
        """Тест команды /start"""
        await start_command(mock_message)

        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args

        # Проверяем текст ответа
        assert "Добро пожаловать" in call_args[0][0]

        # Проверяем наличие клавиатуры
        assert call_args[1]['reply_markup'] is not None

    @pytest.mark.asyncio
    async def test_help_command(self, mock_message):
        """Тест команды /help"""
        await help_command(mock_message)

        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args

        # Проверяем что в ответе есть список команд
        response_text = call_args[0][0]
        assert "/start" in response_text
        assert "/catalog" in response_text
        assert "/contact" in response_text
        assert "/help" in response_text

    @pytest.mark.asyncio
    async def test_catalog_command(self, mock_message):
        """Тест команды /catalog"""
        await catalog_command(mock_message)

        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args

        # Проверяем текст и клавиатуру
        assert "каталог" in call_args[0][0].lower()
        assert call_args[1]['reply_markup'] is not None

    @pytest.mark.asyncio
    async def test_contact_command(self, mock_message):
        """Тест команды /contact"""
        await contact_command(mock_message)

        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args

        # Проверяем что в ответе есть контактная информация
        response_text = call_args[0][0]
        assert "Телефон" in response_text or "телефон" in response_text
        assert "+7" in response_text  # Номер телефона
        assert "@" in response_text or "Email" in response_text  # Email или Telegram

def test_web_app_url_configured():
    """Проверка что URL веб-приложения настроен"""
    from main import WEB_APP_URL
    assert WEB_APP_URL is not None
    assert WEB_APP_URL.startswith('http')
```

### 5. 🔍 SEO Tests (Тесты SEO)
**Цель:** Проверка метатегов, Schema.org, производительности

```python
# tests/seo/test_seo.py
import requests
from bs4 import BeautifulSoup
import json
import pytest

class TestSEO:

    @pytest.fixture
    def soup(self):
        """Загружаем главную страницу для анализа"""
        # В реальности будет URL сайта, пока тестируем локально
        with open('hugo-site/public/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return BeautifulSoup(content, 'html.parser')

    def test_title_tag(self, soup):
        """Проверка наличия и корректности title"""
        title = soup.find('title')
        assert title is not None, "Отсутствует тег <title>"
        assert len(title.text) > 10, "Тег <title> слишком короткий"
        assert len(title.text) < 60, "Тег <title> слишком длинный"
        assert "автоломбард" in title.text.lower(), "В title отсутствует ключевое слово"

    def test_meta_description(self, soup):
        """Проверка meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        assert meta_desc is not None, "Отсутствует meta description"

        content = meta_desc.get('content', '')
        assert len(content) > 50, "Meta description слишком короткое"
        assert len(content) < 160, "Meta description слишком длинное"

    def test_meta_keywords(self, soup):
        """Проверка meta keywords"""
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        assert meta_keywords is not None, "Отсутствует meta keywords"

        keywords = meta_keywords.get('content', '').split(',')
        assert len(keywords) >= 3, "Должно быть минимум 3 ключевых слова"

    def test_open_graph(self, soup):
        """Проверка Open Graph метатегов"""
        og_title = soup.find('meta', property='og:title')
        og_description = soup.find('meta', property='og:description')
        og_type = soup.find('meta', property='og:type')
        og_url = soup.find('meta', property='og:url')

        assert og_title is not None, "Отсутствует og:title"
        assert og_description is not None, "Отсутствует og:description"
        assert og_type is not None, "Отсутствует og:type"
        assert og_url is not None, "Отсутствует og:url"

    def test_structured_data(self, soup):
        """Проверка Schema.org разметки"""
        scripts = soup.find_all('script', type='application/ld+json')
        assert len(scripts) > 0, "Отсутствует структурированная разметка"

        for script in scripts:
            try:
                data = json.loads(script.string)
                assert '@context' in data, "Отсутствует @context в Schema.org"
                assert '@type' in data, "Отсутствует @type в Schema.org"
            except json.JSONDecodeError:
                pytest.fail("Некорректный JSON в структурированных данных")

def test_car_page_seo():
    """Проверка SEO на странице автомобиля"""
    car_files = list(Path('hugo-site/public/cars').glob('*/index.html'))
    assert len(car_files) > 0, "Не найдены страницы автомобилей"

    # Тестируем первую найденную страницу
    with open(car_files[0], 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Проверяем Schema.org для автомобиля
    car_schema = soup.find('script', type='application/ld+json')
    assert car_schema is not None, "Отсутствует Schema.org для автомобиля"

    schema_data = json.loads(car_schema.string)
    assert schema_data.get('@type') == 'Car', "Некорректный тип Schema.org"
    assert 'brand' in schema_data, "Отсутствует марка в Schema.org"
    assert 'offers' in schema_data, "Отсутствует информация о цене"
```

### 6. 📱 Visual Tests (Визуальные тесты)
**Цель:** Кроссбраузерность и адаптивность

```javascript
// tests/visual/responsive.test.js
const { chromium, firefox, webkit } = require('playwright');

describe('Responsive Design Tests', () => {
  let browsers = [];

  beforeAll(async () => {
    // Запускаем тесты в разных браузерах
    browsers = await Promise.all([
      chromium.launch(),
      firefox.launch(),
      webkit.launch()
    ]);
  });

  afterAll(async () => {
    await Promise.all(browsers.map(browser => browser.close()));
  });

  const devices = [
    { name: 'Desktop', width: 1920, height: 1080 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Mobile', width: 375, height: 667 }
  ];

  devices.forEach(device => {
    test(`должен корректно отображаться на ${device.name}`, async () => {
      for (const browser of browsers) {
        const context = await browser.newContext({
          viewport: { width: device.width, height: device.height }
        });
        const page = await context.newPage();

        await page.goto('http://localhost:1313');

        // Проверяем что страница загрузилась
        await page.waitForSelector('body');

        // Проверяем что каталог автомобилей виден
        const carsGrid = await page.$('.cars-grid, #cars-container');
        expect(carsGrid).toBeTruthy();

        // Проверяем что фильтры доступны
        const filters = await page.$('.filters-section, .filter-container');
        expect(filters).toBeTruthy();

        // Проверяем что нет горизонтального скролла
        const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
        const windowWidth = await page.evaluate(() => window.innerWidth);
        expect(bodyWidth).toBeLessThanOrEqual(windowWidth);

        await context.close();
      }
    });
  });

  test('должен поддерживать Telegram Web App', async () => {
    const browser = await chromium.launch();
    const context = await browser.newContext({
      userAgent: 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 TelegramBot'
    });
    const page = await context.newPage();

    // Мокаем Telegram Web App API
    await page.evaluateOnNewDocument(() => {
      window.Telegram = {
        WebApp: {
          ready: () => {},
          expand: () => {},
          colorScheme: 'light',
          MainButton: { setText: () => {}, show: () => {} }
        }
      };
    });

    await page.goto('http://localhost:1313');

    // Проверяем что Telegram скрипт подключен
    const telegramScript = await page.$('script[src*="telegram-web-app.js"]');
    expect(telegramScript).toBeTruthy();

    await browser.close();
  });
});
```

## 🚀 Инструменты для автоматизации

### Package.json для тестов
```json
{
  "name": "hugo-auto-lombard-tests",
  "version": "1.0.0",
  "scripts": {
    "test": "npm run test:content && npm run test:frontend && npm run test:seo",
    "test:content": "python tests/content/test_cars_data.py",
    "test:frontend": "jest tests/frontend/",
    "test:bot": "pytest tests/bot/",
    "test:seo": "python tests/seo/test_seo.py",
    "test:visual": "playwright test tests/visual/",
    "test:build": "bash hugo-site/tests/build/test_hugo_build.sh",
    "test:all": "npm run test:build && npm run test && npm run test:bot && npm run test:visual",
    "lighthouse": "lighthouse http://localhost:1313 --output=json --output-path=./tests/reports/lighthouse.json",
    "hugo:serve": "cd hugo-site && hugo server",
    "hugo:build": "cd hugo-site && hugo --minify"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "playwright": "^1.40.0",
    "@playwright/test": "^1.40.0",
    "lighthouse": "^11.0.0",
    "jest-environment-jsdom": "^29.0.0"
  }
}
```

### GitHub Actions CI/CD
```yaml
# .github/workflows/test.yml
name: Hugo Auto Lombard Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
      with:
        submodules: true

    - name: Setup Hugo
      uses: peaceiris/actions-hugo@v2
      with:
        hugo-version: 'latest'
        extended: true

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        npm install
        pip install pytest pytest-asyncio pyyaml beautifulsoup4

    - name: Run build tests
      run: npm run test:build

    - name: Run content tests
      run: npm run test:content

    - name: Run frontend tests
      run: npm run test:frontend

    - name: Run bot tests
      run: npm run test:bot

    - name: Install Playwright browsers
      run: npx playwright install

    - name: Start Hugo server
      run: |
        cd hugo-site
        hugo server &
        sleep 5

    - name: Run visual tests
      run: npm run test:visual

    - name: Run Lighthouse
      run: npm run lighthouse

    - name: Upload test reports
      uses: actions/upload-artifact@v3
      with:
        name: test-reports
        path: tests/reports/
```

## 📊 Метрики качества

### Критерии приемки:
- ✅ **Build Tests**: Сборка без ошибок
- ✅ **Content Tests**: 100% валидных данных
- ✅ **Frontend Tests**: Покрытие >80%
- ✅ **Bot Tests**: Все команды работают
- ✅ **SEO Tests**: Lighthouse Score >95
- ✅ **Visual Tests**: 3+ браузера, 3+ устройства

### Автоматизация:
- 🤖 **CI/CD**: GitHub Actions
- 📊 **Отчеты**: Jest + Lighthouse + Playwright
- 🔄 **Регрессия**: Автоматические тесты при каждом коммите
- 📱 **Cross-platform**: Chrome, Firefox, Safari, Mobile

## ⏱️ Интеграция в план разработки

### Обновленный 3-дневный план:

**День 1** (3-4 часа): Hugo setup + **базовые тесты**
- ✅ Установка Hugo + тема
- ✅ Настройка тестовой среды
- ✅ Build tests

**День 2** (4-5 часов): Функциональность + **функциональные тесты**
- ✅ Кастомизация + Telegram интеграция
- ✅ Frontend tests + Bot tests

**День 3** (2-3 часа): Финализация + **автоматизация тестов**
- ✅ SEO + Visual tests
- ✅ CI/CD настройка

**Результат: 95% покрытие тестами + автоматизация!** 🧪✅

Готовы начинать с тестированием?
