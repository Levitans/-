@echo off

:: �ô��ļ�����ʱ·���в�������
set curpath=%~dp0
cd /d %curpath%

python --version >nul 2>nul
if %ERRORLEVEL% == 0 (
    goto start
) else (
    echo ϵͳ��δ�ҵ�Python
    echo �밲װPython�������г���
    echo ע��Python��Ҫ��װ3.9���ϰ汾
    pause
    exit 0
)

:start
if exist ".\venv" (
    .\venv\Scripts\python.exe faithlearning.py
) else (
    python -m venv .\venv
)