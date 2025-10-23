"""
Script simples para verificar/criar superusuário
Salve este código e execute no Railway
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    if User.objects.filter(username='admin').exists():
        print("✅ Usuário 'admin' já existe!")
        user = User.objects.get(username='admin')
        print(f"Email: {user.email}")
        print(f"É superusuário: {user.is_superuser}")
    else:
        user = User.objects.create_superuser(
            username='admin',
            email='admin@olharliterario.com',
            password='Admin@2025!Olhar'
        )
        print("✅ SUPERUSUÁRIO CRIADO!")
        print("Username: admin")
        print("Senha: Admin@2025!Olhar")
except Exception as e:
    print(f"Erro: {e}")
