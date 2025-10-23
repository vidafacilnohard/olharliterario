@echo off
REM Limpar variável de ambiente que pode causar conflito
set DJANGO_SETTINGS_MODULE=

echo ======================================
echo Iniciando Olhar Literario com Django
echo ======================================
echo.

cd olhar_literario_django

echo Verificando instalacao do Django...
python -c "import django" 2>nul
if errorlevel 1 (
    echo Django nao encontrado! Instalando dependencias...
    pip install -r ..\requirements.txt
)

echo.
echo Executando migracoes...
python manage.py makemigrations books 2>nul
python manage.py migrate

echo.
echo Criando superusuario (se nao existir)...
python criar_admin.py
echo.

echo.
echo ======================================
echo Servidor Django Iniciado!
echo ======================================
echo.
echo Acesse o site em:
echo   Frontend: http://localhost:8000
echo   Admin:    http://localhost:8000/admin
echo.
echo Para criar um administrador, execute:
echo   python manage.py createsuperuser
echo.
echo Pressione Ctrl+C para parar o servidor
echo.
echo ======================================
echo.

python manage.py runserver 0.0.0.0:8000
