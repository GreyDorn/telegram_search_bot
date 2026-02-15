"""
Конфигурация бота с Telethon (поиск по истории)
ВАЖНО: Этот файл содержит секретные данные!
"""

import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# API credentials (получить на https://my.telegram.org)
API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')

# Токен бота от @BotFather
BOT_TOKEN = os.getenv('BOT_TOKEN', '')

# Номер телефона для авторизации (формат: +79991234567)
PHONE = os.getenv('PHONE', '')

# Список каналов для поиска
CHANNELS_RAW = os.getenv('CHANNELS', '')
CHANNELS = [ch.strip() for ch in CHANNELS_RAW.split(',') if ch.strip()]

# Глубина поиска (количество последних сообщений в каждом канале)
SEARCH_LIMIT = int(os.getenv('SEARCH_LIMIT', '1000'))

# Количество символов для превью результата
PREVIEW_LENGTH = 200

# Название файла сессии
SESSION_NAME = 'bot_session'
