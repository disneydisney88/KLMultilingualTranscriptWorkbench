@echo off
setlocal
set "ROOT=%~dp0"
set "PYTHON_BIN="
where py >nul 2>nul && set "PYTHON_BIN=py -3.12"
if "%PYTHON_BIN%"=="" set "PYTHON_BIN=python"
if not exist "%ROOT%.venv\Scripts\python.exe" (
  %PYTHON_BIN% -m venv "%ROOT%.venv"
)
"%ROOT%.venv\Scripts\python.exe" -m pip install --upgrade pip
"%ROOT%.venv\Scripts\python.exe" -m pip install -r "%ROOT%requirements.txt"
"%ROOT%.venv\Scripts\python.exe" -c "import config; config.ensure_workspace(); print('Workspace ready')"
echo Install complete.
pause
