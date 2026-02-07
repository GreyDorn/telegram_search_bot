# 🐳 Развертывание через Docker

Docker упрощает развертывание бота на любом сервере с Docker.

## ✅ Преимущества Docker:

- 📦 Изолированное окружение
- 🔄 Легкое обновление
- 🚀 Быстрое развертывание
- 💻 Работает везде (VPS, локально, облако)

---

## 🚀 Быстрый старт

### Шаг 1: Создание Dockerfile

Создай файл `Dockerfile` в проекте:

```dockerfile
# Базовый образ Python
FROM python:3.11-slim

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY requirements_telethon.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements_telethon.txt

# Копирование кода бота
COPY bot_telethon.py .
COPY config_telethon.py .

# Копирование session файла (если есть)
COPY bot_session.session* ./

# Команда запуска
CMD ["python", "bot_telethon.py"]
```

### Шаг 2: Создание .dockerignore

```
__pycache__/
*.pyc
.env
.git/
.gitignore
*.md
venv/
```

### Шаг 3: Создание docker-compose.yml

```yaml
version: '3.8'

services:
  telegram-bot:
    build: .
    container_name: telegram_search_bot
    restart: unless-stopped
    environment:
      - API_ID=${API_ID}
      - API_HASH=${API_HASH}
      - BOT_TOKEN=${BOT_TOKEN}
      - PHONE=${PHONE}
      - CHANNELS=${CHANNELS}
      - SEARCH_LIMIT=${SEARCH_LIMIT}
    volumes:
      # Сохранение session файла
      - ./bot_session.session:/app/bot_session.session
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 🖥️ Локальный запуск

### Установка Docker:

**Windows:**
1. Скачай Docker Desktop: https://docker.com/products/docker-desktop
2. Установи и запусти

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Запуск:

```bash
cd C:\Users\user\projects\telegram_search_bot

# Создай .env файл (если еще нет)
# Заполни его данными

# Первая авторизация (без Docker)
python bot_telethon.py
# Введи код → Создастся bot_session.session → Ctrl+C

# Запуск через Docker
docker-compose up -d
```

### Управление:

```bash
# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Статус
docker-compose ps
```

---

## 🌐 Развертывание на VPS

### Шаг 1: Подключение к VPS

```bash
ssh root@your-server-ip
```

### Шаг 2: Установка Docker

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
apt install docker-compose -y
```

### Шаг 3: Загрузка проекта

```bash
# Создание директории
mkdir -p /opt/telegram-bot
cd /opt/telegram-bot

# Через Git
git clone https://github.com/ТвойUsername/telegram_search_bot.git .

# ИЛИ копирование с ПК
# scp -r C:\Users\user\projects\telegram_search_bot root@your-server-ip:/opt/telegram-bot/
```

### Шаг 4: Создание .env

```bash
nano .env
```

Вставь:
```env
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
PHONE=+79991234567
CHANNELS=@channel1,@channel2,@channel3
SEARCH_LIMIT=1000
```

### Шаг 5: Авторизация

```bash
# Временно запусти без Docker для авторизации
apt install python3-pip -y
pip3 install -r requirements_telethon.txt
python3 bot_telethon.py

# Введи код авторизации
# Создастся bot_session.session
# Ctrl+C для остановки
```

### Шаг 6: Запуск через Docker

```bash
# Сборка и запуск
docker-compose up -d

# Проверка логов
docker-compose logs -f
```

---

## 🔄 Автозапуск при перезагрузке

Docker Compose с `restart: unless-stopped` автоматически запустит бота после перезагрузки сервера.

Проверка:
```bash
# Перезагрузка сервера
sudo reboot

# После перезагрузки
docker-compose ps  # Должен быть running
```

---

## 📊 Мониторинг

### Просмотр логов:

```bash
# Все логи
docker-compose logs

# Последние 100 строк
docker-compose logs --tail=100

# В реальном времени
docker-compose logs -f
```

### Использование ресурсов:

```bash
# Статистика контейнера
docker stats telegram_search_bot
```

---

## 🔄 Обновление бота

### Вариант А: Через Git

```bash
cd /opt/telegram-bot
git pull
docker-compose down
docker-compose up -d --build
```

### Вариант Б: Замена файлов

```bash
# На своем ПК
scp bot_telethon.py root@your-server-ip:/opt/telegram-bot/

# На сервере
cd /opt/telegram-bot
docker-compose restart
```

---

## 🐛 Проблемы и решения

### Контейнер не запускается

```bash
# Проверь логи
docker-compose logs

# Проверь .env
cat .env

# Пересобери образ
docker-compose down
docker-compose up -d --build
```

### "Session file not found"

```bash
# Убедись что bot_session.session на месте
ls -la bot_session.session

# Авторизуйся заново
python3 bot_telethon.py
```

### Высокое использование памяти

```bash
# Ограничь память в docker-compose.yml
services:
  telegram-bot:
    # ... другие настройки
    mem_limit: 512m
```

---

## 💡 Продвинутые настройки

### Добавление healthcheck:

В `docker-compose.yml`:

```yaml
services:
  telegram-bot:
    # ... другие настройки
    healthcheck:
      test: ["CMD", "python3", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Ограничение логов:

```yaml
services:
  telegram-bot:
    # ... другие настройки
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"
```

---

## 📦 Альтернатива: Готовый образ

Можешь создать и опубликовать образ на Docker Hub:

```bash
# Сборка
docker build -t yourusername/telegram-search-bot .

# Публикация
docker login
docker push yourusername/telegram-search-bot

# Использование
docker run -d \
  --name telegram-bot \
  --restart unless-stopped \
  -e API_ID=xxx \
  -e API_HASH=xxx \
  -e BOT_TOKEN=xxx \
  -e PHONE=xxx \
  -e CHANNELS=xxx \
  -e SEARCH_LIMIT=1000 \
  -v $(pwd)/bot_session.session:/app/bot_session.session \
  yourusername/telegram-search-bot
```

---

## ✅ Итог

Docker делает развертывание простым и надежным:

- ✅ Один раз настроил - работает везде
- ✅ Легкое обновление
- ✅ Изолированное окружение
- ✅ Автоматический перезапуск

**Готово!** Бот в Docker контейнере! 🐳
