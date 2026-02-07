# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements_telethon.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements_telethon.txt

# Копируем файлы бота
COPY bot_telethon.py .
COPY config_telethon.py .

# Копируем session файл если есть
COPY bot_session.session* ./

# Запускаем бота
CMD ["python", "bot_telethon.py"]
