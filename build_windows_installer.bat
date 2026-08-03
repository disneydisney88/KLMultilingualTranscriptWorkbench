@echo off
setlocal
set "ROOT=%~dp0"
if not exist "%ROOT%.venv\Scripts\python.exe" (
  echo Missing .venv. Run install.bat first.
  pause
  exit /b 1
)
"%ROOT%.venv\Scripts\python.exe" "%ROOT%build_windows_installer.py"
pause
