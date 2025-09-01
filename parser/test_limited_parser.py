#!/usr/bin/env python3
"""
Тест парсера с ограничением на 3 автомобиля для быстрого тестирования
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from avito_parser import AvitoParser

def test_limited():
    """Тест с ограничением в 3 автомобиля"""
    print("🧪 Тест парсера (первые 3 автомобиля)")
    print("=" * 50)
    
    parser = AvitoParser(headless=False)
    
    # URL страницы
    url = "https://www.avito.ru/brands/be5f12b20964ea30a159d92acf5074cb?gdlkerfdnwq=101&page_from=from_item_header&iid=7526372017&page_from=from_item_card&iid=7526372017"
    
    # Ограничиваем количество для теста
    original_parse = parser.parse_avito_page
    
    def limited_parse(url):
        """Парсим только первые 3 автомобиля"""
        print(f"🔍 Парсим страницу: {url}")
        
        if not parser.driver:
            parser.setup_driver()
        
        try:
            parser.driver.get(url)
            time.sleep(5)
            parser.scroll_to_load_all()
            
            car_elements = parser.driver.find_elements(By.CSS_SELECTOR, '[itemtype="http://schema.org/Product"]')
            print(f"📋 Найдено объявлений: {len(car_elements)} (берем первые 3)")
            
            # Ограничиваем до 3
            car_elements = car_elements[:3]
            
            # Собираем ссылки
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
            
            # Парсим каждую карточку
            for i, (car_url, title, price) in enumerate(zip(car_links, car_titles, car_prices), 1):
                try:
                    print(f"\n🚗 Обрабатываем {i}/3: {title}")
                    
                    # Парсим название
                    full_title, brand, model, year = parser.parse_car_title(title)
                    print(f"  📝 Разобрано: {brand} | {model} | {year}")
                    
                    # Базовые детали из заголовка
                    basic_details = parser.parse_car_details(title)
                    print(f"  🔧 Детали: {basic_details}")
                    
                    # Пропускаем детальный парсинг для теста
                    print(f"  💰 Цена: {price:,} ₽")
                    print(f"  🔗 URL: {car_url[:50]}...")
                    
                    # Создаем упрощенный объект
                    from avito_parser import CarData
                    car = CarData(
                        title=full_title,
                        brand=brand,
                        model=model,
                        year=year,
                        price=price,
                        url=car_url,
                        description=f"{brand} {model} {year} года в хорошем состоянии."
                    )
                    
                    parser.cars_data.append(car)
                    print(f"✅ Успешно обработан!")
                    
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
    
    # Импортируем необходимые модули
    import time
    from selenium.webdriver.common.by import By
    from urllib.parse import urljoin
    
    try:
        limited_parse(url)
        
        if parser.cars_data:
            save = input(f"\n💾 Сохранить {len(parser.cars_data)} автомобилей? (y/n): ").lower()
            if save in ['y', 'yes', 'да', 'д']:
                parser.save_to_hugo("../hugo-site/content/cars")
                print("✅ Данные сохранены!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Тест прерван")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")

if __name__ == "__main__":
    test_limited()
