import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

class Obra:
    def __init__(self, id, nome, desc, anoCriacao, periodo, compositor, duracao):
        self.id = id
        self.nome = nome
        self.desc = desc
        self.anoCriacao = anoCriacao
        self.periodo = periodo
        self.compositor = compositor 
        self.duracao = duracao
    
    def __str__(self):
        return f"Obra({self.nome} | {self.desc} | {self.anoCriacao} | {self.periodo} | {self.compositor} | {self.duracao} | {self.id})"   


def ler_csv():
    with open("obras.csv", "r", encoding="utf-8") as f:
        next(f)
        linhas = f.readlines()

    dados = {}
    compositores = []
    obras_por_periodo = {}
    buffer = ""

    for linha in linhas:
        aux = linha.strip("\n")
        buffer += aux

        match = re.match(r'^([^;]+);"?((?:[^"]|"{0,3})*)"?;(\d+);([^;]+);([^;]+);(\d{2}:\d{2}:\d{2});(O.*)$', buffer)
        if match:  
            nome = match.group(1)
            desc = match.group(2)
            anoCriacao = match.group(3)
            periodo = match.group(4)
            compositor = match.group(5)
            duracao = match.group(6)
            id = match.group(7)
            obra = Obra(id, nome, desc, anoCriacao, periodo, compositor, duracao)
            
            dados[id] = obra
            compositores.append(compositor)
            if periodo in obras_por_periodo.keys():
                obras_por_periodo[periodo].append(nome)
            else:
                obras_por_periodo[periodo] = [nome]

            buffer = ""

    return dados, compositores, obras_por_periodo



dados, compositores, obras_por_periodo = ler_csv()

print("-" * 80)
print("LISTA ORDENADA DOS COMPOSITORES MUSICAIS")
print("-" * 80)
compositores.sort()
print("\n".join(compositores))
print("\n")

print("-" * 80)
print("DISTRIBUIÇÃO DAS OBRAS POR PERÍODO")
print("-" * 80)
for periodo, obras in obras_por_periodo.items():
    print(f"▶ Período: {periodo} | Nº de obras: {len(obras)}")
print("\n")

print("-" * 80)
print("OBRAS ORGANIZADAS POR PERÍODO")
print("-" * 80)
for periodo, obras in obras_por_periodo.items():
    obras.sort()
    print(f"▶ Período: {periodo}")
    print("\n".join(obras))
    print("-" * 80)
