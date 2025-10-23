#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para popular o banco de dados com livros de exemplo
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')
django.setup()

from books.models import Book

# Livros de exemplo
livros_exemplo = [
    {
        'titulo': 'Harry Potter e a Pedra Filosofal',
        'autor': 'J. K. Rowling',
        'editora': 'Rocco',
        'ano_publicacao': 2000,
        'isbn': '9788532530787',
        'genero': 'Fantasia',
        'sinopse': 'Harry Potter e a Pedra Filosofal, de J. K. Rowling, é o início da história do Harry, um menino órfão que descobre aos 11 anos que é um bruxo e vai estudar em Hogwarts, onde vive suas primeiras aventuras e enfrenta o vilão Voldemort.',
        'paginas': 264,
        'idioma': 'Português',
    },
    {
        'titulo': 'A Culpa é das Estrelas',
        'autor': 'John Green',
        'editora': 'Intrínseca',
        'ano_publicacao': 2012,
        'isbn': '9788580572261',
        'genero': 'Romance',
        'sinopse': 'O livro A Culpa é das Estrelas, de John Green, conta a história de Hazel Grace, uma jovem com câncer que conhece Augustus Waters em um grupo de apoio. Juntos, eles vivem uma emocionante história de amor, marcada por humor e drama sobre a vida, a morte e o significado de cada momento.',
        'paginas': 288,
        'idioma': 'Português',
    },
    {
        'titulo': 'A Sutil Arte de Ligar o Foda-se',
        'autor': 'Mark Manson',
        'editora': 'Intrínseca',
        'ano_publicacao': 2016,
        'isbn': '9788551001523',
        'genero': 'Autoajuda',
        'sinopse': 'Chega de tentar buscar um sucesso que só existe na sua cabeça. Chega de se torturar para pensar positivo enquanto sua vida vai ladeira abaixo. Na contramão da autoajuda convencional, Manson prova que a chave para pessoas mais confiantes e felizes é parar de fugir dos problemas e encarar as verdades dolorosas.',
        'paginas': 224,
        'idioma': 'Português',
    },
    {
        'titulo': '1984',
        'autor': 'George Orwell',
        'editora': 'Companhia das Letras',
        'ano_publicacao': 1949,
        'isbn': '9788535914849',
        'genero': 'Distopia',
        'sinopse': 'Winston Smith trabalha para o Ministério da Verdade em Londres, maior cidade da pista de pouso Oceânia. É encarregado de reescrever a história para que sempre se adeque à linha partidária contemporânea. O Partido controla tudo na Oceânia, até mesmo os pensamentos das pessoas.',
        'paginas': 416,
        'idioma': 'Português',
    },
    {
        'titulo': 'O Hobbit',
        'autor': 'J. R. R. Tolkien',
        'editora': 'HarperCollins',
        'ano_publicacao': 1937,
        'isbn': '9788595084742',
        'genero': 'Fantasia',
        'sinopse': 'Como a maioria dos hobbits, Bilbo Bolseiro leva uma vida tranquila até o dia em que recebe uma missão do mago Gandalf. Acompanhado por um grupo de anões, ele precisa viajar até a Montanha Solitária para libertar o Reino de Erebor do dragão Smaug.',
        'paginas': 336,
        'idioma': 'Português',
    },
    {
        'titulo': 'O Pequeno Príncipe',
        'autor': 'Antoine de Saint-Exupéry',
        'editora': 'Agir',
        'ano_publicacao': 1943,
        'isbn': '9788522008728',
        'genero': 'Fábula',
        'sinopse': 'Nesta clássica história de amor e amizade, um piloto cai com seu avião no deserto do Saara e encontra um pequeno príncipe vindo de outro planeta. As lições de vida ensinadas pelo príncipe sobre amor, amizade e valores humanos tocam o coração de leitores de todas as idades.',
        'paginas': 96,
        'idioma': 'Português',
    },
]

def popular_livros():
    """Adiciona os livros de exemplo ao banco de dados"""
    print("🔄 Populando banco de dados com livros de exemplo...\n")
    
    livros_criados = 0
    livros_existentes = 0
    
    for livro_data in livros_exemplo:
        # Verificar se o livro já existe
        if Book.objects.filter(titulo=livro_data['titulo']).exists():
            print(f"⏭️  '{livro_data['titulo']}' já existe no banco de dados")
            livros_existentes += 1
            continue
        
        # Criar o livro
        try:
            livro = Book.objects.create(**livro_data)
            print(f"✅ '{livro.titulo}' adicionado com sucesso!")
            livros_criados += 1
        except Exception as e:
            print(f"❌ Erro ao adicionar '{livro_data['titulo']}': {e}")
    
    print("\n" + "="*60)
    print(f"📚 Resumo:")
    print(f"   - Livros criados: {livros_criados}")
    print(f"   - Livros já existentes: {livros_existentes}")
    print(f"   - Total de livros no banco: {Book.objects.count()}")
    print("="*60)
    print("\n✨ Acesse http://localhost:8000/admin para gerenciar os livros!")
    print("✨ Ou acesse http://localhost:8000 para ver os livros no site!")

if __name__ == '__main__':
    popular_livros()
