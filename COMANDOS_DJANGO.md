# Comandos Úteis do Django - Olhar Literário

## 🚀 Configuração Inicial

### Instalar dependências
```bash
pip install -r requirements.txt
```

### Criar banco de dados
```bash
cd olhar_literario_django
python manage.py makemigrations
python manage.py migrate
```

### Criar superusuário
```bash
python manage.py createsuperuser
```

### Iniciar servidor
```bash
python manage.py runserver 0.0.0.0:8000
```

## 📊 Banco de Dados

### Criar novas migrações
```bash
python manage.py makemigrations
```

### Aplicar migrações
```bash
python manage.py migrate
```

### Ver migrações aplicadas
```bash
python manage.py showmigrations
```

### Reverter migração
```bash
python manage.py migrate books 0001  # Voltar para migração 0001
```

### Resetar banco de dados
```bash
python manage.py flush
```

### Fazer backup do banco
```bash
python manage.py dumpdata > backup.json
```

### Restaurar backup
```bash
python manage.py loaddata backup.json
```

## 🔍 Inspeção

### Abrir shell interativo
```bash
python manage.py shell
```

Exemplos no shell:
```python
from django.contrib.auth.models import User
from books.models import Comment, UserProfile

# Ver todos os usuários
User.objects.all()

# Criar usuário
user = User.objects.create_user('teste@example.com', 'teste@example.com', 'senha123')

# Ver comentários
Comment.objects.all()

# Filtrar comentários
Comment.objects.filter(book_title='Harry Potter')

# Contar comentários
Comment.objects.count()
```

### Ver SQL de uma query
```bash
python manage.py shell
```
```python
from books.models import Comment
print(Comment.objects.filter(rating=5).query)
```

### Ver estrutura do banco
```bash
python manage.py dbshell
```
```sql
.tables
.schema books_comment
```

## 🧪 Testes

### Executar todos os testes
```bash
python manage.py test
```

### Executar testes de um app específico
```bash
python manage.py test books
```

### Executar teste específico
```bash
python manage.py test books.tests.CommentTestCase
```

### Executar com cobertura
```bash
pip install coverage
coverage run manage.py test
coverage report
coverage html  # Gera relatório HTML
```

## 👥 Gestão de Usuários

### Criar superusuário
```bash
python manage.py createsuperuser
```

### Mudar senha de usuário
```bash
python manage.py changepassword usuario@example.com
```

### Shell para gerenciar usuários
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User

# Listar todos
for user in User.objects.all():
    print(user.username, user.email)

# Tornar usuário admin
user = User.objects.get(email='usuario@example.com')
user.is_staff = True
user.is_superuser = True
user.save()

# Desativar usuário
user = User.objects.get(email='usuario@example.com')
user.is_active = False
user.save()
```

## 📁 Arquivos Estáticos

### Coletar arquivos estáticos (produção)
```bash
python manage.py collectstatic
```

### Limpar arquivos estáticos coletados
```bash
python manage.py collectstatic --clear --noinput
```

## 🔧 Manutenção

### Ver configurações atuais
```bash
python manage.py diffsettings
```

### Verificar problemas no projeto
```bash
python manage.py check
```

### Verificar problemas de deploy
```bash
python manage.py check --deploy
```

### Limpar sessões expiradas
```bash
python manage.py clearsessions
```

## 📊 Estatísticas Rápidas (Shell)

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from books.models import Comment, UserProfile, AuthToken

# Total de usuários
print(f"Total de usuários: {User.objects.count()}")

# Total de comentários
print(f"Total de comentários: {Comment.objects.count()}")

# Comentários por livro
from django.db.models import Count
books = Comment.objects.values('book_title').annotate(total=Count('id')).order_by('-total')
for book in books[:10]:
    print(f"{book['book_title']}: {book['total']} comentários")

# Média de avaliações
from django.db.models import Avg
avg = Comment.objects.aggregate(Avg('rating'))
print(f"Média de avaliações: {avg['rating__avg']:.2f}")

# Usuários mais ativos
from django.db.models import Count
active_users = User.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:10]
for user in active_users:
    print(f"{user.first_name}: {user.num_comments} comentários")
```

## 🔄 Migração de Dados

### Migrar do Flask para Django
```bash
python migrate_to_django.py
```

### Exportar dados de um model específico
```bash
python manage.py dumpdata books.Comment > comments.json
```

### Importar dados
```bash
python manage.py loaddata comments.json
```

## 🌐 Produção

### Gerar SECRET_KEY nova
```bash
python manage.py shell
```
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Verificar segurança para produção
```bash
python manage.py check --deploy
```

### Criar requirements.txt com versões fixas
```bash
pip freeze > requirements.txt
```

## 📝 Logs e Debug

### Ver logs em tempo real (se configurado)
```bash
tail -f logs/django.log
```

### Ativar debug SQL (settings.py)
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 🎯 Atalhos Úteis

### Ver todas as URLs do projeto
```bash
python manage.py show_urls  # Requer django-extensions
```

Ou manualmente:
```bash
python manage.py shell
```
```python
from django.urls import get_resolver
resolver = get_resolver()
for pattern in resolver.url_patterns:
    print(pattern)
```

### Limpar cache
```bash
python manage.py shell
```
```python
from django.core.cache import cache
cache.clear()
```

## 📦 Extensões Recomendadas

```bash
pip install django-extensions  # Comandos extras
pip install django-debug-toolbar  # Debug visual
pip install django-filter  # Filtros avançados
pip install djangorestframework  # API REST completa
```

## 🆘 Troubleshooting

### Resetar migrações completamente
```bash
# Backup primeiro!
python manage.py dumpdata > backup.json

# Deletar migrations
rm -rf books/migrations/

# Recriar
python manage.py makemigrations books
python manage.py migrate

# Restaurar dados se necessário
python manage.py loaddata backup.json
```

### Erro de import
```bash
# Reinstalar Django
pip uninstall django
pip install django==4.2
```

### Porta já em uso
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

---

💡 **Dica**: Salve este arquivo como referência!
