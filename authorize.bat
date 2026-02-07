@echo off
chcp 65001 >nul
echo ================================================
echo   Авторизация Telegram Bot
echo ================================================
echo.
echo Бот запросит код подтверждения из Telegram.
echo Проверь свой Telegram - там должен прийти код.
echo.
echo Запускаю...
echo.
python bot_telethon.py
pause
