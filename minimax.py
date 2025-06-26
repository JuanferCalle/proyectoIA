from zona_yoshi import (
    get_knight_moves,
    apply_move,
    evaluate_board,
    GREEN,
    RED,
    YOSHI_GREEN,
    YOSHI_RED,
    is_terminal

)


def minimax(board, green_pos, red_pos, depth, is_maximizing, alpha, beta, max_depth):
    if depth == max_depth:
        return evaluate_board(board), None

    if is_maximizing:  # Turno del Yoshi verde (máquina)
        best_value = float('-inf')
        best_move = None
        for move in get_knight_moves(board, green_pos):
            new_board, new_green_pos = apply_move(board, green_pos, move, GREEN)
            value, _ = minimax(new_board, new_green_pos, red_pos, depth + 1, False, alpha, beta, max_depth)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break  # Poda beta
        return best_value, best_move
    else:  # Turno del Yoshi rojo (jugador)
        best_value = float('inf')
        best_move = None
        for move in get_knight_moves(board, red_pos):
            new_board, new_red_pos = apply_move(board, red_pos, move, RED)
            value, _ = minimax(new_board, green_pos, new_red_pos, depth + 1, True, alpha, beta, max_depth)
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break  # Poda alfa
        return best_value, best_move
