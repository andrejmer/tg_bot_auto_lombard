#!/usr/bin/env python3
"""
Простой тест парсера Авито
"""

import sys
import os

# Добавляем текущую папку в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from avito_parser import AvitoParser

def test_parser():
    """Тестирование функций парсера"""
    parser = AvitoParser()

    # Тест парсинга названия
    test_titles = [
        "BMW 5 серия 2.0 AT, 2017, 121 900 км",
        "Infiniti QX80 5.6 AT, 2015, 144 000 км",
        "ВАЗ (LADA) Largus 1.6 MT, 2017, 160 500 км",
        "Lexus GX 4.6 AT, 2015, 124 000 км",
        "Land Rover Discovery 3.0 AT, 2013, 266 000 км"
    ]

    print("🧪 Тестируем парсинг названий:")
    print("=" * 50)

    for title in test_titles:
        full_title, brand, model, year = parser.parse_car_title(title)
        print(f"📝 Исходное: {title}")
        print(f"🏷️  Марка: {brand}")
        print(f"🚗 Модель: {model}")
        print(f"📅 Год: {year}")
        print("-" * 30)

    # Тест парсинга цены
    test_prices = ["2 490 000 ₽", "3 600 000 ₽", "720 000 ₽"]

    print("\n💰 Тестируем парсинг цен:")
    print("=" * 30)

    for price_text in test_prices:
        price = parser.parse_price(price_text)
        print(f"📝 '{price_text}' → {price:,} ₽")

if __name__ == "__main__":
    test_parser()
