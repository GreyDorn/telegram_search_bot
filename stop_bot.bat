@echo off
chcp 65001 >nul
echo ================================================
echo   Остановка Telegram Search Bot
echo ================================================
echo.

REM Поиск и остановка всех процессов Python с bot_hybrid.py
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| find "PID:"') do (
    wmic process where "ProcessId=%%a and CommandLine like '%%bot_hybrid.py%%'" delete 2>nul
)

for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq pythonw.exe" /FO LIST ^| find "PID:"') do (
    wmic process where "ProcessId=%%a and CommandLine like '%%bot_hybrid.py%%'" delete 2>nul
)

echo.
echo Бот остановлен
echo.
pause
