chcp 65001
@echo off

:: 用此文件运行时路径中不能中文
set curpath=%~dp0
cd /d %curpath%

python --version >nul 2>nul
if %ERRORLEVEL% == 0 (
    goto start
) else (
    echo 系统中未找到Python
    echo 请安装Python后再运行程序
    echo 可以访问 https://cdn.npmmirror.com/binaries/python/3.9.0/python-3.9.0.exe 下载Python3.9.0安装包
    echo 注意Python需要安装3.9以上版本
    pause
    exit 0
)

:start
if exist ".\venv" (
    .\venv\Scripts\python.exe .\faithlearning.py
) else (
    echo 系统中未找到虚拟环境
    echo 正在为你创建虚拟环境
    python -m venv .\venv
    echo 虚拟环境创建成功
    echo 请重启程序
)
pause
exit 0