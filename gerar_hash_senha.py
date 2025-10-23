"""
Script para gerar hash de senha Django (standalone)
Execute: python gerar_hash_senha.py
"""

import hashlib
import secrets

def make_password_pbkdf2(password):
    """Gera hash PBKDF2 compatível com Django"""
    salt = secrets.token_hex(12)  # 24 caracteres
    iterations = 600000
    hash_value = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), iterations)
    hash_b64 = hash_value.hex()
    return f'pbkdf2_sha256${iterations}${salt}${hash_b64}'

senha = 'Admin@2025!Olhar'
hash_senha = make_password_pbkdf2(senha)

print("=" * 70)
print("🔐 HASH DA SENHA GERADO COM SUCESSO!")
print("=" * 70)
print(f"Senha original: {senha}")
print(f"\nHash para o banco:\n{hash_senha}")
print("=" * 70)
print("\n📋 COPIE O COMANDO SQL ABAIXO E EXECUTE NO RAILWAY (aba Data):\n")
print(f"""
INSERT INTO auth_user (
    username,
    password,
    email,
    is_superuser,
    is_staff,
    is_active,
    first_name,
    last_name,
    date_joined
) VALUES (
    'admin',
    '{hash_senha}',
    'admin@olharliterario.com',
    true,
    true,
    true,
    '',
    '',
    NOW()
);
""")
print("=" * 70)
print("\n✅ Após executar o SQL acima, faça login:")
print("   URL: https://olharliterario-production.up.railway.app/admin")
print("   Username: admin")
print("   Senha: Admin@2025!Olhar")
print("=" * 70)
