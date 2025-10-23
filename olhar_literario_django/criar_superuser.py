#!/usr/bin/env python
"""
Script para criar superusuário no Railway
Executado automaticamente pelo Procfile durante o deploy
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
password = 'admin123'  # SENHA SIMPLES PARA TESTES

print("=" * 60)
print("🚀 INICIANDO CRIAÇÃO DE SUPERUSUÁRIO")
print("=" * 60)

try:
    # SEMPRE deletar usuários admin existentes para garantir senha correta
    deleted_count = User.objects.filter(username=username).delete()[0]
    if deleted_count > 0:
        print(f"🗑️  Deletados {deleted_count} usuário(s) 'admin' existente(s)")
    
    # Criar novo superusuário com senha garantida
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
    print(f"✅ is_superuser: {user.is_superuser}")
    print(f"✅ is_staff: {user.is_staff}")
    print("=" * 60)
    print("🌐 Acesse: https://olharliterario-production.up.railway.app/admin")
    print("=" * 60)
    
except Exception as e:
    print("=" * 60)
    print(f"❌ ERRO AO CRIAR SUPERUSUÁRIO: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
