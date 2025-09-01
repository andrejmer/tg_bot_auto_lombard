#!/usr/bin/env python3
"""
Скрипт для массового добавления автомобилей в Hugo каталог.
Создает файлы .md с правильной структурой для динамической фильтрации.
"""

import os
import datetime
from pathlib import Path

def create_car_file(car_data):
    """Создает файл автомобиля с правильной структурой"""

    # Генерируем имя файла
    filename = f"{car_data['brand'].lower().replace('-', '').replace(' ', '-')}-{car_data['model'].lower().replace(' ', '-').replace('/', '-')}-{car_data['year']}.md"
    filepath = Path("../hugo-site/content/cars") / filename

    # Шаблон файла
    template = f"""---
title: "{car_data['brand']} {car_data['model']} {car_data['year']}"
date: {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')}
draft: false
image: "images/cars/placeholder.svg"

# КРИТИЧЕСКИ ВАЖНО! Эти поля используются для динамической фильтрации
brand: "{car_data['brand']}"
model: "{car_data['model']}"

year: {car_data['year']}
price: {car_data['price']}
mileage: {car_data.get('mileage', 50000)}
engine_volume: {car_data.get('engine_volume', '2.0')}
fuel_type: "{car_data.get('fuel_type', 'Бензин')}"
transmission: "{car_data.get('transmission', 'AT')}"
drive_type: "{car_data.get('drive_type', 'Передний')}"
body_type: "{car_data.get('body_type', 'Седан')}"
color: "{car_data.get('color', 'Белый')}"
condition: "{car_data.get('condition', 'Хорошее')}"
vin: "{car_data.get('vin', 'XXXXXXXXXXXXXXXXX')}"
owners_count: {car_data.get('owners_count', 1)}
pts_original: {str(car_data.get('pts_original', True)).lower()}
customs_cleared: {str(car_data.get('customs_cleared', True)).lower()}
exchange_possible: {str(car_data.get('exchange_possible', True)).lower()}
credit_available: {str(car_data.get('credit_available', True)).lower()}
description: "{car_data.get('description', f'{car_data["brand"]} {car_data["model"]} {car_data["year"]} в хорошем состоянии')}"
tags: {car_data.get('tags', '["автомобиль"]')}
weight: {car_data.get('weight', 1)}
---

## Характеристики {car_data['brand']} {car_data['model']} {car_data['year']}

| Параметр | Значение |
|----------|----------|
| **Марка** | {car_data['brand']} |
| **Модель** | {car_data['model']} |
| **Год выпуска** | {car_data['year']} |
| **Цена** | {car_data['price']:,} ₽ |
| **Пробег** | {car_data.get('mileage', 50000):,} км |
| **Объем двигателя** | {car_data.get('engine_volume', '2.0')} л |
| **Тип топлива** | {car_data.get('fuel_type', 'Бензин')} |
| **Коробка передач** | {car_data.get('transmission', 'AT')} |
| **Привод** | {car_data.get('drive_type', 'Передний')} |
| **Тип кузова** | {car_data.get('body_type', 'Седан')} |
| **Цвет** | {car_data.get('color', 'Белый')} |
| **Состояние** | {car_data.get('condition', 'Хорошее')} |

## Описание

{car_data.get('description', f'{car_data["brand"]} {car_data["model"]} {car_data["year"]} в хорошем состоянии.')}

### Комплектация:
{car_data.get('equipment', '- Стандартная комплектация')}

### Техническое состояние:
{car_data.get('technical_condition', '- Автомобиль в исправном состоянии')}

**{car_data.get('additional_info', 'Возможен обмен, кредит, лизинг.')}**
"""

    # Создаем директорию если не существует
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Записываем файл
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"✅ Создан файл: {filepath}")
    return filepath

# Пример использования
if __name__ == "__main__":
    # Пример данных ваших автомобилей
    cars_to_add = [
        {
            "brand": "BMW",
            "model": "X7",
            "year": 2021,
            "price": 4500000,
            "mileage": 35000,
            "fuel_type": "Бензин",
            "body_type": "Внедорожник",
            "color": "Черный",
            "description": "BMW X7 2021 года в отличном состоянии. Полная комплектация."
        },
        {
            "brand": "Mercedes-Benz",
            "model": "GLE",
            "year": 2020,
            "price": 4200000,
            "mileage": 28000,
            "fuel_type": "Дизель",
            "body_type": "Внедорожник",
            "color": "Серебристый"
        },
        {
            "brand": "Audi",
            "model": "Q7",
            "year": 2019,
            "price": 3800000,
            "mileage": 45000,
            "fuel_type": "Бензин",
            "body_type": "Внедорожник",
            "color": "Белый"
        }
    ]

    print("🚗 Добавляем автомобили в каталог...")
    for car in cars_to_add:
        create_car_file(car)

    print("\n🎉 Готово! Автомобили добавлены.")
    print("\n📝 Следующие шаги:")
    print("1. Отредактируйте созданные файлы в hugo-site/content/cars/")
    print("2. Запустите: hugo --source hugo-site")
    print("3. Проверьте models-data.json")
    print("4. Задеплойте: git add . && git commit -m 'Add new cars' && git push")
