# Olhar Literário - Projeto Django

Este projeto foi integrado com Django para adicionar um sistema de banco de dados robusto e escalável.

## 🚀 Estrutura do Projeto

```
Olhar Literario/
├── olhar_literario_django/        # Projeto Django
│   ├── manage.py                   # Gerenciador Django
│   ├── olhar_literario_django/    # Configurações do projeto
│   │   ├── settings.py            # Configurações gerais
│   │   ├── urls.py                # URLs principais
│   │   └── wsgi.py                # WSGI para produção
│   └── books/                     # App principal
│       ├── models.py              # Models (UserProfile, AuthToken, Comment)
│       ├── views.py               # Views da API
│       ├── urls.py                # URLs da API
│       └── admin.py               # Admin do Django
├── index.html                     # Frontend
├── script.js                      # JavaScript
├── style.css                      # Estilos
├── images/                        # Imagens e uploads
├── requirements.txt               # Dependências Python
├── iniciar_django.bat             # Script para iniciar Django
├── migrate_to_django.py           # Script de migração de dados
└── README_DJANGO.md               # Este arquivo
```

## 📦 Instalação e Configuração

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Criar Banco de Dados

```bash
cd olhar_literario_django
python manage.py makemigrations
python manage.py migrate
```

### 3. Criar Superusuário (Administrador)

```bash
python manage.py createsuperuser
```

Siga as instruções para criar um usuário administrador que terá acesso ao painel admin.

### 4. Iniciar o Servidor

**Opção 1: Usando o script batch (Windows)**
```bash
iniciar_django.bat
```

**Opção 2: Manual**
```bash
cd olhar_literario_django
python manage.py runserver 0.0.0.0:8000
```

O servidor estará disponível em:
- **Site**: http://localhost:8000
- **Painel Admin**: http://localhost:8000/admin

## 🔄 Migração de Dados do Flask

Se você tinha dados no banco Flask anterior (`database.db`), pode migrá-los:

```bash
python migrate_to_django.py
```

Este script irá:
- ✅ Migrar usuários
- ✅ Migrar comentários
- ⚠️ Tokens precisarão ser regenerados (usuários fazem login novamente)

## 📊 Models do Django

### UserProfile
Perfil estendido do usuário com:
- Telefone
- Data de nascimento
- Biografia
- Foto de perfil

### AuthToken
Sistema de autenticação por token:
- Token único de 64 caracteres
- Expiração automática em 7 dias
- Validação integrada

### Comment
Sistema de comentários e avaliações:
- Comentários por livro
- Avaliação de 1-5 estrelas
- Timestamp automático
- Indexação para consultas rápidas

## 🔌 API Endpoints

### Autenticação
- `POST /api/register` - Registrar novo usuário
- `POST /api/login` - Fazer login

### Perfil
- `GET /api/profile` - Obter perfil (requer auth)
- `POST /api/profile` - Atualizar perfil (requer auth)
- `POST /api/upload-photo` - Upload de foto (requer auth)

### Comentários
- `GET /api/comments` - Listar comentários
- `GET /api/comments?book=TITULO` - Comentários de um livro
- `POST /api/comments` - Criar comentário (requer auth)

## 🛡️ Painel Admin

Acesse http://localhost:8000/admin com o superusuário criado.

Funcionalidades:
- ✅ Gerenciar usuários e perfis
- ✅ Visualizar e moderar comentários
- ✅ Gerenciar tokens de autenticação
- ✅ Estatísticas e filtros avançados

## 🔐 Segurança

- Senhas são hash com bcrypt
- Tokens expiram automaticamente
- CSRF protection (desabilitado para API, configure para produção)
- Validação de dados em todos os endpoints

## 📝 Vantagens do Django

1. **ORM Poderoso**: Consultas SQL simplificadas e seguras
2. **Admin Automático**: Interface administrativa pronta
3. **Migrações**: Controle de versão do banco de dados
4. **Segurança**: Proteções integradas contra ataques comuns
5. **Escalabilidade**: Suporta múltiplos bancos de dados
6. **Comunidade**: Vasta documentação e pacotes

## 🔧 Configurações Importantes

### Arquivo `settings.py`

```python
# Banco de dados (pode trocar para PostgreSQL, MySQL, etc)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Arquivos de mídia (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'images'

# Idioma e fuso horário
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
```

## 🚀 Produção

Para deploy em produção:

1. **Alterar SECRET_KEY** em `settings.py`
2. **DEBUG = False** em `settings.py`
3. **Configurar ALLOWED_HOSTS** apropriadamente
4. **Usar PostgreSQL ou MySQL** ao invés de SQLite
5. **Configurar arquivos estáticos** com WhiteNoise ou CDN
6. **Habilitar HTTPS**
7. **Configurar CSRF tokens** adequadamente

## 📚 Recursos Adicionais

- [Documentação Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/) (para APIs mais avançadas)
- [Django Admin Cookbook](https://books.agiliq.com/projects/django-admin-cookbook/)

## 🐛 Troubleshooting

### Erro ao migrar
```bash
python manage.py migrate --run-syncdb
```

### Resetar banco de dados
```bash
python manage.py flush
```

### Ver migrações aplicadas
```bash
python manage.py showmigrations
```

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação oficial do Django ou abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando Django**
