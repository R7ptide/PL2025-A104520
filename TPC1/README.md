# TPC1 - Somador On/Off  

**Aluno:** Salvador Duarte Magalhães Barreto - *A104520*  
![Alt text](https://github.com/R7ptide/PL2025-A104520/blob/main/image.png)

## Descrição  

O objetivo deste trabalho é criar um programa que some todas as sequências de dígitos encontradas num texto.  
O programa segue as seguintes regras:  

- Sempre que encontrar a string `"Off"`, este comportamento é desativado.  
- Sempre que encontrar a string `"On"`, este comportamento é ativado novamente.  
- Sempre que encontrar o caractere `"="`, o resultado da soma atual é exibido na saída.  

## Implementação  

Para resolver o problema, utilizei um ciclo `while` para percorrer o texto caracter a caracter.  

1. Sempre que encontro um **dígito**, adiciono-o a um acumulador.  
2. Quando encontro um caractere que **não seja um dígito**, verifico se a flag `on` está ativa:  
   - Se estiver ativa, converto o valor acumulado para número e somo ao resultado, depois reseto o acumulador.  
3. Caso encontre a string `"On"`, **ativo a flag**; se encontrar `"Off"`, **desativo-a**.  
4. Se encontrar o caractere `"="`, **imprimo o valor da soma atual**.  
5. No final do ciclo, verifico se restou algum número no acumulador e, se a flag estiver ativa, adiciono-o ao resultado.  

## Código-Fonte  

O código-fonte pode ser encontrado no seguinte repositório:  

📌 [**GitHub - TPC1**](https://github.com/R7ptide/PL2025-A104520/blob/main/TPC1/tpc1.py)  

---

### 🔹 Exemplo de Entrada e Saída  

#### **Entrada:**  
"ola 10 on 2025-02-06 Off 30 on asadsasd40sdfsdf = Off 50 60 = On 70 ="
#### **Saída:**
2083
2083 
2153

