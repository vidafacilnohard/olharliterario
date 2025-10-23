"""
Comando customizado do Django para criar um superusuário automaticamente  
Uso: python manage.py criar_admin
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import sys


class Command(BaseCommand):
    help = 'Cria um superusuário admin automaticamente'

    def handle(self, *args, **options):
        print("=" * 60, file=sys.stderr)
        print("🔧 EXECUTANDO COMANDO criar_admin", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        
        User = get_user_model()
        
        username = 'admin'
        email = 'admin@olharliterario.com'
        password = 'admin123'  # Senha simples para teste
        
        try:
            # SEMPRE deletar usuário antigo e criar novo
            deleted_count = User.objects.filter(username=username).delete()[0]
            if deleted_count > 0:
                self.stdout.write(self.style.WARNING(f'🗑️  {deleted_count} usuário(s) admin antigo(s) deletado(s)'))
            
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
            print(f"❌ ERRO AO CRIAR SUPERUSUÁRIO: {e}", file=sys.stderr)
            self.stdout.write(self.style.ERROR(f'❌ Erro: {e}'))
            import traceback
            traceback.print_exc()
