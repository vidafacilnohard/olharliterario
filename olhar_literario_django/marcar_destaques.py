#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para marcar livros como destaque
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')
django.setup()

from books.models import Book

def marcar_destaques():
    """Marca os primeiros 3 livros como destaque"""
    print("📌 Marcando livros como destaque...\n")
    
    # Pegar os primeiros 3 livros
    livros = Book.objects.all()[:3]
    
    if not livros:
        print("❌ Nenhum livro encontrado no banco de dados!")
        print("   Execute primeiro: python popular_livros.py")
        return
    
    for livro in livros:
        livro.destaque = True
        livro.save()
        print(f"✅ '{livro.titulo}' marcado como destaque!")
    
    print(f"\n📚 Total de livros em destaque: {Book.objects.filter(destaque=True).count()}")
    print("\n✨ Acesse http://localhost:8000 para ver os livros em destaque!")

if __name__ == '__main__':
    marcar_destaques()
