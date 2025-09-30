import random
from GameObject.board import get_valid_locations, get_next_open_row, drop_piece, remove_piece, winning_move, is_terminal_node
from Utils.evaluator import evaluate_board
from Utils.utils import PLAYER_PIECE, AI_PIECE

def minimax(board, depth, maximizingPlayer, level):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board, PLAYER_PIECE, AI_PIECE)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, float('inf'))
            elif winning_move(board, PLAYER_PIECE):
                return (None, float('-inf'))
            else:
                return (None, 0)
        else:
            return (None, evaluate_board(board, level))
    if maximizingPlayer:
        value = float('-inf')
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            new_score = minimax(board, depth-1, False, level)[1]
            remove_piece(board, row, col)
            if new_score > value:
                value, best_col = new_score, col
        return best_col, value
    else:
        value = float('inf')
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_PIECE)
            new_score = minimax(board, depth-1, True, level)[1]
            remove_piece(board, row, col)
            if new_score < value:
                value, best_col = new_score, col
        return best_col, value