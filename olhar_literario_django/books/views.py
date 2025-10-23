from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta
import json
import uuid
from pathlib import Path
from .models import UserProfile, AuthToken, Comment, Book


# Diretório base para arquivos estáticos
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def index_view(request):
    """Serve a página inicial do site"""
    index_path = BASE_DIR / 'index.html'
    if not index_path.exists():
        return JsonResponse({
            'error': 'index.html não encontrado',
            'path': str(index_path),
            'tip': 'Certifique-se de que o arquivo index.html está na pasta raiz do projeto'
        }, status=404)
    return FileResponse(open(index_path, 'rb'), content_type='text/html')


def livro_view(request):
    """Serve a página de detalhes do livro"""
    livro_path = BASE_DIR / 'livro.html'
    if not livro_path.exists():
        return JsonResponse({
            'error': 'livro.html não encontrado',
            'path': str(livro_path)
        }, status=404)
    return FileResponse(open(livro_path, 'rb'), content_type='text/html')


def biblioteca_view(request):
    """Serve a página da biblioteca"""
    biblioteca_path = BASE_DIR / 'biblioteca.html'
    if not biblioteca_path.exists():
        return JsonResponse({
            'error': 'biblioteca.html não encontrado',
            'path': str(biblioteca_path)
        }, status=404)
    return FileResponse(open(biblioteca_path, 'rb'), content_type='text/html')


def perfil_view(request):
    """Serve a página de perfil do usuário"""
    perfil_path = BASE_DIR / 'perfil.html'
    if not perfil_path.exists():
        return JsonResponse({
            'error': 'perfil.html não encontrado',
            'path': str(perfil_path)
        }, status=404)
    return FileResponse(open(perfil_path, 'rb'), content_type='text/html')


def login_view(request):
    """Serve a página de login"""
    login_path = BASE_DIR / 'login.html'
    if not login_path.exists():
        return JsonResponse({
            'error': 'login.html não encontrado',
            'path': str(login_path)
        }, status=404)
    return FileResponse(open(login_path, 'rb'), content_type='text/html')


def registro_view(request):
    """Serve a página de registro"""
    registro_path = BASE_DIR / 'registro.html'
    if not registro_path.exists():
        return JsonResponse({
            'error': 'registro.html não encontrado',
            'path': str(registro_path)
        }, status=404)
    return FileResponse(open(registro_path, 'rb'), content_type='text/html')


def get_user_from_token(request):
    """
    Extrai e valida o token de autenticação do header Authorization
    Retorna o usuário autenticado ou None
    """
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    
    token_string = auth_header.split(' ', 1)[1]
    try:
        token = AuthToken.objects.select_related('user').get(token=token_string)
        if token.is_valid():
            return token.user
    except AuthToken.DoesNotExist:
        pass
    
    return None


def auth_required(view_func):
    """Decorator para proteger views que requerem autenticação"""
    def wrapper(request, *args, **kwargs):
        user = get_user_from_token(request)
        if not user:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        request.authenticated_user = user
        return view_func(request, *args, **kwargs)
    return wrapper


@csrf_exempt
@require_http_methods(["POST"])
def api_register(request):
    """Registra um novo usuário"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    data_nascimento = data.get('dataNascimento')
    
    if not all([nome, email, senha]):
        return JsonResponse({'error': 'Missing fields'}, status=400)
    
    # Verificar se email já existe
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email already registered'}, status=400)
    
    # Criar usuário
    try:
        user = User.objects.create(
            username=email,  # Usar email como username
            email=email,
            first_name=nome,
            password=make_password(senha)
        )
        
        # Criar perfil
        profile = UserProfile.objects.create(
            user=user,
            data_nascimento=data_nascimento if data_nascimento else None
        )
        
        # Criar token
        token = AuthToken.objects.create(user=user)
        
        return JsonResponse({
            'user': {
                'id': user.id,
                'nome': nome,
                'email': email
            },
            'token': token.token
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """Faz login do usuário"""
    try:
        data = json.loads(request.body)
        print(f"Login attempt - Data received: {data}")
    except json.JSONDecodeError as e:
        print(f"Login error - Invalid JSON: {e}")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    email = data.get('email')
    senha = data.get('senha')
    
    print(f"Login attempt - Email: {email}, Password provided: {'Yes' if senha else 'No'}")
    
    if not all([email, senha]):
        print(f"Login error - Missing fields. Email: {email}, Senha: {'provided' if senha else 'missing'}")
        return JsonResponse({'error': 'Email e senha são obrigatórios'}, status=400)
    
    try:
        user = User.objects.get(email=email)
        print(f"User found: {user.username}, checking password...")
        if check_password(senha, user.password):
            print(f"Password correct, creating token...")
            # Criar novo token
            token = AuthToken.objects.create(user=user)
            
            return JsonResponse({
                'user': {
                    'id': user.id,
                    'nome': user.first_name,
                    'email': user.email
                },
                'token': token.token
            })
        else:
            print(f"Password incorrect for user: {user.username}")
            return JsonResponse({'error': 'Email ou senha incorretos'}, status=400)
    except User.DoesNotExist:
        print(f"User not found with email: {email}")
        return JsonResponse({'error': 'Email ou senha incorretos'}, status=400)


@csrf_exempt
@require_http_methods(["GET", "POST"])
@auth_required
def api_profile(request):
    """Obtém ou atualiza perfil do usuário"""
    user = request.authenticated_user
    
    if request.method == 'GET':
        # Obter perfil
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        
        return JsonResponse({
            'id': user.id,
            'nome': user.first_name,
            'email': user.email,
            'dataNascimento': profile.data_nascimento.isoformat() if profile.data_nascimento else None,
            'telefone': profile.telefone or '',
            'bio': profile.bio or '',
            'foto': profile.foto.url if profile.foto else None,
            'is_superuser': user.is_superuser
        })
    
    elif request.method == 'POST':
        # Atualizar perfil
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        nome = data.get('nome')
        telefone = data.get('telefone')
        bio = data.get('bio')
        data_nascimento = data.get('dataNascimento')
        
        # Atualizar usuário
        if nome:
            user.first_name = nome
            user.save()
        
        # Atualizar perfil
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        
        if telefone is not None:
            profile.telefone = telefone
        if bio is not None:
            profile.bio = bio
        if data_nascimento:
            profile.data_nascimento = data_nascimento
        
        profile.save()
        
        return JsonResponse({'success': True})


@csrf_exempt
@require_http_methods(["POST"])
@auth_required
def api_upload_photo(request):
    """Upload de foto de perfil"""
    user = request.authenticated_user
    
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file'}, status=400)
    
    file = request.FILES['file']
    if not file.name:
        return JsonResponse({'error': 'No filename'}, status=400)
    
    # Obter ou criar perfil
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    # Salvar arquivo
    profile.foto = file
    profile.save()
    
    return JsonResponse({'foto': profile.foto.url})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_comments(request):
    """Obtém ou cria comentários"""
    if request.method == 'POST':
        # Criar comentário (requer autenticação)
        user = get_user_from_token(request)
        if not user:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        book_title = data.get('book_title')
        comment_text = data.get('comment')
        rating = data.get('rating', 0)
        
        if not all([book_title, comment_text, rating]):
            return JsonResponse({'error': 'Missing fields'}, status=400)
        
        try:
            comment = Comment.objects.create(
                user=user,
                book_title=book_title,
                comment=comment_text,
                rating=int(rating)
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'GET':
        # Obter comentários
        book = request.GET.get('book')
        
        if book:
            comments = Comment.objects.filter(book_title=book).select_related('user')
        else:
            comments = Comment.objects.all().select_related('user')
        
        comments_data = []
        for comment in comments:
            comments_data.append({
                'id': comment.id,
                'user_id': comment.user.id,
                'user_nome': comment.user.first_name or comment.user.username,
                'book_title': comment.book_title,
                'comment': comment.comment,
                'rating': comment.rating,
                'created_at': comment.created_at.isoformat()
            })
        
        return JsonResponse(comments_data, safe=False)


@require_http_methods(["GET"])
def api_books(request):
    """Obtém lista de livros cadastrados"""
    # Filtros opcionais
    book_id = request.GET.get('id')
    genero = request.GET.get('genero')
    autor = request.GET.get('autor')
    busca = request.GET.get('q')
    titulo = request.GET.get('titulo')
    disponivel = request.GET.get('disponivel')
    destaque = request.GET.get('destaque')
    
    # Query base
    books = Book.objects.filter(disponivel=True)
    
    # Aplicar filtros
    if book_id:
        books = books.filter(id=book_id)
    if titulo:
        books = books.filter(titulo__iexact=titulo)
    if genero:
        books = books.filter(genero__icontains=genero)
    if autor:
        books = books.filter(autor__icontains=autor)
    if busca:
        books = books.filter(titulo__icontains=busca) | books.filter(autor__icontains=busca)
    if disponivel is not None:
        books = books.filter(disponivel=disponivel.lower() == 'true')
    if destaque is not None:
        books = books.filter(destaque=destaque.lower() == 'true')
    
    # Ordenar por destaque primeiro, depois por mais recentes
    books = books.order_by('-destaque', '-data_cadastro')
    
    # Construir resposta
    books_data = []
    for book in books:
        books_data.append({
            'id': book.id,
            'titulo': book.titulo,
            'autor': book.autor,
            'editora': book.editora or '',
            'ano_publicacao': book.ano_publicacao,
            'isbn': book.isbn or '',
            'genero': book.genero or '',
            'sinopse': book.sinopse or '',
            'capa': book.capa.url if book.capa else None,
            'paginas': book.paginas,
            'idioma': book.idioma,
            'disponivel': book.disponivel,
            'media_avaliacoes': round(book.media_avaliacoes(), 1),
            'total_avaliacoes': book.total_avaliacoes()
        })
    
    return JsonResponse(books_data, safe=False)
