# Настройка GitHub Pages для Hugo сайта

## 🚀 Быстрый старт

### 1. Создание GitHub репозитория

1. Перейдите на [GitHub](https://github.com)
2. Нажмите **"New repository"**
3. Заполните:
   - **Repository name**: `tg_bot_auto_lombard`
   - **Description**: `Telegram Bot + Hugo Website for Auto Lombard`
   - ✅ **Public** (для бесплатного GitHub Pages)
   - ❌ **Add README** (у нас уже есть файлы)

### 2. Подключение локального репозитория

```bash
# Добавляем remote (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/tg_bot_auto_lombard.git

# Пушим код
git push -u origin feature/telegram-cards
```

### 3. Настройка GitHub Pages

1. Перейдите в **Settings** вашего репозитория
2. Найдите раздел **"Pages"** в левом меню
3. В **"Source"** выберите **"GitHub Actions"**
4. GitHub автоматически найдет наш workflow файл `.github/workflows/hugo.yml`

### 4. Запуск деплоя

1. Перейдите во вкладку **"Actions"**
2. Нажмите **"Run workflow"** для "Deploy Hugo site to Pages"
3. Дождитесь завершения (обычно 2-3 минуты)

### 5. Получение URL сайта

После успешного деплоя ваш сайт будет доступен по адресу:
```
https://YOUR_USERNAME.github.io/tg_bot_auto_lombard/
```

## 🔧 Настройка Telegram Bot

### Обновление .env файла

```bash
# Обновите WEBAPP_URL в .env файле
WEBAPP_URL=https://YOUR_USERNAME.github.io/tg_bot_auto_lombard
```

### Обновление кнопки меню в @BotFather

1. Напишите @BotFather в Telegram
2. Отправьте `/mybots`
3. Выберите своего бота
4. Выберите **"Bot Settings"** → **"Menu Button"**
5. Выберите **"Configure menu button"**
6. Введите новый URL: `https://YOUR_USERNAME.github.io/tg_bot_auto_lombard/cars/`

## 🧪 Тестирование

1. Перезапустите бота: `python run_bot.py`
2. Откройте Telegram и найдите своего бота
3. Нажмите `/start`
4. Нажмите кнопку **"🚗 Открыть каталог автомобилей"**
5. Сайт должен открыться внутри Telegram!

## 🛠️ Автоматическое обновление

Каждый раз когда вы делаете `git push`, GitHub автоматически:
1. Соберет Hugo сайт
2. Задеплоит на GitHub Pages
3. Обновит ваш сайт

## 📋 Структура URL'ов

- **Главная**: `https://YOUR_USERNAME.github.io/tg_bot_auto_lombard/`
- **Каталог**: `https://YOUR_USERNAME.github.io/tg_bot_auto_lombard/cars/`
- **Конкретная машина**: `https://YOUR_USERNAME.github.io/tg_bot_auto_lombard/cars/bmw-x5-2020/`

## 🔍 Проблемы и решения

### Сайт не обновляется
1. Проверьте статус в **Actions** tab
2. Убедитесь, что workflow завершился успешно
3. Очистите кеш браузера

### 404 ошибка
1. Убедитесь, что `baseURL` в `hugo.toml` правильный
2. Проверьте, что GitHub Pages настроен на "GitHub Actions"

### Стили не загружаются
1. Проверьте, что все CSS файлы в `hugo-site/static/css/`
2. Убедитесь, что пути в layouts правильные

## 🎯 Следующие шаги

1. ✅ Создать GitHub репозиторий
2. ✅ Настроить GitHub Pages
3. ✅ Обновить URL в боте
4. ✅ Протестировать интеграцию
5. 🚀 Profit!

---

**Готово!** У вас есть полноценный сайт с HTTPS и интеграция с Telegram Bot! 🎉
