@echo off

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Run the Python script
python main.py

REM Keep the window open after execution
pause