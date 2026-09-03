@echo off
REM Double-click this file to stop the Plastic Material Metrics Extractor.
cd /d "%~dp0"
echo Stopping the app...
docker compose down
echo Done.
pause
