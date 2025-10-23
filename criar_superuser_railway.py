"""
Script para criar superusuário no Railway via código Python
Execute com: railway run python criar_superuser_railway.py
"""

import os
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')

# Mudar para o diretório correto
import sys
sys.path.insert(0, '/app/olhar_literario_django')

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Dados do superusuário
username = 'admin'
email = 'admin@olharliterario.com'
password = 'Admin@2025!Olhar'  # Senha forte

# Verificar se já existe
if User.objects.filter(username=username).exists():
    print(f"❌ Usuário '{username}' já existe!")
    user = User.objects.get(username=username)
    print(f"✅ Email: {user.email}")
    print(f"✅ É superusuário: {user.is_superuser}")
else:
    # Criar o superusuário
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("=" * 50)
    print("✅ SUPERUSUÁRIO CRIADO COM SUCESSO!")
    print("=" * 50)
    print(f"👤 Username: {username}")
    print(f"📧 Email: {email}")
    print(f"🔑 Senha: {password}")
    print("=" * 50)
    print(f"🌐 Acesse: https://olharliterario-production.up.railway.app/admin")
    print("=" * 50)
