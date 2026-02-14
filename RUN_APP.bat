@echo off
echo ============================================================
echo THOUGHTFUL AI CUSTOMER SUPPORT AGENT
echo ============================================================
echo.
echo Checking dependencies...
echo.

REM Install requirements
py -m pip install -r requirements.txt --quiet

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed
echo.
echo Starting Streamlit application...
echo The app will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Run Streamlit app
py -m streamlit run app.py

pause
