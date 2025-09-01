#!/usr/bin/env python3
"""
Тест полного парсера с загрузкой изображений (ограниченное количество)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from avito_parser import AvitoParser

def test_full_with_images():
    """Тест полного парсера с изображениями (5 автомобилей)"""
    print("📸 Тест полного парсера с загрузкой изображений")
    print("🔢 Ограничиваем до 5 автомобилей для теста")
    print("⏱️  Примерное время: 5-7 минут")
    print("🖼️  Загружаем все фотографии с Авито")
    print("=" * 60)

    # Подтверждение
    answer = input("Продолжить тест полного парсера? (y/n): ").lower()
    if answer not in ['y', 'yes', 'да', 'д']:
        print("❌ Тест отменен")
        return

    parser = AvitoParser(headless=False)
    url = "https://www.avito.ru/brands/be5f12b20964ea30a159d92acf5074cb?gdlkerfdnwq=101&page_from=from_item_header&iid=7526372017&page_from=from_item_card&iid=7526372017"

    # Патчим парсер для ограничения количества
    original_parse = parser.parse_avito_page

    def limited_full_parse(url):
        """Ограниченный полный парсинг с изображениями"""
        print(f"🔍 Парсим страницу: {url}")

        if not parser.driver:
            parser.setup_driver()

        try:
            parser.driver.get(url)

            import time
            from selenium.webdriver.common.by import By
            from urllib.parse import urljoin

            time.sleep(5)
            parser.scroll_to_load_all()

            car_elements = parser.driver.find_elements(By.CSS_SELECTOR, '[itemtype="http://schema.org/Product"]')
            print(f"📋 Найдено объявлений: {len(car_elements)} (берем первые 5)")

            # Ограничиваем до 5
            car_elements = car_elements[:5]

            # Собираем ссылки на все объявления
            car_links = []
            car_titles = []
            car_prices = []

            for i, element in enumerate(car_elements, 1):
                try:
                    title_elem = element.find_element(By.CSS_SELECTOR, '[itemprop="name"]')
                    title = title_elem.text.strip()
                    car_titles.append(title)

                    try:
                        price_elem = element.find_element(By.CSS_SELECTOR, '[itemprop="price"]')
                        price_text = price_elem.get_attribute('content')
                        if not price_text:
                            price_elem = element.find_element(By.CSS_SELECTOR, '[data-marker="item-price"]')
                            price_text = price_elem.text
                        price = parser.parse_price(price_text)
                    except:
                        price = 0
                    car_prices.append(price)

                    link_elem = element.find_element(By.CSS_SELECTOR, '[itemprop="url"]')
                    car_url = urljoin(url, link_elem.get_attribute('href'))
                    car_links.append(car_url)

                except Exception as e:
                    print(f"⚠️ Ошибка при получении данных объявления {i}: {e}")
                    continue

            # Теперь парсим каждую карточку детально с изображениями
            for i, (car_url, title, price) in enumerate(zip(car_links, car_titles, car_prices), 1):
                try:
                    print(f"\n🚗 Обрабатываем {i}/5: {title}")

                    # Парсим название
                    full_title, brand, model, year = parser.parse_car_title(title)
                    basic_details = parser.parse_car_details(title)

                    # Получаем детальную информацию из карточки (включая изображения)
                    detailed_info = parser.parse_car_details_from_page(car_url)

                    # Загружаем изображения
                    image_files = []
                    if detailed_info.get('images'):
                        print(f"  📷 Найдено изображений: {len(detailed_info['images'])}")
                        image_files = parser.download_multiple_images(
                            detailed_info['images'], brand, model, year
                        )
                        print(f"  ✅ Загружено изображений: {len(image_files)}")
                    else:
                        print("  ❌ Изображения не найдены")

                    # Используем более точные данные
                    mileage = basic_details.get('mileage', 0)
                    transmission = basic_details.get('transmission', 'AT')
                    fuel_type = basic_details.get('fuel_type', 'Бензин')

                    # Создаем объект автомобиля
                    from avito_parser import CarData
                    car = CarData(
                        title=full_title,
                        brand=brand,
                        model=model,
                        year=year,
                        price=price,
                        mileage=mileage,
                        engine_volume=basic_details.get('engine_volume'),
                        fuel_type=fuel_type,
                        transmission=transmission,
                        drive_type=detailed_info.get('drive_type_from_page', 'Передний'),
                        body_type=detailed_info.get('body_type_from_page', 'Седан'),
                        color=detailed_info.get('color_from_page', 'Не указан'),
                        url=car_url,
                        image_url=detailed_info.get('images', [None])[0],
                        image_filename=image_files[0] if image_files else None,
                        images=image_files,
                        vin=detailed_info.get('vin_from_page'),
                        description=detailed_info.get('full_description') or f"{brand} {model} {year} года в хорошем состоянии."
                    )

                    parser.cars_data.append(car)
                    print(f"✅ {brand} {model} {year} - {price:,} ₽ (изображений: {len(image_files)})")

                except Exception as e:
                    import traceback
                    print(f"⚠️ Ошибка при обработке объявления {i}: {e}")
                    print(f"  Подробности: {traceback.format_exc()}")
                    continue

            print(f"\n🎉 Успешно обработано {len(parser.cars_data)} автомобилей")

        except Exception as e:
            print(f"❌ Ошибка при парсинге: {e}")

        finally:
            if parser.driver:
                parser.driver.quit()

    try:
        limited_full_parse(url)

        if parser.cars_data:
            print(f"\n📊 Результаты теста:")
            for car in parser.cars_data:
                images_count = len(car.images) if car.images else 0
                print(f"• {car.brand} {car.model} {car.year} - {car.price:,} ₽")
                print(f"  📷 Изображений: {images_count}")
                print(f"  ⛽ {car.fuel_type} | 🔧 {car.transmission}")
                if car.description and car.description != f"{car.brand} {car.model} {car.year} года в хорошем состоянии.":
                    print(f"  📝 {car.description[:80]}...")

            save = input(f"\n💾 Сохранить {len(parser.cars_data)} автомобилей с изображениями? (y/n): ").lower()
            if save in ['y', 'yes', 'да', 'д']:
                parser.save_to_hugo("../hugo-site/content/cars")
                print("✅ Данные сохранены!")

                # Проверяем изображения
                import subprocess
                result = subprocess.run("ls -la ../hugo-site/static/images/cars/", shell=True, capture_output=True, text=True)
                print(f"\n📂 Изображения в папке:")
                print(result.stdout)

                print("\n🌐 Для просмотра запустите:")
                print("cd ../hugo-site && hugo server")
        else:
            print("❌ Автомобили не найдены")

    except KeyboardInterrupt:
        print("\n⏹️ Тест прерван")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")

if __name__ == "__main__":
    test_full_with_images()
