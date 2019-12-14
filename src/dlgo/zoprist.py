

import random

from gotypes import Player, Point

MAX63 = 0x7fffffffffffffff

def to_python(player_state):
    if player_state is None:
        return 'None'
    if player_state is Player.black:
        return Player.black
    return Player.white

def generate_zobrist_hash():
    table = {}
    empty_board = 0
    for row in range(1, 20):
        for col in range(1, 20):
            for state in (Player.black, Player.white, None):
                code = random.randint(0, MAX63)
                table[Point(row, col), state] = code
    return table

if __name__ == '__main__':
    print(generate_zobrist_hash())

