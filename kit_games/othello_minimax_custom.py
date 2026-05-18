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


# def evaluate_custom(state, player:str) -> float:
#     """
#     Evaluates an othello state from the point of view of the given player. 
#     If the state is terminal, returns its utility. 
#     If non-terminal, returns an estimate of its value based on your custom heuristic
#     :param state: state to evaluate (instance of GameState)
#     :param player: player to evaluate the state for (B or W)
#     """

#     if state.is_terminal():
#         # Checar valor de vitoria ou derrota
#         winner = state.winner()
#         # Checar vitoria do jogador
#         if winner == player:
#             return 10000.0
#         # Checar empate
#         elif winner is None:
#             return 0.0
#         # Checar derrota do jogador
#         else:
#             return -10000.0
        

#     # python kit_games/server.py othello advsearch/your_agent/othello_minimax_custom.py advsearch/your_agent/othello_minimax_count.py

#     return mobilidade(state) * 5 + cantos_dominados(state.get_board(), player) * 25 + pecas_estaveis(state.get_board(), player) * 25

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
    
    # 1. PEGA OS DADOS BASE
    my_pieces = board.num_pieces(player)
    opp_pieces = board.num_pieces(opponent)
    total_pieces = my_pieces + opp_pieces
    
    # 2. CALCULA A MÁSCARA
    valor_mascara = evaluate_mask(state, player)
                
    # 3. CONDIÇÃO DE MOBILIDADE 
    # Se for a vez do player, contamos as jogadas legais dele.
    # Quanto mais mobilidade pro player melhor, quanto menos mobilidade para o oponente pior
    mobilidade = 0
    if state.player == player:
        mobilidade = len(list(state.legal_moves())) * 10  # Peso 10 para mobilidade
    else:
        mobilidade = -len(list(state.legal_moves())) * 10
        
    # 4. TRANSIÇÃO DINÂMICA DE FASES 
    if total_pieces < 20:
        # INÍCIO DO JOGO: Foco na máscara e mobilidade. Ter muitas peças é ruim.
        pontuacao = valor_mascara + mobilidade - (my_pieces * 2) 
    
    elif total_pieces <= 30:
        # MEIO DO JOGO: Foco absoluto na máscara e mobilidade extrema.
        pontuacao = valor_mascara + mobilidade

    elif total_pieces <= 40:
        # MEIO DO JOGO: Foco absoluto na máscara e mobilidade extrema.
        pontuacao = valor_mascara + mobilidade + (my_pieces - opp_pieces)*2
    
    elif total_pieces <= 50:
        # MEIO DO JOGO: Foco absoluto na máscara e mobilidade extrema.
        pontuacao = valor_mascara + mobilidade + (my_pieces - opp_pieces)*5

    else:
        # FIM DE JOGO: A máscara perde importância. Contagem de peças dita o vencedor.
        pontuacao = (my_pieces - opp_pieces) * 100 
        
    return float(pontuacao)