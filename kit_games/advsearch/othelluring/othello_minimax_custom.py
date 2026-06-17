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


# Retorna a quantidade de movimentos possiveis do jogador menos
# a quantidade de movimentos possiveis do oponente
def calcula_mobilidade(state, player):
    if state.player == player:
        movimentos_jogador = len(state.legal_moves())
        state.player = state.get_board().opponent(state.player)
        movimentos_oponente = len(state.legal_moves())
        state.player = state.get_board().opponent(state.player)
    else:
        movimentos_oponente = len(state.legal_moves())
        state.player = state.get_board().opponent(state.player)
        movimentos_jogador = len(state.legal_moves())
        state.player = state.get_board().opponent(state.player)
    return float(movimentos_jogador - movimentos_oponente)

# Retorna a quantidade de cantos dominados pelo jogador
def cantos_dominados(board, player, opponent):
    n = len(board.tiles[0])
    tiles = board.tiles

    bordas = (
        [(0, n-1)] +
        [(n-1, 0)] +
        [(0, 0)] +
        [(n-1, n-1)]
    )
    qtd_cantos_player = 0
    qtd_cantos_oponente = 0
    for i in bordas:
        if tiles[i[0]][i[1]] == player:
            qtd_cantos_player += 1
        elif tiles[i[0]][i[1]] == opponent:
            qtd_cantos_oponente += 1
    return (qtd_cantos_player - qtd_cantos_oponente)

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
def evaluate_mask(board, player, opponent) -> float:

    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on the positional value of the pieces.
    You must use the EVAL_TEMPLATE above to compute the positional value of the pieces.
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """

    LINHAS_TABULEIRO = COLUNAS_TABULEIRO = 8
    
    # Calcular valor posicional do jogador
    valor_posicional = 0
    tabuleiro_str = board.tiles
    
    for linha in range(LINHAS_TABULEIRO):
        for coluna in range(COLUNAS_TABULEIRO):
            peca = tabuleiro_str[linha][coluna]
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
    
    # 1. PEGA OS DADOS BASE
    my_pieces = board.num_pieces(player)
    opp_pieces = board.num_pieces(opponent)
    total_pieces = my_pieces + opp_pieces
    
    # 2. CALCULA A MÁSCARA E CANTOS
    valor_mascara = evaluate_mask(board, player, opponent)
    cantos = cantos_dominados(board, player, opponent) * 150
                
    # 3. CONDIÇÃO DE MOBILIDADE 
    # Se for a vez do player, contamos as jogadas legais dele.
    # Quanto mais mobilidade pro player melhor, quanto menos mobilidade para o oponente pior
    mobilidade = calcula_mobilidade(state, player)
        
    # 4. TRANSIÇÃO DINÂMICA DE FASES 
    if total_pieces < 20:
        # INÍCIO DO JOGO: Foco na máscara e mobilidade. Ter muitas peças é ruim.
        return float(valor_mascara + mobilidade * 10 + cantos - (my_pieces * 5))
        
    elif total_pieces <= 50:
        # MEIO DO JOGO: Foco absoluto na máscara e mobilidade extrema.
        return float(valor_mascara + mobilidade * 10 + cantos)
        
    else:
        # FIM DE JOGO: A máscara perde importância. Contagem de peças dita o vencedor.
        diferenca_pecas = (my_pieces - opp_pieces) * 100
        return float(diferenca_pecas + cantos)
        