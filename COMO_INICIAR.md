# 🚀 Como Iniciar o Olhar Literário

## ⚡ Método Mais Fácil (1 clique)

### Windows

**Opção 1: Script Batch (Recomendado)**
```
📁 Duplo clique em: iniciar.bat
```

**Opção 2: PowerShell (Colorido)**
```
📁 Clique com botão direito em: iniciar.ps1
   Selecione: "Executar com PowerShell"
```

### Linux/Mac
```bash
cd olhar_literario_django
python3 manage.py migrate
python3 manage.py runserver
```

---

## 🌐 Acessar o Site

Após iniciar, acesse:

- **Frontend (Site)**: http://localhost:8000
- **Painel Admin**: http://localhost:8000/admin

O navegador abrirá automaticamente (se usar `iniciar.ps1`)

---

## 📋 O que o script faz automaticamente:

1. ✅ Verifica se Python está instalado
2. ✅ Verifica se Django está instalado
3. ✅ Instala dependências se necessário
4. ✅ Cria o banco de dados
5. ✅ Aplica migrações
6. ✅ Inicia o servidor Django
7. ✅ Serve o frontend (HTML, CSS, JS)
8. ✅ Abre o navegador automaticamente

**Tudo em um único comando! 🎉**

---

## 🔑 Criar Administrador (Primeira vez)

Após iniciar o servidor pela primeira vez:

1. Abra outro terminal
2. Execute:
   ```bash
   cd olhar_literario_django
   python manage.py createsuperuser
   ```
3. Siga as instruções
4. Acesse http://localhost:8000/admin

---

## 🛑 Parar o Servidor

Pressione `Ctrl + C` no terminal

---

## ❓ Problemas?

### Django não instalado
```bash
pip install -r requirements.txt
```

### Porta 8000 ocupada
```bash
cd olhar_literario_django
python manage.py runserver 8080
```
Acesse: http://localhost:8080

### Erro de migração
```bash
cd olhar_literario_django
python manage.py migrate --run-syncdb
```

### Python não encontrado
Instale Python 3.8+: https://www.python.org/downloads/

---

## 📚 Mais Informações

- `README_DJANGO.md` - Documentação completa
- `QUICKSTART_DJANGO.md` - Guia rápido
- `COMANDOS_DJANGO.md` - Lista de comandos

---

## 🎯 Resumo Visual

```
┌─────────────────────────────────────────┐
│                                         │
│  Windows: Duplo clique em iniciar.bat   │
│                                         │
│           ↓                             │
│                                         │
│  Servidor inicia automaticamente        │
│                                         │
│           ↓                             │
│                                         │
│  Navegador abre em localhost:8000       │
│                                         │
│           ↓                             │
│                                         │
│  Pronto! Frontend + Backend rodando!    │
│                                         │
└─────────────────────────────────────────┘
```

**É simples assim! 🚀**
