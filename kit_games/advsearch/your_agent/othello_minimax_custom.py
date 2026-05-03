import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move
from .othello_minimax_mask import evaluate_mask

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

# So pode usar nos cantos
def pecas_estaveis(board, player):
    n = len(board.tiles[0])
    tiles = board.tiles
    bordas = (
        [(0, c)   for c in range(n)] +
        [(n-1, c) for c in range(n)] +
        [(r, 0)   for r in range(1, n-1)] +
        [(r, n-1) for r in range(1, n-1)]
    )

    num_estaveis = 0
    # Para cada borda
    for pos in bordas:
        lin, col = pos 
        if tiles[lin][col] == '.':
            continue
        # Em cada direcao
        for direcao in board.DIRECTIONS:
            # Verificar peca
            verifica = [lin, col]
            while True:
                verifica[0] += direcao[0]
                verifica[1] += direcao[1]
                # chegou na extremidade = estavel
                if not board.is_within_bounds(verifica):
                    break 
                 # encontrou adversário ou vazio antes = instavel
                if tiles[verifica[0]][verifica[1]] != player:
                    num_estaveis += 1
    return num_estaveis

# Retorna a quantidade de movimentos possiveis do jogador menos
# a quantidade de movimentos possiveis do oponente
def mobilidade(state):
    movimentos_jogador = len(state.legal_moves())
    state.player = state.get_board().opponent(state.player)
    movimentos_oponente = len(state.legal_moves())
    state.player = state.get_board().opponent(state.player)
    return movimentos_jogador - movimentos_oponente

# Retorna a quantidade de cantos dominados pelo jogador
def cantos_dominados(board, player):
    n = len(board.tiles[0])
    tiles = board.tiles

    bordas = (
        [(0, n-1)] +
        [(n-1, 0)] +
        [(0, 0)] +
        [(n-1, n-1)]
    )
    qtd_cantos = 0
    for i in bordas:
        if tiles[i[0]][i[1]] == player:
            qtd_cantos += 1
    return qtd_cantos

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada 
    # Remova-o e coloque uma chamada para o minimax_move (que vc implementara' no modulo minimax).
    # A chamada a minimax_move deve receber sua funcao evaluate como parametro.

    return minimax_move(state, max_depth=3, eval_func=evaluate_custom)


def evaluate_custom(state, player:str) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on your custom heuristic
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """

    if state.is_terminal():
        # Checar valor de vitoria ou derrota
        winner = state.winner()
        # Checar vitoria do jogador
        if winner == player:
            return 10000.0
        # Checar empate
        elif winner is None:
            return 0.0
        # Checar derrota do jogador
        else:
            return -10000.0
        

    # python kit_games/server.py othello advsearch/your_agent/othello_minimax_custom.py advsearch/your_agent/othello_minimax_count.py

    return mobilidade(state) * 5 + cantos_dominados(state.get_board(), player) * 25 + pecas_estaveis(state.get_board(), player) * 25
