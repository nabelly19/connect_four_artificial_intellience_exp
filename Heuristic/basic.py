from Utils.utils import ROWS, COLUMNS, EMPTY

def evaluate_window(window, piece, opp_piece):
    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    return score

def score_position_beginner(board, piece):
    score = 0
    center_array = [board[r][COLUMNS//2] for r in range(ROWS)]
    score += center_array.count(piece) * 3

    # horizontal
    for r in range(ROWS):
        row_array = [board[r][c] for c in range(COLUMNS)]
        for c in range(COLUMNS-3):
            score += evaluate_window(row_array[c:c+4], piece, 'R' if piece=='Y' else 'Y')

    # vertical
    for c in range(COLUMNS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS-3):
            score += evaluate_window(col_array[r:r+4], piece, 'R' if piece=='Y' else 'Y')

    # diagonal
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            score += evaluate_window([board[r+i][c+i] for i in range(4)], piece, 'R' if piece=='Y' else 'Y')
    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            score += evaluate_window([board[r-i][c+i] for i in range(4)], piece, 'R' if piece=='Y' else 'Y')
    return score