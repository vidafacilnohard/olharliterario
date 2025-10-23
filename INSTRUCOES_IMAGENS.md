# 📸 Instruções para Adicionar Capas de Livros

## Como funciona o sistema de capas:

O site busca automaticamente capas com base no **nome do livro**. 

### Regra de nomenclatura:

O sistema converte o título do livro para um nome de arquivo:
- Remove acentos
- Remove caracteres especiais  
- Converte para minúsculas
- Substitui espaços por hífens

### Exemplos:

| Título do Livro | Nome do Arquivo |
|----------------|-----------------|
| Dom Casmurro | `dom-casmurro.jpg` |
| Grande Sertão: Veredas | `grande-sertao-veredas.jpg` |
| Memórias Póstumas de Brás Cubas | `memorias-postumas-de-bras-cubas.jpg` |
| O Cortiço | `o-cortico.jpg` |
| Capitães da Areia | `capitaes-da-areia.jpg` |
| Iracema | `iracema.jpg` |

## Como adicionar capas:

### Opção 1: Salvar imagens na pasta images/

1. Baixe a capa do livro da internet
2. Renomeie o arquivo seguindo a regra acima
3. Coloque na pasta `images/`
4. Pronto! O sistema encontra automaticamente

### Opção 2: Fazer upload no Django Admin

1. Acesse: https://olharliterario-production.up.railway.app/admin
2. Edite o livro
3. Faça upload no campo "Capa"
4. Salve

## Onde encontrar capas:

- **Amazon**: https://www.amazon.com.br/
- **Google Images**: busque por "capa do livro [nome]"
- **Skoob**: https://www.skoob.com.br/
- **Livraria Cultura**: https://www.livrariacultura.com.br/

## Formato recomendado:

- **Tipo**: JPG ou PNG
- **Proporção**: Vertical (ex: 300x450px)
- **Tamanho**: Menos de 500KB

---

**Nota**: Se não encontrar uma capa, não se preocupe! O sistema mostra automaticamente um placeholder bonito com o nome do livro. 🎨
