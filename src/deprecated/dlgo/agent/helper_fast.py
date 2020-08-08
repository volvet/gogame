

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from dlgo.gotypes import Point

__all__ = [
    'is_point_an_eye',
]

def is_point_an_eye(board, point, color):
    if board.get(point) is not None:
        return False

    for neighbor in board.neighbors(point):
        neighbor_color = board.get(neighbor)
        if neighbor_color != color:
            return False
    pass