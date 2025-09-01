#!/usr/bin/env python3
"""
Тест детального парсера Авито (с заходом в карточки)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from avito_parser import AvitoParser

def test_detailed_parsing():
    """Тест парсинга с заходом в карточки"""
    print("🧪 Тестируем детальный парсер Авито")
    print("=" * 50)

    # Создаем парсер
    parser = AvitoParser(headless=False)

    # Тестовый URL (только для демонстрации, реальный URL в main функции)
    test_url = "https://www.avito.ru/brands/be5f12b20964ea30a159d92acf5074cb?gdlkerfdnwq=101&page_from=from_item_header&iid=7526372017&page_from=from_item_card&iid=7526372017"

    print(f"🔗 URL: {test_url}")
    print("⚠️  ВНИМАНИЕ: Это займет больше времени, так как парсер заходит в каждую карточку")
    print("🖼️  Будут загружены реальные изображения")
    print("📝 Будут получены полные описания")

    answer = input("\nПродолжить? (y/n): ").lower()

    if answer in ['y', 'yes', 'да', 'д']:
        try:
            # Ограничиваем количество для теста
            print("🔬 Запускаем тестовый парсинг первых объявлений...")
            parser.parse_avito_page(test_url)

            if parser.cars_data:
                print(f"\n📊 Результаты теста:")
                for i, car in enumerate(parser.cars_data[:3], 1):
                    print(f"\n{i}. {car.brand} {car.model} {car.year}")
                    print(f"   💰 Цена: {car.price:,} ₽")
                    print(f"   🖼️  Изображений: {len(car.images) if car.images else 0}")
                    print(f"   📝 Описание: {car.description[:100]}...")
                    if car.vin:
                        print(f"   🔢 VIN: {car.vin}")

                save = input(f"\n💾 Сохранить {len(parser.cars_data)} автомобилей? (y/n): ").lower()
                if save in ['y', 'yes', 'да', 'д']:
                    parser.save_to_hugo("../hugo-site/content/cars")
                    parser.save_to_json("detailed_test_results.json")
                    print("✅ Данные сохранены!")
            else:
                print("❌ Автомобили не найдены")

        except KeyboardInterrupt:
            print("\n⏹️ Тест прерван")
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
    else:
        print("❌ Тест отменен")

if __name__ == "__main__":
    test_detailed_parsing()
