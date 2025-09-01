# 🚀 Деплой Hugo сайта на GitHub Pages

## 📋 Пошаговая инструкция

### 1. Создание GitHub репозитория

1. Перейдите на [GitHub](https://github.com/andrejmer)
2. Нажмите **"New repository"** (зеленая кнопка)
3. Заполните:
   - **Repository name**: `tg_bot_auto_lombard`
   - **Description**: `Telegram Bot + Hugo Website for Auto Lombard`
   - ✅ **Public** (обязательно для бесплатного GitHub Pages)
   - ❌ Не добавляйте README, .gitignore, license (у нас уже есть)

### 2. Подключение к GitHub

```bash
# В вашем терминале в папке проекта:

# Добавляем remote
git remote add origin https://github.com/andrejmer/tg_bot_auto_lombard.git

# Переключаемся на main ветку
git checkout -b main

# Пушим код
git push -u origin main
```

### 3. Настройка GitHub Pages

1. Перейдите в ваш новый репозиторий: `https://github.com/andrejmer/tg_bot_auto_lombard`
2. Нажмите **"Settings"** (верхнее меню)
3. В левом меню найдите **"Pages"**
4. В разделе **"Source"** выберите **"GitHub Actions"**
5. GitHub автоматически найдет наш workflow файл

### 4. Запуск автодеплоя

1. Перейдите во вкладку **"Actions"**
2. Вы увидите workflow **"Deploy Hugo site to Pages"**
3. Он запустится автоматически после push
4. Дождитесь зеленой галочки (обычно 2-3 минуты)

### 5. Ваш сайт готов! 🎉

После успешного деплоя сайт будет доступен по адресу:
```
https://andrejmer.github.io/tg_bot_auto_lombard/
```

## 🤖 Обновление Telegram Bot

### Обновите .env файл:
```bash
# Измените WEBAPP_URL в вашем .env файле
WEBAPP_URL=https://andrejmer.github.io/tg_bot_auto_lombard
```

### Обновите кнопку меню в @BotFather:

1. Откройте Telegram, найдите @BotFather
2. Отправьте `/mybots`
3. Выберите своего бота
4. **"Bot Settings"** → **"Menu Button"** → **"Configure menu button"**
5. Введите новый URL: `https://andrejmer.github.io/tg_bot_auto_lombard/cars/`

## 🧪 Финальное тестирование

```bash
# Запустите бота с новым URL
python run_bot.py
```

В Telegram:
1. Найдите своего бота
2. Отправьте `/start`
3. Нажмите **"🚗 Открыть каталог автомобилей"**
4. Сайт должен открыться внутри Telegram с HTTPS! ✅

## 🔄 Автоматические обновления

Теперь каждый раз когда вы делаете изменения:

```bash
git add .
git commit -m "Update website"
git push
```

GitHub автоматически пересоберет и обновит ваш сайт!

## 📱 Итоговые URL'ы

- **Сайт**: `https://andrejmer.github.io/tg_bot_auto_lombard/`
- **Каталог**: `https://andrejmer.github.io/tg_bot_auto_lombard/cars/`
- **Telegram Bot**: Ваш bot с Web App интеграцией

---

## 🛠️ Команды для копирования

```bash
# Коммитим изменения
git add .
git commit -m "feat: Add GitHub Pages deployment"

# Добавляем remote и пушим
git remote add origin https://github.com/andrejmer/tg_bot_auto_lombard.git
git checkout -b main
git push -u origin main
```

**Готово! Теперь у вас полноценный HTTPS сайт и рабочий Telegram Bot! 🚀**
