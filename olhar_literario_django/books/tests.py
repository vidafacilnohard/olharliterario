from django.test import TestCase, Client
from django.contrib.auth.models import User
from books.models import UserProfile, AuthToken, Comment
from django.utils import timezone
import json


class UserAuthTestCase(TestCase):
    """Testes para autenticação de usuários"""
    
    def setUp(self):
        self.client = Client()
    
    def test_user_registration(self):
        """Testa o registro de um novo usuário"""
        data = {
            'nome': 'João Silva',
            'email': 'joao@example.com',
            'senha': 'senha123',
            'dataNascimento': '1990-01-01'
        }
        response = self.client.post('/api/register', 
                                   data=json.dumps(data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('token', response_data)
        self.assertIn('user', response_data)
        self.assertEqual(response_data['user']['email'], 'joao@example.com')
    
    def test_user_login(self):
        """Testa o login de um usuário existente"""
        # Criar usuário primeiro
        user = User.objects.create_user(
            username='maria@example.com',
            email='maria@example.com',
            password='senha123',
            first_name='Maria'
        )
        
        # Tentar login
        data = {
            'email': 'maria@example.com',
            'senha': 'senha123'
        }
        response = self.client.post('/api/login',
                                   data=json.dumps(data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('token', response_data)
        self.assertEqual(response_data['user']['nome'], 'Maria')


class UserProfileTestCase(TestCase):
    """Testes para perfil de usuário"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='teste@example.com',
            email='teste@example.com',
            password='senha123',
            first_name='Usuário Teste'
        )
        self.token = AuthToken.objects.create(user=self.user)
        self.auth_header = f'Bearer {self.token.token}'
    
    def test_get_profile(self):
        """Testa a obtenção do perfil do usuário"""
        response = self.client.get('/api/profile',
                                  HTTP_AUTHORIZATION=self.auth_header)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['email'], 'teste@example.com')
    
    def test_update_profile(self):
        """Testa a atualização do perfil"""
        update_data = {
            'nome': 'Nome Atualizado',
            'telefone': '(11) 98765-4321',
            'bio': 'Amante de livros'
        }
        response = self.client.post('/api/profile',
                                   data=json.dumps(update_data),
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=self.auth_header)
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar se foi atualizado
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Nome Atualizado')


class CommentTestCase(TestCase):
    """Testes para comentários"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='leitor@example.com',
            email='leitor@example.com',
            password='senha123',
            first_name='Leitor Ávido'
        )
        self.token = AuthToken.objects.create(user=self.user)
        self.auth_header = f'Bearer {self.token.token}'
    
    def test_create_comment(self):
        """Testa a criação de um comentário"""
        comment_data = {
            'book_title': 'Harry Potter',
            'comment': 'Livro incrível!',
            'rating': 5
        }
        response = self.client.post('/api/comments',
                                   data=json.dumps(comment_data),
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=self.auth_header)
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o comentário foi criado
        comment = Comment.objects.get(book_title='Harry Potter')
        self.assertEqual(comment.rating, 5)
        self.assertEqual(comment.user, self.user)
    
    def test_get_comments(self):
        """Testa a listagem de comentários"""
        # Criar alguns comentários
        Comment.objects.create(
            user=self.user,
            book_title='1984',
            comment='Distópico fascinante',
            rating=5
        )
        Comment.objects.create(
            user=self.user,
            book_title='1984',
            comment='Muito bom!',
            rating=4
        )
        
        # Listar todos
        response = self.client.get('/api/comments')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        
        # Filtrar por livro
        response = self.client.get('/api/comments?book=1984')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)


class TokenAuthTestCase(TestCase):
    """Testes para o sistema de tokens"""
    
    def test_token_creation(self):
        """Testa a criação de um token"""
        user = User.objects.create_user(
            username='token@example.com',
            email='token@example.com',
            password='senha123'
        )
        
        token = AuthToken.objects.create(user=user)
        
        self.assertIsNotNone(token.token)
        self.assertEqual(len(token.token), 32)  # UUID hex tem 32 caracteres
        self.assertTrue(token.is_valid())
    
    def test_token_expiration(self):
        """Testa a expiração de tokens"""
        user = User.objects.create_user(
            username='expired@example.com',
            email='expired@example.com',
            password='senha123'
        )
        
        # Criar token expirado
        from datetime import timedelta
        token = AuthToken.objects.create(user=user)
        token.expires_at = timezone.now() - timedelta(days=1)
        token.save()
        
        self.assertFalse(token.is_valid())
