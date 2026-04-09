import random
from typing import Tuple, Callable


###########################################################################
# @ Func: Retorna um movimento calculado pelo algoritmo minimax para o 
# estado de jogo fornecido.
# @ Param: state - estado do jogo
#          max_depth - profundidade maxima da busca (-1 = ilimitada)
#          eval_func - funcao de avaliacao para estados terminais ou folhas
###########################################################################
def minimax_move(state, max_depth:int, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    alpha, beta = float('-inf'), float('inf')
    player = state.player

    for move in state.legal_moves():
        new_state = state.next_state(move)
        value = minimax(new_state, player, max_depth, False, eval_func, alpha, beta)
        if value > alpha:
            alpha = value
            best_move = move

    return best_move

###########################################################################
# @ Func: Retorna o valor minimax de um estado, simulando o jogador 
# maximizador e o jogador minimizador
# @ Param: state - estado do jogo (GameState)
#          player - jogador para o qual estamos calculando a utilidade
#          depth - profundidade da busca
#          maximizing_player - indica se o jogador atual é o maximizador
#          eval_func - função de avaliação
#          alpha - valor alpha para a poda alpha-beta
#          beta - valor beta para a poda alpha-beta
###########################################################################
def minimax(state, player, depth, maximizing_player, eval_func, alpha, beta) -> float:
    # Se a profundidade eh 0 passamos da profundidade maxima (diminuir -1 nunca vai chegar em 0)
    # Se o estado eh terminal, entao avaliamos o estado usando a funcao de avaliacao
    if depth == 0 or state.is_terminal():
        return eval_func(state, player)

    # Simula o jogador maximizador, se for o turno dele
    if maximizing_player:
        max_eval = float('-inf') # 'Alpha' local
        for child in state.legal_moves():
            new_state = state.next_state(child)
            eval = minimax(new_state, player, depth - 1, False, eval_func, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval) # Atualiza o valor alpha com o minimax dos filhos
            if beta <= alpha:
                break
        return max_eval

    # Simula o jogador minimizador, se for o turno dele
    else:
        min_eval = float('inf') # 'Beta' local
        for child in state.legal_moves():
            new_state = state.next_state(child)
            eval = minimax(new_state, player, depth - 1, True, eval_func, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval) # Atualiza o valor beta com o minimax dos filhos
            if beta <= alpha: # poda alpha-beta
                break
        return min_eval