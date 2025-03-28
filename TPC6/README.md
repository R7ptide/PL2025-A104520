# TPC6 - Recursivo Descendente para expressões aritméticas

**Aluno:** Salvador Duarte Magalhães Barreto - *A104520*  
![Alt text](https://github.com/R7ptide/EngWeb2025-A104520/blob/main/image.png)

## Descrição  

Este trabalho consiste em criar um parser LL(1) recursivo descendente que reconheça expressões aritméticas e calcule o respetivo valor.

Exemplos de algumas frases:

```2+3
67-(2+3*4)
(9-2)*(13-4)
```

## Implementação
A gramática que desenvolvi segue a seguinte estrutura:
```
Exp  -> Termo Exp2
Exp2 -> "+" Termo Exp 
      | "-" Termo Exp 
      | ε
Termo -> Fator Termo2
Termo2 -> "*" Fator Termo 
        | "/" Fator Termo
        | ε
Fator -> "(" Exp ")"
       | num
```  

A implementação está dividida em três ficheiros:

### 1. Analisador Léxico (`expr_analex.py`)

O analisador léxico utiliza a biblioteca `ply.lex` para identificar os tokens que compõem as expressões aritméticas. Os tokens suportados são:

- Parênteses `(` e `)`
- Operadores `+`, `-`, `*` e `/`
- Números inteiros

O lexer também ignora espaços e tabulações e identifica erros léxicos.

### 2. Analisador Sintático (`expr_anasin.py`)

O analisador sintático implementa um parser recursivo descendente baseado na gramática definida. A função principal `rec_Parser()` recebe uma expressão, analisa-a recursivamente e devolve o resultado da sua avaliação.

As principais funções do parser incluem:

- `rec_Expr()`: Trata expressões e operadores `+` e `-`
- `rec_Termo()`: Trata termos e operadores `*` e `/`
- `rec_Fator()`: Trata números e expressões entre parênteses

### 3. Programa Principal (`expr_program.py`)

O programa principal executa um loop interativo onde o utilizador pode inserir expressões aritméticas, que são analisadas e calculadas pelo parser. O resultado da expressão é então apresentado no ecrã.

### Exemplo de execução
```
Expressão> (3+5)*2
Resultado: 16
```

## Código-Fonte  

O código-fonte pode ser encontrado no seguinte repositório:  

📌 [**Lexer**](https://github.com/R7ptide/PL2025-A104520/blob/main/TPC6/expr_analex.py)  
📌 [**Parser**](https://github.com/R7ptide/PL2025-A104520/blob/main/TPC6/expr_anasin.py)  
📌 [**Program**](https://github.com/R7ptide/PL2025-A104520/blob/main/TPC6/expr_program.py)  
