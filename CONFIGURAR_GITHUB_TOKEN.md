# 🔐 Configurar Token do GitHub no Railway

## O que é isso?

Quando você faz upload de uma capa de livro pelo Django admin, o sistema automaticamente:
1. ✅ Salva o arquivo em `olhar_literario_django/media/book_covers/`
2. ✅ Faz commit automático no GitHub via API
3. ✅ O arquivo fica salvo permanentemente no repositório
4. ✅ Não é perdido quando o Railway faz redeploy

## Como configurar:

### **Passo 1: Criar um Token de Acesso no GitHub**

1. Acesse: https://github.com/settings/tokens
2. Clique em **"Generate new token"** → **"Generate new token (classic)"**
3. Configure:
   - **Note**: `Railway Upload Token - Olhar Literario`
   - **Expiration**: `No expiration` (ou 1 ano)
   - **Selecione os escopos:**
     - ✅ `repo` (Full control of private repositories)
       - ✅ `repo:status`
       - ✅ `repo_deployment`
       - ✅ `public_repo`
       - ✅ `repo:invite`
4. Clique em **"Generate token"**
5. **COPIE O TOKEN** (ele só aparece uma vez!)
   - Formato: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### **Passo 2: Adicionar o Token no Railway**

1. Acesse: https://railway.app/
2. Entre no projeto **"olharliterario"**
3. Vá em **"Variables"** (ou "Settings" → "Environment Variables")
4. Clique em **"New Variable"**
5. Adicione:
   - **Variable Name**: `GITHUB_TOKEN`
   - **Value**: Cole o token que você copiou
6. Clique em **"Add"**
7. O Railway vai fazer **redeploy automático**

### **Passo 3: Testar**

Após o deploy:
1. Acesse o admin: https://olharliterario-production.up.railway.app/admin
2. Login: `admin` / `admin123`
3. Crie um livro e faça upload de uma capa
4. **Verifique no GitHub:**
   - Acesse: https://github.com/vidafacilnohard/olharliterario
   - Vá em `olhar_literario_django/media/book_covers/`
   - A imagem deve aparecer lá!

## 🎯 Resultado:

Agora **todas as capas** que você fizer upload vão:
- ✅ Ser salvas no GitHub automaticamente
- ✅ Ficar disponíveis permanentemente
- ✅ Não serem perdidas em redepl

oys
- ✅ Carregar direto do repositório

## ⚠️ Importante:

- Guarde o token em um lugar seguro
- Não compartilhe o token com ninguém
- Se perder o token, gere um novo e atualize no Railway

---

**Problemas?** Me avise e te ajudo! 🚀
