import sys
import json
import os

from datetime import datetime
from tokenizer import lexer

FILENAME = "stock.json"

def carregar_stock():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_stock(stock):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=4, ensure_ascii=False)


def formatar_saldo(s):
    euros = int(s)
    centimos = round((s - euros) * 100)

    if euros != 0 and centimos != 0.0:
        return f"{euros}e{centimos:02d}c"
    elif euros == 0:
        return f"{centimos:02d}c"
    else:
        return f"{euros}e"
     
     
def calcular_troco(s):
    moedas = [2.0, 1.0, 0.5, 0.2, 0.1, 0.05]
    etiquetas = {
        2.0: "2e",
        1.0: "1e",
        0.5: "50c",
        0.2: "20c",
        0.1: "10c",
        0.05: "5c"
    }

    troco = []
    for moeda in moedas:
        while s >= moeda:
            troco.append(etiquetas[moeda])
            s = round(s - moeda, 2)

    agrupado = {}
    for moeda in troco:
        if moeda in agrupado:
            agrupado[moeda] += 1
        else:
            agrupado[moeda] = 1

    resultado = [(qtd, moeda) for moeda, qtd in agrupado.items()]

    return resultado


def formatar_troco(ltroco):
    troco = [f"{qtd}x {moeda}" for qtd, moeda in ltroco]

    if len(troco) == 0:
        return "maq: Sem troco"
    elif len(troco) == 1:
        return f"maq: Pode retirar o troco: {troco[0]}."
    else:
        return f"maq: Pode retirar o troco: {', '.join(troco[:-1])} e {troco[-1]}."


def interpretar_linha(linha):
    lexer.input(linha)

    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)

    return tokens


def listar(stock):
    print("maq:")
    print(f"{'cod':<5}|{' nome':<22}|{'quantidade ':>12}|{'preço':>7}")
    print("-" * 50)
    for item in stock:
        print(f"{item['cod']:<5}  {item['nome']:<22} {item['quant']:>10} {item['preco']:>7.2f}")
    print("\n")


def selecionar(produtos, cod, s):                
    item = None
    for i in produtos:
        if i["cod"] == cod:
            item = i

    if item is None:
        print("maq: Produto inexistente\n")
    elif item["quant"] == 0:
        print("maq: Produto esgotado\n")
    elif s < item["preco"]:
        print("maq: Saldo insufuciente para satisfazer o seu pedido")
        print(f"maq: Saldo = {formatar_saldo(s)}; Pedido = {formatar_saldo(item["preco"])}\n")
    else:
        s -= item["preco"]
        item["quant"] -= 1
        print(f'maq: Pode retirar o produto dispensado "{item["nome"]}"')
        print(f"maq: Saldo = {formatar_saldo(s)}\n")
    
    return produtos, s


def main():
    data = datetime.today().strftime('%Y-%m-%d')
    stock = carregar_stock()
    saldo = 0.0

    if stock != []:
        print("maq: " + data + ", Stock carregado, Estado atualizado.")
        print("maq: Bom dia. Estou disponível para atender o seu pedido.")
        
        for linha in sys.stdin:
            tokens = interpretar_linha(linha) 
            #for t in tokens:
            #    print(f"{t.type} -> {t.value}")
            if not tokens:
                continue

            cmd = tokens[0].type

            if cmd == 'LISTAR':
                listar(stock)

            elif cmd == 'MOEDA':
                for token in tokens[1:]:
                    if token.type == 'PONTO':
                        break
                    elif token.type == 'VALOR':
                        val = token.value
                        if val.endswith('e'):
                            saldo += int(val[:-1])
                        elif val.endswith('c'):
                            saldo += int(val[:-1]) / 100
                    elif token.type == 'VIRGULA':
                        continue
                    else:
                        print(f"Valor inválido: {token.value}")
                print(f"maq: Saldo = {formatar_saldo(saldo)}\n")
            
            elif cmd == 'SELECIONAR':
                if len(tokens) >= 2 and tokens[1].type == 'CODIGO':
                    cod = tokens[1].value
                    stock, saldo = selecionar(stock, cod, saldo)

            elif cmd == 'SAIR':
                print(formatar_troco(calcular_troco(saldo))) 
                break
    
        guardar_stock(stock)

    else:
        print("maq: " + data + ", Não foi possível carregar Stock, Interrompendo")

    print("maq: Até à próxima")        


if __name__ == "__main__":
    main()
