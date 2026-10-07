@echo off
cd /d "%~dp0"
python make_voice.py %*
echo.
pause
