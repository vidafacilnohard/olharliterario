#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de verificação da instalação Django
Execute para verificar se tudo está funcionando corretamente
"""

import sys
import os
from pathlib import Path

def check_mark(condition):
    return "✓" if condition else "✗"

def test_color(condition, text):
    if condition:
        return f"✅ {text}"
    else:
        return f"❌ {text}"

print("=" * 70)
print("🔍 VERIFICAÇÃO DA INSTALAÇÃO DJANGO - OLHAR LITERÁRIO")
print("=" * 70)
print()

# 1. Verificar Python
print("1. Verificando Python...")
python_version = sys.version_info
python_ok = python_version >= (3, 8)
print(f"   {test_color(python_ok, f'Python {python_version.major}.{python_version.minor}.{python_version.micro}')}")
if not python_ok:
    print("   ⚠️  Requer Python 3.8 ou superior")
print()

# 2. Verificar Django
print("2. Verificando Django...")
try:
    import django
    django_ok = True
    print(f"   {test_color(True, f'Django {django.get_version()} instalado')}")
except ImportError:
    django_ok = False
    print(f"   {test_color(False, 'Django NÃO instalado')}")
    print("   💡 Execute: pip install -r requirements.txt")
print()

# 3. Verificar Pillow
print("3. Verificando Pillow (para imagens)...")
try:
    import PIL
    pillow_ok = True
    print(f"   {test_color(True, f'Pillow {PIL.__version__} instalado')}")
except ImportError:
    pillow_ok = False
    print(f"   {test_color(False, 'Pillow NÃO instalado')}")
    print("   💡 Execute: pip install Pillow")
print()

# 4. Verificar estrutura de arquivos
print("4. Verificando estrutura de arquivos...")
base_dir = Path(__file__).resolve().parent
required_files = [
    ('olhar_literario_django/manage.py', 'manage.py'),
    ('olhar_literario_django/olhar_literario_django/settings.py', 'settings.py'),
    ('olhar_literario_django/books/models.py', 'models.py'),
    ('olhar_literario_django/books/views.py', 'views.py'),
    ('index.html', 'index.html'),
    ('script.js', 'script.js'),
    ('style.css', 'style.css'),
]

all_files_ok = True
for filepath, name in required_files:
    full_path = base_dir / filepath
    exists = full_path.exists()
    all_files_ok = all_files_ok and exists
    print(f"   {check_mark(exists)} {name}")

if not all_files_ok:
    print("   ⚠️  Alguns arquivos estão faltando")
print()

# 5. Verificar banco de dados
print("5. Verificando banco de dados...")
db_path = base_dir / 'olhar_literario_django' / 'db.sqlite3'
db_exists = db_path.exists()
print(f"   {test_color(db_exists, 'Banco de dados')}")
if not db_exists:
    print("   💡 Execute: cd olhar_literario_django && python manage.py migrate")
print()

# 6. Verificar pasta de imagens
print("6. Verificando pasta de uploads...")
images_dir = base_dir / 'images'
images_ok = images_dir.exists()
print(f"   {test_color(images_ok, 'Pasta images/')}")
if not images_ok:
    print("   💡 A pasta será criada automaticamente")
print()

# 7. Verificar se pode importar os models
print("7. Verificando models Django...")
if django_ok:
    try:
        sys.path.insert(0, str(base_dir / 'olhar_literario_django'))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')
        django.setup()
        
        from books.models import UserProfile, AuthToken, Comment
        models_ok = True
        print(f"   {test_color(True, 'Models carregados com sucesso')}")
        print(f"      - UserProfile")
        print(f"      - AuthToken")
        print(f"      - Comment")
    except Exception as e:
        models_ok = False
        print(f"   {test_color(False, 'Erro ao carregar models')}")
        print(f"      {str(e)}")
else:
    models_ok = False
    print(f"   {test_color(False, 'Não foi possível verificar (Django não instalado)')}")
print()

# Resumo
print("=" * 70)
print("📊 RESUMO DA VERIFICAÇÃO")
print("=" * 70)
print()

checks = {
    "Python 3.8+": python_ok,
    "Django instalado": django_ok,
    "Pillow instalado": pillow_ok,
    "Arquivos necessários": all_files_ok,
    "Banco de dados criado": db_exists,
    "Models funcionais": models_ok if django_ok else None,
}

all_ok = True
for name, status in checks.items():
    if status is None:
        print(f"   ⚠️  {name}: Não verificado")
    elif status:
        print(f"   ✅ {name}: OK")
    else:
        print(f"   ❌ {name}: FALHOU")
        all_ok = False

print()
print("=" * 70)

if all_ok:
    print("🎉 TUDO FUNCIONANDO PERFEITAMENTE!")
    print()
    print("Próximos passos:")
    print("1. cd olhar_literario_django")
    print("2. python manage.py createsuperuser  (criar admin)")
    print("3. python manage.py runserver        (iniciar servidor)")
    print()
    print("Depois acesse:")
    print("   Site:  http://localhost:8000")
    print("   Admin: http://localhost:8000/admin")
else:
    print("⚠️  ALGUNS PROBLEMAS ENCONTRADOS")
    print()
    print("Siga as dicas (💡) acima para resolver.")
    print()
    print("Ou consulte:")
    print("   - QUICKSTART_DJANGO.md")
    print("   - README_DJANGO.md")
    print("   - COMANDOS_DJANGO.md")

print("=" * 70)
