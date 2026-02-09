#!/bin/bash
# Автоматическая настройка VPS для Telegram бота
# Выполняй этот скрипт на сервере

set -e  # Остановка при ошибке

echo "🚀 Начинаю настройку VPS для Telegram бота..."
echo ""

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Получение данных
read -p "Введи свой GitHub username: " GITHUB_USER
read -p "Введи API_ID (из my.telegram.org): " API_ID
read -p "Введи API_HASH (из my.telegram.org): " API_HASH
read -p "Введи BOT_TOKEN (от @BotFather): " BOT_TOKEN
read -p "Введи PHONE (формат +79991234567): " PHONE
read -p "Введи CHANNELS (через запятую, например @channel1,@channel2): " CHANNELS

echo ""
echo -e "${YELLOW}⏳ Шаг 1/7: Обновление системы...${NC}"
apt update && apt upgrade -y

echo ""
echo -e "${YELLOW}⏳ Шаг 2/7: Установка Python, pip и Git...${NC}"
apt install python3 python3-pip git nano -y

echo ""
echo -e "${YELLOW}⏳ Шаг 3/7: Загрузка проекта с GitHub...${NC}"
cd ~
if [ -d "telegram_search_bot" ]; then
    echo "Папка уже существует, удаляю..."
    rm -rf telegram_search_bot
fi
git clone https://github.com/$GITHUB_USER/telegram_search_bot.git
cd telegram_search_bot

echo ""
echo -e "${YELLOW}⏳ Шаг 4/7: Установка зависимостей...${NC}"
pip3 install -r requirements_telethon.txt

echo ""
echo -e "${YELLOW}⏳ Шаг 5/7: Создание .env файла...${NC}"
cat > .env << EOF
API_ID=$API_ID
API_HASH=$API_HASH
BOT_TOKEN=$BOT_TOKEN
PHONE=$PHONE
CHANNELS=$CHANNELS
SEARCH_LIMIT=1000
EOF

echo ""
echo -e "${GREEN}✅ .env файл создан!${NC}"

echo ""
echo -e "${YELLOW}⏳ Шаг 6/7: Авторизация бота (введи код из Telegram)...${NC}"
echo "Сейчас запустится бот. Введи код подтверждения из Telegram."
echo "После успешной авторизации нажми Ctrl+C"
echo ""
python3 bot_telethon.py

echo ""
echo -e "${YELLOW}⏳ Шаг 7/7: Настройка автозапуска (systemd)...${NC}"

cat > /etc/systemd/system/telegram-bot.service << 'EOF'
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
EOF

systemctl daemon-reload
systemctl start telegram-bot
systemctl enable telegram-bot

echo ""
echo -e "${GREEN}🎉 Готово! Бот настроен и запущен!${NC}"
echo ""
echo "📊 Проверка статуса:"
systemctl status telegram-bot --no-pager
echo ""
echo "💡 Полезные команды:"
echo "  • Статус бота: systemctl status telegram-bot"
echo "  • Логи: journalctl -u telegram-bot -f"
echo "  • Перезапуск: systemctl restart telegram-bot"
echo "  • Остановка: systemctl stop telegram-bot"
echo ""
echo -e "${GREEN}✅ Бот работает 24/7!${NC}"
