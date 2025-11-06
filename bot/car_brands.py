"""
Справочники марок и моделей автомобилей с поддержкой Dadata API
Обновление данных: 1 раз в день
"""

import os
import json
import aiohttp
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional


# Настройки Dadata API
DADATA_API_KEY = os.getenv("DADATA_API_KEY", "")
DADATA_BRANDS_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/car_brand"

# Путь к файлу кэша
CACHE_FILE = Path(__file__).parent / "car_brands_cache.json"
CACHE_DURATION = timedelta(days=1)  # Обновлять раз в день


# Локальный справочник (фоллбек если API не работает)
LOCAL_CAR_BRANDS = {
    "BMW": [
        "1 серия", "2 серия", "3 серия", "4 серия", "5 серия", "6 серия", "7 серия", "8 серия",
        "X1", "X2", "X3", "X4", "X5", "X6", "X7", "iX", "i3", "i4", "i8", "Z4", "M2", "M3", "M4", "M5"
    ],
    "Mercedes-Benz": [
        "A-класс", "B-класс", "C-класс", "CLA-класс", "CLS-класс", "E-класс", "S-класс",
        "GLA-класс", "GLB-класс", "GLC-класс", "GLE-класс", "GLS-класс", "G-класс",
        "EQA", "EQB", "EQC", "EQE", "EQS", "AMG GT", "SL-класс", "V-класс", "Vito"
    ],
    "Audi": [
        "A1", "A3", "A4", "A5", "A6", "A7", "A8", "Q2", "Q3", "Q4 e-tron", "Q5", "Q7", "Q8",
        "e-tron", "e-tron GT", "RS3", "RS4", "RS5", "RS6", "RS7", "RS Q8", "TT", "R8"
    ],
    "Toyota": [
        "Camry", "Corolla", "RAV4", "Highlander", "Land Cruiser", "Prado", "Fortuner",
        "C-HR", "Yaris", "Supra", "Crown", "Alphard", "Vellfire", "Hilux", "Tundra"
    ],
    "Lexus": [
        "ES", "IS", "LS", "GS", "RC", "LC", "UX", "NX", "RX", "GX", "LX", "LM"
    ],
    "Volkswagen": [
        "Polo", "Golf", "Jetta", "Passat", "Arteon", "Tiguan", "Touareg", "T-Roc",
        "ID.3", "ID.4", "ID.5", "Multivan", "Transporter", "Amarok"
    ],
    "Hyundai": [
        "Solaris", "Accent", "Elantra", "Sonata", "i30", "Tucson", "Santa Fe",
        "Creta", "Palisade", "Kona", "Ioniq 5", "Ioniq 6", "Staria"
    ],
    "Kia": [
        "Rio", "K5", "Stinger", "Cerato", "Ceed", "Sportage", "Sorento",
        "Seltos", "Soul", "Carnival", "EV6", "Niro"
    ],
    "Mazda": ["2", "3", "6", "CX-3", "CX-30", "CX-5", "CX-50", "CX-60", "CX-90", "MX-5", "MX-30"],
    "Honda": ["Civic", "Accord", "CR-V", "HR-V", "Pilot", "Passport", "Ridgeline", "Odyssey"],
    "Nissan": ["Almera", "Sentra", "Teana", "Murano", "Qashqai", "X-Trail", "Patrol", "Juke", "Ariya", "GT-R"],
    "Ford": ["Focus", "Mondeo", "Mustang", "Fiesta", "EcoSport", "Kuga", "Explorer", "Ranger", "F-150", "Bronco"],
    "Chevrolet": ["Aveo", "Cruze", "Malibu", "Camaro", "Corvette", "Tahoe", "Suburban", "Traverse", "Silverado"],
    "Skoda": ["Rapid", "Octavia", "Superb", "Kodiaq", "Karoq", "Kamiq", "Enyaq", "Scala", "Fabia"],
    "Renault": ["Logan", "Sandero", "Kaptur", "Arkana", "Duster", "Megane", "Talisman", "Koleos", "Kangoo"],
    "Peugeot": ["208", "308", "408", "508", "2008", "3008", "5008", "Rifter", "e-208", "e-2008"],
    "Citroen": ["C3", "C4", "C5 Aircross", "Berlingo", "SpaceTourer", "e-C4"],
    "Mitsubishi": ["Lancer", "Outlander", "ASX", "Eclipse Cross", "Pajero", "Pajero Sport", "L200"],
    "Subaru": ["Impreza", "Legacy", "Outback", "Forester", "XV", "Crosstrek", "Ascent", "BRZ", "WRX"],
    "Volvo": ["S60", "S90", "V60", "V90", "XC40", "XC60", "XC90", "C40", "EX30", "EX90"],
    "Porsche": ["911", "718 Boxster", "718 Cayman", "Panamera", "Cayenne", "Macan", "Taycan"],
    "Land Rover": ["Defender", "Discovery", "Discovery Sport", "Range Rover", "Range Rover Sport", "Range Rover Evoque"],
    "Jeep": ["Wrangler", "Cherokee", "Grand Cherokee", "Compass", "Renegade", "Gladiator"],
    "Infiniti": ["Q50", "Q60", "Q70", "QX50", "QX55", "QX60", "QX80"],
    "Genesis": ["G70", "G80", "G90", "GV60", "GV70", "GV80"],
    "Tesla": ["Model 3", "Model S", "Model X", "Model Y", "Cybertruck"],
    "ВАЗ (LADA)": ["Granta", "Vesta", "Largus", "XRAY", "Niva", "Niva Travel"],
    "УАЗ": ["Patriot", "Hunter", "Pickup", "Profi"],
}


class CarBrandsManager:
    """Менеджер справочников с кэшированием и API"""

    def __init__(self):
        self.brands_cache: Dict[str, List[str]] = {}
        self.cache_loaded = False
        self.last_update: Optional[datetime] = None

    def _load_cache(self):
        """Загружает кэш из файла"""
        try:
            if CACHE_FILE.exists():
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.brands_cache = data.get('brands', {})
                    last_update_str = data.get('last_update')
                    if last_update_str:
                        self.last_update = datetime.fromisoformat(last_update_str)
                    self.cache_loaded = True
                    print(f"✅ Кэш загружен из файла. Последнее обновление: {self.last_update}")
        except Exception as e:
            print(f"⚠️ Ошибка загрузки кэша: {e}")
            self.brands_cache = LOCAL_CAR_BRANDS.copy()

    def _save_cache(self):
        """Сохраняет кэш в файл"""
        try:
            data = {
                'brands': self.brands_cache,
                'last_update': self.last_update.isoformat() if self.last_update else None
            }
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Кэш сохранен в файл")
        except Exception as e:
            print(f"⚠️ Ошибка сохранения кэша: {e}")

    def _is_cache_expired(self) -> bool:
        """Проверяет, устарел ли кэш"""
        if not self.last_update:
            return True
        return datetime.now() - self.last_update > CACHE_DURATION

    async def _fetch_brands_from_api(self) -> List[str]:
        """Получает список марок из Dadata API"""
        if not DADATA_API_KEY or DADATA_API_KEY == "YOUR_DADATA_KEY_HERE":
            print("⚠️ DADATA_API_KEY не установлен")
            return []

        try:
            headers = {
                "Authorization": f"Token {DADATA_API_KEY}",
                "Content-Type": "application/json"
            }

            data = {"query": "", "count": 200}

            async with aiohttp.ClientSession() as session:
                async with session.post(DADATA_BRANDS_URL, json=data, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        brands = [item["value"] for item in result.get("suggestions", [])]
                        print(f"✅ Получено {len(brands)} марок из Dadata API")
                        return brands
                    else:
                        print(f"⚠️ Ошибка Dadata API: {response.status}")
                        return []

        except Exception as e:
            print(f"⚠️ Ошибка при запросе к Dadata: {e}")
            return []

    async def update_cache_if_needed(self):
        """Обновляет кэш если он устарел (раз в день)"""
        # Загружаем кэш из файла если еще не загружен
        if not self.cache_loaded:
            self._load_cache()

        # Проверяем нужно ли обновление
        if not self._is_cache_expired():
            print(f"✅ Кэш актуален (обновлен: {self.last_update})")
            return

        print("🔄 Обновление справочника марок из API...")

        # Получаем марки из API
        api_brands = await self._fetch_brands_from_api()

        if api_brands:
            # Создаем новый справочник с моделями из локальной базы
            new_cache = {}
            for brand in api_brands:
                # Если есть модели в локальном справочнике - используем их
                if brand in LOCAL_CAR_BRANDS:
                    new_cache[brand] = LOCAL_CAR_BRANDS[brand]
                else:
                    # Для новых марок - пустой список (пользователь введет вручную)
                    new_cache[brand] = []

            self.brands_cache = new_cache
            self.last_update = datetime.now()
            self._save_cache()
            print(f"✅ Справочник обновлен! Марок: {len(self.brands_cache)}")
        else:
            # Если API не сработал - используем локальный справочник
            if not self.brands_cache:
                self.brands_cache = LOCAL_CAR_BRANDS.copy()
                self.last_update = datetime.now()
                self._save_cache()
                print("⚠️ Используем локальный справочник (API недоступен)")

    def get_all_brands(self) -> List[str]:
        """Возвращает список всех марок"""
        if not self.brands_cache:
            self.brands_cache = LOCAL_CAR_BRANDS.copy()
        return sorted(self.brands_cache.keys())

    def get_models_for_brand(self, brand: str) -> List[str]:
        """Возвращает список моделей для марки"""
        return self.brands_cache.get(brand, [])


# Глобальный экземпляр менеджера
_manager = CarBrandsManager()


# Публичные функции для совместимости
async def update_brands_cache():
    """Обновляет кэш справочников (вызывается при старте бота)"""
    await _manager.update_cache_if_needed()


def get_all_brands() -> List[str]:
    """Возвращает список всех марок"""
    return _manager.get_all_brands()


def get_models_for_brand(brand: str) -> List[str]:
    """Возвращает список моделей для марки"""
    return _manager.get_models_for_brand(brand)


# Для обратной совместимости
CAR_BRANDS = LOCAL_CAR_BRANDS
