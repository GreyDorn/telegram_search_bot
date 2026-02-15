#!/bin/bash
# Переключение на bot_hybrid.py

echo "🔄 Переключение на bot_hybrid.py..."
echo ""

# Остановка текущего бота
systemctl stop telegram-bot
echo "✅ Текущий бот остановлен"

# Изменение файла службы
sed -i 's/bot_telethon.py/bot_hybrid.py/g' /etc/systemd/system/telegram-bot.service
echo "✅ Служба обновлена на bot_hybrid.py"

# Перезагрузка конфигурации
systemctl daemon-reload
echo "✅ Конфигурация перезагружена"

# Запуск нового бота
systemctl start telegram-bot
echo "✅ Гибридный бот запущен!"

echo ""
echo "🎉 Готово! Теперь бот работает через @username"
echo ""
echo "📊 Статус:"
systemctl status telegram-bot --no-pager
echo ""
echo "💡 Теперь:"
echo "  1. Найди своего бота в Telegram по @username"
echo "  2. Напиши ему /start"
echo "  3. Отправь слово для поиска"
