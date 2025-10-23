import os
import re

# Diretório dos templates
templates_dir = 'olhar_literario_django/templates'

# Padrões de substituição
replacements = [
    (r'href="style\.css"', r'href="{% static \'style.css\' %}"'),
    (r'src="script\.js"', r'src="{% static \'script.js\' %}"'),
    (r'src="logo\.png"', r'src="{% static \'logo.png\' %}"'),
]

# Processar cada arquivo HTML
for filename in os.listdir(templates_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(templates_dir, filename)
        print(f"Processando: {filename}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar {% load static %} no início se não existir
        if '{% load static %}' not in content:
            content = '{% load static %}\n' + content
        
        # Aplicar substituições
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Salvar arquivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ {filename} atualizado")

print("\n✅ Todos os templates atualizados!")
