# TPC2 - Análise de um dataset de obras musicais  

**Aluno:** Salvador Duarte Magalhães Barreto - *A104520*  
![Alt text](https://github.com/R7ptide/EngWeb2025-A104520/blob/main/image.png)

## Descrição  

O objetivo deste trabalho é ler e processar um dataset, **sem utilizar** o módulo CSV do Python, e criar os seguintes resultados:  

1. Lista ordenada alfabeticamente dos compositores musicais;
2. Distribuição das obras por período: quantas obras catalogadas em cada período;
3. Dicionário em que a cada período está a associada uma lista alfabética dos títulos das obras
desse período.
 

## Implementação  

Para implementar este trabalho, desenvolvi a função `ler_csv()`, que percorre cada linha do ficheiro, extrai os campos relevantes utilizando expressões regulares (regex) e organiza os dados em diferentes estruturas para facilitar a análise.  

### **Leitura do ficheiro CSV**  

O ficheiro `obras.csv` é lido linha por linha, ignorando a primeira linha (cabeçalho). Os dados são armazenados num buffer para lidar corretamente com possíveis quebras de linha ('\n').  

### **Expressão Regular Utilizada**  

Para extrair os campos do CSV, foi utilizada a seguinte expressão regular:  

```
^([^;]+);"?((?:[^"]|"{0,2})*)"?;(\d+);([^;]+);([^;]+);(\d{2}:\d{2}:\d{2});(O.*)$
```

Esta regex tem como objetivo capturar corretamente as diferentes entradas do ficheiro CSV, para utilizei grupos para os diferentes campos. Analisando por partes:

- `^([^;]+);` → Captura o primeiro campo (nome da obra), usando uma classe que exclui o caracter ';'.
- `"?((?:[^"]|"{0,2})*)"?;` → Captura o segundo campo (descrição da obra), que pode estar entre aspas.
    - `"?` → Permite que a descrição possa ou não começar com aspas.
    - `(?:[^"]|"{0,3})*` → Permite caracteres normais ou aspas ("), garantindo que uma citação dentro do campo seja capturada corretamente.
        - `?:` →  Serve para agrupar os elementos seguintes sem os armazenar separadamente.
        - `[^"]` → Captura qualquer caracter que não seja uma aspa. 
        - `"{0,3}` → Captura quaquer sequência de até 3 aspas que possam surgir dentro da descrição.
    - `"?` → Permite que a descrição possa ou não terminar com aspas.
- `(\d+);` → Captura o ano de criação da obra.
- `([^;]+);` → Captura o período da obra (por exemplo, "Barroco", "Romantismo").
- `([^;]+);` → Captura o nome do compositor.
- `(\d{2}:\d{2}:\d{2});` → Captura a duração da obra no formato hh:mm:ss.
- `(O.*)$` → Captura o identificador único da obra, que começa sempre com "O" e é o último campo da linha.

A cada iteração, quando a regex encontra uma correspondência válida, os dados são extraídos e armazenados nas respetivas estruturas de dados.

>**Observação:** A classe 'Obra' foi apenas criada para debugging e testes sobre a obtenção e distrubuição correta dos dados 

### Estruturas de Dados Utilizadas

Após a extração dos campos, os dados são organizados nas seguintes estruturas:

- **dados** (dict): Dicionário onde cada chave é o identificador da obra (id), e o valor é um objeto da classe Obra (usado apenas para debugging).
- **compositores** (list): Lista de compositores encontrados no dataset.
- **obras_por_periodo** (dict): Dicionário onde a chave é o período e o valor é uma lista de nomes das obras pertencentes a esse período.

### Geração dos Resultados

Após a leitura e estruturação dos dados, são gerados três tipos de saída:

1. **Lista ordenada dos compositores:**
    - A lista de compositores é ordenada alfabeticamente, utilizando a função `sort()`, e é impressa no terminal .

2. **Distribuição das obras por período:**
    - Para cada período musical, é apresentado o número de obras associadas, utilizando o dicionário `obras_por_periodo` e a função `len()` aplicada à lista de cada período, para calcular a quantidade de obras por período.

3. **Obras organizadas por período:**
    - As obras são agrupadas por período e ordenadas alfabeticamente dentro de cada grupo, utilizando novamente a função `sort`.


## Código-Fonte  

O código-fonte pode ser encontrado no seguinte repositório:  

📌 [**GitHub - TPC2**](https://github.com/R7ptide/PL2025-A104520/blob/main/TPC2/tpc2.py)  
