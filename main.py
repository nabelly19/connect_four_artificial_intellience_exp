import time
from GameObject.board import (
    create_board, print_board,
    get_next_open_row, drop_piece,
    winning_move, is_terminal_node
)
from GameObject.agent import pick_best_move, evaluate_board
from Utils.utils import PLAYER_PIECE, AI_PIECE, KEY_TO_COL


def game_loop(level="intermediario"):
    print(f"\n🎮 Iniciando Connect Four - Nível {level.upper()} 🎮\n")

    board = create_board()
    game_over = False
    turn = 0  # 0 = Humano (vermelho), 1 = Agente (amarelo)

    print_board(board)

    while not game_over:
        # ======== TURNO HUMANO ========
        if turn == 0:
            col_input = input("👉 Sua jogada (A S D F G H J): ")
            if col_input not in KEY_TO_COL:
                print("Entrada inválida. Use as teclas corretas.")
                continue

            col = KEY_TO_COL[col_input]
            row = get_next_open_row(board, col)
            if row is None:
                print("⚠️ Coluna cheia, tente outra.")
                continue

            drop_piece(board, row, col, PLAYER_PIECE)
            print_board(board)

            if winning_move(board, PLAYER_PIECE):
                print("🏆 Você venceu! Parabéns!")
                game_over = True
            elif is_terminal_node(board, PLAYER_PIECE, AI_PIECE):
                print("🤝 Empate!")
                game_over = True

            turn = 1  # passa a vez pro agente

        # ======== TURNO AGENTE ========
        else:
            print("\n🤖 Agente está pensando...")
            start_time = time.time()
            col, value, elapsed = pick_best_move(board, level, time_limit=3)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            print_board(board)
            print(f"⏱️ Tempo gasto: {elapsed:.3f}s")
            print(f"📊 Avaliação do estado: {evaluate_board(board, level)}")

            if winning_move(board, AI_PIECE):
                print("🤖 O Agente venceu! Mais sorte na próxima 😎")
                game_over = True
            elif is_terminal_node(board, PLAYER_PIECE, AI_PIECE):
                print("🤝 Empate!")
                game_over = True

            turn = 0  # volta para o humano


if __name__ == "__main__":
    print("Escolha o nível do agente:")
    print("1 - Iniciante")
    print("2 - Intermediário")
    print("3 - Profissional")
    choice = input("Digite 1/2/3: ")

    if choice == "1":
        level = "iniciante"
    elif choice == "2":
        level = "intermediario"
    else:
        level = "profissional"

    game_loop(level)
