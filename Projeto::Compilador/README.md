# PL-Trabalho-Prático
 - Marco Soares Gonçalves - A104614 
 - Salvador Duarte Magalhães Barreto - A104520

## Índice
- [Introdução](#introdução)
- [Decisões tomadas para a análise léxica](#decisões-tomadas-para-a-análise-léxica)
- [Símbolos literais e Identificadores](#símbolos-literais-e-identificadores)
  - [Delimitadores e pontuação](#delimitadores-e-pontuação)
  - [Operadores de comparação](#operadores-de-comparação)
  - [Operadores](#operadores)
  - [Palavras de estrutura em Pascal](#palavras-de-estrutura-em-pascal)
  - [Tipos de dados](#tipos-de-dados)
  - [Estruturas de controlo](#estruturas-de-controlo)
  - [Funções de I/O e funções auxiliares](#funções-de-io-e-funções-auxiliares)
  - [Comentários](#comentários)
- [Tokenizer](#tokenizer)
  - [Utilização](#utilização)

## Introdução

O projeto desenvolvido é um compilador da linguagem Pascal para a máquina virtual disponível em [https://ewvm.epl.di.uminho.pt](https://ewvm.epl.di.uminho.pt). 

Este projeto está dividido em duas componentes principais, sendo estas :

- **Tokenizer**: Responsável por converter o código pascal em uma sequência de tokens.
- **Analyser**: Gera o código a ser executado na máquina virtual.

Devido ao nosso mau planeamento inicial das tarefas, acabamos por demorar mais do que o esperado, pelo que não conseguimos implementar as functions, ainda que, tenhamos desenvolvido o código VM que corresponde ao **exemplo 7** fornecido no enunciado do projeto.

No que diz respeito às funcionalidades implementadas, o nosso projeto fornece suporte para:

- **Tipos de dados**: Inteiros, Booleanos, Reais, Strings e Arrays;
- **Estruturas de controlo**: If-Then-Else, While-Do, For-To e For-Downto;
- **Funções input/output**: write, writeln, readln;
- **Operações**: Aritméticas, lógicas e comparações;
- **Outras funções** : A única outra função implementada foi a length.

Para além disso, criamos um ficheiro "gramatica.txt" que contém a gramática BNF utilizada para desenvolver o analisador sintático. 

## Decisões tomadas para a análise léxica

Antes de começarmos a implementação do tokenizer tomamos decisões relativamente à categorização dos diversos tokens a identificar.

### Símbolos literais e Identificadores

- **ID**: Usado para identificar nomes de variáveis e o próprio nome do programa;
- **NUMBER**: Usado para categorizar todos os números;
- **FRASE**: Estes tokens representam as strings que vêm dentro de aspas. Em um excerto de código `writeln("Hello World")` o token FRASE iria representar "Hello World".

### Delimitadores e pontuação
- **LPARENT/RPARENT**: Usados para identificar `(` e `)` respetivamente;
- **LBRACKET/RBRACKET**: Usados para identificar `{` e `}`, respetivamente;
- **SEMICOLON, DOT, COLON, COMMA**: Representam, os símbolos `;`, `.`, `:` e `,` respetivamente, sendo que cada um tem o seu nome associados diretamente ao símbolo que representam.
- **RANGE**: Representa `..` usado nas declarações de arrays.

### Operadores de comparação
- **EQUALS, GREATER, GE, LESSE, LE, NOTEQUAL**: Representam, os símbolos `=`, `>`, `>=`, `<`, `<=` e `<>` respetivamente.

### Opeadores  
- **TIMES, DIV, DIVIDE, MOD, PLUS, MINUS, AND, OR, NOT**: Usados para identificar os respetivos símbolos, `*`, `div`, `/`, `mod`(resto da divisão), `+`, `-`,`and`, `or` e `not`. 

### Palavras de estrutura em Pascal
- **PROGRAM**: Identifica o símbolo `program`, que em Pascal representa o início do programa;
- **VAR**: Identifica o símbolo `var`, que em Pascal é usado sempre que se declara variáveis;
- **BEGIN/END**: Identificam os símbolos `begin` e `end`, respetivamente e em Pascal estes delimitam blocos de código;
- **FUNCTION**: Identifica o símbolo `function`, que em Pascal é usado para declarar uma função.

### Tipos de dados
- **INTEGER, REAL, BOOLEAN, STRING**: Representam os tipos de dados básicos, que possuem o mesmo nome;
- **ARRAY, OF**: Identificam os símbolos `array`e `of`, respetivamente, que são usados para definir arrays (`array[1..10] of integer`).

### Estruturas de controlo
- **IF, THEN, ELSE**: Identificam os símbolos `if`, `then` e `else`, respetivamente, que são usados em instruções condicionais;
- **FOR, TO, DOWNTO, DO**: Identificam os símbolos `for`, `to`, `downto` e `do`, respetivamente, que são usados em ciclos do tipo for;
- **WHILE, DO**: Identificam os símbolos `while` e `do`, respetivamente que são usados em ciclos do tipo while.

### Funções de I/O e funções auxiliares
- **WRITE/WRITELN**: Identificam as instruções output com o mesmo nome;
- **READLN**: Identifica a instrução de input de mesmo nome;
- **LENGTH**: Identifica o símbolo `length`, que representa a função que retorna o tamanho de uma string ou array. 

### Comentários
- **COMMENT**: Identifica os comentários que seguem a seguinte estrutura `{ ... }`. Estes vão ser ignorados durante a execução.

## Tokenizer

Como já foi mencionado anteriormente, o tokenizer tem a função de converter o código pascal em uma sequência de tokens. Para desenvolvermos este componente recorremos à biblioteca **"Ply.lex"**, tal como era pretendido. A implementação segue a seguinte estrutura:

- **Expressões regulares simples**: Para tokens de delimitação e pontuação e para os vários operadores. Para além disso também capturam o **ID** (ex: `t_LPARENT = r'\('`) 

- **Funções específicas**: Usadas para tokens que têm precedência sobre identificadores genéricos

O tokenizer foi configurado com a flag `re.IGNORECASE`, por forma a que seja indiferente a maiúsculas e minúsculas, o que é essencial para a linguagem Pascal onde as palavras podem ser escritas em qualquer combinação das duas (ex: `BEGIN`, `begin`, `Begin`).

Para evitar conflitos entre palavras reservadas e identificadores, utilizamos funções específicas para cada palavra reservada (ex: `def t_PROGRAM(t):`). Esta abordagem garante que palavras como "program" sejam reconhecidas como tokens específicos e não como identificadores genéricos.

**Exemplos de precedência implementados:**
- `writeln` deve ser reconhecido antes de `write`
- `downto` deve ser reconhecido antes de `to`
- `>=`, `<=` e `<>` devem ser reconhecidos antes de `>` e `<`

Os comentários entre chavetas `{...}` são reconhecidos mas ignorados.

### Utilização

O tokenizer pode ser executado independentemente através da linha de comando:

```bash
python3 tokenizer.py <arquivo.pas>
```
Obtendo o seguinte output:
```bash
=== Tokens encontrados no arquivo: testes/teste1.pas ===

LexToken(PROGRAM, 'program', 1, 0)
LexToken(ID, 'HelloWorld', 1, 8)
LexToken(SEMICOLON, ';', 1, 18)
LexToken(BEGIN, 'begin', 2, 20)
LexToken(WRITELN, 'writeln', 3, 30)
LexToken(LPARENT, '(', 3, 37)
LexToken(FRASE, ''Ola, Mundo!'', 3, 38)
LexToken(RPARENT, ')', 3, 51)
LexToken(SEMICOLON, ';', 3, 52)
LexToken(END, 'end', 4, 54)
LexToken(DOT, '.', 4, 57)
```

## Decisões para a a análise sintática

Inicialmente guiamo-nos pelos exemplos pascal fornecidos no enunciado, traduzindo-os diretamente para o código VM. Com isto feito, começamos a definir a gramática (gramatica.txt) para o nosso analyzer, guiando-nos exemplo a exemplo. No entanto, esta abordagem provou-se ineficiente, visto que à medida que fomos avançando nos exemplos fornecidos, muita da gramática que previamente estava correta tinha de ser atualizada ou até mesmo reescrita. Estas várias atualizações e reescritas consumiram muito tempo e são aquilo que consideramos nos ter impedido de implementar as funcionalidades opcionais "function" e "procedure".

## Abordagens utilizadas no analisador sintático

Estas abordagens são diretamente baseadas na gramática definida no ficheiro, e como tal, a estrutura do código reflete as regras definidas nessa gramática.

### Variáveis

A abordagem que consideramos mais pertinente no que toca à declaração de variáveis é a sua alocação à priori, ou seja, a reserva do seu espaço na stack mal estas apareçam. Deste modo, conseguimos ter uma separação da lógica do programa e das declarações necessárias ao seu funcionamento. Para garantir o seu bom funcionamento recorremos às seguintes variáveis globais:

- **tabela_de_simbolos** : Um dicionário que associa a cada variável o seu tipo e posição na stack;
- **next_index** : Um contador auxiliar utilizado apenas durante o processo de declaração de variáveis, para saber qual a próxima posição da stack;

No que diz respeito aos diferentes tipos de variáveis, seguimos as seguintes abordagens:

- **Inteiros/Reais** : Estes são tratados da forma habitual, sendo que a sua declaração é feita através de um simples `PUSHI` e `PUSHF`, respetivamente;
- **Booleanos** : Estes são tratados como inteiros `1` ou `0`, que representam respetivamente, `true` e `false`.
- **Arrays** : Estes foram implementados recorrendo à  `struct heap`. O seu espaço é imediatamente alocado na dita heap através do comando `ALOC n`. O acesso aos seus elementos é feito através das instruções `LOADN` e `STOREN`. Os índices são ajustados de base 1 (Pascal) para base 0 (VM) através da operação subtração de 1. 
- **Strings** : As são tratadas como sendo arrays de caracteres,com uma implementação mais complexa que utiliza um **apontador** para o espaço alocado na heap e requer três variáveis auxiliares: O **valor** da string original, um **iterador** para percorrer a string durante o seu preenchimento e finalmente o seu **tamanho** . Cada caractere é armazenado através do seu código ASCII, utilizando a instrução `CHARAT`.

### Lógica do programa

No que diz respeito à lógica do programa, utilizamos contadores globais (**if_counter**,**for_counter** e **while_counter**) para o controlo de fluxo das estruturas `if`,`for` e `while`, assim cada um gera um **bloco** com o seu próprio identificador, evitando que existam conflitos de blocos. 

Ainda no controlo de fluxo, não podemos deixar de mencionar aquele que foi o problema que mais dificulades nos trouxe: O **Dangling-else**. Este ocorre quando o analisador não consegue determinar a que bloco if pertence o else, resultando em conflitos **shift/reduce**. Para resolver este problema guiámo-nos por uma solução que encontramos [online](http://www.parsifalsoft.com/ifelse.html). Através da distinção entre **open-statements** e **close-statements**, garantimos que cada bloco else esteja associado ao bloco if mais próximo, resolvendo assim a causa dos conflitos.

No que toca às **expressões aritméticas e lógicas**, optamos por definir explicitamente uma hierarquia de operadores, de modo a respeitar ordem das operações do Pascal.

A implementação do comando `readln` precisou de um tratamento especial, devido ao facto de serem tratadas como arrays. O tratamento aplicado foi:
1. Ler a string com o `READ` e coloca-la na variável auxiliar(**valor**) mencionada anteriormente. 
2. Calcular o seu tamanho com o `STRLEN` e guarda-la na variável (**tamanho**) mencionada anteriormente.
3. Alocar o espaço pertendido na sruct heap, usando `ALLOCN` e o tamanho calculado antes.
4. Percorrer a string original, caracter a caracter, e armazenando na heap o seu valor ASCII, utilizando a variável auxiliar **iterador** mencionada anteriormente.

Sobre funções nativas ao pascal, apenas implementamos a `length`.

## Testes

Para validar a funcionalidade do nosso compilador, desenvolvemos testes que incluem tanto os exemplos fornecidos no enunciado quanto testes adicionais criados por nós.

### Testes de Erro Propositais
- **teste9.pas**: Programa incompleto (sem `begin...end`) -  Erro sintático esperado
- **teste10.pas**: Programa com variáveis não declaradas -  Erro semântico esperado

### Testes de Funcionalidades Específicas

- **teste8.pas**: Teste de `if...else if..else` : Validou a resolução do **Dangling-else**

- **teste11.pas**: Teste de `write(array[indice])` : Validou a funcionalidade de escrita de elementos de array
  
- **teste12.pas**: Manipulação de strings com `length()` : Validou operações com strings e contagem de caracteres
  
- **teste13.pas**: Simulação de matriz 3x3 : Verificou a manipulação de índices em arrays unidimensionais
  
- **teste14.pas**: Ciclos `for-to` e `for-downto` : Validou ambas as direções de ciclos for e estruturas while

- **teste15.pas e teste16.pas**: Testes que contêm um pouco de tudo

### Metodologia de Teste

Para cada teste, seguimos o seguinte processo:

1. **Compilação**: `python3 analizer.py testes/testeX.pas`, o resultado é gerado na pasta `codigo_vm` com o nome `testeX_result.txt`  
2. **Verificação**: Confirmação da geração do código VM correspondente
3. **Análise**: Revisão do código VM gerado para validar a correção da tradução


## Conclusão

Conseguimos implementar um compilador pascal funcional, que realiza a análise léxica e sintática de programas simples. Ainda que não tenhamos dado especial atenção à eficiência do código VM gerado, consideramos que a utilização da struct heap para strings e arrays é um ponto positivo no que toca a conseguir programas mais eficientes. Embora o nosso planeamento inicial se tenha provado muito ineficiente, acreditamos que o trabalho reflete um esforço significativo por ambas as partes do grupo em compreender a gramática da linguagem, na resolução de problemas como o Dangling-else e na utilização da gramática BNF estudada ao longo deste semestre.
