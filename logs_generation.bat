@echo off

:: Get the directory path of the batch script
set "script_dir=%~dp0"

:: Check if the script is running as administrator by attempting to open a protected file
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~dpnx0' -Verb RunAs"
    exit /b
)

:: Run the Python script
python "%script_dir%logs.py"

