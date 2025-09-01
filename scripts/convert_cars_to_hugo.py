#!/usr/bin/env python3
"""
Скрипт для конвертации JSON данных автомобилей в Markdown файлы Hugo
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

def slugify(text):
    """Создает URL-friendly slug из текста"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def format_price(price):
    """Форматирует цену с разделителями"""
    return f"{price:,}".replace(',', ' ')

def convert_cars_to_hugo():
    """Конвертирует JSON данные автомобилей в Markdown файлы Hugo"""

    # Пути к файлам
    json_file = Path('web/assets/data/cars.json')
    output_dir = Path('hugo-site/content/cars')

    # Проверяем наличие JSON файла
    if not json_file.exists():
        print(f"❌ Файл {json_file} не найден!")
        return False

    # Создаем выходную папку
    output_dir.mkdir(parents=True, exist_ok=True)

    # Загружаем данные
    with open(json_file, 'r', encoding='utf-8') as f:
        cars = json.load(f)

    print(f"📊 Найдено {len(cars)} автомобилей для конвертации...")

    # Конвертируем каждый автомобиль
    for i, car in enumerate(cars, 1):
        try:
            # Создаем slug для URL
            slug = slugify(f"{car['brand']}-{car['model']}-{car['year']}")
            filename = f"{slug}.md"
            file_path = output_dir / filename

            # Создаем Front Matter
            front_matter = f"""---
title: "{car['brand']} {car['model']} {car['year']}"
date: {car['created_at']}
draft: false

# Основная информация
brand: "{car['brand']}"
model: "{car['model']}"
year: {car['year']}
price: {car['price']}
currency: "{car['currency']}"
mileage: {car['mileage']}

# Технические характеристики
engine:
  volume: "{car['engine']['volume']}"
  type: "{car['engine']['type']}"
  power: {car['engine']['power']}
transmission: "{car['transmission']}"
drive: "{car['drive']}"
body: "{car['body']}"
color: "{car['color']}"
condition: "{car['condition']}"
vin: "{car['vin']}"

# Изображения
images:"""

            # Добавляем изображения
            for image in car['images']:
                front_matter += f'\n  - "{image}"'

            # Добавляем характеристики
            front_matter += f"""

# Характеристики
features:"""
            for feature in car['features']:
                front_matter += f'\n  - "{feature}"'

            # Добавляем контакты
            front_matter += f"""

# Контакты
contact:
  manager: "{car['contacts']['manager']}"
  phone: "{car['contacts']['phone']}"
  telegram: "{car['contacts']['telegram']}"

# Локация
location:
  city: "{car['location']['city']}"
  address: "{car['location']['address']}"

# SEO
description: "{car['brand']} {car['model']} {car['year']} - {format_price(car['price'])} ₽. {car['description'][:100]}..."
keywords: ["{car['brand']}", "{car['model']}", "{car['year']}", "автоломбард", "{car['body'].lower()}"]

# Статус и метки
status: "{car['status']}"
featured: {'true' if i <= 3 else 'false'}  # Первые 3 автомобиля как рекомендуемые

# Таксономии для фильтрации
brands: ["{car['brand']}"]
body_types: ["{car['body']}"]
fuel_types: ["{car['engine']['type']}"]
conditions: ["{car['condition']}"]

# Метаданные
created_at: "{car['created_at']}"
updated_at: "{car['updated_at']}"
car_id: "{car['id']}"
---"""

            # Создаем основной контент
            content = f"""
{car['description']}

## Технические характеристики

| Параметр | Значение |
|----------|----------|
| **Марка** | {car['brand']} |
| **Модель** | {car['model']} |
| **Год выпуска** | {car['year']} |
| **Пробег** | {format_price(car['mileage'])} км |
| **Двигатель** | {car['engine']['volume']}L {car['engine']['type']} |
| **Мощность** | {car['engine']['power']} л.с. |
| **Коробка передач** | {car['transmission']} |
| **Привод** | {car['drive']} |
| **Тип кузова** | {car['body']} |
| **Цвет** | {car['color']} |
| **Состояние** | {car['condition']} |
| **VIN** | `{car['vin']}` |

## Комплектация и опции

Автомобиль оснащен следующими опциями:

"""

            # Добавляем список опций
            for feature in car['features']:
                content += f"- ✅ **{feature}**\n"

            content += f"""

## Цена и условия

💰 **Цена**: **{format_price(car['price'])} ₽**

### Что включено в стоимость:
- Полная диагностика автомобиля
- Проверка юридической чистоты
- Помощь в оформлении документов
- Гарантия на техническое состояние

### Возможности:
- 💳 Оплата наличными или картой
- 📄 Помощь с оформлением кредита
- 🚗 Возможность trade-in
- 📋 Полный пакет документов

## Связаться с нами

Хотите посмотреть этот автомобиль? Свяжитесь с нашим менеджером:

👤 **Менеджер**: {car['contacts']['manager']}
📞 **Телефон**: [{car['contacts']['phone']}](tel:{car['contacts']['phone'].replace(' ', '').replace('(', '').replace(')', '').replace('-', '')})
💬 **Telegram**: [{car['contacts']['telegram']}](https://t.me/{car['contacts']['telegram'][1:]})

📍 **Адрес салона**: {car['location']['city']}, {car['location']['address']}
🕐 **Режим работы**: ПН-ВС с 9:00 до 21:00

### Как купить этот автомобиль?

1. **Свяжитесь с менеджером** по телефону или в Telegram
2. **Приезжайте на осмотр** в наш автосалон
3. **Проведите тест-драйв** и убедитесь в качестве
4. **Оформите сделку** с помощью наших специалистов

---

*Автомобиль размещен: {datetime.fromisoformat(car['created_at'].replace('Z', '+00:00')).strftime('%d.%m.%Y')}*
*Последнее обновление: {datetime.fromisoformat(car['updated_at'].replace('Z', '+00:00')).strftime('%d.%m.%Y')}*
"""

            # Записываем файл
            full_content = front_matter + content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_content)

            print(f"✅ {i:2d}/6: {car['brand']} {car['model']} {car['year']} → {filename}")

        except Exception as e:
            print(f"❌ Ошибка при обработке автомобиля {car.get('id', 'unknown')}: {e}")
            return False

    print(f"\n🎉 Успешно конвертировано {len(cars)} автомобилей!")
    print(f"📁 Файлы сохранены в: {output_dir}")

    return True

def main():
    """Основная функция"""
    print("🚗 Конвертация JSON автомобилей в Hugo Markdown...")
    print("=" * 50)

    if convert_cars_to_hugo():
        print("\n✅ Конвертация завершена успешно!")
        print("\n📋 Следующие шаги:")
        print("1. cd hugo-site")
        print("2. hugo server")
        print("3. Открыть http://localhost:1313")
    else:
        print("\n❌ Конвертация завершилась с ошибками!")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
