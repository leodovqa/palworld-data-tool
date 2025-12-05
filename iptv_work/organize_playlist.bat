@echo off
echo IPTV Playlist Organizer
echo ======================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Python found. Running organizer...
echo.

REM Run the organizer script
python organize_iptv.py

echo.
echo Done! Check the organized playlist file.
pause 