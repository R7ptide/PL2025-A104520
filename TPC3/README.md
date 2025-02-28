# TPC3 - Conversor de MarkDown para HTML  

**Aluno:** Salvador Duarte Magalhães Barreto - *A104520*  
![Alt text](https://github.com/R7ptide/EngWeb2025-A104520/blob/main/image.png)

## Descrição  

O objetivo deste trabalho é criar em Python um pequeno conversor de MarkDown para HTML para os elementos descritos na "Basic Syntax" da Cheat Sheet:

1. Cabeçalhos: linhas iniciadas por "# texto", ou "## texto" ou "### texto"
2. Bold: pedaços de texto entre "**"
3. Itálico: pedaços de texto entre "*"
4. Lista numerada
5. Link: [texto](endereço URL)
6. Imagem: ![texto alternativo](path para a imagem)
 

## Implementação  

O código implementa a conversão utilizando expressões regulares para identificar e substituir elementos Markdown pelas suas respetivas representações em HTML. A função principal `markdown_to_html(file)` é responsável por ler um ficheiro Markdown, processá-lo e gerar um ficheiro HTML correspondente.
Para maior parte das conversões utilizei a função `re.sub()` para substituír diretamente os valores do texto.

### Conversão de Cabeçalhos
```
re.sub(r'^###\s+(.+)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
re.sub(r'^##\s+(.+)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
re.sub(r'^#\s+(.+)', r'<h1>\1</h1>', text, flags=re.MULTILINE)
```
As expressões regulares são usadas para identificar e substituir os cabeçalhos `#`, `##` e `###` por seus equivalentes `<h1>`, `<h2>` e `<h3>`. 

A ordem das substituições é importante. Primeiro, processamos os cabeçalhos de nível 3, depois os de nível 2 e, por último, os de nível 1. Isto evita que um cabeçalho `### Título` seja convertido primeiro em `<h1>## Título</h1>`, impedindo a conversão correta para `<h3>Título\</h3>`.
A flag `re.MULTILINE` serve para garantir que cada linha seja analisada separadamente.

### Conversão de texto em negrito e itálico

```
re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
```

Os textos entre `**` são convertidos em `<b>`, e os textos entre `*` são convertidos em `<i>`. O uso de `\1` permite capturar e substituir o conteúdo dentro dos delimitadores Markdown.

### Conversão de imagens e links

```
re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', text)
re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
```

A conversão de imagens é realizada antes da conversão de links porque as imagens seguem a mesma estrutura de parênteses, mas são precedidas por `!`. Se a conversão de links fosse feita primeiro, poderia interferir na conversão correta das imagens.

### Conversão de listas
```
lines = text.split('\n')
    html_lines = []
    in_ol = False
    for line in lines:
        match = re.match(r'^(\d+)\.\s+(.+)', line)
        if match:
            if not in_ol:
                html_lines.append('<ol>')
                in_ol = True
            html_lines.append(f'<li>{match.group(2)}</li>')
        else:
            if in_ol:
                html_lines.append('</ol>')
                in_ol = False
            html_lines.append(line)
    if in_ol:
        html_lines.append('</ol>')
```

Por fim, esta parte do código verifica se a linha corresponde a um item de lista numerada e insere corretamente as tags `<ol>` e `<li>`, garantindo que a estrutura da lista seja mantida. O uso de `match.group(2)` permite extrair apenas o conteúdo da lista sem incluir o número.

A abordagem de iterar pelas linhas uma a uma foi escolhida para evitar que diferentes listas numeradas no Markdown sejam combinadas em um único bloco `<ol>`, garantindo a correta separação entre listas distintas.

## Código-Fonte  

O código-fonte pode ser encontrado no seguinte repositório:  

📌 [**GitHub - TPC3**](https://github.com/R7ptide/PL2025-A104520/blob/main/TPC3/tpc3.py)  
