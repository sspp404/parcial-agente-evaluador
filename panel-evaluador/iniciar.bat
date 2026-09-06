@echo off
REM Arranca el backend del panel y abre el navegador solo.
REM Doble click en este archivo alcanza. Ctrl+C en la ventana para cortar.
cd /d "%~dp0"
python server\app.py
pause
