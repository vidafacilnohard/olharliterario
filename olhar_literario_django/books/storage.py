"""
Sistema de upload automático para GitHub usando a API
Quando uma capa é enviada pelo Django admin, faz commit via API do GitHub
"""
import os
import base64
import requests
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class GitHubStorage(FileSystemStorage):
    """
    Storage customizado que faz commit automático no GitHub via API
    quando um arquivo é salvo
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.github_repo = os.environ.get('GITHUB_REPO', 'vidafacilnohard/olharliterario')
        self.github_branch = 'master'
    
    def _save(self, name, content):
        """
        Salva o arquivo localmente e faz commit automático no GitHub via API
        """
        # Salvar o arquivo normalmente
        full_path = super()._save(name, content)
        
        # Fazer commit via API do GitHub (só em produção e se tiver token)
        if not settings.DEBUG and self.github_token:
            # Ler o conteúdo do arquivo salvo
            with open(self.path(full_path), 'rb') as f:
                file_content = f.read()
            
            self._github_commit(full_path, file_content)
        
        return full_path
    
    def _github_commit(self, file_path, content):
        """
        Faz commit do arquivo no GitHub via API
        """
        try:
            # Caminho relativo no repositório
            repo_path = f"olhar_literario_django/media/{file_path}"
            
            # Codificar conteúdo em base64
            content_base64 = base64.b64encode(content).decode('utf-8')
            
            # URL da API do GitHub
            url = f"https://api.github.com/repos/{self.github_repo}/contents/{repo_path}"
            
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Verificar se arquivo já existe (para pegar o SHA)
            response = requests.get(url, headers=headers)
            sha = None
            if response.status_code == 200:
                sha = response.json().get('sha')
            
            # Dados do commit
            data = {
                'message': f'AUTO: Upload de capa - {os.path.basename(file_path)}',
                'content': content_base64,
                'branch': self.github_branch
            }
            
            if sha:
                data['sha'] = sha  # Atualizar arquivo existente
            
            # Fazer commit via API
            response = requests.put(url, json=data, headers=headers)
            
            if response.status_code in [200, 201]:
                print(f"✅ Arquivo {file_path} commitado no GitHub via API!")
            else:
                print(f"⚠️ Erro ao fazer commit no GitHub: {response.status_code}")
                print(f"   Resposta: {response.text}")
                
        except Exception as e:
            print(f"⚠️ Erro ao fazer commit via API do GitHub: {e}")


class GitHubMediaStorage(GitHubStorage):
    """
    Storage específico para arquivos de mídia (capas de livros, fotos de perfil)
    """
    
    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.MEDIA_ROOT
        kwargs['base_url'] = settings.MEDIA_URL
        super().__init__(*args, **kwargs)
