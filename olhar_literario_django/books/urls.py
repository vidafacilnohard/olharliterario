from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Página inicial
    path('', views.index_view, name='index'),
    path('index.html', views.index_view, name='index_html'),
    
    # Página de login e registro
    path('login.html', views.login_view, name='login'),
    path('registro.html', views.registro_view, name='registro'),
    
    # Página de detalhes do livro
    path('livro.html', views.livro_view, name='livro'),
    
    # Página da biblioteca
    path('biblioteca.html', views.biblioteca_view, name='biblioteca'),
    
    # Página de perfil
    path('perfil.html', views.perfil_view, name='perfil'),
    
    # API - Autenticação
    path('api/register', views.api_register, name='api_register'),
    path('api/login', views.api_login, name='api_login'),
    
    # API - Perfil
    path('api/profile', views.api_profile, name='api_profile'),
    path('api/upload-photo', views.api_upload_photo, name='api_upload_photo'),
    
    # API - Comentários
    path('api/comments', views.api_comments, name='api_comments'),
    
    # API - Livros
    path('api/books', views.api_books, name='api_books'),
]
