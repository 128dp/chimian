@echo off
REM Quick launcher for Streamlit-based GUI
REM Plastic Material Metrics Extractor

cls
echo.
echo ========================================
echo Plastic Material Metrics Extractor
echo Streamlit Version
echo ========================================
echo.
echo Launching application...
echo.

cd /d "%~dp0"
C:/Python314/python.exe -m streamlit run streamlit_app.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start Streamlit
    echo.
    echo Please ensure:
    echo 1. Python 3.8 or higher is installed
    echo 2. Dependencies are installed (run: pip install -r requirements.txt)
    echo.
    pause
)
