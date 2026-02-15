#!/bin/bash
# Автоматическая синхронизация с GitHub и перезапуск бота

cd /root/telegram_search_bot

# Проверка обновлений
git fetch origin main

# Сравнение локальной и удаленной версий
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "$(date): Обнаружены обновления, применяю..."
    
    # Загрузка изменений
    git pull origin main
    
    # Перезапуск бота
    systemctl restart telegram-bot
    
    echo "$(date): Бот обновлен и перезапущен!"
else
    echo "$(date): Обновлений нет"
fi
