@echo off
:: start_backend.bat — One-click backend launcher for QUANTUM AGENT
:: Uses Python 3.12 which was installed to fix the broken Python 3.14 issue.

echo.
echo  ╔══════════════════════════════════════╗
echo  ║      QUANTUM AGENT — Backend         ║
echo  ║      Starting FastAPI on port 8000   ║
echo  ╚══════════════════════════════════════╝
echo.

cd /d "%~dp0backend"

:: Use the working Python 3.12 installation
"C:\Users\DELL\AppData\Local\Programs\Python\Python312\python.exe" main.py

pause
