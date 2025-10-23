#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para migrar dados do banco Flask (database.db) para Django
Execute após criar as migrações do Django:
    python manage.py makemigrations
    python manage.py migrate
    python migrate_to_django.py
"""

import os
import sys
import sqlite3
import django
from pathlib import Path
from datetime import datetime

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / 'olhar_literario_django'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')
django.setup()

from django.contrib.auth.models import User
from books.models import UserProfile, AuthToken, Comment


def migrate_users(cursor):
    """Migra usuários do Flask para Django"""
    print("Migrando usuários...")
    
    cursor.execute('SELECT id, nome, email, password_hash, dataNascimento, telefone, bio, foto FROM users')
    users_data = cursor.fetchall()
    
    migrated = 0
    for row in users_data:
        old_id, nome, email, password_hash, data_nasc, telefone, bio, foto = row
        
        # Verificar se usuário já existe
        if User.objects.filter(email=email).exists():
            print(f"  ⚠ Usuário {email} já existe, pulando...")
            continue
        
        # Criar usuário Django
        user = User.objects.create(
            username=email,
            email=email,
            first_name=nome or '',
            password=password_hash  # Mantém o hash original
        )
        
        # Criar perfil
        profile = UserProfile.objects.create(
            user=user,
            telefone=telefone,
            data_nascimento=data_nasc if data_nasc else None,
            bio=bio
        )
        
        # Se havia foto, copiar referência (você pode precisar copiar os arquivos manualmente)
        if foto:
            # A foto estava em images/user_X_...
            # No Django, será em media/profile_photos/
            print(f"  ℹ Foto do usuário {email}: {foto} (copie manualmente se necessário)")
        
        migrated += 1
        print(f"  ✓ Usuário {email} migrado")
    
    print(f"\n{migrated} usuários migrados com sucesso!\n")
    return migrated


def migrate_tokens(cursor):
    """Migra tokens de autenticação"""
    print("Migrando tokens...")
    
    cursor.execute('SELECT token, user_id, expires_at FROM tokens')
    tokens_data = cursor.fetchall()
    
    migrated = 0
    for row in tokens_data:
        token_str, old_user_id, expires_str = row
        
        # Buscar usuário correspondente pelo ID antigo
        # Como não temos mapeamento direto, vamos pular tokens por enquanto
        # Em produção, você pode criar um mapeamento id_antigo -> user_novo
        print(f"  ℹ Token {token_str[:8]}... encontrado (migração manual necessária)")
        # Você pode implementar lógica de mapeamento aqui se necessário
    
    print(f"\nTokens requerem migração manual ou novo login dos usuários.\n")
    return 0


def migrate_comments(cursor):
    """Migra comentários"""
    print("Migrando comentários...")
    
    cursor.execute('''
        SELECT c.user_id, c.book_title, c.comment, c.rating, c.created_at, u.email
        FROM comments c
        LEFT JOIN users u ON u.id = c.user_id
    ''')
    comments_data = cursor.fetchall()
    
    migrated = 0
    for row in comments_data:
        old_user_id, book_title, comment_text, rating, created_str, email = row
        
        if not email:
            print(f"  ⚠ Comentário sem email de usuário, pulando...")
            continue
        
        # Buscar usuário Django pelo email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            print(f"  ⚠ Usuário {email} não encontrado, pulando comentário...")
            continue
        
        # Criar comentário
        try:
            created_at = datetime.fromisoformat(created_str) if created_str else None
            comment = Comment.objects.create(
                user=user,
                book_title=book_title,
                comment=comment_text,
                rating=rating or 5
            )
            if created_at:
                # Atualizar data de criação manualmente
                Comment.objects.filter(id=comment.id).update(created_at=created_at)
            
            migrated += 1
            print(f"  ✓ Comentário de {email} sobre '{book_title}' migrado")
        except Exception as e:
            print(f"  ✗ Erro ao migrar comentário: {e}")
    
    print(f"\n{migrated} comentários migrados com sucesso!\n")
    return migrated


def main():
    # Verificar se database.db existe
    db_path = BASE_DIR / 'database.db'
    if not db_path.exists():
        print("❌ Arquivo database.db não encontrado!")
        print("Execute o servidor Flask primeiro para criar o banco de dados.")
        return
    
    print("=" * 60)
    print("MIGRAÇÃO DE DADOS: Flask → Django")
    print("=" * 60)
    print()
    
    # Conectar ao banco antigo
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Migrar em ordem
        users_count = migrate_users(cursor)
        tokens_count = migrate_tokens(cursor)
        comments_count = migrate_comments(cursor)
        
        print("=" * 60)
        print("RESUMO DA MIGRAÇÃO")
        print("=" * 60)
        print(f"Usuários migrados: {users_count}")
        print(f"Comentários migrados: {comments_count}")
        print()
        print("⚠ IMPORTANTE:")
        print("  - Tokens de autenticação não foram migrados")
        print("  - Usuários precisarão fazer login novamente")
        print("  - Verifique as fotos de perfil em images/")
        print()
        print("✓ Migração concluída!")
        
    except Exception as e:
        print(f"\n❌ Erro durante migração: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()


if __name__ == '__main__':
    main()
