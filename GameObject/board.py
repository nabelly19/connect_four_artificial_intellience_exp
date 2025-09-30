# Generates the board and manage players movement throw it

from Utils.utils import ROWS, COLUMNS, EMPTY

def create_board():
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    print('\nTabuleiro (Linha 0 = topo):')
    for r in range(ROWS):
        print(' '.join(board[r]))
    print('Teclas: A S D F G H J -> Colunas 0 1 2 3 4 5 6')
    
def is_valid_location(board, col):
    return board[0][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece
    
def remove_piece(board, row, col):
    board[row][col] = EMPTY
    
def get_valid_locations(board):
    return [c for c in range(COLUMNS) if is_valid_location(board, c)]

def winning_move(board, piece):
    # vertical & horizontal & diagonals
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                return True
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                return True
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                return True
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                return True
    return False

def is_terminal_node(board, player_piece, ai_piece):
    return (winning_move(board, player_piece) or
        winning_move(board, ai_piece) or
        len(get_valid_locations(board)) == 0)