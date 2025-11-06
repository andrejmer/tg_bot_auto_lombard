"""
FSM States для создания объявлений автомобилей
"""

from aiogram.fsm.state import State, StatesGroup


class CarCreationStates(StatesGroup):
    """Состояния для создания объявления автомобиля"""
    
    # Основная информация
    brand = State()              # Марка автомобиля
    model = State()              # Модель автомобиля
    year = State()               # Год выпуска
    
    # Технические характеристики
    engine_volume = State()      # Объем двигателя
    fuel_type = State()          # Тип топлива
    transmission = State()       # Коробка передач
    drive_type = State()         # Тип привода
    body_type = State()          # Тип кузова
    
    # Состояние и пробег
    mileage = State()            # Пробег
    condition = State()          # Состояние
    color = State()              # Цвет
    
    # Документы и владение
    vin = State()                # VIN номер
    owners_count = State()       # Количество владельцев
    pts_original = State()       # ПТС оригинал
    
    # Дополнительно
    exchange_possible = State()  # Возможен обмен
    credit_available = State()   # Кредит/Лизинг
    
    # Цена и описание
    price = State()              # Цена
    description = State()        # Описание
    
    # Фотографии
    photos = State()             # Загрузка фотографий
    
    # Подтверждение
    confirm = State()            # Подтверждение создания

