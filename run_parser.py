#!/usr/bin/env python3
"""
Быстрый запуск парсера Авито
"""

import sys
import os

# Добавляем текущую папку в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from avito_parser import AvitoParser

def main():
    print("🚗 Запуск парсера Авито для автоломбарда")
    print("=" * 50)

    # URL со страницы пользователя
    avito_url = "https://www.avito.ru/brands/be5f12b20964ea30a159d92acf5074cb?gdlkerfdnwq=101&page_from=from_item_header&iid=7526372017&page_from=from_item_card&iid=7526372017"

    print(f"🔗 URL: {avito_url[:80]}...")
    print("🌐 Открываем браузер (НЕ закрывайте его вручную)")
    print("⏱️  Процесс может занять 2-5 минут")
    print("=" * 50)

    # Создаем парсер (НЕ headless = показываем браузер)
    parser = AvitoParser(headless=False)

    try:
        # Парсим
        parser.parse_avito_page(avito_url)

        if parser.cars_data:
            print(f"\n✅ Найдено автомобилей: {len(parser.cars_data)}")

            # Показываем первые 3 для проверки
            print("\n📋 Примеры найденных автомобилей:")
            for i, car in enumerate(parser.cars_data[:3], 1):
                print(f"{i}. {car.brand} {car.model} {car.year} - {car.price:,} ₽")

            if len(parser.cars_data) > 3:
                print(f"... и еще {len(parser.cars_data) - 3} автомобилей")

            # Спрашиваем, сохранять ли
            answer = input("\n💾 Сохранить в Hugo каталог? (y/n): ").lower()

            if answer in ['y', 'yes', 'да', 'д']:
                parser.save_to_hugo()
                parser.save_to_json()

                print("\n🎉 Готово!")
                print("📁 Файлы созданы в: hugo-site/content/cars/")
                print("📊 JSON сохранен в: avito_cars.json")
                print("\n📝 Следующие шаги:")
                print("1. hugo --source hugo-site")
                print("2. git add . && git commit -m 'Add cars from Avito'")
                print("3. git push")
            else:
                print("❌ Сохранение отменено")
        else:
            print("❌ Автомобили не найдены")
            print("🔧 Возможные причины:")
            print("  - Авито изменил структуру страницы")
            print("  - Страница заблокирована")
            print("  - Неправильный URL")

    except KeyboardInterrupt:
        print("\n⏹️ Остановлено пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        print("🔧 Попробуйте еще раз или проверьте подключение к интернету")

if __name__ == "__main__":
    main()
