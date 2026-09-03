@echo off
REM Installation script for Plastic Material Metrics Extractor
REM This script installs Python dependencies

echo.
echo ========================================
echo Plastic Material Metrics Extractor
echo Installation Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org
    echo.
    pause
    exit /b 1
)

echo Detected Python:
python --version
echo.

REM Install requirements
echo Installing required packages...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error: Failed to install requirements
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo To start the application, run:
echo   python main.py
echo.
echo To see a demo of the extraction process, run:
echo   python demo.py
echo.
pause
