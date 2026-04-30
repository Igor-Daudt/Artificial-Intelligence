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
    # Um fator de posicao maior da mais importancia ao mask em comparacao com count
    fator_de_posicao = 12

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
        
    # Obtem o valor das outras heuristicas
    valor_mask = evaluate_mask(state, player)
    board = state.get_board()
    valor_contagem = board.num_pieces(player)
    valor_contagem_oponente = board.num_pieces(board.opponent(player))

    valor_exploracao = (valor_contagem + valor_contagem_oponente) / fator_de_posicao

    return valor_exploracao * valor_contagem + valor_mask / valor_exploracao
