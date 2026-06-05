@echo off
:: start_frontend.bat — One-click frontend launcher for QUANTUM AGENT

echo.
echo  ╔══════════════════════════════════════╗
echo  ║      QUANTUM AGENT — Frontend        ║
echo  ║      Starting React on port 5173     ║
echo  ╚══════════════════════════════════════╝
echo.

cd /d "%~dp0frontend"
npm run dev

pause
