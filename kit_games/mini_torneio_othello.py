import os
import time
import importlib
import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom

import advsearch.timer as timer

from server import Server

# teste do agente minimax contra o jogador random
torneio = [
    {"nome": "Contagem de peças", 
    "path": "advsearch/your_agent/othello_minimax_count.py", 
    "vitorias": 0},
    {"nome": "Valor posicional", 
    "path": "advsearch/your_agent/othello_minimax_mask.py", 
    "vitorias": 0},
    {"nome": "Heurística customizada", 
    "path": "advsearch/your_agent/othello_minimax_custom.py", 
    "vitorias": 0},
    {"nome": "MCTS", 
    "path": "advsearch/your_agent/mcts.py", 
    "vitorias": 0}
]
historico = []
# valor de diferentes heuristicas
n = len(torneio)
print("---- Torneio -----")
for i in range(n):
    for j in range(n):
        if i != j:
            h1 = torneio[i]
            h2 = torneio[j]
            print("Jogo atual:")
            nome1 = h1["nome"]
            nome2 = h2["nome"]
            print(f"{nome1} X {nome2}")
            p1 = h1["path"]
            p2 = h2["path"]
            s = Server("othello", p1, p2, 5, "historia.txt", "output.txt", 0)
            s.run()
            if s.result == 0:
                print(f"Vitória da heurística: {nome1}")
                historico.append(f"Vitória da heurística: {nome1} sobre a heurísitca {nome2}")
                h1["vitorias"] += 1 
            elif s.result == 1:
                print(f"Vitória da heurística: {nome2}")
                historico.append(f"Vitória da heurística: {nome2} sobre a heurísitca {nome1}")
                h2["vitorias"] += 1
            else:
                print("Empate")
print("----- Estatísticas ------")
for i in range(n):
    nome = torneio[i]["nome"]
    vitorias = torneio[i]["vitorias"]
    print(f"Vezes que a heurística {nome} ganhou: {vitorias}")
for hist in historico:
    print(hist)