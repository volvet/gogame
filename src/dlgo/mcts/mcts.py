
import math
import random
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from dlgo import agent
from dlgo.gotypes import Player
from dlgo.utils import coords_from_point

__all__ = [
    'MCTSAgent',
]


class MCTSNode(object):
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.win_count = {
            Player.black: 0,
            Player.white: 0,
        }
        self.num_rollouts = 0
        self.children = []
        self.unvisited_move = game_state.legal_moves()
        pass

    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_move)-1)
        new_move = self.unvisited_move.pop(index)
        new_game_state = self.game_state.apply_move(new_move)
        new_node = MCTSNode(new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node

    def record_win(self, winner):
        self.win_count[winner] += 1
        self.num_rollouts += 1

    def can_add_child(self):
        return len(self.unvisited_move) > 0

    def is_terminal(self):
        return self.game_state.is_over()

    def win_frac(self, player):
        if self.num_rollouts > 0:
            return float(self.win_count[player])/float(self.num_rollouts)
        return float(0)

class MCTSAgent(agent.Agent):
    def __init__(self, num_round, temperature):
        agent.Agent.__init__(self)
        self.num_round = num_round
        self.temperature = temperature
        pass

    def select_move(self, game_state):
        root = MCTSNode(game_state)
        pass

    def select_child(self, node):
        pass

def mcts_test():
    pass

if __name__ == '__main__':
    mcts_test()

