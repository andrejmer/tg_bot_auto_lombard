#!/usr/bin/env python3
"""
Простой тест загрузки изображений с обновленными селекторами
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from avito_parser import AvitoParser, CarData
import time
from selenium.webdriver.common.by import By
from urllib.parse import urljoin

def test_images():
    """Тест с 2 автомобилями для проверки загрузки изображений"""
    print("📸 Тест загрузки изображений с обновленными селекторами")
    print("🔢 Тестируем 2 автомобиля")
    print("=" * 50)

    parser = AvitoParser(headless=False)
    url = "https://www.avito.ru/brands/be5f12b20964ea30a159d92acf5074cb?gdlkerfdnwq=101&page_from=from_item_header&iid=7526372017&page_from=from_item_card&iid=7526372017"

    try:
        if not parser.driver:
            parser.setup_driver()

        parser.driver.get(url)
        time.sleep(5)
        parser.scroll_to_load_all()

        car_elements = parser.driver.find_elements(By.CSS_SELECTOR, '[itemtype="http://schema.org/Product"]')
        print(f"📋 Найдено объявлений: {len(car_elements)} (тестируем первые 2)")

        # Берем только первые 2
        car_elements = car_elements[:2]

        # Собираем базовые данные
        car_data = []
        for i, element in enumerate(car_elements, 1):
            try:
                title_elem = element.find_element(By.CSS_SELECTOR, '[itemprop="name"]')
                title = title_elem.text.strip()

                try:
                    price_elem = element.find_element(By.CSS_SELECTOR, '[itemprop="price"]')
                    price_text = price_elem.get_attribute('content')
                    if not price_text:
                        price_elem = element.find_element(By.CSS_SELECTOR, '[data-marker="item-price"]')
                        price_text = price_elem.text
                    price = parser.parse_price(price_text)
                except:
                    price = 0

                link_elem = element.find_element(By.CSS_SELECTOR, '[itemprop="url"]')
                car_url = urljoin(url, link_elem.get_attribute('href'))

                car_data.append((title, price, car_url))

            except Exception as e:
                print(f"⚠️ Ошибка при получении данных объявления {i}: {e}")
                continue

        # Теперь детально парсим каждую карточку
        for i, (title, price, car_url) in enumerate(car_data, 1):
            try:
                print(f"\n🚗 Тестируем {i}/2: {title}")

                # Парсим название
                full_title, brand, model, year = parser.parse_car_title(title)
                basic_details = parser.parse_car_details(title)

                print(f"  📝 {brand} {model} {year}")
                print(f"  💰 {price:,} ₽")

                # Получаем изображения из карточки
                detailed_info = parser.parse_car_details_from_page(car_url)

                if detailed_info.get('images'):
                    print(f"  🎯 Найдено изображений на странице: {len(detailed_info['images'])}")
                    for j, img_url in enumerate(detailed_info['images'][:3], 1):
                        print(f"    {j}. {img_url[:60]}...")

                    # Загружаем изображения
                    image_files = parser.download_multiple_images(
                        detailed_info['images'], brand, model, year
                    )

                    print(f"  ✅ Успешно загружено: {len(image_files)} изображений")
                    for img_file in image_files:
                        print(f"    📁 {img_file}")

                    # Создаем автомобиль с изображениями
                    car = CarData(
                        title=full_title,
                        brand=brand,
                        model=model,
                        year=year,
                        price=price,
                        mileage=basic_details.get('mileage', 0),
                        engine_volume=basic_details.get('engine_volume', '2.0'),
                        fuel_type=basic_details.get('fuel_type', 'Бензин'),
                        transmission=basic_details.get('transmission', 'AT'),
                        url=car_url,
                        images=image_files,
                        image_filename=image_files[0] if image_files else None,
                        description=detailed_info.get('full_description') or f"{brand} {model} {year} года в хорошем состоянии."
                    )

                    parser.cars_data.append(car)

                else:
                    print(f"  ❌ Изображения не найдены")

            except Exception as e:
                import traceback
                print(f"⚠️ Ошибка при обработке объявления {i}: {e}")
                print(f"  Подробности: {traceback.format_exc()}")
                continue

        print(f"\n📊 Итоги теста:")
        for car in parser.cars_data:
            images_count = len(car.images) if car.images else 0
            print(f"• {car.brand} {car.model} {car.year}")
            print(f"  📷 Изображений: {images_count}")
            if car.images:
                print(f"  📁 Файлы: {', '.join(car.images)}")

        if parser.cars_data:
            save = input(f"\n💾 Сохранить {len(parser.cars_data)} автомобилей с изображениями? (y/n): ").lower()
            if save in ['y', 'yes', 'да', 'д']:
                parser.save_to_hugo("../hugo-site/content/cars")
                print("✅ Данные сохранены!")

                # Показываем содержимое папки с изображениями
                import subprocess
                result = subprocess.run("ls -la ../hugo-site/static/images/cars/", shell=True, capture_output=True, text=True)
                print(f"\n📂 Содержимое папки изображений:")
                print(result.stdout)

    except KeyboardInterrupt:
        print("\n⏹️ Тест прерван")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
    finally:
        if parser.driver:
            parser.driver.quit()

if __name__ == "__main__":
    test_images()
