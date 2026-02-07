@echo off
chcp 65001 >nul
echo ================================================
echo   Проверка статуса Telegram Search Bot
echo ================================================
echo.

REM Проверка процессов Python
set BOT_RUNNING=0

for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| find "PID:"') do (
    wmic process where "ProcessId=%%a and CommandLine like '%%bot_hybrid.py%%'" get ProcessId 2>nul | find "%%a" >nul
    if not errorlevel 1 (
        set BOT_RUNNING=1
        echo [OK] Бот РАБОТАЕТ (python.exe, PID: %%a^)
    )
)

for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq pythonw.exe" /FO LIST ^| find "PID:"') do (
    wmic process where "ProcessId=%%a and CommandLine like '%%bot_hybrid.py%%'" get ProcessId 2>nul | find "%%a" >nul
    if not errorlevel 1 (
        set BOT_RUNNING=1
        echo [OK] Бот РАБОТАЕТ (pythonw.exe, PID: %%a^)
    )
)

if %BOT_RUNNING%==0 (
    echo [ОШИБКА] Бот НЕ РАБОТАЕТ
    echo.
    echo Для запуска выполните: start_bot_auto.bat
)

echo.
echo Проверьте также Telegram: @chinesetop_bot
echo.
pause
