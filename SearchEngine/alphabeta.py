import random, time
from GameObject.board import get_valid_locations, get_next_open_row, drop_piece, remove_piece, winning_move, is_terminal_node
from Utils.evaluator import evaluate_board
from Utils.utils import PLAYER_PIECE, AI_PIECE

def order_moves(board, moves, level, piece):
    from Heuristic.basic import score_position_beginner
    from Heuristic.intermediate import score_position_intermediate
    from Heuristic.advanced import score_position_professional

    scores = []
    for col in moves:
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, piece)
        if level == 'iniciante':
            s = score_position_beginner(board, AI_PIECE)
        elif level == 'intermediario':
            s = score_position_intermediate(board, AI_PIECE)
        else:
            s = score_position_professional(board, AI_PIECE)
        remove_piece(board, row, col)
        scores.append((s, col))
    scores.sort(reverse=True)
    return [col for _, col in scores]

def alphabeta(board, depth, alpha, beta, maximizingPlayer, level, start_time=None, time_limit=None):
    if start_time and time_limit and time.time() - start_time > time_limit:
        return (None, evaluate_board(board, level), True)

    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board, PLAYER_PIECE, AI_PIECE)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, float('inf'), False)
            elif winning_move(board, PLAYER_PIECE):
                return (None, float('-inf'), False)
            else:
                return (None, 0, False)
        else:
            return (None, evaluate_board(board, level), False)

    if maximizingPlayer:
        value = float('-inf')
        best_col = random.choice(valid_locations)
        for col in order_moves(board, valid_locations, level, AI_PIECE):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            _, new_score, timed_out = alphabeta(board, depth-1, alpha, beta, False, level, start_time, time_limit)
            remove_piece(board, row, col)
            if timed_out:
                return (None, 0, True)
            if new_score > value:
                value, best_col = new_score, col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value, False
    else:
        value = float('inf')
        best_col = random.choice(valid_locations)
        for col in order_moves(board, valid_locations, level, PLAYER_PIECE):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_PIECE)
            _, new_score, timed_out = alphabeta(board, depth-1, alpha, beta, True, level, start_time, time_limit)
            remove_piece(board, row, col)
            if timed_out:
                return (None, 0, True)
            if new_score < value:
                value, best_col = new_score, col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value, False