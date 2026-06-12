@echo off
setlocal
cd /d "%~dp0"

echo Starting Ugra Mahalakshmy Astrology App...
echo.

py -3.11 --version >nul 2>nul
if %ERRORLEVEL%==0 (
    set "PY=py -3.11"
    goto python_found
)

py -3.10 --version >nul 2>nul
if %ERRORLEVEL%==0 (
    set "PY=py -3.10"
    goto python_found
)

echo Python 3.11 or 3.10 was not found.
echo Please install Python 3.11 from https://www.python.org/downloads/release/python-3119/
echo During setup, tick "Add python.exe to PATH".
echo.
echo Important: Python 3.14 is too new for the Swiss Ephemeris Windows package.
pause
exit /b 1

:python_found
echo Python found.
%PY% --version
echo.

echo Preparing app environment...
%PY% -m venv .venv
if not exist ".venv\Scripts\python.exe" (
    echo Could not create the app environment.
    pause
    exit /b 1
)

echo Installing app requirements...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Installation failed. Please check your internet connection and run this again.
    pause
    exit /b 1
)

echo.
echo App is starting.
echo Open this link in your browser:
echo http://127.0.0.1:8000
echo.
echo Keep this window open while using the app.
echo.
".venv\Scripts\python.exe" -m uvicorn app:app --host 127.0.0.1 --port 8000
pause
