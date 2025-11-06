"""
Менеджер для создания и управления объявлениями автомобилей
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import aiofiles
import aiohttp


class CarManager:
    """Класс для управления объявлениями автомобилей"""
    
    def __init__(self, hugo_site_path: str = "../hugo-site"):
        self.hugo_site_path = Path(hugo_site_path)
        self.content_path = self.hugo_site_path / "content" / "cars"
        self.images_path = self.hugo_site_path / "static" / "images" / "cars"
        
        # Создаем директории если их нет
        self.content_path.mkdir(parents=True, exist_ok=True)
        self.images_path.mkdir(parents=True, exist_ok=True)
    
    def slugify(self, text: str) -> str:
        """Создает slug из текста (для имен файлов)"""
        # Транслитерация
        translit_dict = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
        }
        
        text = text.lower()
        result = []
        for char in text:
            if char in translit_dict:
                result.append(translit_dict[char])
            elif char.isalnum() or char in ['-', '_']:
                result.append(char)
            elif char == ' ':
                result.append('-')
        
        slug = ''.join(result)
        # Удаляем повторяющиеся дефисы
        slug = re.sub(r'-+', '-', slug)
        return slug.strip('-')
    
    async def save_photo(self, photo_data: bytes, filename: str) -> str:
        """Сохраняет фотографию и возвращает путь"""
        filepath = self.images_path / filename
        
        async with aiofiles.open(filepath, 'wb') as f:
            await f.write(photo_data)
        
        # Возвращаем путь относительно static
        return f"images/cars/{filename}"
    
    async def create_car_listing(self, car_data: Dict) -> str:
        """Создает объявление автомобиля (markdown файл для Hugo)"""
        
        # Генерируем имя файла
        brand = car_data.get('brand', 'unknown')
        model = car_data.get('model', 'unknown')
        year = car_data.get('year', datetime.now().year)
        
        slug = f"{self.slugify(brand)}-{self.slugify(model)}-{year}"
        filename = f"{slug}.md"
        filepath = self.content_path / filename
        
        # Если файл существует, добавляем номер
        counter = 1
        while filepath.exists():
            filename = f"{slug}-{counter}.md"
            filepath = self.content_path / filename
            counter += 1
        
        # Формируем заголовок
        title = f"{brand} {model} {car_data.get('engine_volume', '')} {car_data.get('transmission', '')}, {year}"
        if car_data.get('mileage'):
            title += f", {car_data.get('mileage')} км"
        
        # Формируем список изображений
        images = car_data.get('images', [])
        images_str = ', '.join([f'"{img}"' for img in images])
        
        # Формируем front matter
        front_matter = f"""---
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')}
draft: false
image: "{images[0] if images else ''}"
images: [{images_str}]

# Данные для фильтрации
brand: "{car_data.get('brand', '')}"
model: "{car_data.get('model', '')}"

year: {car_data.get('year', datetime.now().year)}
price: {car_data.get('price', 0)}
mileage: {car_data.get('mileage', 0)}
engine_volume: {car_data.get('engine_volume', 0)}
fuel_type: "{car_data.get('fuel_type', 'Бензин')}"
transmission: "{car_data.get('transmission', 'MT')}"
drive_type: "{car_data.get('drive_type', 'Передний')}"
body_type: "{car_data.get('body_type', 'Седан')}"
color: "{car_data.get('color', 'Не указан')}"
condition: "{car_data.get('condition', 'Хорошее')}"
vin: "{car_data.get('vin', 'Не указан')}"
owners_count: {car_data.get('owners_count', 1)}
pts_original: {str(car_data.get('pts_original', True)).lower()}
customs_cleared: true
exchange_possible: {str(car_data.get('exchange_possible', False)).lower()}
credit_available: {str(car_data.get('credit_available', True)).lower()}
description: "{car_data.get('description', '').replace('"', '\\"')}"
source_url: ""
tags: ["автомобиль", "telegram"]
weight: 1
---

## Характеристики {brand} {model} {year}

| Параметр | Значение |
|----------|----------|
| **Марка** | {car_data.get('brand', '')} |
| **Модель** | {car_data.get('model', '')} |
| **Год выпуска** | {year} |
| **Цена** | {car_data.get('price', 0):,} ₽ |
| **Пробег** | {car_data.get('mileage', 0):,} км |
| **Объем двигателя** | {car_data.get('engine_volume', 0)} л |
| **Тип топлива** | {car_data.get('fuel_type', 'Бензин')} |
| **Коробка передач** | {car_data.get('transmission', 'MT')} |
| **Тип кузова** | {car_data.get('body_type', 'Седан')} |
| **Цвет** | {car_data.get('color', 'Не указан')} |
| **Состояние** | {car_data.get('condition', 'Хорошее')} |

## Описание

{car_data.get('description', 'Описание отсутствует.')}

### Контакты
- Телефон: +7 (999) 123-45-67
- Email: info@auto-lombard.ru

**Возможен обмен, кредит, лизинг.**
"""
        
        # Сохраняем файл
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(front_matter)
        
        return str(filepath)
    
    def format_car_summary(self, car_data: Dict) -> str:
        """Форматирует краткую информацию об автомобиле для предпросмотра"""
        
        summary = f"""
🚗 **{car_data.get('brand', '')} {car_data.get('model', '')}**

📅 Год: {car_data.get('year', '')}
💰 Цена: {car_data.get('price', 0):,} ₽
🛣 Пробег: {car_data.get('mileage', 0):,} км

⚙️ Двигатель: {car_data.get('engine_volume', '')} л, {car_data.get('fuel_type', '')}
🔧 КПП: {car_data.get('transmission', '')}
🚙 Кузов: {car_data.get('body_type', '')}
🎨 Цвет: {car_data.get('color', '')}

📝 Состояние: {car_data.get('condition', '')}
👥 Владельцев: {car_data.get('owners_count', '')}
📋 ПТС: {'Оригинал' if car_data.get('pts_original') else 'Дубликат'}

📸 Фотографий: {len(car_data.get('images', []))}

💬 Описание:
{car_data.get('description', 'Не указано')[:200]}...
"""
        return summary

