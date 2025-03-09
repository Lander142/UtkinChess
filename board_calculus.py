import chess
from table_hard import *

def mobility_for_color(board, color):
    board_copy = board.copy()
    board_copy.turn = color
    return sum(1 for _ in board_copy.legal_moves)

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
    
    pawn_sum = sum(PAWN_TABLE[i] for i in board.pieces(chess.PAWN, chess.WHITE))
    pawn_sum += sum(-PAWN_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK))
    
    knight_sum = sum(KNIGHTS_TABLE[i] for i in board.pieces(chess.KNIGHT, chess.WHITE))
    knight_sum += sum(-KNIGHTS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK))
    
    bishop_sum = sum(BISHOPS_TABLE[i] for i in board.pieces(chess.BISHOP, chess.WHITE))
    bishop_sum += sum(-BISHOPS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK))
    
    rook_sum = sum(ROOKS_TABLE[i] for i in board.pieces(chess.ROOK, chess.WHITE))
    rook_sum += sum(-ROOKS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK))
    
    queens_sum = sum(QUEENS_TABLE[i] for i in board.pieces(chess.QUEEN, chess.WHITE))
    queens_sum += sum(-QUEENS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK))
    
    kings_sum = sum(KINGS_TABLE[i] for i in board.pieces(chess.KING, chess.WHITE))
    kings_sum += sum(-KINGS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK))
    
    positional = pawn_sum + knight_sum + bishop_sum + rook_sum + queens_sum + kings_sum

    mobility_white = mobility_for_color(board, chess.WHITE)
    mobility_black = mobility_for_color(board, chess.BLACK)
    mobility_value = 10 * (mobility_white - mobility_black)  

    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    center_control_white = sum(1 for square in center_squares 
                               if board.piece_at(square) and board.piece_at(square).color == chess.WHITE)
    center_control_black = sum(1 for square in center_squares 
                               if board.piece_at(square) and board.piece_at(square).color == chess.BLACK)
    center_control_value = 20 * (center_control_white - center_control_black)  

    evaluation = material + positional + mobility_value + center_control_value
    return evaluation
