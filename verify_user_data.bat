@echo off
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 exit /b %errorlevel%

echo Starting Server...
start /b python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 > server.log 2>&1
echo Waiting for server to start...
timeout /t 5 /nobreak > nul

echo Running Tests...
python test_user_data.py

echo Killing Server (Find process by port 8000)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /f /pid %%a
