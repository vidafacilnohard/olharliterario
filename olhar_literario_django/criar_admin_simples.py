import os
import django

print("=" * 70)
print("🚀 INICIANDO CRIAÇÃO DE SUPERUSUÁRIO (VERSÃO SIMPLIFICADA)")
print("=" * 70)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
password = 'admin123'
email = 'admin@olharliterario.com'

try:
    # Deletar todos os admins
    deletados = User.objects.filter(username=username).count()
    User.objects.filter(username=username).delete()
    print(f"🗑️  Deletados: {deletados} usuário(s)")
    
    # Criar novo
    user = User.objects.create_superuser(username, email, password)
    
    print("=" * 70)
    print("✅ ✅ ✅ SUPERUSUÁRIO CRIADO COM SUCESSO! ✅ ✅ ✅")
    print("=" * 70)
    print(f"👤 Username: {username}")
    print(f"🔑 Senha: {password}")
    print(f"⭐ Superuser: {user.is_superuser}")
    print(f"👔 Staff: {user.is_staff}")
    print("=" * 70)
    
except Exception as e:
    print("=" * 70)
    print(f"❌ ❌ ❌ ERRO: {e}")
    print("=" * 70)
    raise
