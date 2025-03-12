# TPC4 - Tokenizer

**Aluno:** Salvador Duarte Magalhães Barreto - *A104520*  
![Alt text](https://github.com/R7ptide/EngWeb2025-A104520/blob/main/image.png)

## Descrição  

O objetivo deste trabalho é implementar um tokenizador que processa uma linguagem de consulta simplificada, inspirada em consultas SPARQL, e identifica os diferentes tokens presentes num texto. O programa utiliza expressões regulares para reconhecer os padrões lexicais e atribui a cada token um tipo, valor, linha e posição no texto original.

## Implementação  

### Especificação dos Tokens
Defini a seguinte lista de tokens:
```
token_specification = [
    ('COMMENT', r'#.*'),
    ('SELECT', r'select'),
    ('WHERE', r'where'),
    ('LIMIT', r'LIMIT'),
    ('VAR', r'\?[a-zA-z]+'),  
    ('IDS', r'[a-z]+:[a-zA-Z]+(\s"[^.]+)?'),
    ('SEP', r'\.'),
    ('LPARENT', r'\{'),
    ('RPARENT', r'\}'),
    ('NUM', r'\d+'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('ERRO', r'.') 
]
```
Cada entrada tem o nome do token e a expressão regular que o identifica. Os principais são:

- `SELECT`, `WHERE`, `LIMIT` – Palavras-chave da linguagem.
- `VAR` – Variáveis iniciadas por `?`.
- `IDS` – Identificadores como `dbo:MusicalArtist`.
- `SEP` – Ponto final de separação (`.`).
- `LPARENT` e `RPARENT` – Chaves `{}`.
- `NUM` – Números.
- `COMMENT`, `SKIP`, `NEWLINE` – Comentários, espaços e novas linhas (ignorados no resultado).
- `ERRO` – Qualquer caracter não reconhecido por outro padrão

### Construção da expressão regular
```
reg = '|'.join([f'(?P<{id}>{expreg})' for id, expreg in token_specification])
```
Aqui estamos a construir uma única expressão regular, a partir da lista `token_specification`.
Cada expressão é envolvida na forma `(?P<NOME>regex)`, o que permite que o Python nomeie o grupo capturado.

### Reconhecimento dos tokens
Para preparar a análise começo por utilizar `re.finditer(reg, code)`, que retorna um iterador com todas as correspondências encontradas no texto. 

Para cada correspondência, utilizo `m.groupdict()` para retornar um dicionário onde só uma chave terá um valor não vazio, indicando qual foi o token reconhecido.

De seguida verifico qual campo do dicionário tem valor, e guardo um tuple com:
- tipo do token
- valor reconhecido 
- linha onde foi encontrado
- posição no texto (m.span() → tuplo com início e fim da correspondência)

Se o token for uma quebra de linha, incrementa o número da linha. Espaços, tabs e comentários são ignorados.



## Código-Fonte  

O código-fonte pode ser encontrado no seguinte repositório:  

📌 [**GitHub - TPC3**](https://github.com/R7ptide/PL2025-A104520/blob/main/TPC4/tpc4.py)  
