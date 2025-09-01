#!/usr/bin/env python3
"""
Скрипт для парсинга автомобилей с Авито и создания файлов для Hugo каталога.
Использует Selenium для обхода антиробота.
"""

import os
import re
import time
import json
import datetime
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass
from typing import List, Optional

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("❌ Selenium не установлен!")
    print("📦 Установите: pip install selenium webdriver-manager")
    print("🌐 Или установите ChromeDriver: brew install chromedriver")
    exit(1)

@dataclass
class CarData:
    """Структура данных автомобиля"""
    title: str
    brand: str
    model: str
    year: int
    price: int
    mileage: Optional[int] = None
    engine_volume: Optional[str] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    drive_type: Optional[str] = None
    body_type: Optional[str] = None
    color: Optional[str] = None
    condition: str = "Хорошее"
    description: Optional[str] = None
    vin: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    image_filename: Optional[str] = None
    images: Optional[List[str]] = None

class AvitoParser:
    def __init__(self, headless: bool = False, max_images: int = 10):
        """Инициализация парсера"""
        self.driver = None
        self.headless = headless
        self.max_images = max_images
        self.cars_data: List[CarData] = []

        # Карта трансмиссий
        self.transmission_map = {
            'MT': 'MT', 'МТ': 'MT', 'механика': 'MT', 'ручная': 'MT',
            'AT': 'AT', 'АТ': 'AT', 'автомат': 'AT', 'автоматическая': 'AT',
            'CVT': 'AT', 'робот': 'AT', 'вариатор': 'AT'
        }

        # Карта типов топлива
        self.fuel_map = {
            'бензин': 'Бензин', 'дизель': 'Дизель', 'гибрид': 'Гибрид',
            'электро': 'Электро', 'газ': 'Газ'
        }

    def setup_driver(self):
        """Настройка Chrome драйвера"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless")

        # Настройки для обхода детекции
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        try:
            # Автоматическая установка ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Chrome драйвер запущен")
        except Exception as e:
            print(f"❌ Ошибка запуска драйвера: {e}")
            print("🔧 Попробуйте: brew install chromedriver")
            raise

    def parse_car_title(self, title: str) -> tuple:
        """Парсинг названия автомобиля"""
        # Примеры: "BMW 5 серия 2.0 AT, 2017", "Infiniti QX80 5.6 AT, 2015"

        # Убираем технические характеристики в конце
        title_clean = re.sub(r',.*$', '', title)
        title_clean = re.sub(r'\d+\.\d+\s+(AT|MT)', '', title_clean).strip()

        # Разбираем на части
        parts = title_clean.split()
        if len(parts) < 2:
            return title, "Не определен", title, 2020

        brand = parts[0]

        # Особые случаи для брендов
        if brand.upper() in ['ВАЗ', 'VAZ']:
            brand = "ВАЗ (LADA)"
        elif brand.upper() == 'LAND' and len(parts) > 1 and parts[1].upper() == 'ROVER':
            brand = "Land Rover"
            parts = parts[1:]  # убираем "LAND" из частей

        # Ищем год в конце
        year = 2020
        year_match = re.search(r'\b(19|20)\d{2}\b', title)
        if year_match:
            year = int(year_match.group())

        # Модель - все что между брендом и годом
        model_parts = []
        for part in parts[1:]:
            if re.match(r'\b(19|20)\d{2}\b', part):
                break
            if not re.match(r'\d+\.\d+', part):  # пропускаем объем двигателя
                model_parts.append(part)

        model = ' '.join(model_parts) if model_parts else "Не определена"

        return title, brand, model, year

    def parse_price(self, price_text: str) -> int:
        """Парсинг цены"""
        # Убираем все кроме цифр
        price_clean = re.sub(r'[^\d]', '', price_text)
        try:
            return int(price_clean)
        except ValueError:
            return 0

    def parse_mileage(self, text: str) -> Optional[int]:
        """Парсинг пробега"""
        mileage_match = re.search(r'(\d+(?:\s*\d+)*)\s*(?:км|тыс)', text.lower())
        if mileage_match:
            mileage_str = re.sub(r'\s+', '', mileage_match.group(1))
            try:
                mileage = int(mileage_str)
                # Если число меньше 1000, вероятно это тысячи км
                if mileage < 1000:
                    mileage *= 1000
                return mileage
            except ValueError:
                pass
        return None

    def parse_car_details(self, title: str, description: str = "") -> dict:
        """Парсинг деталей автомобиля из текста"""
        text = f"{title} {description}".lower()

        details = {}

        # Парсинг трансмиссии
        for key, value in self.transmission_map.items():
            if key.lower() in text:
                details['transmission'] = value
                break

        # Парсинг типа топлива
        for key, value in self.fuel_map.items():
            if key in text:
                details['fuel_type'] = value
                break

        # Парсинг объема двигателя
        engine_match = re.search(r'(\d+\.\d+)', title)
        if engine_match:
            details['engine_volume'] = engine_match.group(1)

        # Парсинг пробега
        mileage = self.parse_mileage(text)
        if mileage:
            details['mileage'] = mileage

        return details

    def download_image(self, image_url: str, filename: str, images_dir: str = "../hugo-site/static/images/cars") -> bool:
        """Загрузка изображения с Авито"""
        try:
            # Создаем директорию если не существует
            images_path = Path(images_dir)
            images_path.mkdir(parents=True, exist_ok=True)

            # Полный путь к файлу
            filepath = images_path / filename

            # Если файл уже существует, пропускаем
            if filepath.exists():
                print(f"📷 Изображение уже существует: {filename}")
                return True

            # Заголовки для запроса
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

            # Загружаем изображение
            response = requests.get(image_url, headers=headers, timeout=10)
            response.raise_for_status()

            # Сохраняем файл
            with open(filepath, 'wb') as f:
                f.write(response.content)

            print(f"✅ Загружено изображение: {filename}")
            return True

        except Exception as e:
            print(f"❌ Ошибка загрузки изображения {filename}: {e}")
            return False

    def generate_image_filename(self, brand: str, model: str, year: int, index: int = 0) -> str:
        """Генерация имени файла для изображения"""
        # Очищаем название от специальных символов
        clean_brand = re.sub(r'[^\w\-]', '', brand.lower().replace(' ', '-'))
        clean_model = re.sub(r'[^\w\-]', '', model.lower().replace(' ', '-'))

        # Формируем имя файла
        if index > 0:
            return f"{clean_brand}-{clean_model}-{year}-{index}.jpg"
        else:
            return f"{clean_brand}-{clean_model}-{year}.jpg"

    def wait_and_click(self, element, timeout=10):
        """Безопасное ожидание и клик"""
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except TimeoutException:
            return False

    def scroll_to_load_all(self):
        """Прокрутка страницы для загрузки всех объявлений"""
        print("📜 Прокручиваем страницу для загрузки всех объявлений...")

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Прокручиваем вниз
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Ждем загрузки
            time.sleep(3)

            # Проверяем, изменилась ли высота страницы
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        print("✅ Все объявления загружены")

    def parse_car_details_from_page(self, car_url: str) -> dict:
        """Парсинг детальной страницы автомобиля"""
        try:
            print(f"  🔗 Переходим в карточку: {car_url}")

            # Открываем страницу автомобиля в новой вкладке
            self.driver.execute_script(f"window.open('{car_url}', '_blank');")
            self.driver.switch_to.window(self.driver.window_handles[-1])

            # Ждем загрузки
            time.sleep(3)

            details = {}

                        # Ищем все изображения
            images = []
            try:
                # Изображения в галерее предварительного просмотра
                gallery_items = self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="image-preview/item"] img')
                for img in gallery_items:
                    src = img.get_attribute('src')
                    if src and not any(x in src.lower() for x in ['placeholder', 'no-photo']):
                        # Получаем изображение в высоком качестве
                        # Заменяем параметры на максимальное качество
                        if '?cqp=' in src:
                            # Используем параметры для высокого качества
                            base_url = src.split('?cqp=')[0]
                            high_quality_src = f"{base_url}?size=1200x900"
                        else:
                            high_quality_src = src
                        
                        if high_quality_src not in images:
                            images.append(high_quality_src)

                # Если не нашли в галерее, ищем основное изображение
                if not images:
                    main_imgs = self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="image-frame/image"], .desktop-1i6k59z, img[alt*="цена"]')
                    for img in main_imgs:
                        src = img.get_attribute('src')
                        if src and not any(x in src.lower() for x in ['placeholder', 'no-photo']):
                            if '?cqp=' in src:
                                base_url = src.split('?cqp=')[0]
                                high_quality_src = f"{base_url}?size=1200x900"
                            else:
                                high_quality_src = src
                            
                            if high_quality_src not in images:
                                images.append(high_quality_src)

            except NoSuchElementException:
                pass

            details['images'] = images[:self.max_images]  # Ограничиваем количество изображений

            # Полное описание
            try:
                desc_elem = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="item-view/item-description"], .item-description-text, [itemprop="description"]')
                details['full_description'] = desc_elem.text.strip()
            except NoSuchElementException:
                details['full_description'] = None

            # Характеристики из таблицы
            try:
                params = self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="item-view/item-params"], .item-params .item-params-list li')
                for param in params:
                    param_text = param.text.strip()
                    if 'Год выпуска' in param_text:
                        details['year_from_page'] = param_text.split(':')[-1].strip()
                    elif 'Пробег' in param_text:
                        details['mileage_from_page'] = param_text.split(':')[-1].strip()
                    elif 'Коробка передач' in param_text:
                        details['transmission_from_page'] = param_text.split(':')[-1].strip()
                    elif 'Тип топлива' in param_text:
                        details['fuel_type_from_page'] = param_text.split(':')[-1].strip()
                    elif 'Привод' in param_text:
                        details['drive_type_from_page'] = param_text.split(':')[-1].strip()
                    elif 'Тип кузова' in param_text:
                        details['body_type_from_page'] = param_text.split(':')[-1].strip()
                    elif 'Цвет' in param_text:
                        details['color_from_page'] = param_text.split(':')[-1].strip()
                    elif 'VIN' in param_text:
                        details['vin_from_page'] = param_text.split(':')[-1].strip()
            except NoSuchElementException:
                pass

            # Закрываем вкладку и возвращаемся к списку
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

            return details

        except Exception as e:
            print(f"  ❌ Ошибка при парсинге карточки: {e}")
            # Попытка вернуться к основной вкладке при ошибке
            try:
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass
            return {}

    def download_multiple_images(self, images: list, brand: str, model: str, year: int) -> list:
        """Загрузка нескольких изображений"""
        downloaded_files = []

        for i, image_url in enumerate(images):
            try:
                filename = self.generate_image_filename(brand, model, year, i)
                if self.download_image(image_url, filename):
                    downloaded_files.append(filename)
                    print(f"  📷 Загружено изображение {i+1}/{len(images)}: {filename}")
                else:
                    print(f"  ❌ Не удалось загрузить изображение {i+1}")
            except Exception as e:
                print(f"  ⚠️ Ошибка загрузки изображения {i+1}: {e}")
                continue

        return downloaded_files

    def parse_avito_page(self, url: str):
        """Парсинг страницы Авито с переходом в каждую карточку"""
        print(f"🔍 Парсим страницу: {url}")

        if not self.driver:
            self.setup_driver()

        try:
            self.driver.get(url)

            # Ждем загрузки страницы
            time.sleep(5)

            # Прокручиваем для загрузки всех объявлений
            self.scroll_to_load_all()

            # Ищем все карточки объявлений
            car_elements = self.driver.find_elements(By.CSS_SELECTOR, '[itemtype="http://schema.org/Product"]')

            print(f"📋 Найдено объявлений: {len(car_elements)}")
            print(f"⏱️  Примерное время парсинга: {len(car_elements) * 5} секунд")

            # Собираем ссылки на все объявления
            car_links = []
            car_titles = []
            car_prices = []

            for i, element in enumerate(car_elements, 1):
                try:
                    # Заголовок
                    title_elem = element.find_element(By.CSS_SELECTOR, '[itemprop="name"]')
                    title = title_elem.text.strip()
                    car_titles.append(title)

                    # Цена
                    try:
                        # Сначала пробуем получить из content атрибута
                        price_elem = element.find_element(By.CSS_SELECTOR, '[itemprop="price"]')
                        price_text = price_elem.get_attribute('content')
                        if not price_text:
                            # Если content пустой, пробуем text из data-marker
                            price_elem = element.find_element(By.CSS_SELECTOR, '[data-marker="item-price"]')
                            price_text = price_elem.text
                        price = self.parse_price(price_text)
                    except:
                        price = 0
                    car_prices.append(price)

                    # Ссылка на объявление
                    link_elem = element.find_element(By.CSS_SELECTOR, '[itemprop="url"]')
                    car_url = urljoin(url, link_elem.get_attribute('href'))
                    car_links.append(car_url)

                except Exception as e:
                    print(f"⚠️ Ошибка при получении данных объявления {i}: {e}")
                    continue

            # Теперь парсим каждую карточку детально
            for i, (car_url, title, price) in enumerate(zip(car_links, car_titles, car_prices), 1):
                try:
                    print(f"\n🚗 Обрабатываем {i}/{len(car_links)}: {title}")

                    # Парсим название
                    full_title, brand, model, year = self.parse_car_title(title)

                    # Базовые детали из заголовка
                    basic_details = self.parse_car_details(title)

                    # Получаем детальную информацию из карточки
                    detailed_info = self.parse_car_details_from_page(car_url)

                    # Загружаем изображения
                    image_files = []
                    if detailed_info.get('images'):
                        image_files = self.download_multiple_images(
                            detailed_info['images'], brand, model, year
                        )

                                        # Используем более точные данные из карточки, если они есть
                    mileage = basic_details.get('mileage', 0)
                    if detailed_info.get('mileage_from_page'):
                        try:
                            mileage_text = detailed_info['mileage_from_page']
                            mileage = self.parse_mileage(mileage_text)
                        except:
                            pass

                    transmission = basic_details.get('transmission', 'AT')
                    if detailed_info.get('transmission_from_page'):
                        trans_text = detailed_info['transmission_from_page'].lower()
                        for key, value in self.transmission_map.items():
                            if key.lower() in trans_text:
                                transmission = value
                                break

                    fuel_type = basic_details.get('fuel_type', 'Бензин')
                    if detailed_info.get('fuel_type_from_page'):
                        fuel_text = detailed_info['fuel_type_from_page'].lower()
                        for key, value in self.fuel_map.items():
                            if key in fuel_text:
                                fuel_type = value
                                break

                    # Создаем объект автомобиля с полной информацией
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
                        image_url=detailed_info.get('images', [None])[0] if detailed_info.get('images') else None,
                        image_filename=image_files[0] if image_files else None,
                        images=image_files,
                        vin=detailed_info.get('vin_from_page'),
                        description=detailed_info.get('full_description') or f"{brand} {model} {year} года в хорошем состоянии."
                    )

                    # Убрали добавление списка изображений в описание

                    self.cars_data.append(car)
                    print(f"✅ {brand} {model} {year} - {price:,} ₽ (изображений: {len(image_files)})")

                except Exception as e:
                    import traceback
                    print(f"⚠️ Ошибка при обработке объявления {i}: {e}")
                    print(f"  Подробности: {traceback.format_exc()}")
                    continue

            print(f"\n🎉 Успешно обработано {len(self.cars_data)} автомобилей")

        except Exception as e:
            print(f"❌ Ошибка при парсинге: {e}")

        finally:
            if self.driver:
                self.driver.quit()

    def save_to_hugo(self, output_dir: str = "../hugo-site/content/cars"):
        """Сохранение в формате Hugo"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        print(f"💾 Сохраняем {len(self.cars_data)} автомобилей в Hugo...")

        for car in self.cars_data:
            # Генерируем имя файла
            filename = f"{car.brand.lower().replace(' ', '-').replace('(', '').replace(')', '')}-{car.model.lower().replace(' ', '-').replace('/', '-')}-{car.year}.md"
            filename = re.sub(r'[^\w\-.]', '', filename)

            filepath = output_path / filename

                        # Определяем изображения
            if car.images and len(car.images) > 0:
                images_list = [f"images/cars/{img}" for img in car.images]
                images_yaml = '[' + ', '.join([f'"{img}"' for img in images_list]) + ']'
                main_image = images_list[0]
            else:
                images_yaml = '["images/cars/placeholder.svg"]'
                main_image = "images/cars/placeholder.svg"

            # Шаблон файла
            content = f"""---
title: "{car.title}"
date: {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')}
draft: false
image: "{main_image}"
images: {images_yaml}

# Данные для фильтрации
brand: "{car.brand}"
model: "{car.model}"

year: {car.year}
price: {car.price}
mileage: {car.mileage or 50000}
engine_volume: {car.engine_volume or '2.0'}
fuel_type: "{car.fuel_type}"
transmission: "{car.transmission}"
drive_type: "{car.drive_type or 'Передний'}"
body_type: "{car.body_type or 'Седан'}"
color: "{car.color or 'Не указан'}"
condition: "{car.condition}"
vin: "{car.vin or 'Не указан'}"
owners_count: 1
pts_original: true
customs_cleared: true
exchange_possible: true
credit_available: true
description: "{car.description}"
source_url: "{car.url}"
tags: ["авито", "автомобиль"]
weight: 1
---

## Характеристики {car.brand} {car.model} {car.year}

| Параметр | Значение |
|----------|----------|
| **Марка** | {car.brand} |
| **Модель** | {car.model} |
| **Год выпуска** | {car.year} |
| **Цена** | {car.price:,} ₽ |
| **Пробег** | {car.mileage or 'Не указан'} км |
| **Объем двигателя** | {car.engine_volume or 'Не указан'} л |
| **Тип топлива** | {car.fuel_type} |
| **Коробка передач** | {car.transmission} |
| **Состояние** | {car.condition} |

## Описание

{car.description}

### Контакты
- Телефон: +7 (999) 123-45-67
- Email: info@auto-lombard.ru

**Возможен обмен, кредит, лизинг.**
"""

            # Сохраняем файл
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Создан: {filepath}")

    def save_to_json(self, filename: str = "avito_cars.json"):
        """Сохранение в JSON для анализа"""
        data = []
        for car in self.cars_data:
            data.append({
                'title': car.title,
                'brand': car.brand,
                'model': car.model,
                'year': car.year,
                'price': car.price,
                'mileage': car.mileage,
                'fuel_type': car.fuel_type,
                'transmission': car.transmission,
                'url': car.url,
                'image_url': car.image_url,
                'image_filename': car.image_filename,
                'images': car.images
            })

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"💾 Данные сохранены в {filename}")

def main():
    """Главная функция"""
    print("🚗 Авито Парсер для автоломбарда")
    print("=" * 50)

    # URL страницы пользователя
    avito_url = "https://www.avito.ru/brands/be5f12b20964ea30a159d92acf5074cb?gdlkerfdnwq=101&page_from=from_item_header&iid=7526372017&page_from=from_item_card&iid=7526372017"

    # Создаем парсер
    parser = AvitoParser(headless=False)  # False = показывать браузер

    try:
        # Парсим страницу
        parser.parse_avito_page(avito_url)

        if parser.cars_data:
            # Сохраняем в Hugo
            parser.save_to_hugo()

            # Сохраняем в JSON для анализа
            parser.save_to_json()

            print("\n🎉 Парсинг завершен!")
            print(f"📊 Обработано автомобилей: {len(parser.cars_data)}")
            print(f"📁 Файлы созданы в: hugo-site/content/cars/")
            print("\n📝 Следующие шаги:")
            print("1. Проверьте созданные файлы")
            print("2. Запустите: hugo --source hugo-site")
            print("3. Проверьте models-data.json")
            print("4. Задеплойте: git add . && git commit -m 'Add cars from Avito' && git push")

        else:
            print("❌ Не удалось найти автомобили")

    except KeyboardInterrupt:
        print("\n⏹️ Парсинг прерван пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
