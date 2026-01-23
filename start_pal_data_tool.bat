@echo off
title Palworld Data Tool Server
echo Changing directory to the project folder...
cd /d "D:\Github\palworld-data-tool"

:start
echo Starting the Palworld Data Tool server...
npm start

echo Server stopped unexpectedly. Restarting in 5 seconds...
timeout /t 5 /nobreak
goto start