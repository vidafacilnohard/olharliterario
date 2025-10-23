# 🚂 Guia Completo: Railway + PostgreSQL - Passo a Passo

## 📌 PARTE 1: Configurar PostgreSQL no Railway

### **Passo 1: Acessar o Railway**
1. Acesse: https://railway.app
2. Faça login com sua conta GitHub
3. Você verá seu dashboard com seus projetos

### **Passo 2: Criar/Abrir o Projeto**
1. Se já tem um projeto: clique nele
2. Se não tem: clique em **"New Project"**

### **Passo 3: Adicionar PostgreSQL**
1. Dentro do seu projeto, clique no botão **"+ New"** (canto superior direito)
2. Selecione **"Database"**
3. Clique em **"Add PostgreSQL"**
4. ⏳ Aguarde alguns segundos...
5. ✅ Um novo serviço "Postgres" aparecerá no seu projeto!

### **Passo 4: Verificar Variáveis do PostgreSQL**
1. Clique no card/serviço **"Postgres"** que acabou de criar
2. Vá na aba **"Variables"**
3. Você verá várias variáveis automáticas:
   - `DATABASE_URL` ← **Esta é a mais importante!**
   - `PGHOST`
   - `PGPORT`
   - `PGUSER`
   - `PGPASSWORD`
   - `PGDATABASE`

> ⚠️ **IMPORTANTE:** O Railway cria automaticamente a variável `DATABASE_URL`. Você NÃO precisa copiar ou configurar nada aqui!

---

## 📌 PARTE 2: Conectar o Repositório GitHub

### **Passo 5: Adicionar o Serviço da Aplicação**
1. Volte para a visualização geral do projeto (clique no nome do projeto no topo)
2. Clique em **"+ New"** novamente
3. Selecione **"GitHub Repo"**
4. Procure por: **"olharliterario"** ou **"vidafacilnohard/olharliterario"**
5. Clique no repositório para conectar
6. ⏳ O Railway começará a fazer o deploy automaticamente

### **Passo 6: Aguardar o Primeiro Deploy**
1. Você verá logs aparecendo em tempo real
2. O Railway vai:
   - ✅ Detectar Python
   - ✅ Instalar dependências do `requirements.txt`
   - ✅ Executar o `Procfile`
   - ❌ **PROVAVELMENTE VAI FALHAR** (é normal, faltam variáveis!)

---

## 📌 PARTE 3: Configurar Variáveis de Ambiente

### **Passo 7: Acessar as Variáveis da Aplicação**
1. Clique no card/serviço da sua **aplicação Django** (não o Postgres)
2. Vá na aba **"Variables"**

### **Passo 8: Adicionar SECRET_KEY**

**8.1 - Gerar uma SECRET_KEY:**

No seu computador, abra o terminal e execute:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Vai aparecer algo como:
```
django-insecure-a8f9h2j3k4l5m6n7o8p9q0r1s2t3u4v5w6x7y8z9
```

**8.2 - Adicionar no Railway:**
1. Na aba Variables, clique em **"+ New Variable"**
2. **Variable name:** `SECRET_KEY`
3. **Value:** Cole a chave que você gerou
4. Clique em **"Add"**

### **Passo 9: Adicionar DEBUG**
1. Clique em **"+ New Variable"** novamente
2. **Variable name:** `DEBUG`
3. **Value:** `False`
4. Clique em **"Add"**

### **Passo 10: Conectar ao PostgreSQL**

**IMPORTANTE:** Você precisa referenciar o banco PostgreSQL que criou!

**10.1 - Obter a referência do PostgreSQL:**
1. Na visualização geral do projeto, você verá 2 serviços:
   - Postgres (banco de dados)
   - olharliterario (aplicação)

2. Clique no serviço **"Postgres"**
3. Vá na aba **"Variables"**
4. Copie o valor de **`DATABASE_URL`** (algo como `postgresql://postgres:...`)

**10.2 - Adicionar na aplicação:**
1. Volte para o serviço da **aplicação Django**
2. Vá na aba **"Variables"**
3. Clique em **"+ New Variable"**
4. **Variable name:** `DATABASE_URL`
5. **Value:** Cole a URL do PostgreSQL que você copiou
6. Clique em **"Add"**

**OU use a referência automática (RECOMENDADO):**
1. Clique em **"+ New Variable"**
2. **Variable name:** `DATABASE_URL`
3. **Value:** Clique no ícone de **"$"** (Reference)
4. Selecione: **Postgres** → **DATABASE_URL**
5. Clique em **"Add"**

---

## 📌 PARTE 4: Deploy e Verificação

### **Passo 11: Forçar Novo Deploy**
1. Na aplicação Django, vá na aba **"Settings"**
2. Role até **"Service"** → **"Redeploy"**
3. Clique em **"Redeploy"**
4. ⏳ Aguarde o deploy...

### **Passo 12: Verificar os Logs**
1. Vá na aba **"Deployments"**
2. Clique no deploy mais recente
3. Veja os logs em tempo real
4. Você deve ver:
   ```
   Running migrations...
   Operations to perform:
     Apply all migrations: admin, auth, books, contenttypes, sessions
   Running migrations:
     Applying books.0001_initial... OK
   ...
   Starting server with Gunicorn...
   ```

### **Passo 13: Gerar Domínio Público**
1. Vá na aba **"Settings"**
2. Role até **"Networking"** → **"Public Networking"**
3. Clique em **"Generate Domain"**
4. ✅ Uma URL será gerada: `https://olharliterario-production.up.railway.app`

### **Passo 14: Acessar o Site**
1. Clique na URL gerada ou copie e cole no navegador
2. ✅ Seu site deve estar funcionando!

---

## 📌 PARTE 5: Criar Superusuário

### **Opção A: Usando Railway CLI (Recomendado)**

**1. Instalar Railway CLI:**
```bash
npm i -g @railway/cli
```

**2. Fazer Login:**
```bash
railway login
```

**3. Conectar ao Projeto:**
```bash
railway link
```
Selecione seu projeto da lista.

**4. Criar Superusuário:**
```bash
railway run python olhar_literario_django/manage.py createsuperuser
```

Preencha:
- Username: `admin`
- Email: `admin@olharliterario.com`
- Password: (escolha uma senha forte)

### **Opção B: Usando Django Shell (Alternativa)**

Se o CLI não funcionar, você pode criar via código:

1. No Railway, vá em **"Deployments"**
2. Clique no deploy ativo
3. Role até encontrar **"Shell"** ou **"Console"** (se disponível)
4. Execute:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@olharliterario.com', 'sua_senha_aqui')
```

---

## 📌 PARTE 6: Adicionar Livros

### **Passo 15: Acessar o Admin**
1. Acesse: `https://seu-dominio.railway.app/admin`
2. Login com o superusuário criado
3. Vá em **"Books"** → **"+ Add"**

### **Passo 16: Cadastrar Livros**
Adicione alguns livros de teste:

**Exemplo 1:**
- Título: O Pequeno Príncipe
- Autor: Antoine de Saint-Exupéry
- Editora: Agir
- Ano: 1943
- ISBN: 9788522008731
- Gênero: Infantojuvenil
- Sinopse: (adicione uma sinopse)
- Páginas: 96
- Idioma: Português
- Disponível: ✅
- Destaque: ✅

**Exemplo 2:**
- Título: 1984
- Autor: George Orwell
- Editora: Companhia das Letras
- Ano: 1949
- ISBN: 9788535914849
- Gênero: Ficção
- Sinopse: (adicione uma sinopse)
- Páginas: 416
- Idioma: Português
- Disponível: ✅
- Destaque: ✅

---

## ✅ CHECKLIST FINAL

Antes de considerar concluído, verifique:

- [ ] PostgreSQL criado no Railway
- [ ] Repositório conectado
- [ ] Variável `SECRET_KEY` configurada
- [ ] Variável `DEBUG=False` configurada
- [ ] Variável `DATABASE_URL` referenciando o Postgres
- [ ] Deploy bem-sucedido (sem erros nos logs)
- [ ] Domínio público gerado
- [ ] Site acessível via navegador
- [ ] Superusuário criado
- [ ] Admin acessível em `/admin`
- [ ] Pelo menos 3 livros cadastrados
- [ ] Livros aparecem na página inicial

---

## 🆘 PROBLEMAS COMUNS

### ❌ Erro: "DATABASE_URL not found"
**Solução:** Verifique se você referenciou o Postgres corretamente na variável `DATABASE_URL` da aplicação.

### ❌ Erro: "relation 'books_book' does not exist"
**Solução:** As migrations não rodaram. Force um redeploy.

### ❌ Erro: "DisallowedHost"
**Solução:** O domínio do Railway já está em `ALLOWED_HOSTS = ['*']`. Se continuar, adicione o domínio específico.

### ❌ Site abre mas não carrega estilos
**Solução:** Execute:
```bash
railway run python olhar_literario_django/manage.py collectstatic --noinput
```

### ❌ Não consigo criar superusuário
**Solução:** Use a Railway CLI ou crie via código Python no console do Railway.

---

## 🔄 ATUALIZAÇÕES AUTOMÁTICAS

✅ **Cada vez que você fizer um `git push` no GitHub, o Railway automaticamente:**
1. Detecta as mudanças
2. Faz um novo deploy
3. Executa as migrations
4. Reinicia o servidor

Não precisa fazer nada manualmente! 🎉

---

## 📊 MONITORAMENTO

No Railway você pode monitorar:
- 📈 **CPU e Memória** - Aba "Metrics"
- 📝 **Logs em tempo real** - Aba "Deployments"
- 💾 **Uso do banco** - Clique no serviço Postgres
- 🚀 **Status do serviço** - Indicador na página inicial

---

**✅ Pronto! Seu site está no ar com PostgreSQL! 🎉**

Qualquer dúvida, consulte a documentação:
- Railway: https://docs.railway.app
- Django: https://docs.djangoproject.com
