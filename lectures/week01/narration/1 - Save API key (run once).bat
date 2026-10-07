@echo off
echo This saves your ElevenLabs API key for your Windows user account on this computer.
echo It is stored as a user environment variable, not in the Dropbox folder.
echo.
set /p KEY=Paste your ElevenLabs API key and press Enter: 
if "%KEY%"=="" (
  echo No key entered. Nothing was saved.
  pause
  exit /b 1
)
setx ELEVENLABS_API_KEY "%KEY%" >nul
echo.
echo Saved. You only need to do this once on this computer.
pause
