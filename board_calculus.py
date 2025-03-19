import chess
from table_values import *

def mobility_for_color(board, color):
    board_copy = board.copy()
    board_copy.turn = color
    return sum(1 for _ in board_copy.legal_moves)

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 400,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 1100
}

def piece_safety_evaluation(board, color):
    safety_score = 0
    opponent = not color
    for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        for square in board.pieces(piece_type, color):
            attackers = board.attackers(opponent, square)
            defenders = board.attackers(color, square)
        
            if attackers:
                if len(defenders) < len(attackers):
                    penalty = PIECE_VALUES[piece_type] * 0.5
                    safety_score -= penalty
    return safety_score
def evaluate(board):
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    
    material = (100 * (wp - bp) +
                300 * (wn - bn) +
                400 * (wb - bb) +
                500 * (wr - br) +
                900 * (wq - bq))
    
    pawn_sum = sum(pawn_table[i] for i in board.pieces(chess.PAWN, chess.WHITE))
    pawn_sum += sum(-pawn_table[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK))
    
    knight_sum = sum(knights_table[i] for i in board.pieces(chess.KNIGHT, chess.WHITE))
    knight_sum += sum(-knights_table[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK))
    
    bishop_sum = sum(bishops_table[i] for i in board.pieces(chess.BISHOP, chess.WHITE))
    bishop_sum += sum(-bishops_table[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK))
    
    rook_sum = sum(rooks_table[i] for i in board.pieces(chess.ROOK, chess.WHITE))
    rook_sum += sum(-rooks_table[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK))
    
    queens_sum = sum(queens_table[i] for i in board.pieces(chess.QUEEN, chess.WHITE))
    queens_sum += sum(-queens_table[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK))
    
    kings_sum = sum(kings_table[i] for i in board.pieces(chess.KING, chess.WHITE))
    kings_sum += sum(-kings_table[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK))
    
    positional = pawn_sum + knight_sum + bishop_sum + rook_sum + queens_sum + kings_sum

    mobility_white = mobility_for_color(board, chess.WHITE)
    mobility_black = mobility_for_color(board, chess.BLACK)
    mobility_value = 5 * (mobility_white - mobility_black)  

    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    center_control_white = sum(1 for square in center_squares 
                               if board.piece_at(square) and board.piece_at(square).color == chess.WHITE)
    center_control_black = sum(1 for square in center_squares 
                               if board.piece_at(square) and board.piece_at(square).color == chess.BLACK)
    center_control_value = 20 * (center_control_white - center_control_black)  

    safety_white = piece_safety_evaluation(board, chess.WHITE)
    safety_black = piece_safety_evaluation(board, chess.BLACK)
    safety_value = safety_white - safety_black

    evaluation = material + positional + mobility_value + center_control_value + safety_value
    # print(f'material: {material}, positional: {positional}, mobility_value: {mobility_value}, center_control_value: {center_control_value}, safety_value: {safety_value}')
    return evaluation
