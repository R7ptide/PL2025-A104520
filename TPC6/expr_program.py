from expr_anasin import rec_Parser

while True:
    linha = input("Expressão> ")
    result = rec_Parser(linha)
    
    print("Resultado:", result)
   