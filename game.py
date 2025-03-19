import pygame, chess
import sys
import time
import math
from engine2_0 import minimax, determine_best_move


def square_to_pixel(square, player_is_white, board_size):
    square_size = board_size // 8  
    file = chess.square_file(square)  
    rank = chess.square_rank(square) 
    if player_is_white:
        x = file * square_size
        y = (7 - rank) * square_size
    else:
        x = (7 - file) * square_size
        y = rank * square_size
    return (x, y)

def get_square_from_pos(pos, player_is_white, board_size):
    square_size = board_size // 8 
    x, y = pos
    if player_is_white:
        file = x // square_size
        rank = 7 - (y // square_size)
    else:
        file = 7 - (x // square_size)
        rank = y // square_size
    return chess.square(file, rank)

def draw_board(screen, board, player_is_white, selected_square, board_size):
    square_size = board_size // 8 
    light_color = (240, 217, 181)   
    dark_color = (181, 136, 99)    
    
    piece_font = pygame.font.Font("DejaVuSans.ttf", square_size - 10)
    piece_symbols = {
        'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
        'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
    }
    
    for rank in range(8):
        for file in range(8):
            if player_is_white:
                board_rank = rank
                board_file = file
            else:
                board_rank = 7 - rank
                board_file = 7 - file
            square = chess.square(board_file, board_rank)
            x, y = square_to_pixel(square, player_is_white, board_size)
            if (board_file + board_rank) % 2 == 0:
                square_color = light_color
            else:
                square_color = dark_color
            
            rect = pygame.Rect(x, y, square_size, square_size)
            pygame.draw.rect(screen, square_color, rect)
            if selected_square is not None and square == selected_square:
                pygame.draw.rect(screen, (255, 0, 0), rect, 3)
            piece = board.piece_at(square)
            if piece is not None:
                symbol = piece_symbols[piece.symbol()]
                text = piece_font.render(symbol, True, (0, 0, 0))
                text_rect = text.get_rect(center=(x + square_size / 2, y + square_size / 2))
                screen.blit(text, text_rect)

def draw_text(screen, text, pos, font_size=32, color=(0, 0, 0)):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def get_promotion_choice(screen, board_size, player_is_white):
    promotion_pieces = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
    if player_is_white:
        icons = {chess.QUEEN: '♕', chess.ROOK: '♖', chess.BISHOP: '♗', chess.KNIGHT: '♘'}
    else:
        icons = {chess.QUEEN: '♛', chess.ROOK: '♜', chess.BISHOP: '♝', chess.KNIGHT: '♞'}
    
    button_width = 80
    button_height = 80
    total_width = len(promotion_pieces) * button_width + (len(promotion_pieces) - 1) * 10
    start_x = (board_size - total_width) // 2
    start_y = (board_size - button_height) // 2
    promotion_buttons = []
    for i, piece in enumerate(promotion_pieces):
        rect = pygame.Rect(start_x + i * (button_width + 10), start_y, button_width, button_height)
        promotion_buttons.append((rect, piece))
    
    promotion_font = pygame.font.SysFont("DejaVuSans.ttf", 60)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect, piece in promotion_buttons:
                    if rect.collidepoint(pos):
                        return piece
        overlay = pygame.Surface((board_size, board_size))
        overlay.set_alpha(200)
        overlay.fill((50, 50, 50))
        screen.blit(overlay, (0, 0))
        for rect, piece in promotion_buttons:
            pygame.draw.rect(screen, (200, 200, 200), rect)
            text = promotion_font.render(icons[piece], True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        pygame.display.flip()

global counter
counter = 0
def main():
    pygame.init()
    board_size = 640
    screen = pygame.display.set_mode((board_size, board_size + 50))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()
    global counter, arr

    while True:
        board = chess.Board()   
        selected_square = None 
        message = ""           
        counter = 0
        arr = []

        player_is_white = None
        choosing_color = True
        while choosing_color:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    white_button = pygame.Rect(50, board_size // 2 - 25, 200, 50)
                    black_button = pygame.Rect(board_size - 250, board_size // 2 - 25, 200, 50)
                    if white_button.collidepoint(pos):
                        player_is_white = True
                        choosing_color = False
                    elif black_button.collidepoint(pos):
                        player_is_white = False
                        choosing_color = False
            screen.fill((200, 200, 200))
            draw_text(screen, "Выберите цвет", (board_size // 2 - 100, board_size // 2 - 100), 36)
            pygame.draw.rect(screen, (211, 211, 211), (50, board_size // 2 - 25, 200, 50))
            draw_text(screen, "Белые", (50 + 50, board_size // 2 - 15), 36)
            pygame.draw.rect(screen, (100, 100, 100), (board_size - 250, board_size // 2 - 25, 200, 50))
            draw_text(screen, "Чёрные", (board_size - 250 + 30, board_size // 2 - 15), 36)
            pygame.display.flip()
            clock.tick(30)
        
        if not player_is_white:
            engine_move = determine_best_move(board, True)
            if engine_move is not None:
                board.push(engine_move)
        
        game_running = True
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    restart_button_rect = pygame.Rect(board_size - 160, board_size + 5, 150, 40)
                    if restart_button_rect.collidepoint(pos):
                        game_running = False
                        break
                    if pos[1] <= board_size:
                        if board.turn == player_is_white and not board.is_game_over():
                            square = get_square_from_pos(pos, player_is_white, board_size)
                            piece = board.piece_at(square)
                            if selected_square is None:
                                if piece is not None and piece.color == player_is_white:
                                    selected_square = square
                            else:
                                move = chess.Move(selected_square, square)
                                promotion_needed = False
                                moving_piece = board.piece_at(selected_square)
                                if moving_piece is not None and moving_piece.piece_type == chess.PAWN:
                                    if (player_is_white and chess.square_rank(square) == 7) or (not player_is_white and chess.square_rank(square) == 0):
                                        promotion_needed = True
                                if promotion_needed:
                                    promo_piece = get_promotion_choice(screen, board_size, player_is_white)
                                    move = chess.Move(selected_square, square, promotion=promo_piece)
                                if move in board.legal_moves:
                                    board.push(move)
                                    selected_square = None
                                    if board.is_game_over():
                                        message = "Игра окончена"
                                    else:
                                        counter += 1
                                        t1 = time.time()
                                        engine_move = determine_best_move(board, not player_is_white)
                                        t2 = time.time()
                                        arr.append(round(t2-t1, 3))
                                        print(f'({counter};{round(t2-t1, 3)})')
                                        print(arr)
                                        if engine_move is not None:
                                            board.push(engine_move)
                                            if board.is_game_over():
                                                message = "Игра окончена"
                                else:
                                    if piece is not None and piece.color == player_is_white:
                                        selected_square = square
                                    else:
                                        selected_square = None
            screen.fill((0, 0, 0))
            draw_board(screen, board, player_is_white, selected_square, board_size)
            draw_text(screen, message, (10, board_size + 10), 32, (255, 0, 0))
            restart_button_rect = pygame.Rect(board_size - 160, board_size + 5, 150, 40)
            pygame.draw.rect(screen, (180, 180, 180), restart_button_rect)
            draw_text(screen, "Перезапуск", (board_size - 150, board_size + 15), 28, (0, 0, 0))
            pygame.display.flip()
            clock.tick(30)

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.set_start_method('spawn')
    main()