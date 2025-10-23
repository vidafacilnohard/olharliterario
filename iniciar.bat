@echo off
title Olhar Literario - Servidor Django
color 0A

REM Limpar variável de ambiente que pode causar conflito
set DJANGO_SETTINGS_MODULE=

echo.
echo     ╔════════════════════════════════════════════════════════╗
echo     ║                                                        ║
echo     ║           OLHAR LITERARIO - SERVIDOR DJANGO           ║
echo     ║                                                        ║
echo     ╚════════════════════════════════════════════════════════╝
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale o Python 3.8 ou superior:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [1/4] Verificando Python... OK
echo.

REM Verificar se Django está instalado
python -c "import django" 2>nul
if errorlevel 1 (
    echo [2/4] Django nao encontrado. Instalando dependencias...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERRO] Falha ao instalar dependencias!
        echo.
        pause
        exit /b 1
    )
) else (
    echo [2/4] Django encontrado... OK
)
echo.

REM Entrar na pasta do Django
cd olhar_literario_django

REM Criar migrações e aplicar
echo [3/4] Configurando banco de dados...
python manage.py makemigrations books >nul 2>&1
python manage.py migrate >nul 2>&1
if errorlevel 1 (
    echo.
    echo [AVISO] Erro ao criar banco de dados. Tentando novamente...
    python manage.py migrate --run-syncdb
)
echo      Banco de dados configurado com sucesso!
echo.

echo [4/4] Iniciando servidor...
echo.
echo     ╔════════════════════════════════════════════════════════╗
echo     ║                  SERVIDOR ATIVO!                       ║
echo     ╠════════════════════════════════════════════════════════╣
echo     ║                                                        ║
echo     ║  Frontend:  http://localhost:8000                     ║
echo     ║  Admin:     http://localhost:8000/admin               ║
echo     ║                                                        ║
echo     ║  Pressione Ctrl+C para parar o servidor               ║
echo     ║                                                        ║
echo     ╚════════════════════════════════════════════════════════╝
echo.

REM Iniciar o servidor Django
python manage.py runserver 0.0.0.0:8000

REM Se o servidor parar, voltar para a pasta original
cd ..
echo.
echo Servidor encerrado.
pause
