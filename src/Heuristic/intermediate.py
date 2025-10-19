from Utils.utils import ROWS, COLUMNS, EMPTY

def evaluate_window_intermediate(window, piece, opp_piece):
    score = 0
    if window.count(piece) == 4:
        score += 1000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 50
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 10
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80
    if window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score -= 5
    return score

def score_position_intermediate(board, piece):
    score = 0
    opp_piece = 'R' if piece=='Y' else 'Y'
    center_array = [board[r][COLUMNS//2] for r in range(ROWS)]
    score += center_array.count(piece) * 6

    for r in range(ROWS):
        row_array = [board[r][c] for c in range(COLUMNS)]
        for c in range(COLUMNS-3):
            score += evaluate_window_intermediate(row_array[c:c+4], piece, opp_piece)

    for c in range(COLUMNS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS-3):
            score += evaluate_window_intermediate(col_array[r:r+4], piece, opp_piece)

    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            score += evaluate_window_intermediate([board[r+i][c+i] for i in range(4)], piece, opp_piece)
    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            score += evaluate_window_intermediate([board[r-i][c+i] for i in range(4)], piece, opp_piece)
    return score