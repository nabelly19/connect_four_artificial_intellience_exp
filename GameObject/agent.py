import time, random
from GameObject.board import get_valid_locations
from SearchEngine.minimax import minimax
from SearchEngine.alphabeta import alphabeta
from Utils.utils import PLAYER_PIECE, AI_PIECE
from Utils.evaluator import evaluate_board   

def pick_best_move(board, level, time_limit=None):
    valid_locations = get_valid_locations(board)

    if level == 'iniciante':
        col, value = minimax(board, 2, True, level)
        return col, value, 0
    elif level == 'intermediario':
        col, value, _ = alphabeta(board, 4, float('-inf'), float('inf'), True, level)
        return col, value, 0
    else:
        start_time = time.time()
        best_move = random.choice(valid_locations)
        best_value = None
        depth = 1

        while True:
            elapsed = time.time() - start_time
            if elapsed > time_limit:
                break

            col, value, timed_out = alphabeta(
                board, depth, float('-inf'), float('inf'),
                True, level, start_time, time_limit
            )

            if timed_out:
                break

            if col is not None:
                best_move, best_value = col, value

            depth += 1
            if depth > 12:
                break

        return best_move, (best_value if best_value is not None else 0), time.time() - start_time