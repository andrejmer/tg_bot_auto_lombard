#!/usr/bin/env python3
"""
Отладочный скрипт для проверки селекторов Авито
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

def debug_avito_selectors():
    """Отладка селекторов для поиска объявлений на Авито"""
    print("🔍 Отладка селекторов Авито")
    print("=" * 50)

    # Настройка Chrome
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Скрываем автоматизацию
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    url = "https://www.avito.ru/brands/be5f12b20964ea30a159d92acf5074cb?gdlkerfdnwq=101&page_from=from_item_header&iid=7526372017&page_from=from_item_card&iid=7526372017"

    try:
        print(f"📱 Открываем: {url}")
        driver.get(url)

        # Ждем загрузки
        time.sleep(5)

        print("\n🔍 Проверяем различные селекторы для объявлений:")

        # Пробуем разные селекторы
        selectors_to_try = [
            '[data-marker="item"]',
            '[data-marker="catalog-serp"] [data-marker="item"]',
            '.items-item',
            '.iva-item-content',
            '.js-catalog-item-enum',
            '.item_table',
            '[itemtype="http://schema.org/Product"]',
            '[data-marker="items-list"] > div',
            '.items-list-item',
            '.snippet-horizontal'
        ]

        found_elements = {}

        for selector in selectors_to_try:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                found_elements[selector] = len(elements)
                print(f"  {selector}: {len(elements)} элементов")
            except Exception as e:
                print(f"  {selector}: ошибка - {e}")

        # Найдем наиболее вероятный селектор
        best_selector = max(found_elements.items(), key=lambda x: x[1])
        print(f"\n✅ Лучший селектор: {best_selector[0]} ({best_selector[1]} элементов)")

        if best_selector[1] > 0:
            print(f"\n🔍 Анализируем первый элемент с селектором {best_selector[0]}:")

            elements = driver.find_elements(By.CSS_SELECTOR, best_selector[0])
            first_element = elements[0]

            # Проверяем селекторы для данных
            data_selectors = {
                'title': ['[itemprop="name"]', '.item-title', '.snippet-title', 'h3 a', '.title-root'],
                'price': ['[itemprop="price"]', '.price-text', '.snippet-price', '.js-item-price'],
                'link': ['[itemprop="url"]', 'a[href*="/avito.ru/"]', '.item-title a', '.snippet-title a']
            }

            for data_type, selectors in data_selectors.items():
                print(f"\n  {data_type.upper()}:")
                for sel in selectors:
                    try:
                        sub_elements = first_element.find_elements(By.CSS_SELECTOR, sel)
                        if sub_elements:
                            element = sub_elements[0]
                            text = element.text.strip() if element.text else "Нет текста"
                            href = element.get_attribute('href') if element.tag_name == 'a' else "Нет ссылки"
                            print(f"    {sel}: НАЙДЕН - '{text[:50]}...' {href[:50] if href != 'Нет ссылки' else ''}")
                        else:
                            print(f"    {sel}: НЕ НАЙДЕН")
                    except Exception as e:
                        print(f"    {sel}: ОШИБКА - {e}")

        print(f"\n📄 Сохраняем HTML страницы для анализа...")
        with open("avito_page_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("✅ HTML сохранен в avito_page_debug.html")

        input("\n⏸️  Нажмите Enter для закрытия браузера...")

    except Exception as e:
        print(f"❌ Ошибка: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    debug_avito_selectors()
