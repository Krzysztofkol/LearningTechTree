@echo off
echo Starting Deep Learning Path Application...

:: Start the backend (Flask server)
start cmd /k "echo Starting Flask server... && python app.py"

:: Wait for a moment to ensure the server has started
timeout /t 1

:: Open the frontend in the default web browser
start http://localhost:9696

echo Application started. Check the opened command prompt for Flask server logs.
echo Press any key to exit this window...
pause >nul