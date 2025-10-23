"""
Gerar hash de senha SIMPLES para teste
"""

import hashlib
import secrets

def make_password_pbkdf2(password):
    """Gera hash PBKDF2 compatível com Django"""
    salt = secrets.token_hex(12)
    iterations = 600000
    hash_value = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), iterations)
    hash_b64 = hash_value.hex()
    return f'pbkdf2_sha256${iterations}${salt}${hash_b64}'

# Senha SIMPLES para teste
senha = 'admin123'
hash_senha = make_password_pbkdf2(senha)

print("=" * 70)
print("🔐 HASH PARA SENHA SIMPLES (TESTE)")
print("=" * 70)
print(f"Senha: {senha}")
print(f"\nHash completo:")
print(hash_senha)
print("=" * 70)
print("\n📋 EXECUTE NO RAILWAY (UPDATE):\n")
print(f"""UPDATE auth_user 
SET password = '{hash_senha}',
    is_superuser = true,
    is_staff = true,
    is_active = true
WHERE username = 'admin';""")
print("\n" + "=" * 70)
print("✅ Depois faça login com:")
print("   Username: admin")
print(f"   Senha: {senha}")
print("=" * 70)
