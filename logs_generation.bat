@echo off

:: Get the directory path of the batch script
set "script_dir=%~dp0"

:: Run CMD as administrator
powershell -Command "Start-Process cmd -Verb RunAs"

:: Check if CMD is opened as admin
if %errorlevel% neq 0 (
    echo Failed to open CMD as administrator.
    exit /b
)

:: Wait for CMD to open
timeout /t 2 /nobreak >nul

:: Run the Python script
python "%script_dir%\logs.py"

:: Wait for user input to close the window
pause
