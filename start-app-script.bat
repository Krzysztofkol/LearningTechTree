@echo off
echo Starting Deep Learning Path Application...

:: Start the backend (Flask server)
start cmd /k "echo Starting Flask server... && python backend.py"

:: Wait for a moment to ensure the server has started
timeout /t .1

:: Open the frontend in the default web browser
start http://localhost:9696