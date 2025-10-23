from django.contrib import admin
from .models import UserProfile, AuthToken, Comment, Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'editora', 'ano_publicacao', 'genero', 'disponivel', 'destaque', 'total_avaliacoes', 'media_avaliacoes']
    search_fields = ['titulo', 'autor', 'isbn', 'editora', 'genero']
    list_filter = ['genero', 'disponivel', 'destaque', 'ano_publicacao', 'idioma']
    list_editable = ['disponivel', 'destaque']
    ordering = ['-destaque', '-data_cadastro', 'titulo']
    readonly_fields = ['data_cadastro', 'total_avaliacoes', 'media_avaliacoes']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'autor', 'editora', 'ano_publicacao', 'isbn')
        }),
        ('Detalhes', {
            'fields': ('genero', 'idioma', 'paginas', 'sinopse')
        }),
        ('Capa do Livro', {
            'fields': ('capa_url', 'capa'),
            'description': 'Opção 1: Cole o link do Google Drive OU Opção 2: Faça upload da imagem'
        }),
        ('Status', {
            'fields': ('disponivel', 'destaque', 'data_cadastro')
        }),
        ('Estatísticas', {
            'fields': ('total_avaliacoes', 'media_avaliacoes'),
            'classes': ('collapse',)
        }),
    )
    
    def media_avaliacoes(self, obj):
        media = obj.media_avaliacoes()
        if media > 0:
            return f'{media:.1f}★'
        return 'Sem avaliações'
    media_avaliacoes.short_description = 'Média'
    
    def total_avaliacoes(self, obj):
        return obj.total_avaliacoes()
    total_avaliacoes.short_description = 'Total de Avaliações'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefone', 'data_nascimento']
    search_fields = ['user__username', 'user__email']
    list_filter = ['data_nascimento']


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_valid']
    search_fields = ['user__username', 'token']
    list_filter = ['created_at', 'expires_at']
    
    def is_valid(self, obj):
        from django.utils import timezone
        return obj.expires_at > timezone.now()
    is_valid.boolean = True
    is_valid.short_description = 'Token Válido'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_book_info', 'rating', 'created_at']
    search_fields = ['user__username', 'book_title', 'comment', 'book__titulo']
    list_filter = ['rating', 'created_at', 'book']
    ordering = ['-created_at']
    autocomplete_fields = ['book']
    
    def get_book_info(self, obj):
        if obj.book:
            return f'{obj.book.titulo}'
        return obj.book_title
    get_book_info.short_description = 'Livro'
