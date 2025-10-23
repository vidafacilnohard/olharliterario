"""
Gerar hash usando o método EXATO do Django
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.olhar_literario_django.settings')

import django
import sys
sys.path.insert(0, 'olhar_literario_django')

try:
    django.setup()
    from django.contrib.auth.hashers import make_password
    
    senha = 'admin123'
    hash_senha = make_password(senha)
    
    print("=" * 70)
    print("🔐 HASH GERADO COM DJANGO OFICIAL")
    print("=" * 70)
    print(f"Senha: {senha}")
    print(f"\nHash completo:")
    print(hash_senha)
    print("=" * 70)
    print("\n📋 COPIE ESTE HASH E ATUALIZE NO RAILWAY:\n")
    print(hash_senha)
    print("\n" + "=" * 70)
    print("✅ Depois faça login com:")
    print("   Username: admin")
    print(f"   Senha: {senha}")
    print("=" * 70)
    
except Exception as e:
    print(f"Erro ao configurar Django: {e}")
    print("\n⚠️  Usando método alternativo...")
    
    # Fallback para método manual
    import hashlib
    import base64
    import secrets
    
    senha = 'admin123'
    algorithm = 'pbkdf2_sha256'
    iterations = 600000
    salt = secrets.token_urlsafe(12)
    
    hash_obj = hashlib.pbkdf2_hmac(
        'sha256',
        senha.encode('utf-8'),
        salt.encode('utf-8'),
        iterations
    )
    hash_b64 = base64.b64encode(hash_obj).decode('ascii').strip()
    
    hash_final = f'{algorithm}${iterations}${salt}${hash_b64}'
    
    print("=" * 70)
    print("🔐 HASH ALTERNATIVO")
    print("=" * 70)
    print(f"Senha: {senha}")
    print(f"\nHash completo:")
    print(hash_final)
    print("=" * 70)
