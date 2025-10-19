from Heuristic.basic import score_position_beginner
from Heuristic.intermediate import score_position_intermediate
from Heuristic.advanced import score_position_professional
from Utils.utils import PLAYER_PIECE, AI_PIECE


def evaluate_board(board, level):
    if level == 'iniciante':
        return score_position_beginner(board, AI_PIECE) - score_position_beginner(board, PLAYER_PIECE)
    elif level == 'intermediario':
        return score_position_intermediate(board, AI_PIECE) - score_position_intermediate(board, PLAYER_PIECE)
    else:
        return score_position_professional(board, AI_PIECE) - score_position_professional(board, PLAYER_PIECE)
