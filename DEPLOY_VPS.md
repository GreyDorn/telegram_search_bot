# 🖥️ Развертывание на VPS сервере

VPS (Virtual Private Server) - самый надежный вариант для бота. Полный контроль, без ограничений.

## ✅ Преимущества VPS:

- 💪 Полный контроль над сервером
- 🔒 Безопасность
- ⚡ Высокая производительность
- 🔄 Автозапуск после перезагрузки
- 💾 Постоянное хранилище

## 💰 Стоимость:

- **DigitalOcean:** от $4-6/мес
- **Vultr:** от $2.5-6/мес
- **Timeweb (РФ):** от 150₽/мес
- **Reg.ru (РФ):** от 199₽/мес

---

## 🚀 Пошаговая инструкция

### Шаг 1: Аренда VPS

#### Рекомендую DigitalOcean:

1. Регистрация на https://digitalocean.com
2. Create → Droplets
3. Выбери параметры:
   - **OS:** Ubuntu 22.04 LTS
   - **Plan:** Basic ($6/мес)
   - **CPU:** Regular (1GB RAM достаточно)
   - **Datacenter:** Ближайший к тебе
4. Добавь SSH ключ (или используй пароль)
5. Create Droplet

Получишь IP адрес: `123.456.789.123`

---

### Шаг 2: Подключение к серверу

Открой PowerShell:

```bash
# Замени IP на свой
ssh root@123.456.789.123

# Введи пароль (если используешь пароль)
```

---

### Шаг 3: Настройка сервера

После подключения выполни:

```bash
# Обновление системы
apt update && apt upgrade -y

# Установка Python и pip
apt install python3 python3-pip git -y

# Проверка версии
python3 --version  # Должно быть 3.10+
```

---

### Шаг 4: Создание пользователя для бота

```bash
# Создание пользователя (не запускай от root!)
adduser botuser

# Добавление в sudo группу
usermod -aG sudo botuser

# Переключение на пользователя
su - botuser
```

---

### Шаг 5: Загрузка проекта

#### Вариант А: Через Git (рекомендуется)

```bash
cd ~
git clone https://github.com/ТвойUsername/telegram_search_bot.git
cd telegram_search_bot
```

#### Вариант Б: Через SCP (копирование с ПК)

На своем ПК (в PowerShell):

```bash
# Замени IP и путь
scp -r C:\Users\user\projects\telegram_search_bot root@123.456.789.123:/home/botuser/
```

---

### Шаг 6: Установка зависимостей

На сервере:

```bash
cd ~/telegram_search_bot

# Установка зависимостей
pip3 install -r requirements_telethon.txt
```

---

### Шаг 7: Создание .env файла

```bash
# Создание .env файла
nano .env
```

Вставь свои данные:

```env
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
PHONE=+79991234567
CHANNELS=@channel1,@channel2,@channel3
SEARCH_LIMIT=1000
```

Сохрани: `Ctrl+X` → `Y` → `Enter`

---

### Шаг 8: Первый запуск (авторизация)

```bash
python3 bot_telethon.py
```

Введи код подтверждения из Telegram.

После успешной авторизации появится файл `bot_session.session`.

Останови бота: `Ctrl+C`

---

### Шаг 9: Настройка автозапуска (systemd)

Создай systemd service:

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
User=botuser
WorkingDirectory=/home/botuser/telegram_search_bot
ExecStart=/usr/bin/python3 /home/botuser/telegram_search_bot/bot_telethon.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Сохрани: `Ctrl+X` → `Y` → `Enter`

---

### Шаг 10: Запуск и активация

```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Запуск бота
sudo systemctl start telegram-bot

# Автозапуск при старте системы
sudo systemctl enable telegram-bot

# Проверка статуса
sudo systemctl status telegram-bot
```

Должно быть: `Active: active (running)`

---

## 📊 Управление ботом

### Просмотр логов:

```bash
# Последние 50 строк
sudo journalctl -u telegram-bot -n 50

# В реальном времени
sudo journalctl -u telegram-bot -f

# За сегодня
sudo journalctl -u telegram-bot --since today
```

### Управление:

```bash
# Остановка
sudo systemctl stop telegram-bot

# Запуск
sudo systemctl start telegram-bot

# Перезапуск
sudo systemctl restart telegram-bot

# Статус
sudo systemctl status telegram-bot
```

---

## 🔄 Обновление бота

### Если используешь Git:

```bash
cd ~/telegram_search_bot
git pull
sudo systemctl restart telegram-bot
```

### Если копируешь файлы:

```bash
# На своем ПК
scp bot_telethon.py botuser@123.456.789.123:/home/botuser/telegram_search_bot/

# На сервере
sudo systemctl restart telegram-bot
```

---

## 🔒 Безопасность

### 1. Настройка файрвола:

```bash
# Установка UFW
sudo apt install ufw -y

# Разрешение SSH
sudo ufw allow ssh

# Включение файрвола
sudo ufw enable
```

### 2. Отключение root логина по SSH:

```bash
sudo nano /etc/ssh/sshd_config
```

Найди и измени:
```
PermitRootLogin no
```

Перезапусти SSH:
```bash
sudo systemctl restart ssh
```

### 3. Регулярные обновления:

```bash
# Раз в неделю
sudo apt update && sudo apt upgrade -y
```

---

## 🐛 Проблемы и решения

### Бот не запускается

```bash
# Проверь логи
sudo journalctl -u telegram-bot -n 100

# Проверь статус
sudo systemctl status telegram-bot
```

### "Module not found"

```bash
# Переустанови зависимости
cd ~/telegram_search_bot
pip3 install -r requirements_telethon.txt --force-reinstall
sudo systemctl restart telegram-bot
```

### Бот падает после перезагрузки сервера

```bash
# Проверь автозапуск
sudo systemctl is-enabled telegram-bot

# Если disabled, включи
sudo systemctl enable telegram-bot
```

---

## 💡 Полезные команды

### Мониторинг ресурсов:

```bash
# Использование CPU/RAM
htop

# Место на диске
df -h

# Процессы Python
ps aux | grep python
```

### Бэкап session файла:

```bash
# Скачать на свой ПК
scp botuser@123.456.789.123:/home/botuser/telegram_search_bot/bot_session.session C:\Users\user\backup\
```

---

## 📈 Мониторинг работы

### Создай простой скрипт мониторинга:

```bash
nano ~/check_bot.sh
```

Вставь:

```bash
#!/bin/bash
if ! systemctl is-active --quiet telegram-bot; then
    echo "Bot is down! Restarting..."
    sudo systemctl restart telegram-bot
fi
```

Сделай исполняемым:
```bash
chmod +x ~/check_bot.sh
```

Добавь в cron (проверка каждые 5 минут):
```bash
crontab -e
```

Добавь строку:
```
*/5 * * * * /home/botuser/check_bot.sh
```

---

## ✅ Итог

Теперь бот:
- ✅ Работает 24/7
- ✅ Автоматически запускается после перезагрузки
- ✅ Логи сохраняются
- ✅ Можно управлять удаленно

**Готово!** Бот на VPS настроен! 🎉

---

## 📞 Рекомендуемые провайдеры VPS

### Международные:
- **DigitalOcean** - https://digitalocean.com (от $4/мес)
- **Vultr** - https://vultr.com (от $2.5/мес)
- **Hetzner** - https://hetzner.com (от €3.79/мес)

### Российские:
- **Timeweb** - https://timeweb.com (от 150₽/мес)
- **Reg.ru** - https://reg.ru (от 199₽/мес)
- **Beget** - https://beget.com (от 200₽/мес)

Выбирай по цене и локации! 🌍
