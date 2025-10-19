import pygame
import time
import math
from Utils.utils import COLUMNS, ROWS

class UserInterface:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.font = pygame.font.Font(None, 28)
        self.large_font = pygame.font.Font(None, 36)
        # controla a animação de "IA pensando"
        self._thinking_start = None

    def draw_score(self, player1_score, player2_score, pos=(10,10)):
        score_text = f"Player: {player1_score}   AI: {player2_score}"
        text_surface = self.font.render(score_text, True, (0, 0, 0))
        self.screen.blit(text_surface, pos)

    def draw_buttons(self):
        # placeholder: podes desenhar retângulos com textos e detectar cliques no controller
        pass

    def _update_thinking_timer(self, controller):
        # inicia/reset timer quando controller.ai_thinking muda
        if controller.ai_thinking:
            if self._thinking_start is None:
                self._thinking_start = time.time()
        else:
            self._thinking_start = None

    def draw_status(self, controller, offset_x, offset_y, board_width):
        # controller deve expor: ai_thinking, turn, game_over
        if controller.game_over:
            msg = "Jogo terminado - Clique para reiniciar"
            surf = self.large_font.render(msg, True, (200, 50, 50))
            x = offset_x + (board_width - surf.get_width()) // 2

            # calcula y desejado e aplica clamp para manter dentro da tela
            desired_y = offset_y - 60
            screen_h = self.screen.get_height()
            top_margin = 8
            bottom_margin = 8
            y = max(top_margin, min(desired_y, screen_h - surf.get_height() - bottom_margin))

            self.screen.blit(surf, (x, y))
            return

        if controller.ai_thinking:
            msg = "IA jogando"
            color = (200, 120, 0)
        else:
            msg = "Sua vez" if controller.turn == 0 else "Vez da IA"
            color = (0, 0, 0)

        surf = self.font.render(msg, True, color)
        x = offset_x + (board_width - surf.get_width()) // 2

        # calcular y e clamp também para mensagens menores
        desired_y = offset_y - 28
        screen_h = self.screen.get_height()
        top_margin = 8
        bottom_margin = 8
        y = max(top_margin, min(desired_y, screen_h - surf.get_height() - bottom_margin))

        self.screen.blit(surf, (x, y))

        # salva posição/medida do texto para o spinner usar se necessário
        # (opcional: facilita posicionamento consistente)
        self._last_status_pos = (x, y, surf.get_width(), surf.get_height())

    def draw_thinking_spinner(self, offset_x, offset_y, board_width):
        # desenha três pontos animados ao lado da mensagem "IA jogando"
        if self._thinking_start is None:
            return
        now = time.time()
        elapsed = now - self._thinking_start

        # quantidade de pontos (0..3) cicla com o tempo
        dots_count = (int(elapsed * 2) % 4)  # 0,1,2,3

        # posicionamento: se temos a última posição do status, use-a para alinhar;
        # caso contrário, centraliza baseado no board_width
        if hasattr(self, "_last_status_pos"):
            text_x, text_y, text_w, text_h = self._last_status_pos
            text_right = text_x + text_w
            spinner_x = text_right + 12
            spinner_y = text_y + text_h // 2
        else:
            # fallback: centraliza e posiciona à direita do centro
            text_center_x = offset_x + board_width // 2
            spinner_x = text_center_x + 60
            spinner_y = offset_y - 12

        # parâmetros visuais
        dot_radius = 4
        spacing = 14
        base_color = (200, 120, 0)
        faded_color = (200, 120, 0, 90)  # alpha não usado diretamente em draw.circle

        # desenha até 3 pontos, ativando os primeiros `dots_count`
        for i in range(3):
            cx = spinner_x + i * spacing
            cy = spinner_y
            if i < dots_count:
                color = base_color
            else:
                # cor mais clara para ponto inativo (simula "desligado")
                color = (220, 190, 140)
            pygame.draw.circle(self.screen, color, (int(cx), int(cy)), dot_radius)

    def update(self, controller, offset_x, offset_y, board_width):
        # atualiza timer/estado e desenha HUD centralizada
        self._update_thinking_timer(controller)
        self.draw_score(0, 0, pos=(offset_x, offset_y - 90))
        self.draw_status(controller, offset_x, offset_y, board_width)
        # desenha spinner apenas quando ai_thinking ativo
        if controller.ai_thinking:
            self.draw_thinking_spinner(offset_x, offset_y, board_width)
        self.draw_buttons()