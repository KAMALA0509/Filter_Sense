@echo off
setlocal
cd /d "%~dp0"
echo FilterSense v2 - starting from %cd%
echo.
if exist .venv\Scripts\python.exe goto ready
echo [1/3] Creating Python environment. Please wait...
py -3.12 --version >nul 2>&1
if not errorlevel 1 (
 py -3.12 -m venv .venv
 goto checkenv
)
py -3.11 --version >nul 2>&1
if not errorlevel 1 (
 py -3.11 -m venv .venv
 goto checkenv
)
python -c "import sys; assert sys.version_info[:2] in [(3,11),(3,12)]" >nul 2>&1
if errorlevel 1 goto nopython
python -m venv .venv
:checkenv
if not exist .venv\Scripts\python.exe goto fail
:ready
echo [2/3] Checking required packages. Internet is needed on first run.
.venv\Scripts\python.exe -m pip install -r software\requirements.txt
if errorlevel 1 goto fail
echo [3/3] Starting dashboard at http://localhost:8501
echo Keep this window open. Press Ctrl+C to stop.
.venv\Scripts\python.exe -m streamlit run software\app.py --browser.gatherUsageStats false
if errorlevel 1 goto fail
pause
exit /b
:nopython
echo Python 3.11 or 3.12 was not found. Install from python.org with the Python launcher.
pause
exit /b 1
:fail
echo Setup or launch failed. Please share the error printed above.
pause
exit /b 1
