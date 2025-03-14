import berserk
from engine2_0 import minimax, _determine_best_move
import chess
import chess.engine
import chess.pgn
import requests
import json
import time
TOKEN = "lip_MOrrl5rCv8CfvBH6JL5B"


# Создаём сессию и клиента для работы с API Lichess
session = berserk.TokenSession(TOKEN)
client = berserk.Client(session=session)

def stream_events():
    """
    Поток входящих событий от Lichess (вызовы, начало игры и т.д.)
    """
    for event in client.bots.stream_incoming_events():
        yield event

def stream_game(game_id):
    """
    Поток обновлений по конкретной игре.
    """
    url = f"https://lichess.org/api/bot/game/stream/{game_id}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    with requests.get(url, headers=headers, stream=True) as response:
        for line in response.iter_lines():
            if line:
                yield json.loads(line)

def make_move(game_id, move):
    """
    Отправка хода (в формате UCI) в игру.
    """
    client.bots.make_move(game_id, move)

def play_game(game_id):
    board = chess.Board()
    while True:
        try:
            for event in stream_game(game_id):
                if 'state' in event:
                    moves_str = event['state'].get('moves', "")
                    board.reset()
                    for move in moves_str.split():
                        board.push_uci(move)
                    if board.is_game_over():
                        print("Игра закончена!")
                        return  # Завершаем цикл, если игра окончена
                    if board.turn == chess.WHITE:  # или сравните с нужной вам стороной
                        best_move = _determine_best_move(board, True)
                    else:
                        best_move = _determine_best_move(board, False)
                    if best_move:
                        print(f"Сделан ход: {best_move.uci()}")
                        make_move(game_id, best_move.uci())
        except Exception as e:
            print("Ошибка при обработке событий:", e)
            # Можно сделать задержку и попробовать переподключиться


def main():
    """
    Главный цикл бота: принимает вызовы и запускает игру.
    """
    for event in stream_events():
        event_type = event.get('type')
        if event_type == 'challenge':
            challenge = event['challenge']
            # Принимаем только вызовы для стандартных игр
            if challenge.get('variant', {}).get('key') == 'standard':
                print("Принят вызов:", challenge['id'])
                client.bots.accept_challenge(challenge['id'])
        elif event_type == 'gameStart':
            game_id = event['game']['id']
            print("Началась игра:", game_id)
            play_game(game_id)


while True:
    main()
    time.sleep(10)
