@echo off
REM CV Revamping App - Development Startup Batch File
REM This can be used with Windows Task Scheduler for automatic startup

echo 🚀 Starting CV Revamping Application...

REM Change to the project directory
cd /d "%~dp0"

REM Start the PowerShell script
powershell -ExecutionPolicy Bypass -File "start-dev.ps1"

pause 