@echo off
title Florista Bot
echo ====================================
echo Zapusk Telegram-bota Florista...
echo ====================================
cd /d "%~dp0"
call venv\Scripts\activate.bat
python bot.py
pause