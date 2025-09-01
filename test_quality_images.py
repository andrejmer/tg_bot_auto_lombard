#!/usr/bin/env python3
"""
Тест качества изображений с 3 автомобилями
"""

import sys
import os
sys.path.append('parser')

from parser.avito_parser import AvitoParser

def test_quality():
    """Тест с 3 автомобилями для проверки качества изображений"""
    print("📸 Тест качества изображений")
    print("🔧 Используем параметры ?size=1200x900 для высокого качества")
    print("🚗 Тестируем 3 автомобиля")
    print("=" * 50)
    
    # Создаем временную функцию для ограниченного парсинга
    parser = AvitoParser(headless=False, max_images=10)
    
    import time
    from selenium.webdriver.common.by import By
    from urllib.parse import urljoin
    
    url = "https://www.avito.ru/brands/be5f12b20964ea30a159d92acf5074cb?gdlkerfdnwq=101&page_from=from_item_header&iid=7526372017&page_from=from_item_card&iid=7526372017"
    
    try:
        if not parser.driver:
            parser.setup_driver()
        
        parser.driver.get(url)
        time.sleep(5)
        parser.scroll_to_load_all()
        
        car_elements = parser.driver.find_elements(By.CSS_SELECTOR, '[itemtype="http://schema.org/Product"]')
        print(f"📋 Найдено объявлений: {len(car_elements)} (тестируем первые 3)")
        
        # Ограничиваем до 3 для теста
        car_elements = car_elements[:3]
        
        # Собираем данные
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
        
        # Парсим каждую карточку
        for i, (title, price, car_url) in enumerate(car_data, 1):
            try:
                print(f"\n🚗 Тестируем {i}/3: {title}")
                
                # Парсим название
                full_title, brand, model, year = parser.parse_car_title(title)
                basic_details = parser.parse_car_details(title)
                
                # Получаем изображения высокого качества
                detailed_info = parser.parse_car_details_from_page(car_url)
                
                if detailed_info.get('images'):
                    print(f"  🎯 Найдено изображений: {len(detailed_info['images'])}")
                    
                    # Показываем примеры URL для проверки качества
                    for j, img_url in enumerate(detailed_info['images'][:2], 1):
                        print(f"    {j}. {img_url}")
                        if '?size=' in img_url:
                            print(f"       ✅ Высокое качество (1200x900)")
                        else:
                            print(f"       ⚠️ Оригинальное качество")
                    
                    # Загружаем изображения
                    image_files = parser.download_multiple_images(
                        detailed_info['images'], brand, model, year
                    )
                    
                    print(f"  ✅ Загружено: {len(image_files)} изображений")
                    
                    # Создаем автомобиль
                    from parser.avito_parser import CarData
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
                print(f"⚠️ Ошибка: {e}")
                print(f"  Подробности: {traceback.format_exc()}")
                continue
        
        if parser.cars_data:
            save = input(f"\n💾 Сохранить {len(parser.cars_data)} автомобилей? (y/n): ").lower()
            if save in ['y', 'yes', 'да', 'д']:
                parser.save_to_hugo("hugo-site/content/cars")
                print("✅ Тест завершен!")
                
                # Показываем размер файлов
                import subprocess
                result = subprocess.run("ls -lah hugo-site/static/images/cars/*.jpg | head -5", shell=True, capture_output=True, text=True)
                print(f"\n📊 Размеры файлов изображений:")
                print(result.stdout)
        
    except KeyboardInterrupt:
        print("\n⏹️ Тест прерван")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
    finally:
        if parser.driver:
            parser.driver.quit()

if __name__ == "__main__":
    test_quality()
