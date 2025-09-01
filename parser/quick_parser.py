#!/usr/bin/env python3
"""
Быстрый парсер Авито без захода в детальные карточки
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from avito_parser import AvitoParser, CarData
import time
from selenium.webdriver.common.by import By
from urllib.parse import urljoin

class QuickAvitoParser(AvitoParser):
    """Быстрая версия парсера без детального анализа карточек"""

    def parse_avito_page_quick(self, url: str):
        """Быстрый парсинг без захода в карточки"""
        print(f"🔍 Быстрый парсинг страницы: {url}")

        if not self.driver:
            self.setup_driver()

        try:
            self.driver.get(url)
            time.sleep(5)
            self.scroll_to_load_all()

            car_elements = self.driver.find_elements(By.CSS_SELECTOR, '[itemtype="http://schema.org/Product"]')
            print(f"📋 Найдено объявлений: {len(car_elements)}")

            for i, element in enumerate(car_elements, 1):
                try:
                    print(f"\n🚗 Обрабатываем {i}/{len(car_elements)}")

                    # Заголовок
                    title_elem = element.find_element(By.CSS_SELECTOR, '[itemprop="name"]')
                    title = title_elem.text.strip()

                    # Цена
                    try:
                        price_elem = element.find_element(By.CSS_SELECTOR, '[itemprop="price"]')
                        price_text = price_elem.get_attribute('content')
                        if not price_text:
                            price_elem = element.find_element(By.CSS_SELECTOR, '[data-marker="item-price"]')
                            price_text = price_elem.text
                        price = self.parse_price(price_text)
                    except:
                        price = 0

                    # Ссылка
                    link_elem = element.find_element(By.CSS_SELECTOR, '[itemprop="url"]')
                    car_url = urljoin(url, link_elem.get_attribute('href'))

                    # Парсим название
                    full_title, brand, model, year = self.parse_car_title(title)

                    # Детали из заголовка
                    basic_details = self.parse_car_details(title)

                    # Правильно извлекаем данные
                    mileage = basic_details.get('mileage', 0)
                    engine_volume = basic_details.get('engine_volume', '2.0')
                    transmission = basic_details.get('transmission', 'AT')

                    # Определяем тип топлива по объему двигателя
                    fuel_type = "Бензин"
                    if engine_volume:
                        try:
                            volume = float(engine_volume)
                            if volume >= 2.5:
                                fuel_type = "Бензин"
                            elif volume <= 2.0:
                                fuel_type = "Бензин"
                        except:
                            fuel_type = "Бензин"

                    # Создаем объект автомобиля
                    car = CarData(
                        title=full_title,
                        brand=brand,
                        model=model,
                        year=year,
                        price=price,
                        mileage=mileage,
                        engine_volume=engine_volume,
                        fuel_type=fuel_type,
                        transmission=transmission,
                        drive_type="Полный",
                        body_type="Внедорожник",
                        color="Не указан",
                        url=car_url,
                        description=f"{brand} {model} {year} года. Пробег {mileage:,} км. Двигатель {engine_volume}л, {fuel_type}, {transmission}."
                    )

                    self.cars_data.append(car)
                    print(f"✅ {brand} {model} {year} - {price:,} ₽")
                    print(f"   🔧 {engine_volume}л {fuel_type} {transmission}")
                    print(f"   📏 {mileage:,} км")

                except Exception as e:
                    print(f"⚠️ Ошибка при обработке объявления {i}: {e}")
                    continue

            print(f"\n🎉 Успешно обработано {len(self.cars_data)} автомобилей")

        except Exception as e:
            print(f"❌ Ошибка при парсинге: {e}")

        finally:
            if self.driver:
                self.driver.quit()

def run_quick_parser():
    """Запуск быстрого парсера"""
    print("🚀 Быстрый парсер Авито (без детального анализа)")
    print("⚡ Время работы: 2-3 минуты")
    print("📝 Получаем базовые данные из заголовков")
    print("=" * 50)

    url = "https://www.avito.ru/brands/be5f12b20964ea30a159d92acf5074cb?gdlkerfdnwq=101&page_from=from_item_header&iid=7526372017&page_from=from_item_card&iid=7526372017"

    parser = QuickAvitoParser(headless=False)

    try:
        parser.parse_avito_page_quick(url)

        if parser.cars_data:
            print(f"\n📊 Результаты:")
            for car in parser.cars_data[:5]:
                print(f"• {car.brand} {car.model} {car.year} - {car.price:,} ₽")
                print(f"  {car.fuel_type} {car.transmission} | {car.mileage:,} км")

            save = input(f"\n💾 Сохранить {len(parser.cars_data)} автомобилей? (y/n): ").lower()
            if save in ['y', 'yes', 'да', 'д']:
                # Очищаем старые файлы
                import subprocess
                subprocess.run("find ../hugo-site/content/cars -name '*.md' -not -name '_index.md' -delete", shell=True)

                parser.save_to_hugo("../hugo-site/content/cars")
                print("✅ Данные сохранены!")

                print("\n🌐 Запустите Hugo для просмотра:")
                print("cd ../hugo-site && hugo server")
        else:
            print("❌ Автомобили не найдены")

    except KeyboardInterrupt:
        print("\n⏹️ Прервано пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")

if __name__ == "__main__":
    run_quick_parser()
