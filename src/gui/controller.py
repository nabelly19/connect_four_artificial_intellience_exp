import pygame
import threading
import queue
import time

from Game.board import create_board, get_next_open_row, drop_piece, winning_move, is_terminal_node
from Game.agent import pick_best_move
from Utils.utils import ROWS, COLUMNS, PLAYER_PIECE, AI_PIECE, EMPTY
from gui.ui import UserInterface

class GameController:
    def __init__(self, level="intermediario", ai_time_limit=3):
        self.level = level
        self.ai_time_limit = ai_time_limit
        self.board = create_board()
        self.turn = 0  # 0 = humano, 1 = ai
        self.game_over = False
        self._ai_q = queue.Queue()
        self._ai_thread = None
        self.ai_thinking = False

    def human_move(self, col):
        if self.game_over or self.turn != 0:
            return False
        row = get_next_open_row(self.board, col)
        if row is None:
            return False
        drop_piece(self.board, row, col, PLAYER_PIECE)
        if winning_move(self.board, PLAYER_PIECE) or is_terminal_node(self.board, PLAYER_PIECE, AI_PIECE):
            self.game_over = True
        else:
            self.turn = 1
            self.ai_thinking = True       # define imediatamente após a jogada humana
            self._start_ai()
        return True

    def _start_ai(self):
        if self._ai_thread and self._ai_thread.is_alive():
            return
        snapshot = self.board.copy()
        def worker(board_snapshot, out_q):
            time.sleep(1.5)  # atraso de 2s antes de a IA começar a pensar
            col, value, elapsed = pick_best_move(board_snapshot, self.level, time_limit=self.ai_time_limit)
            out_q.put((col, value, elapsed))
        self._ai_thread = threading.Thread(target=worker, args=(snapshot, self._ai_q), daemon=True)
        self._ai_thread.start()

    def poll_ai(self):
        if self.game_over or self.turn != 1:
            return None
        try:
            col, value, elapsed = self._ai_q.get_nowait()
        except queue.Empty:
            return None
        # IA terminou — desligar o indicador
        self.ai_thinking = False
        row = get_next_open_row(self.board, col)
        if row is not None:
            drop_piece(self.board, row, col, AI_PIECE)
            if winning_move(self.board, AI_PIECE) or is_terminal_node(self.board, PLAYER_PIECE, AI_PIECE):
                self.game_over = True
            else:
                self.turn = 0
        return (col, value, elapsed)

def draw_board(screen, board, tile_size):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 20, 60)
    YELLOW = (240, 200, 0)

    screen.fill(WHITE)

    board_width = COLUMNS * tile_size
    board_height = (ROWS + 1) * tile_size
    screen_width, screen_height = screen.get_size()

    # Calcula as margens para centralizar
    offset_x = (screen_width - board_width) // 2
    offset_y = (screen_height - board_height) // 2

    for r in range(ROWS):
        for c in range(COLUMNS):
            x = offset_x + c * tile_size
            y = offset_y + (r + 1) * tile_size  # linha extra no topo
            pygame.draw.rect(screen, WHITE, (x, y, tile_size, tile_size))

            piece = board[r, c]
            color = BLACK
            if piece == PLAYER_PIECE:
                color = RED
            elif piece == AI_PIECE:
                color = YELLOW

            pygame.draw.circle(screen, color, (x + tile_size // 2, y + tile_size // 2), tile_size // 2 - 6)

def run_pygame(level="intermediario"):
    pygame.init()
    # tamanho do tile pode ser ajustado; manter responsivo simples
    tile_size = 60
    width = COLUMNS * tile_size + 100
    height = (ROWS + 1) * tile_size + 100
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect Four")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    ctrl = GameController(level=level)
    ui = UserInterface(screen, ctrl.board)
    running = True
    hover_x = None

    board_width = COLUMNS * tile_size
    board_height = (ROWS + 1) * tile_size
    screen_width, screen_height = screen.get_size()
    offset_x = (screen_width - board_width) // 2
    offset_y = (screen_height - board_height) // 2

    # mensagem temporária (ex.: coluna cheia) com timeout
    temp_msg = None
    temp_msg_until = 0.0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEMOTION:
                hover_x = event.pos[0]

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # se jogo terminado: clique reinicia
                if ctrl.game_over:
                    ctrl = GameController(level=level)
                    ui = UserInterface(screen, ctrl.board)
                    temp_msg = None
                    continue

                # só aceitar clicks dentro da área do tabuleiro
                if not (offset_x <= mx < offset_x + board_width and
                        offset_y <= my < offset_y + board_height):
                    continue

                # se não for turno do humano, ignora
                if ctrl.turn != 0 or ctrl.ai_thinking:
                    temp_msg = "Aguarde a vez da IA"
                    temp_msg_until = time.time() + 1.2
                    continue

                # calcula coluna com base no offset
                col = int((mx - offset_x) // tile_size)
                if col < 0 or col >= COLUMNS:
                    continue

                moved = ctrl.human_move(col)
                if not moved:
                    temp_msg = "Jogada inválida / Coluna cheia"
                    temp_msg_until = time.time() + 1.5

        # checa se a IA terminou (não bloqueante)
        ai_result = ctrl.poll_ai()
        if ai_result:
            col, value, elapsed = ai_result
            # pode-se setar uma mensagem breve ou animar peça; aqui apenas log
            temp_msg = f"IA jogou coluna {col} em {elapsed:.2f}s"
            temp_msg_until = time.time() + 1.8

        # desenha tabuleiro primeiro
        draw_board(screen, ctrl.board, tile_size)

        # preview da peça no topo (mostra onde cairia)
        if hover_x is not None and not ctrl.game_over and not ctrl.ai_thinking:
            col = int((hover_x - offset_x) // tile_size)
            if 0 <= col < COLUMNS:
                x = offset_x + col * tile_size + tile_size // 2
                y = offset_y + tile_size // 2
                color = (220, 20, 60) if ctrl.turn == 0 else (240, 200, 0)
                pygame.draw.circle(screen, color, (x, y), tile_size // 2 - 6)

        # HUD via UserInterface (sobrepõe ao tabuleiro)
        ui.update(ctrl, offset_x, offset_y, board_width)

        # desenha mensagem temporária se existir
        if temp_msg and time.time() < temp_msg_until:
            surf = font.render(temp_msg, True, (255, 255, 255))
            screen.blit(surf, (offset_x, offset_y - 60))
        else:
            temp_msg = None

        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

    pygame.quit()