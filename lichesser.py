
import berserk                     
from engine2_0 import minimax, determine_best_move  
import chess                       
import chess.engine                
import chess.pgn                   
import requests                   
import json                        
import time                        


TOKEN = "TOKEN"
arr = []

session = berserk.TokenSession(TOKEN)
client = berserk.Client(session=session)

def stream_events():
    for event in client.bots.stream_incoming_events():
        yield event

def stream_game(game_id):
    url = f"https://lichess.org/api/bot/game/stream/{game_id}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    with requests.get(url, headers=headers, stream=True) as response:
        for line in response.iter_lines():
            if line:
                yield json.loads(line)

def make_move(game_id, move):
    client.bots.make_move(game_id, move)
    time.sleep(8)
    play_game(game_id)

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
                        return
                    t1 = time.time()
                    if board.turn == chess.WHITE:  
                        best_move = determine_best_move(board, True)
                    else:
                        best_move = determine_best_move(board, False)
                    t2 = time.time()
                    arr.append(round(t2-t1, 3))
                    print(arr)
                    if best_move:
                        print(f"Сделан ход: {best_move.uci()}")
                        make_move(game_id, best_move.uci())
        except Exception as e:
            print("Ошибка при обработке событий:", e)
            time.sleep(5)
            play_game(game_id)

def main():
    for event in stream_events():
        event_type = event.get('type')
        if event_type == 'challenge':
            challenge = event['challenge']
            if challenge.get('variant', {}).get('key') == 'standard':
                print("Принят вызов:", challenge['id'])
                client.bots.accept_challenge(challenge['id'])
        elif event_type == 'gameStart':
            game_id = event['game']['id']
            print("Началась игра:", game_id)
            play_game(game_id)

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.set_start_method('spawn')
    main()