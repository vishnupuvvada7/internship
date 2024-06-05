@echo off
setlocal enabledelayedexpansion

REM Get the directory of the batch file
for %%i in ("%~dp0.") do set "batch_dir=%%~fi"

REM Run as administrator
powershell -Command "Start-Process 'python' -ArgumentList '\"%batch_dir%\services.py\"' -Verb RunAs"
