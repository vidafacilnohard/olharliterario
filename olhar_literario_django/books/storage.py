"""
Sistema de upload automático para GitHub usando a API
Quando uma capa é enviada pelo Django admin, faz commit via API do GitHub
e retorna a URL do arquivo no GitHub para servir diretamente (CDN)
"""
import os
import base64
import requests
from django.conf import settings
from django.core.files.storage import Storage
from django.core.files.base import ContentFile


class GitHubStorage(Storage):
    """
    Storage customizado que:
    1. Faz upload direto para o GitHub via API
    2. Retorna URL do GitHub para servir o arquivo (usa GitHub como CDN)
    3. Não salva arquivos localmente (Railway não persiste uploads)
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.github_repo = os.environ.get('GITHUB_REPO', 'vidafacilnohard/olharliterario')
        self.github_branch = 'master'
        # Usar JSDelivr como CDN - sem limite de requisições e com cache
        self.base_url = f'https://cdn.jsdelivr.net/gh/{self.github_repo}@{self.github_branch}/olhar_literario_django/media/'
    
    def _save(self, name, content):
        """
        Salva o arquivo direto no GitHub e retorna o caminho
        """
        # Ler conteúdo
        content.seek(0)
        file_content = content.read()
        
        # Fazer upload para o GitHub
        if self.github_token:
            success = self._github_upload(name, file_content)
            if not success:
                print(f"⚠️ Falha ao fazer upload para o GitHub: {name}")
        else:
            print(f"⚠️ GITHUB_TOKEN não configurado. Configure para uploads automáticos.")
        
        return name
    
    def _github_upload(self, file_path, content):
        """
        Faz upload do arquivo no GitHub via API
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
                print(f"✅ Arquivo {file_path} enviado para o GitHub!")
                print(f"🌐 URL: {self.base_url}{file_path}")
                return True
            else:
                print(f"⚠️ Erro ao fazer upload para o GitHub: {response.status_code}")
                print(f"   Resposta: {response.text}")
                return False
                
        except Exception as e:
            print(f"⚠️ Erro ao fazer upload via API do GitHub: {e}")
            return False
    
    def url(self, name):
        """
        Retorna a URL do arquivo no GitHub (CDN público)
        """
        return f"{self.base_url}{name}"
    
    def exists(self, name):
        """
        Verifica se arquivo existe no GitHub
        """
        if not self.github_token:
            return False
            
        repo_path = f"olhar_literario_django/media/{name}"
        url = f"https://api.github.com/repos/{self.github_repo}/contents/{repo_path}"
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(url, headers=headers)
        return response.status_code == 200
    
    def delete(self, name):
        """
        Deleta arquivo do GitHub
        """
        if not self.github_token:
            return
            
        repo_path = f"olhar_literario_django/media/{name}"
        url = f"https://api.github.com/repos/{self.github_repo}/contents/{repo_path}"
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Pegar SHA do arquivo
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            sha = response.json().get('sha')
            
            # Deletar arquivo
            data = {
                'message': f'AUTO: Deletar - {os.path.basename(name)}',
                'sha': sha,
                'branch': self.github_branch
            }
            
            requests.delete(url, json=data, headers=headers)


class GitHubMediaStorage(GitHubStorage):
    """
    Storage específico para arquivos de mídia (capas de livros, fotos de perfil)
    Usa GitHub como CDN - arquivos são servidos direto do repositório
    """
    def deconstruct(self):
        """
        Permite que o Django serialize este storage em migrations
        """
        return ('books.storage.GitHubMediaStorage', [], {})

