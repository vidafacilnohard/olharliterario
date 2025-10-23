# 🚂 Guia de Deploy - Railway com PostgreSQL

## 📋 Passo a Passo Completo

### **1. Preparação no Railway**

1. Acesse https://railway.app e faça login
2. Crie um novo projeto ou selecione o existente
3. Clique em **"+ New"** → **"Database"** → **"Add PostgreSQL"**
4. O Railway criará automaticamente o banco e a variável `DATABASE_URL`

### **2. Conectar o Repositório GitHub**

1. No Railway, clique em **"+ New"** → **"GitHub Repo"**
2. Selecione: `vidafacilnohard/olharliterario`
3. O Railway detectará automaticamente o `Procfile`

### **3. Configurar Variáveis de Ambiente**

No painel do Railway, vá em **Variables** e adicione:

```bash
# Django Secret Key (gere uma nova!)
SECRET_KEY=sua-chave-secreta-aqui

# Debug (sempre False em produção)
DEBUG=False

# DATABASE_URL já está configurado automaticamente pelo PostgreSQL
```

**Para gerar SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **4. Deploy Automático**

Após conectar o repositório:
- ✅ O Railway detecta `Procfile` e `railway.json`
- ✅ Instala dependências do `requirements.txt`
- ✅ Executa migrations automaticamente
- ✅ Coleta arquivos estáticos
- ✅ Inicia o servidor com Gunicorn

### **5. Acessar o Site**

1. No Railway, clique em **"Settings"** → **"Generate Domain"**
2. Copie a URL gerada (ex: `https://olharliterario-production.up.railway.app`)
3. Acesse e teste!

### **6. Criar Superusuário**

No Railway, vá em **"Deployments"** → selecione o último deploy → **"View Logs"**

Ou conecte via Railway CLI:
```bash
railway login
railway link
railway run python olhar_literario_django/manage.py createsuperuser
```

### **7. Adicionar Livros**

1. Acesse: `https://seu-dominio.railway.app/admin`
2. Login com o superusuário
3. Adicione livros pela interface admin

## 🔧 Arquivos Importantes Criados

- ✅ `Procfile` - Comando de inicialização
- ✅ `railway.json` - Configurações do Railway
- ✅ `runtime.txt` - Versão do Python
- ✅ `requirements.txt` - Dependências (com PostgreSQL)
- ✅ `settings.py` - Configurado para PostgreSQL + SQLite local

## 🎯 O que Funciona Agora

- ✅ **PostgreSQL** em produção (Railway)
- ✅ **SQLite** em desenvolvimento local
- ✅ **Detecção automática** do ambiente
- ✅ **Arquivos estáticos** servidos com WhiteNoise
- ✅ **Migrations automáticas** no deploy
- ✅ **Gunicorn** como servidor WSGI

## 🏠 Desenvolvimento Local

Continua funcionando normalmente:
```bash
iniciar_django.bat
```

O projeto detecta automaticamente que não está no Railway e usa SQLite.

## 📊 Monitoramento

No Railway, você pode ver:
- 📈 **Logs** em tempo real
- 💾 **Uso de banco de dados**
- 🚀 **Status dos deploys**
- 📊 **Métricas de performance**

## 🆘 Troubleshooting

**Erro de CSRF:**
```python
# Já configurado! Railway domains estão em CSRF_TRUSTED_ORIGINS
```

**Migrations não rodaram:**
```bash
railway run python olhar_literario_django/manage.py migrate
```

**Arquivos estáticos não carregam:**
```bash
railway run python olhar_literario_django/manage.py collectstatic --noinput
```

## 🔄 Atualizações Futuras

Cada push no GitHub atualiza automaticamente o Railway! 🎉

---

**Feito com 💚 por Olhar Literário**
