#!/usr/bin/env python
"""
Script para criar superusuário no Railway
Execute com: railway run python olhar_literario_django/criar_superuser.py
"""

import os
import sys
import django

# Adicionar o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Credenciais do superusuário
username = 'admin'
email = 'admin@olharliterario.com'
password = 'Admin@2025!Olhar'

try:
    # Verificar se já existe
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        print("⚠️  Usuário já existe!")
        print(f"👤 Username: {user.username}")
        print(f"📧 Email: {user.email}")
        print(f"🔐 É superusuário: {user.is_superuser}")
        
        # Atualizar para garantir que é superusuário
        if not user.is_superuser:
            user.is_superuser = True
            user.is_staff = True
            user.set_password(password)
            user.save()
            print("✅ Atualizado para superusuário!")
    else:
        # Criar novo superusuário
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("=" * 60)
        print("🎉 SUPERUSUÁRIO CRIADO COM SUCESSO!")
        print("=" * 60)
        print(f"👤 Username: {username}")
        print(f"📧 Email: {email}")
        print(f"🔑 Senha: {password}")
        print("=" * 60)
        print("🌐 Acesse: https://olharliterario-production.up.railway.app/admin")
        print("=" * 60)
        
except Exception as e:
    print(f"❌ Erro ao criar superusuário: {e}")
    sys.exit(1)
