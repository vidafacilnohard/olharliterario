@echo off
echo Criando superusuário no Railway...
railway run python olhar_literario_django/manage.py createsuperuser --noinput --username admin --email admin@olharliterario.com
echo.
echo ============================================
echo Agora configure a senha:
echo railway run python olhar_literario_django/manage.py changepassword admin
echo ============================================
