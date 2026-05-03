@echo off
title Homs Store - Backend Server
echo ============================================
echo         HOMS STORE - Backend Server
echo ============================================
echo.
echo Starting Flask backend on http://localhost:5000
echo.
echo Keep this window open while using the website!
echo.
cd /d "%~dp0backend"
python app.py
pause
