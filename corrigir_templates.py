import os
import glob

# Diretório dos templates
templates_dir = 'olhar_literario_django/templates'

# Processar cada arquivo HTML
for filepath in glob.glob(os.path.join(templates_dir, '*.html')):
    filename = os.path.basename(filepath)
    print(f"Processando: {filename}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remover barras de escape e corrigir sintaxe
    content = content.replace(r"{% static \'", '{% static "')
    content = content.replace(r"\' %}", '" %}')
    
    # Salvar arquivo
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ {filename} corrigido")

print("\n✅ Todos os templates corrigidos!")
