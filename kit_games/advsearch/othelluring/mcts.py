import random
import math
import time
from typing import Tuple

EVAL_TEMPLATE = [
    [100, -30, 6, 2, 2, 6, -30, 100],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [100, -30, 6, 2, 2, 6, -30, 100]
]

def evaluate_mask(state, player:str) -> float:

    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on the positional value of the pieces.
    You must use the EVAL_TEMPLATE above to compute the positional value of the pieces.
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """

    LINHAS_TABULEIRO = COLUNAS_TABULEIRO = 8
    opponent = 'W' if player == 'B' else 'B'
    
    # Calcular valor posicional do jogador
    valor_posicional = 0
    # String alterada para analise
    tabuleiro_str = state.get_board().__str__().replace('\n', '')
    
    for linha in range(LINHAS_TABULEIRO):
        for coluna in range(COLUNAS_TABULEIRO):
            peca = tabuleiro_str[linha * LINHAS_TABULEIRO + coluna]
            if peca == player:
                valor_posicional += EVAL_TEMPLATE[linha][coluna]
            elif peca == opponent:
                valor_posicional -= EVAL_TEMPLATE[linha][coluna]
                
    return float(valor_posicional)


def make_move(state, tempo_limite=0.5) -> Tuple[int, int]:
    melhor_jogada = mcts_search(state, tempo_limite)
    
    if melhor_jogada is not None:
        x, y = melhor_jogada
        return (int(x), int(y))
    else:
        jogadas_legais = list(state.legal_moves())
        if jogadas_legais:
            x, y = jogadas_legais[0]
            return (int(x), int(y))
        return (-1, -1)


def mcts_search(initial_state, tempo_limite=4.5):
    start_time = time.time()
    root_node = MCTSNode(initial_state)
    
    cor = initial_state.player

    while time.time() - start_time < tempo_limite:
        node = root_node
        
        # 1. SELECT
        while not node.state.is_terminal() and node.is_fully_expanded():
            node = node.best_child()

        # 2. EXPAND
        if not node.state.is_terminal() and not node.is_fully_expanded():
            move = random.choice(node.untried_moves)
            node.untried_moves.remove(move)
            next_state = node.state.next_state(move)
            child_node = MCTSNode(next_state, parent=node, move_from_parent=move)
            node.children.append(child_node)
            node = child_node 

        # 3. SIMULATION
        sim_state = node.state.copy()
        profundidade = 0
        
        while not sim_state.is_terminal() and profundidade < 7:
            possible_moves = list(sim_state.legal_moves())
            move = random.choice(possible_moves)
            sim_state = sim_state.next_state(move)
            profundidade += 1

        # 4. BACKPROPAGADE
        if sim_state.is_terminal():
            winner = sim_state.winner() 
            # Empate ou sem vencedor válido ganha 0.5
            pontuacao_final = 1.0 if winner == cor else (0.5 if (winner == 'Draw' or winner is None) else 0.0)
        else:
            valor_mascara = evaluate_mask(sim_state, cor)
            # Normaliza para uma probabilidade de vitória entre 0 e 1
            pontuacao_final = 1.0 / (1.0 + math.exp(-valor_mascara / 50.0))
        
        # Propaga a pontuação de volta pela árvore
        while node is not None:
            node.visits += 1
            if node.parent is not None:
                jogador_que_fez_a_jogada = node.parent.state.player
                
                if cor == jogador_que_fez_a_jogada:
                    node.wins += pontuacao_final 
                else:
                    node.wins += (1.0 - pontuacao_final) 
                    
            node = node.parent

    best_final_child = max(root_node.children, key=lambda c: c.visits)
    return best_final_child.move_from_parent


class MCTSNode:
    __slots__ = ['state', 'parent', 'move_from_parent', 'children', 'untried_moves', 'visits', 'wins']

    def __init__(self, state, parent=None, move_from_parent=None):
        self.state = state
        self.parent = parent
        self.move_from_parent = move_from_parent
        self.children = []
        self.visits = 0
        self.wins = 0.0
        
        if not state.is_terminal():
            self.untried_moves = list(state.legal_moves()) 
        else:
            self.untried_moves = []

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c_param=1.41):
        best_score = -float('inf')
        best_node = None
        
        for child in self.children:
            exploit = child.wins / child.visits
            explore = math.sqrt(2.0 * math.log(self.visits) / child.visits)
            score = exploit + c_param * explore
            
            if score > best_score:
                best_score = score
                best_node = child
                
        return best_node