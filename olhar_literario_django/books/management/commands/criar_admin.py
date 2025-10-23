"""
Comando customizado do Django para criar um superusuário automaticamente
Uso: python manage.py criar_admin
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Cria um superusuário admin automaticamente'

    def handle(self, *args, **options):
        User = get_user_model()
        
        username = 'admin'
        email = 'admin@olharliterario.com'
        password = 'Admin@2025!Olhar'
        
        try:
            # Verific se já existe
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                self.stdout.write(self.style.WARNING('⚠️  Usuário já existe!'))
                self.stdout.write(f'👤 Username: {user.username}')
                self.stdout.write(f'📧 Email: {user.email}')
                self.stdout.write(f'🔐 É superusuário: {user.is_superuser}')
                
                # Atualizar para garantir que é superusuário
                user.is_superuser = True
                user.is_staff = True
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS('✅ Atualizado para superusuário!'))
            else:
                # Criar novo superusuário
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS('=' * 60))
                self.stdout.write(self.style.SUCCESS('🎉 SUPERUSUÁRIO CRIADO COM SUCESSO!'))
                self.stdout.write(self.style.SUCCESS('=' * 60))
                self.stdout.write(f'👤 Username: {username}')
                self.stdout.write(f'📧 Email: {email}')
                self.stdout.write(f'🔑 Senha: {password}')
                self.stdout.write(self.style.SUCCESS('=' * 60))
            
            self.stdout.write(self.style.SUCCESS('🌐 Acesse: https://olharliterario-production.up.railway.app/admin'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro: {e}'))
