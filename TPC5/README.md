# TPC5 - Máquina de Vending

**Aluno:** Salvador Duarte Magalhães Barreto - *A104520*  
![Alt text](https://github.com/R7ptide/EngWeb2025-A104520/blob/main/image.png)

## Descrição  

Este trabalho consiste na implementação de um sistema de interação com uma **máquina de vending**, onde o utilizador pode inserir comandos para visualizar o stock disponível, inserir moedas, comprar produtos ou sair da máquina.  

Para interpretar os comandos inseridos, utilizei um **tokenizer** implementado com a biblioteca **PLY**, que permite processar a entrada linha a linha, identificar tokens válidos e executar ações associadas.

Os principais comandos suportados pela máquina são:
- `LISTAR`: lista todos os produtos disponíveis.
- `MOEDA`: permite inserir múltiplas moedas, separadas por vírgulas, e terminadas com um ponto (`.`).
- `SELECIONAR <CÓDIGO>`: seleciona um produto com base no código.
- `SAIR`: termina a sessão e devolve o troco.

O sistema carrega o stock inicial a partir de um ficheiro `stock.json`, atualiza o estado à medida que os produtos são comprados e guarda o stock novamente ao sair.

## Implementação  

A implementação foi dividida em dois ficheiros principais:

### 1. `tpc5.py` 

Este ficheiro contém a lógica principal da aplicação e é responsável por:
- **Carregar o stock de produtos** a partir do ficheiro `stock.json`.
- **Ler e interpretar os comandos do utilizador** através do `tokenizer`.
- **Gerir o saldo e troco**, permitindo inserção de moedas e cálculo da devolução correta ao utilizador.
- **Executar operações na máquina**, como listar produtos (`LISTAR`), processar a compra de um item (`SELECIONAR <CÓDIGO>`) e encerrar a sessão (`SAIR`).
- **Atualizar o ficheiro `stock.json`** quando um produto é comprado, garantindo que a informação se mantém consistente.

---

### 2. `tokenizer.py` 

Este ficheiro define o **tokenizer** usando a biblioteca `PLY`.  
- **Regras definidas para cada comando**:
  - `LISTAR`
  - `MOEDA` (com valores válidos: `2e`, `1e`, `50c`, `20c`, `10c`, `5c`)
  - `SELECIONAR` seguido de um código (`ex: A01`)
  - `SAIR` para terminar a sessão
- **Ignora espaços em branco e caracteres inválidos**, tornando o reconhecimento mais eficiente.

## Código-Fonte  

O código-fonte pode ser encontrado no seguinte repositório:  

📌 [**Máquina de Vending**](https://github.com/R7ptide/PL2025-A104520/blob/main/TPC5/tpc5.py)  
📌 [**Tokenizer**](https://github.com/R7ptide/PL2025-A104520/blob/main/TPC5/tokenizer.py)  
