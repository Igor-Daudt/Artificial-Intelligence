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


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    return minimax_move(state, max_depth=3, eval_func=evaluate_count)


def evaluate_count(state, player:str) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on the number of pieces of each color.
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
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
        
    # Se nao eh terminal, retorna count da quantidade de pecas
    return state.get_board().num_pieces(player)
