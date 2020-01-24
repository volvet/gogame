

import random

from gotypes import Player, Point


__all__ = [
    'EMPTY_BOARD',
    'generate_zobrist_hash',
]

MAX63 = 0x7fffffffffffffff
EMPTY_BOARD = 0x0


def generate_zobrist_hash():
    table = {}
    empty_board = 0
    for row in range(1, 20):
        for col in range(1, 20):
            for state in (Player.black, Player.white):
                code = random.randint(0, MAX63)
                table[Point(row, col), state] = code
    return table



def zobrist_test():
    table = generate_zobrist_hash()

    stones = []
    for s in range(1, 50):
        for state in (Player.black, Player.white):
            stone = [Point(random.randint(1, 19), random.randint(1, 19)), state]
            stones.append(stone)

    l = 0
    for s in stones:
        l ^= table[s[0], s[1]]

    random.shuffle(stones)

    r = 0
    for s in stones:
        r ^= table[s[0], s[1]]

    assert l == r
    for s in stones:
        l ^= table[s[0], s[1]]

    assert l == 0

if __name__ == '__main__':
    zobrist_test()

