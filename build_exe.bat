@echo off
setlocal
cd /d "%~dp0"

set PYTHON=C:\Users\WeZh735\AppData\Local\Programs\Python\Python312\python.exe

if not exist "%PYTHON%" (
    echo Python 3.12 was not found at:
    echo %PYTHON%
    pause
    exit /b 1
)

echo Installing/updating PyInstaller...
"%PYTHON%" -m pip install pyinstaller
if errorlevel 1 exit /b 1

echo Building Chimian.exe...
"%PYTHON%" -m PyInstaller --noconfirm --clean chimian.spec
if errorlevel 1 (
    echo Build failed.
    pause
    exit /b 1
)

echo.
echo Build complete:
echo %~dp0dist\Chimian.exe
pause