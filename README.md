# 📚 Olhar Literário - Site Literário

Site completo de uma plataforma literária com design moderno e funcional.

## ⚡ **NOVO: Versão Django com Banco de Dados!**

Este projeto agora possui duas versões:

1. **Flask (Original)** - Simples e rápida
2. **Django (Nova)** - Com banco de dados completo, admin e mais recursos!

### 🎯 Escolha sua versão:

**Django (Recomendado)** 👈
- ✅ Sistema de banco de dados robusto
- ✅ Painel administrativo completo
- ✅ Escalável para produção
- ✅ ORM poderoso
- 📖 [Guia de Início Rápido Django](QUICKSTART_DJANGO.md)
- 📚 [Documentação Completa](README_DJANGO.md)

**Flask (Original)**
- ✅ Simples e minimalista
- ✅ Fácil de entender
- ✅ Bom para desenvolvimento rápido

## 🚀 Como Executar

### DJANGO (Nova versão - Recomendada)

#### ⚡ Método Mais Fácil (1 clique):
```bash
# Windows - Duplo clique em:
iniciar.bat

# Ou PowerShell (colorido):
iniciar.ps1
```

#### Manual:
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Iniciar servidor Django
cd olhar_literario_django
python manage.py migrate
python manage.py runserver
```

**O script faz tudo automaticamente!** ✨
- ✅ Verifica instalação
- ✅ Cria banco de dados
- ✅ Inicia servidor
- ✅ Abre navegador

Acesse:
- **Site**: http://localhost:8000
- **Admin**: http://localhost:8000/admin

📖 [Guia Completo de Inicialização](COMO_INICIAR.md)

### FLASK (Versão original)

#### Opção 1: Usando o arquivo batch (Windows)
1. Dê duplo clique no arquivo `iniciar_servidor.bat`
2. O servidor iniciará automaticamente

#### Opção 2: Usando Python diretamente
```bash
python server.py
```

## 🌐 Como Acessar

Após iniciar o servidor, você verá as URLs disponíveis:

- **Localhost:** `http://localhost:8000`
- **IP Local:** `http://SEU_IP:8000` (ex: http://192.168.1.100:8000)

### Acessar de outros dispositivos na mesma rede:

1. Anote o **IP Local** mostrado no terminal
2. No celular/tablet/outro computador, abra o navegador
3. Digite: `http://IP_LOCAL:8000`
4. Exemplo: `http://192.168.1.100:8000`

⚠️ **Importante:** Ambos os dispositivos devem estar na mesma rede WiFi!

## ✨ Funcionalidades

### Header
- ✅ Logo responsivo
- ✅ Barra de busca com filtros (livros/autores/editoras)
- ✅ Menu "Explorar" com categorias
- ✅ Botões de Cadastro e Login
- ✅ Chat interativo

### Banner
- ✅ Animações de livros e lápis flutuantes
- ✅ Design com gradiente coral/salmão

### Seção de Livros
- ✅ Cards de livros com:
  - Capa do livro
  - Título e descrição
  - Botão de comentário
  - Nome do autor
  - Marca-página decorativo

### Modais
- ✅ Login
- ✅ Cadastro
- ✅ Comentários com avaliação por estrelas

### Interatividade
- ✅ Sistema de notificações
- ✅ Animações suaves
- ✅ Dropdowns funcionais
- ✅ Design responsivo (mobile-friendly)

## 🎨 Tecnologias

- **HTML5** - Estrutura
- **CSS3** - Estilização e animações
- **JavaScript** - Interatividade
- **Python** - Servidor local

## 📱 Compatibilidade

- ✅ Desktop (Windows, Mac, Linux)
- ✅ Tablets
- ✅ Smartphones
- ✅ Todos os navegadores modernos

## 🛠️ Estrutura de Arquivos

```
Olhar Literario/
├── olhar_literario_django/         # 🆕 Projeto Django
│   ├── manage.py                   # Gerenciador Django
│   ├── olhar_literario_django/    # Configurações
│   │   ├── settings.py            # Configurações do projeto
│   │   ├── urls.py                # URLs principais
│   │   └── wsgi.py                # WSGI para produção
│   └── books/                     # App principal
│       ├── models.py              # Models (DB)
│       ├── views.py               # Views da API
│       ├── urls.py                # URLs da app
│       ├── admin.py               # Config do admin
│       └── tests.py               # Testes automatizados
├── index.html                     # Frontend
├── style.css                      # Estilos
├── script.js                      # JavaScript
├── images/                        # Imagens e uploads
├── server.py                      # Servidor Flask (original)
├── iniciar_servidor.bat           # Iniciar Flask
├── iniciar_django.bat             # 🆕 Iniciar Django
├── migrate_to_django.py           # 🆕 Script de migração
├── requirements.txt               # Dependências
├── README.md                      # Este arquivo
├── README_DJANGO.md               # 🆕 Documentação Django
├── QUICKSTART_DJANGO.md           # 🆕 Guia rápido
└── COMANDOS_DJANGO.md             # 🆕 Comandos úteis
```

## 🔧 Requisitos

- Python 3.6 ou superior
- Navegador web moderno
- Conexão de rede (para acesso via IP)

## 📝 Notas

- O servidor roda na porta **8000** por padrão
- Para parar o servidor: pressione `Ctrl+C`
- Certifique-se de que a porta 8000 não está sendo usada por outro programa
- Se o firewall bloquear, permita acesso à porta 8000

## 🎯 Funcionalidades (Versão Django)

- ✅ Sistema de banco de dados (SQLite/PostgreSQL/MySQL)
- ✅ Sistema de autenticação completo
- ✅ Comentários salvos no banco
- ✅ API RESTful funcional
- ✅ Painel administrativo
- ✅ Upload de fotos de perfil
- ✅ Sistema de tokens
- ✅ Migrações automáticas
- [ ] Sistema de recomendação (futuro)
- [ ] Integração com redes sociais (futuro)

## 📚 Documentação

- 📖 [Guia de Início Rápido Django](QUICKSTART_DJANGO.md)
- 📚 [Documentação Completa Django](README_DJANGO.md)
- 🛠️ [Comandos Úteis Django](COMANDOS_DJANGO.md)
- 🔄 [Migração Flask → Django](migrate_to_django.py)
- ⚖️ [Comparação Flask vs Django](comparacao_flask_django.py)

## 👨‍💻 Desenvolvimento

Site desenvolvido com base no design fornecido, incluindo:
- Design fiel à imagem de referência
- Cores e tipografia originais
- Animações personalizadas
- Interatividade completa

## 📞 Suporte

Se encontrar problemas:
1. Verifique se o Python está instalado: `python --version`
2. Verifique se a porta 8000 está livre
3. Tente usar uma porta diferente alterando em `server.py`

---

**Desenvolvido com ❤️ para Olhar Literário**
