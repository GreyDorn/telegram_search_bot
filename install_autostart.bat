@echo off
chcp 65001 >nul
echo ================================================
echo   Установка автозапуска Telegram Search Bot
echo ================================================
echo.
echo Этот скрипт добавит бота в автозагрузку Windows.
echo Бот будет запускаться автоматически при включении компьютера.
echo.
pause

REM Получаем путь к текущей папке
set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%start_bot_auto.bat

echo.
echo Создание задачи в Планировщике заданий Windows...
echo.

REM Удаляем старую задачу, если существует
schtasks /Delete /TN "TelegramSearchBot" /F 2>nul

REM Создаем новую задачу
schtasks /Create /SC ONLOGON /TN "TelegramSearchBot" /TR "\"%SCRIPT_PATH%\"" /RL HIGHEST /F

if %ERRORLEVEL%==0 (
    echo.
    echo [OK] Автозапуск успешно установлен!
    echo.
    echo Бот будет запускаться автоматически при входе в систему.
    echo.
    echo Для проверки статуса: check_bot_status.bat
    echo Для остановки бота: stop_bot.bat
    echo Для удаления автозапуска: uninstall_autostart.bat
) else (
    echo.
    echo [ОШИБКА] Не удалось создать задачу автозапуска.
    echo Попробуйте запустить этот файл от имени администратора.
)

echo.
pause
