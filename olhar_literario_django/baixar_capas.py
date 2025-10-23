"""
Script para baixar capas de livros clássicos brasileiros
"""
import urllib.request
import os

# Criar pasta images se não existir
os.makedirs('../images', exist_ok=True)

# URLs das capas dos livros (imagens de domínio público ou de sites de livrarias)
capas = {
    'dom-casmurro.jpg': 'https://m.media-amazon.com/images/I/81Jx0sWw1-L._SY466_.jpg',
    'grande-sertao-veredas.jpg': 'https://m.media-amazon.com/images/I/71vJZ5QHPVL._SY466_.jpg',
    'memorias-postumas-de-bras-cubas.jpg': 'https://m.media-amazon.com/images/I/71nXXXN0iZL._SY466_.jpg',
    'o-cortico.jpg': 'https://m.media-amazon.com/images/I/71kBZ3YAPSL._SY466_.jpg',
    'capitaes-da-areia.jpg': 'https://m.media-amazon.com/images/I/81zoR3wr2kL._SY466_.jpg',
    'iracema.jpg': 'https://m.media-amazon.com/images/I/81QlKJPnmUL._SY466_.jpg'
}

print("=" * 60)
print("📚 BAIXANDO CAPAS DE LIVROS CLÁSSICOS")
print("=" * 60)

for filename, url in capas.items():
    filepath = os.path.join('../images', filename)
    
    if os.path.exists(filepath):
        print(f"✅ {filename} - Já existe")
        continue
    
    try:
        print(f"⬇️  Baixando {filename}...")
        urllib.request.urlretrieve(url, filepath)
        print(f"✅ {filename} - Download concluído!")
    except Exception as e:
        print(f"❌ {filename} - Erro: {e}")

print("=" * 60)
print("✅ PROCESSO CONCLUÍDO!")
print("=" * 60)
print("\nArquivos salvos em: ../images/")
print("\nAgora faça:")
print("1. git add images/")
print("2. git commit -m 'ADD: Capas dos livros clássicos'")
print("3. git push origin master")
