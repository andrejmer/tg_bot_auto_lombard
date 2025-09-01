#!/usr/bin/env python3
"""
Утилита для оптимизации изображений автомобилей
"""

import os
from pathlib import Path
from PIL import Image

def optimize_images(images_dir: str = "hugo-site/static/images/cars"):
    """Оптимизация всех изображений в директории"""
    images_path = Path(images_dir)

    if not images_path.exists():
        print(f"❌ Директория {images_dir} не найдена")
        return

    print(f"🖼️  Оптимизируем изображения в {images_dir}")

    # Поддерживаемые форматы
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}

    for image_file in images_path.glob('*'):
        if image_file.suffix.lower() in supported_formats:
            try:
                print(f"📷 Обрабатываем: {image_file.name}")

                # Открываем изображение
                with Image.open(image_file) as img:
                    # Конвертируем в RGB если необходимо
                    if img.mode in ('RGBA', 'LA'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')

                    # Изменяем размер если слишком большое
                    max_width = 800
                    max_height = 600

                    if img.width > max_width or img.height > max_height:
                        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                        print(f"  📏 Изменен размер до {img.width}x{img.height}")

                    # Сохраняем в формате WebP
                    webp_file = image_file.with_suffix('.webp')
                    img.save(webp_file, 'WebP', quality=85, optimize=True)

                    # Сохраняем также оптимизированную JPEG версию
                    if image_file.suffix.lower() != '.jpg':
                        jpg_file = image_file.with_suffix('.jpg')
                        img.save(jpg_file, 'JPEG', quality=85, optimize=True)
                    else:
                        # Оптимизируем существующий JPEG
                        img.save(image_file, 'JPEG', quality=85, optimize=True)

                    # Размеры файлов
                    original_size = image_file.stat().st_size
                    webp_size = webp_file.stat().st_size if webp_file.exists() else 0

                    print(f"  💾 Исходный: {original_size//1024}KB → WebP: {webp_size//1024}KB")

            except Exception as e:
                print(f"❌ Ошибка при обработке {image_file.name}: {e}")

    print("✅ Оптимизация изображений завершена")

if __name__ == "__main__":
    try:
        from PIL import Image
        optimize_images()
    except ImportError:
        print("❌ Pillow не установлен!")
        print("📦 Установите: pip install Pillow")
