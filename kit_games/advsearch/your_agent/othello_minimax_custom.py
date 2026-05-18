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

def evaluate_custom(state, player:str) -> float:
    if state.is_terminal():
        winner = state.winner()
        if winner == player: return 10000.0
        elif winner != player and winner is not None and winner != '-' and winner != 'Draw': return -10000.0
        else: return 0.0
        
    opponent = 'W' if player == 'B' else 'B'
    board = state.get_board()
    
    my_pieces = board.num_pieces(player)
    opp_pieces = board.num_pieces(opponent)
    total_pieces = my_pieces + opp_pieces
    
    # Usamos a base da heuristica posicional
    valor_mascara = evaluate_mask(state, player)
                
    # Se for a vez do player, contamos as jogadas legais dele.
    # Quanto mais mobilidade pro player melhor, quanto menos mobilidade para o oponente pior
    mobilidade = 0
    if state.player == player:
        mobilidade = len(list(state.legal_moves())) * 10  # Peso 10 para mobilidade
    else:
        mobilidade = -len(list(state.legal_moves())) * 10
        
    #Diferentes pontuacoes para cada parte do jogo
    if total_pieces < 20:
        # Inicio: Foco na máscara e mobilidade. Ter muitas peças eh ruim.
        pontuacao = valor_mascara + mobilidade - (my_pieces * 2) 
    
    elif total_pieces <= 30:
        # Inicio do meio: Foco absoluto na máscara e mobilidade extrema.
        pontuacao = valor_mascara + mobilidade

    elif total_pieces <= 40:
        # Meio do jogo: Foco na máscara e mobilidade porém considerando um pouco as peças.
        pontuacao = valor_mascara + mobilidade + (my_pieces - opp_pieces)*2
    
    elif total_pieces <= 50:
        # Inicio do fim: Ainda importante do valor da mascara e mobilidade mas considerando mais a máscara.
        pontuacao = valor_mascara + mobilidade + (my_pieces - opp_pieces)*5

    else:
        # Fim: A máscara perde importância. Contagem de peças eh muito mais importante.
        pontuacao = (my_pieces - opp_pieces) * 100 
        
    return float(pontuacao)