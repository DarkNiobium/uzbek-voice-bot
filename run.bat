@echo off
chcp 65001 > nul
echo ========================================================
echo   Telegram Ovozli Xabarlar Transkripsiyasi (Gemini 3.5)
echo ========================================================

IF NOT EXIST ".env" (
    echo [DIQQAT] .env fayli topilmadi. .env.example dan nusxa olinmoqda...
    copy .env.example .env
    echo Iltimos, .env faylini ochib BOT_TOKEN va GEMINI_API_KEY larni kiriting!
    notepad .env
    pause
    exit /b
)

IF NOT EXIST "venv\Scripts\python.exe" (
    echo [SOZLASH] Virtual muhit yaratilmoqda...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) ELSE (
    call venv\Scripts\activate.bat
)

echo.
echo Bot ishga tushirilmoqda...
python bot.py
pause
