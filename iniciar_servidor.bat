@echo off
title Servidor Olhar Literario
color 0A
echo.
echo ========================================
echo  Iniciando Servidor Olhar Literario
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale o Python em: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado!
echo.
echo Iniciando servidor...
echo.

REM Inicia o servidor Python
python server.py

pause
