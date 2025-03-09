import pygame, chess
import sys
from engine2_0 import minimax, _determine_best_move
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
    
    piece_font = pygame.font.SysFont("DejaVu Sans", square_size - 10)
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

def main():
    pygame.init()
    board_size = 640
    screen = pygame.display.set_mode((board_size, board_size + 50))
    pygame.display.set_caption("Chess Engine")
    clock = pygame.time.Clock()
    
    board = chess.Board()
    selected_square = None
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
        draw_text(screen, "Выберите цвет", (board_size // 2 - 150, board_size // 2 - 100), 36)
        pygame.draw.rect(screen, (255, 255, 255), (50, board_size // 2 - 25, 200, 50))
        draw_text(screen, "Белые", (50 + 50, board_size // 2 - 15), 36)
        pygame.draw.rect(screen, (100, 100, 100), (board_size - 250, board_size // 2 - 25, 200, 50))
        draw_text(screen, "Чёрные", (board_size - 250 + 30, board_size // 2 - 15), 36)
        pygame.display.flip()
        clock.tick(30)
    
    if not player_is_white:
        engine_move = _determine_best_move(board, True)
        if engine_move is not None:
            board.push(engine_move)
    
    message = ""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.turn == player_is_white and not board.is_game_over():
                    pos = pygame.mouse.get_pos()
                    if pos[1] > board_size:
                        continue
                    square = get_square_from_pos(pos, player_is_white, board_size)
                    piece = board.piece_at(square)
                    if selected_square is None:
                        if piece is not None and piece.color == player_is_white:
                            selected_square = square
                    else:
                        move = chess.Move(selected_square, square)
                        if move in board.legal_moves:
                            board.push(move)
                            selected_square = None
                            if board.is_game_over():
                                message = "Игра окончена"
                            else:
                                engine_move = _determine_best_move(board, not player_is_white)
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
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
main()