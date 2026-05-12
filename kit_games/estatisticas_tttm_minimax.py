import os
import time
import importlib
import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom

import advsearch.timer as timer

from server import Server

# teste do agente minimax contra o jogador random
# faremos 100 testes e veremos o resultado
n = 100
vitorias_minimax = 0
vitorias_random = 0
empates = 0
p1 = "advsearch/your_agent/tttm_minimax.py"
p2 = "advsearch/randomplayer/agent.py"
for i in range(n):
    s = Server("tttm", p1, p2, 5, "historia.txt", "output.txt", 0)
    s.run()
    if s.result == 0:
        vitorias_minimax += 1
    elif s.result == 1:
        vitorias_random += 1 
    else:
        empates += 1

# teste do agente minimax contra outro minimax
# faremos 100 testes e veremos o resultado
vitorias_minimax1 = 0
vitorias_minimax2 = 0
empates2 = 0
p1 = "advsearch/your_agent/tttm_minimax.py"
p2 = "advsearch/your_agent/tttm_minimax.py"
for i in range(n):
    s = Server("tttm", p1, p2, 5, "historia.txt", "output.txt", 0)
    s.run()
    if s.result == 0:
        vitorias_minimax1 += 1
    elif s.result == 1:
        vitorias_minimax2 += 1 
    else:
        empates2 += 1
print("\nTeste de agente minimax versus agente aleatório")
print("---------- Estatísticas -----------")
print("Vezes que o algortimo minimax ganhou: ", vitorias_minimax)
print("Vezes que o agente aleatório ganhou: ", vitorias_random)
print("Vezes que os dois empataram: ", empates)

print("\nTeste de agente minimax versus agente minimax")
print("---------- Estatísticas -----------")
print("Vezes que o algortimo minimax ganhou: ", vitorias_minimax1)
print("Vezes que o agente aleatório ganhou: ", vitorias_minimax2)
print("Vezes que os dois empataram: ", empates2)