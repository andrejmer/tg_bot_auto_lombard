#!/usr/bin/env python3
"""
Тест селекторов для цены на Авито
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def test_price_selectors():
    """Тестируем различные селекторы для получения цены"""
    print("💰 Тестируем селекторы цены")
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    url = "https://www.avito.ru/brands/be5f12b20964ea30a159d92acf5074cb?gdlkerfdnwq=101&page_from=from_item_header&iid=7526372017&page_from=from_item_card&iid=7526372017"
    
    try:
        driver.get(url)
        time.sleep(5)
        
        # Находим объявления
        car_elements = driver.find_elements(By.CSS_SELECTOR, '[itemtype="http://schema.org/Product"]')
        print(f"Найдено объявлений: {len(car_elements)}")
        
        if car_elements:
            first_car = car_elements[0]
            
            # Пробуем разные селекторы для цены
            price_selectors = [
                '[itemprop="price"]',
                '[data-marker="item-price"]',
                '.price-text',
                '.iva-item-price',
                '.js-item-price',
                'meta[itemprop="price"]',
                'span[itemprop="price"]',
                'div[itemprop="price"]',
                '[class*="price"]',
                '[data-testid*="price"]'
            ]
            
            print("\n💰 Тестируем селекторы цены:")
            for selector in price_selectors:
                try:
                    elements = first_car.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for i, elem in enumerate(elements):
                            text = elem.text.strip()
                            content = elem.get_attribute('content')
                            inner_html = elem.get_attribute('innerHTML')[:100]
                            
                            print(f"  {selector} [{i}]:")
                            print(f"    Text: '{text}'")
                            print(f"    Content: '{content}'")
                            print(f"    HTML: '{inner_html}...'")
                    else:
                        print(f"  {selector}: НЕ НАЙДЕН")
                except Exception as e:
                    print(f"  {selector}: ОШИБКА - {e}")
            
            # Выводим весь HTML первого объявления для анализа
            print(f"\n📄 HTML первого объявления:")
            html = first_car.get_attribute('outerHTML')
            with open("first_car.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("✅ Сохранено в first_car.html")
            
        input("\n⏸️  Нажмите Enter для закрытия...")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_price_selectors()
