@echo off
REM ==========================================
REM Launch Katalon Dashboard (Streamlit)
REM ==========================================

REM Optional: change directory to project root if needed
cd /d C:\git\katalon-dashboard

REM Optional: activate virtual environment (if you have one)
REM call .venv\Scripts\activate

REM Run Streamlit
streamlit run src\dashboard\app.py

REM Keep the window open after it exits
pause
