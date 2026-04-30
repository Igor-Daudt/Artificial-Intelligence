import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

# mask template adjusted from https://web.fe.up.pt/~eol/IA/MIA0203/trabalhos/Damas_Othelo/Docs/Eval.html
# could optimize for symmetries but just put all values here for coding speed :P
# DO NOT CHANGE! 
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


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    return minimax_move(state, max_depth=3, eval_func=evaluate_mask)


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

    # Se o estado eh terminal, avalia
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
        
    # Calcular valor posicional do jogador
    valor_posicional = 0
    # String alterada para analise
    tabuleiro_str = state.get_board().__str__().replace('\n', '')
    for linha in range(LINHAS_TABULEIRO):
        for coluna in range(COLUNAS_TABULEIRO):
            if tabuleiro_str[linha * LINHAS_TABULEIRO + coluna] == player:
                valor_posicional += EVAL_TEMPLATE[linha][coluna]
    
    return valor_posicional   # substitua pelo seu codigo
