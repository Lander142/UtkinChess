import chess
import multiprocessing
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
    
    repetition_penalty = -500
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

def evaluate_move(args):
    move, board, is_white, depth = args
    board_copy = board.copy()  
    board_copy.push(move)
    value = minimax(depth - 1, board_copy, -10000, 10000, not is_white)
    return (move, value)

def determine_best_move(board, is_white, depth=4):
    moves = list(board.legal_moves)
    tasks = [(move, board, is_white, depth) for move in moves]
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = pool.map(evaluate_move, tasks)
    pool.close()
    pool.join()

    best_move = None
    if is_white:
        best_value = -float('inf')
        for move, value in results:
            if value > best_value:
                best_value = value
                best_move = move
    else:
        best_value = float('inf')
        for move, value in results:
            if value < best_value:
                best_value = value
                best_move = move

    return best_move
