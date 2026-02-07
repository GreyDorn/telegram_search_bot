# ⚡ Быстрое развертывание в облаке

Краткое руководство - выбери вариант и следуй инструкции.

---

## 🎯 Рекомендация: VPS

**Самый надежный и простой вариант для долгосрочного использования.**

### Стоимость: $4-6/мес (или 150₽/мес в РФ)

### За 15 минут:

1. **Аренда VPS**
   - DigitalOcean: https://digitalocean.com
   - Timeweb (РФ): https://timeweb.com
   - Vultr: https://vultr.com

2. **Подключение**
   ```bash
   ssh root@ваш-ip-адрес
   ```

3. **Установка**
   ```bash
   # Обновление системы
   apt update && apt upgrade -y
   
   # Установка Python и Git
   apt install python3 python3-pip git -y
   
   # Клонирование проекта
   git clone https://github.com/ваш-username/telegram_search_bot.git
   cd telegram_search_bot
   
   # Установка зависимостей
   pip3 install -r requirements_telethon.txt
   ```

4. **Настройка .env**
   ```bash
   nano .env
   ```
   
   Вставь:
   ```env
   API_ID=твой_api_id
   API_HASH=твой_api_hash
   BOT_TOKEN=твой_токен
   PHONE=+твой_номер
   CHANNELS=@channel1,@channel2
   SEARCH_LIMIT=1000
   ```
   
   Сохрани: `Ctrl+X` → `Y` → `Enter`

5. **Авторизация**
   ```bash
   python3 bot_telethon.py
   ```
   Введи код из Telegram → `Ctrl+C`

6. **Автозапуск**
   ```bash
   sudo nano /etc/systemd/system/telegram-bot.service
   ```
   
   Вставь:
   ```ini
   [Unit]
   Description=Telegram Search Bot
   After=network.target
   
   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/telegram_search_bot
   ExecStart=/usr/bin/python3 /root/telegram_search_bot/bot_telethon.py
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   Сохрани и запусти:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start telegram-bot
   sudo systemctl enable telegram-bot
   sudo systemctl status telegram-bot
   ```

**✅ Готово!** Бот работает 24/7!

📖 Подробная инструкция: `DEPLOY_VPS.md`

---

## 🆓 Альтернатива: Railway.app (бесплатный старт)

**Простое развертывание за 5 минут, бесплатный план.**

### Стоимость: Бесплатно (500 часов/мес), потом $5/мес

### За 5 минут:

1. **Регистрация**
   - Открой https://railway.app
   - Войди через GitHub

2. **Загрузи проект на GitHub**
   ```bash
   cd C:\Users\user\projects\telegram_search_bot
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/твой-username/telegram_search_bot.git
   git push -u origin main
   ```

3. **Создай проект на Railway**
   - New Project → Deploy from GitHub
   - Выбери репозиторий

4. **Настрой переменные**
   - Variables → Add:
   ```
   API_ID=твой_api_id
   API_HASH=твой_api_hash
   BOT_TOKEN=твой_токен
   PHONE=+твой_номер
   CHANNELS=@channel1,@channel2
   SEARCH_LIMIT=1000
   ```

5. **Авторизация (локально)**
   ```bash
   # На своем ПК
   python bot_telethon.py
   # Введи код → создастся bot_session.session
   
   # Загрузи session в Git
   git add bot_session.session
   git commit -m "Add session"
   git push
   ```

**✅ Готово!** Railway автоматически развернет бота!

📖 Подробная инструкция: `DEPLOY_RAILWAY.md`

---

## 🐳 Для опытных: Docker

**Изолированное окружение, легкое обновление.**

### На VPS с Docker:

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt install docker-compose -y

# Клонирование проекта
git clone https://github.com/твой-username/telegram_search_bot.git
cd telegram_search_bot

# Создание .env файла
nano .env  # заполни данные

# Авторизация
pip3 install -r requirements_telethon.txt
python3 bot_telethon.py  # введи код

# Запуск через Docker
docker-compose up -d

# Проверка логов
docker-compose logs -f
```

**✅ Готово!** Бот в Docker контейнере!

📖 Подробная инструкция: `DEPLOY_DOCKER.md`

---

## 📊 Что выбрать?

### Я новичок → **Railway.app**
- Самый простой
- Бесплатный старт
- Веб-интерфейс

### Я хочу надежность → **VPS**
- Полный контроль
- Стабильность
- $4-6/мес

### Я знаю Docker → **Docker на VPS**
- Профессиональный подход
- Изоляция
- Гибкость

---

## 🔑 Где взять данные

### API_ID и API_HASH:
1. https://my.telegram.org
2. API development tools
3. Create application

### BOT_TOKEN:
1. [@BotFather](https://t.me/botfather) в Telegram
2. `/newbot`
3. Скопируй токен

### PHONE:
- Твой номер телефона в формате `+79991234567`

### CHANNELS:
- Список каналов через запятую: `@channel1,@channel2`

---

## 💡 Мой выбор для тебя

**Если впервые разворачиваешь бота:**
1. Попробуй Railway.app (бесплатно)
2. Если понравится - арендуй VPS

**Если планируешь долгосрочное использование:**
- Сразу VPS (DigitalOcean или Timeweb)

**Если умеешь в Docker:**
- VPS + Docker = ❤️

---

## 📞 Помощь

Выбрал вариант? Открой подробную инструкцию:

- 🖥️ VPS → `DEPLOY_VPS.md`
- 🚂 Railway → `DEPLOY_RAILWAY.md`
- 🐳 Docker → `DEPLOY_DOCKER.md`
- 🤔 Не знаю что выбрать → `HOSTING_GUIDE.md`

**Удачи!** 🚀
