@echo off
chcp 65001 >nul
REM Автоматический запуск бота в фоновом режиме

cd /d "%~dp0"

REM Проверка, не запущен ли уже бот
tasklist /FI "WINDOWTITLE eq Telegram Search Bot" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Бот уже запущен
    exit /b
)

REM Запуск бота в скрытом окне с логированием
start "Telegram Search Bot" /MIN pythonw.exe bot_hybrid.py

REM Ожидание запуска
timeout /t 3 /nobreak >nul

echo Бот запущен в фоновом режиме
