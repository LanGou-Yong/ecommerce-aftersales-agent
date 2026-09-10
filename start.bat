@echo off
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" start_demo.py
  goto :eof
)
if exist "venv\Scripts\python.exe" (
  "venv\Scripts\python.exe" start_demo.py
  goto :eof
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python start_demo.py
  goto :eof
)

echo Python not found.
echo Create a venv, then: pip install -r requirements.txt
pause
exit /b 1
