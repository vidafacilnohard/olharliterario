from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid
from .storage import GitHubMediaStorage


# Storage para fazer commit automático no GitHub
github_storage = GitHubMediaStorage()


class Book(models.Model):
    """
    Modelo para cadastro de livros
    """
    titulo = models.CharField(max_length=255, verbose_name='Título')
    autor = models.CharField(max_length=255, verbose_name='Autor')
    editora = models.CharField(max_length=255, blank=True, null=True, verbose_name='Editora')
    ano_publicacao = models.IntegerField(blank=True, null=True, verbose_name='Ano de Publicação')
    isbn = models.CharField(max_length=13, blank=True, null=True, unique=True, verbose_name='ISBN')
    genero = models.CharField(max_length=100, blank=True, null=True, verbose_name='Gênero')
    sinopse = models.TextField(blank=True, null=True, verbose_name='Sinopse')
    capa_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Link da Capa (Google Drive)',
        help_text='Cole o link compartilhado do Google Drive (será convertido automaticamente). Ex: https://drive.google.com/file/d/ABC123/view'
    )
    capa = models.ImageField(
        upload_to='book_covers/', 
        blank=True, 
        null=True, 
        verbose_name='Capa (Upload - Opcional)',
        help_text='Deixe em branco se usar o link do Google Drive acima'
    )
    paginas = models.IntegerField(blank=True, null=True, verbose_name='Número de Páginas')
    idioma = models.CharField(max_length=50, default='Português', verbose_name='Idioma')
    disponivel = models.BooleanField(default=True, verbose_name='Disponível')
    destaque = models.BooleanField(default=False, verbose_name='Livro em Destaque')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    
    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['-data_cadastro', 'titulo']
        indexes = [
            models.Index(fields=['titulo']),
            models.Index(fields=['autor']),
            models.Index(fields=['genero']),
        ]
    
    def __str__(self):
        return f'{self.titulo} - {self.autor}'
    
    def get_capa_url(self):
        """Retorna a URL da capa (upload ou URL externa)"""
        if self.capa:
            return self.capa.url
        elif self.capa_url:
            # Converter link do Google Drive automaticamente
            if 'drive.google.com' in self.capa_url:
                # Extrair ID do link do Google Drive
                file_id = None
                if '/file/d/' in self.capa_url:
                    # Link formato: https://drive.google.com/file/d/ID/view
                    file_id = self.capa_url.split('/file/d/')[1].split('/')[0]
                elif 'id=' in self.capa_url:
                    # Link formato: https://drive.google.com/uc?export=view&id=ID
                    file_id = self.capa_url.split('id=')[1].split('&')[0]
                
                if file_id:
                    # Usar drive.usercontent.com que é melhor para embed
                    converted_url = f'https://drive.google.com/thumbnail?id={file_id}&sz=w1000'
                    print(f"[DEBUG] Convertendo link do Google Drive: {self.capa_url} -> {converted_url}")
                    return converted_url
            print(f"[DEBUG] Retornando capa_url direto: {self.capa_url}")
            return self.capa_url
        print(f"[DEBUG] Livro '{self.titulo}' não tem capa configurada")
        return None
    
    def save(self, *args, **kwargs):
        """Salvar e normalizar URL do Google Drive"""
        if self.capa_url and 'drive.google.com' in self.capa_url:
            # Converter automaticamente ao salvar
            if '/file/d/' in self.capa_url and 'uc?export=view' not in self.capa_url:
                file_id = self.capa_url.split('/file/d/')[1].split('/')[0]
                self.capa_url = f'https://drive.google.com/uc?export=view&id={file_id}'
        super().save(*args, **kwargs)
    
    def media_avaliacoes(self):
        """Retorna a média das avaliações do livro"""
        comentarios = self.comentarios.all()
        if comentarios:
            return sum(c.rating for c in comentarios) / len(comentarios)
        return 0
    
    def total_avaliacoes(self):
        """Retorna o total de avaliações"""
        return self.comentarios.count()


class UserProfile(models.Model):
    """
    Perfil estendido do usuário com informações adicionais
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'
    
    def __str__(self):
        return f'Perfil de {self.user.username}'


class AuthToken(models.Model):
    """
    Token de autenticação personalizado para API
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        verbose_name = 'Token de Autenticação'
        verbose_name_plural = 'Tokens de Autenticação'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4().hex
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        return self.expires_at > timezone.now()
    
    def __str__(self):
        return f'Token de {self.user.username} - {self.token[:8]}...'


class Comment(models.Model):
    """
    Comentários e avaliações de livros
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comentarios', blank=True, null=True, verbose_name='Livro')
    book_title = models.CharField(max_length=255)
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 a 5 estrelas
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['book_title', '-created_at']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f'{self.user.username} - {self.book_title} ({self.rating}★)'
