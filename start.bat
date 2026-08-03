@echo off
setlocal
set "ROOT=%~dp0"
if not exist "%ROOT%.venv\Scripts\python.exe" (
  echo Missing .venv. Run install.bat first.
  pause
  exit /b 1
)
set GRADIO_ANALYTICS_ENABLED=False
"%ROOT%.venv\Scripts\python.exe" "%ROOT%app.py"
