# Olhar Literário - Guia de Início Rápido com Django

## ⚡ Início Rápido (3 passos)

### 1. Instalar Django
```bash
pip install -r requirements.txt
```

### 2. Configurar o Banco de Dados
```bash
cd olhar_literario_django
python manage.py migrate
```

### 3. Iniciar o Servidor
```bash
# Windows
..\iniciar_django.bat

# Ou manualmente
python manage.py runserver 0.0.0.0:8000
```

Pronto! Acesse http://localhost:8000

## 🔑 Criar Usuário Administrador

```bash
cd olhar_literario_django
python manage.py createsuperuser
```

Depois acesse http://localhost:8000/admin

## 📚 Mais Informações

Veja `README_DJANGO.md` para documentação completa.
