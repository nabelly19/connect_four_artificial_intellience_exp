import random
from Utils.utils import ROWS, COLUMNS, EMPTY

def evaluate_window_professional(window, piece, opp_piece):
    score = 0
    count_piece = window.count(piece)
    count_opp = window.count(opp_piece)
    count_empty = window.count(EMPTY)

    if count_piece == 4:
        score += 100000
    elif count_piece == 3 and count_empty == 1:
        score += 500
    elif count_piece == 2 and count_empty == 2:
        score += 50

    if count_opp == 3 and count_empty == 1:
        score -= 400
    if count_opp == 2 and count_empty == 2:
        score -= 20

    if count_piece >= 2 and count_opp == 0:
        score += count_piece * 5
    return score

def score_position_professional(board, piece):
    score = 0
    opp_piece = 'R' if piece=='Y' else 'Y'
    center_col = COLUMNS // 2
    for c in range(COLUMNS):
        col_count = sum(1 for r in range(ROWS) if board[r][c] == piece)
        score += col_count * (6 - abs(center_col - c))

    for r in range(ROWS):
        row_array = [board[r][c] for c in range(COLUMNS)]
        for c in range(COLUMNS-3):
            score += evaluate_window_professional(row_array[c:c+4], piece, opp_piece)

    for c in range(COLUMNS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS-3):
            score += evaluate_window_professional(col_array[r:r+4], piece, opp_piece)

    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            score += evaluate_window_professional([board[r+i][c+i] for i in range(4)], piece, opp_piece)
    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            score += evaluate_window_professional([board[r-i][c+i] for i in range(4)], piece, opp_piece)

    return score + random.random()*0.1