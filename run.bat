@echo off
REM Quick start script for the Plastic Material Metrics Extractor
REM Run this to launch the GUI application

cls
echo.
echo ========================================
echo Plastic Material Metrics Extractor
echo ========================================
echo.
echo Launching application...
echo.

cd /d "%~dp0"
python main.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start the application
    echo.
    echo Please ensure:
    echo 1. Python 3.8 or higher is installed
    echo 2. Dependencies are installed (run: install.bat)
    echo.
    pause
)
