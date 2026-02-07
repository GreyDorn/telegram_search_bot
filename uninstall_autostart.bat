@echo off
chcp 65001 >nul
echo ================================================
echo   Удаление автозапуска Telegram Search Bot
echo ================================================
echo.

REM Удаляем задачу из Планировщика заданий
schtasks /Delete /TN "TelegramSearchBot" /F

if %ERRORLEVEL%==0 (
    echo.
    echo [OK] Автозапуск успешно удален!
    echo.
    echo Бот больше не будет запускаться автоматически.
    echo Вы можете запускать его вручную через start_bot_auto.bat
) else (
    echo.
    echo [ОШИБКА] Задача не найдена или не удалось удалить.
)

echo.
pause
