@echo off
chcp 65001 >nul
title PDF번역기

echo =============================================
echo  PDF번역기 시작 중...
echo =============================================
echo.

cd /d "%~dp0"

set PYTHON_CMD=
for %%P in (
    "%USERPROFILE%\anaconda3\python.exe"
    "%USERPROFILE%\miniconda3\python.exe"
    "%LOCALAPPDATA%\anaconda3\python.exe"
    "%LOCALAPPDATA%\miniconda3\python.exe"
    "C:\ProgramData\anaconda3\python.exe"
    "C:\anaconda3\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
    "C:\Python39\python.exe"
    "C:\Python38\python.exe"
) do (
    if exist %%P (
        set PYTHON_CMD=%%P
        goto :found_python
    )
)

python --version >nul 2>&1
if %errorlevel% equ 0 (set PYTHON_CMD=python && goto :found_python)

echo [오류] Python을 찾을 수 없습니다.
pause
exit /b 1

:found_python
echo [*] Python: %PYTHON_CMD%

if not exist ".env" (
    echo [오류] .env 파일이 없습니다.
    echo openrouter_API_KEY=sk-or-v1-... 를 입력하세요.
    pause
    exit /b 1
)

netstat -ano | findstr ":5000" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (start "" "http://127.0.0.1:5000" && exit /b 0)

echo [*] 서버를 시작합니다...
start /b "" %PYTHON_CMD% launcher.py
timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:5000"

echo.
echo 이 창을 닫으면 서버가 종료됩니다.
echo =============================================
