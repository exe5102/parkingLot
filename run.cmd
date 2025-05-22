@echo off
rem 切換工作目錄至批次檔
cd /d "%~dp0"

rem 設定環境變數
set FLASK_ENV=development
set FLASK_APP=app.py
set FLASK_DEBUG=1

rem 啟動應用程式
echo Starting Flask application...
flask run --reload --debugger --host 0.0.0.0 --port 5000

exit /b 0