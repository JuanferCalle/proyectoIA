import numpy as np
from itertools import product

# zona_yoshi.py

import numpy as np

CELL_SIZE = 60     # Tamaño de cada celda del tablero en píxeles
BOARD_SIZE = 8     # Tamaño del tablero (8x8)

# Tipos de casillas
NORMAL = 1
SPECIAL = 2
GREEN = 3
RED = 4
YOSHI_GREEN = 5
YOSHI_RED = 6

# Movimiento de caballo
KNIGHT_MOVES = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)]

# Tablero inicial
def crear_tablero():
    return np.array([
        [2, 3, 2, 1, 1, 4, 2, 2],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [3, 1, 5, 1, 1, 1, 1, 2],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 6, 1, 1, 1, 1],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [2, 2, 2, 1, 1, 2, 2, 2],
    ])

# Zonas especiales (esquinas + celdas adyacentes)
SPECIAL_ZONES = {
    "top_left": [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
    "top_right": [(0, 7), (0, 6), (1, 7), (1, 6), (2, 7)],
    "bottom_left": [(7, 0), (6, 0), (7, 1), (6, 1), (5, 0)],
    "bottom_right": [(7, 7), (6, 7), (7, 6), (6, 6), (5, 7)]
}

def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def get_knight_moves(board, pos):
    x, y = pos
    moves = []
    for dx, dy in KNIGHT_MOVES:
        nx, ny = x + dx, y + dy
        if in_bounds(nx, ny) and board[nx][ny] not in (GREEN, RED, YOSHI_GREEN, YOSHI_RED):
            moves.append((nx, ny))
    return moves

def clone_board(board):
    return np.copy(board)

def apply_move(board, yoshi_pos, move, player):
    new_board = clone_board(board)
    x, y = yoshi_pos
    new_x, new_y = move

    # Quitar Yoshi anterior
    if player == GREEN:
        new_board[x][y] = NORMAL if new_board[x][y] == YOSHI_GREEN else new_board[x][y]
        new_board[new_x][new_y] = YOSHI_GREEN
    else:
        new_board[x][y] = NORMAL if new_board[x][y] == YOSHI_RED else new_board[x][y]
        new_board[new_x][new_y] = YOSHI_RED

    # Pintar si es casilla especial sin pintar
    if board[new_x][new_y] == SPECIAL:
        new_board[new_x][new_y] = player

    return new_board, (new_x, new_y)

def evaluate_board(board):
    green_positions = np.argwhere(board == YOSHI_GREEN)
    red_positions = np.argwhere(board == YOSHI_RED)

    if green_positions.size == 0 or red_positions.size == 0:
        if green_positions.size == 0:
            return float('-inf')  # Verde perdió
        else:
            return float('inf')   # Rojo perdió

    green_pos = tuple(green_positions[0])
    red_pos = tuple(red_positions[0])

    # Inicialización de métricas
    cell_scores = {GREEN: 0, RED: 0}
    zone_scores = {GREEN: 0, RED: 0}
    mobility = {GREEN: 0, RED: 0}

    # Casillas pintadas
    cell_scores[GREEN] = np.sum(board == GREEN)
    cell_scores[RED] = np.sum(board == RED)

    # Zonas especiales ganadas
    for zone in SPECIAL_ZONES.values():
        green_count = sum(1 for x, y in zone if board[x][y] == GREEN)
        red_count = sum(1 for x, y in zone if board[x][y] == RED)
        if green_count >= 3:
            zone_scores[GREEN] += 1
        elif red_count >= 3:
            zone_scores[RED] += 1

    # Movilidad (número de movimientos disponibles)
    mobility[GREEN] = len(get_knight_moves(board, green_pos))
    mobility[RED] = len(get_knight_moves(board, red_pos))

    # Función de evaluación final
    return (
        10 * (zone_scores[GREEN] - zone_scores[RED]) +
        2 * (cell_scores[GREEN] - cell_scores[RED]) +
        (mobility[GREEN] - mobility[RED])
    )

def is_terminal(board):
    return not np.any(board == SPECIAL)
if __name__ == "__main__":
    print("zona_yoshi.py se ejecutó directamente (no como módulo)")
