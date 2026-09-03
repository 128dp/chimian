@echo off
REM Double-click this file to start the Plastic Material Metrics Extractor.
REM Requires Docker Desktop to be installed and running.
cd /d "%~dp0"

echo Checking Docker...
docker info >nul 2>&1
if errorlevel 1 (
    echo.
    echo Docker Desktop doesn't seem to be running.
    echo Please open Docker Desktop, wait for it to finish starting, then run this file again.
    echo.
    pause
    exit /b 1
)

echo Starting the app - this may take a minute the first time...
docker compose up --build -d
if errorlevel 1 (
    echo.
    echo Something went wrong starting the app. See the messages above.
    pause
    exit /b 1
)

echo Opening the app in your browser...
timeout /t 3 /nobreak >nul
start "" "http://localhost:8501"

echo.
echo The app is running. Keep Docker Desktop open in the background.
echo To stop it later, double-click stop-app.bat
pause
