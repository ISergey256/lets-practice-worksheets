@echo off
rem Double-click: starts the worksheet website and opens it in the browser.
cd /d "%~dp0"
python scripts\server.py
pause
