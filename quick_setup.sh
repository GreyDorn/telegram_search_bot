#!/bin/bash
# Автоматическая настройка бота на сервере

cd ~/telegram_search_bot

# Создание .env файла
cat > .env << 'ENVEOF'
API_ID=33256748
API_HASH=2b6b122193f0fcee7fd0e4b95612d004
BOT_TOKEN=8343593792:AAFCTEitzIYDCBXrW3SIm6zi0sX50o0Mvy0
PHONE=+79516069961
CHANNELS=@kitaiskiy_with_em,@sofiya_chinese,@eastwestchinese,@chinesequizzes,@chinese_lingvistika_slovar,@veresk_chinesedragon,@bookchinese,@chinese_with_native_speakers,@chinaprofessionals,@zhou_xin,@chinesechime,@living_chinese,@studychinese_ru,@chinarydom,@spirit_code,@chinese_everyday,@kitayskya,@dobrchineseru,@MilenaRadichenko,@ya_v_kitae,@zhongwenshuji,@chinesezen,@chinese_521,@chineseforfuture,@sinotati,@zhongwendianying,@hsk4pro,@chinese_language_kris,@kitaeved,@chineseclown
SEARCH_LIMIT=1000
ENVEOF

echo "✅ .env файл создан!"
echo ""
echo "📱 Сейчас запустится бот для авторизации."
echo "Введи код из Telegram, затем нажми Ctrl+C"
echo ""

# Запуск бота для авторизации
python3 bot_telethon.py
