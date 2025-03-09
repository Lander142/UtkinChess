import chess
from board_calculus import evaluate

MATE_SCORE = 10000  

def minimax(depth, board, alpha, beta, is_maximizing):
    if depth <= 0 or board.is_game_over():
        if board.is_game_over():
            if board.is_checkmate():
                return -MATE_SCORE + depth if is_maximizing else MATE_SCORE - depth
            else:
                return 0
        return evaluate(board)
    
    repetition_penalty = -50  
    extra_penalty = repetition_penalty if board.can_claim_threefold_repetition() else 0

    if is_maximizing:
        best_value = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = minimax(depth - 1, board, alpha, beta, False) + extra_penalty
            board.pop()
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value
    else:
        best_value = float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = minimax(depth - 1, board, alpha, beta, True) + extra_penalty
            board.pop()
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value


def _determine_best_move(board, is_white, depth=3):
    best_move_value = -100000 if is_white else 100000
    best_move_final = None
    for move in board.legal_moves:
        board.push(move)
        value = minimax(depth - 1, board, -10000, 10000, not is_white)
        board.pop()
        if (is_white and value > best_move_value) or (not is_white and value < best_move_value):
            best_move_value = value
            best_move_final = move
    return best_move_final

