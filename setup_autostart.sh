#!/bin/bash
# Настройка автозапуска бота

echo "🔧 Настройка автозапуска бота..."
echo ""

# Создание systemd службы
cat > /etc/systemd/system/telegram-bot.service << 'SERVICEEOF'
[Unit]
Description=Telegram Search Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/telegram_search_bot
ExecStart=/usr/bin/python3 /root/telegram_search_bot/bot_telethon.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEEOF

echo "✅ Служба создана!"

# Перезагрузка systemd
systemctl daemon-reload
echo "✅ Конфигурация обновлена!"

# Запуск службы
systemctl start telegram-bot
echo "✅ Бот запущен!"

# Автозапуск
systemctl enable telegram-bot
echo "✅ Автозапуск настроен!"

echo ""
echo "🎉 Готово! Бот работает 24/7!"
echo ""
echo "📊 Статус:"
systemctl status telegram-bot --no-pager
echo ""
echo "💡 Полезные команды:"
echo "  • Логи: journalctl -u telegram-bot -f"
echo "  • Перезапуск: systemctl restart telegram-bot"
echo "  • Остановка: systemctl stop telegram-bot"
echo "  • Статус: systemctl status telegram-bot"
