#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para criar superusuário admin automaticamente
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Dados do superusuário padrão
USERNAME = 'admin'
EMAIL = 'admin@olharliterario.com'
PASSWORD = 'admin123'

try:
    if not User.objects.filter(username=USERNAME).exists():
        User.objects.create_superuser(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD
        )
        print(f"✓ Superusuário '{USERNAME}' criado com sucesso!")
        print(f"  Username: {USERNAME}")
        print(f"  Email: {EMAIL}")
        print(f"  Senha: {PASSWORD}")
        print()
        print("Acesse: http://localhost:8000/admin")
    else:
        print(f"✓ Superusuário '{USERNAME}' já existe!")
        print("Acesse: http://localhost:8000/admin")
except Exception as e:
    print(f"✗ Erro ao criar superusuário: {e}")
