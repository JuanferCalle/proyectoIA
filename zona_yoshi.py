import numpy as np
import random

# Configuración del tablero
CELL_SIZE = 60
BOARD_SIZE = 8

# Tipos de casillas
NORMAL = 1
SPECIAL = 2
GREEN = 3
RED = 4
YOSHI_GREEN = 5
YOSHI_RED = 6
POSSIBLE_MOVE = 7  # Nuevo tipo para movimientos posibles (amarillo)

# Movimientos del caballo
KNIGHT_MOVES = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)]

# Zonas especiales (esquinas + celdas adyacentes)
SPECIAL_ZONES = {
    "top_left": [(0, 0), (0, 1), (0,2), (1, 0), (2, 0)],
    "top_right": [(0, 7), (0, 6), (0,5), (1, 7), (2, 7)],
    "bottom_left": [(7, 0), (6, 0), (5,0), (7, 1), (7, 2)],
    "bottom_right": [(7, 7), (6, 7), (5,7), (7,6), (7,5)]
}

def in_bounds(x, y):
    """Verifica si una posición está dentro del tablero"""
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def crear_tablero():
    """Crea un tablero predefinido con posiciones fijas"""
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

def get_knight_moves(board, pos):
    """Obtiene todos los movimientos válidos de caballo desde una posición"""
    x, y = pos
    moves = []
    for dx, dy in KNIGHT_MOVES:
        nx, ny = x + dx, y + dy
        if in_bounds(nx, ny) and board[nx][ny] not in (GREEN, RED, YOSHI_GREEN, YOSHI_RED, POSSIBLE_MOVE):
            moves.append((nx, ny))
    return moves

def show_possible_moves(board, yoshi_pos):
    """Muestra los movimientos posibles del Yoshi rojo en amarillo"""
    new_board = clone_board(board)
    possible_moves = get_knight_moves(board, yoshi_pos)
    
    # Marcar los movimientos posibles en amarillo
    for x, y in possible_moves:
        if new_board[x][y] not in (YOSHI_GREEN, YOSHI_RED):
            new_board[x][y] = POSSIBLE_MOVE
    
    return new_board, possible_moves

def clear_possible_moves(board):
    """Limpia los movimientos posibles del tablero"""
    new_board = clone_board(board)
    # Restaurar las casillas que estaban marcadas como movimientos posibles
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if new_board[x][y] == POSSIBLE_MOVE:
                special_positions = set(pos for zona in SPECIAL_ZONES.values() for pos in zona)
                if (x, y) in special_positions:
                    new_board[x][y] = SPECIAL
                else:
                    new_board[x][y] = NORMAL
    return new_board

def clone_board(board):
    """Crea una copia profunda del tablero"""
    return np.copy(board)

def apply_move(board, yoshi_pos, move, player):
    """Aplica un movimiento al tablero y devuelve el nuevo estado"""
    # Primero limpiamos los movimientos posibles
    new_board = clear_possible_moves(board)
    x, y = yoshi_pos
    new_x, new_y = move

    # Obtener el tablero original para verificar qué tipo de casilla era originalmente
    original_board = crear_tablero()
    
    # Restaurar celda anterior a su estado original
    if new_board[x][y] == YOSHI_GREEN:
        special_positions = set(pos for zona in SPECIAL_ZONES.values() for pos in zona)
        if (x, y) in special_positions and original_board[x][y] == SPECIAL:
            new_board[x][y] = GREEN
        else:
            new_board[x][y] = NORMAL
    elif new_board[x][y] == YOSHI_RED:
        special_positions = set(pos for zona in SPECIAL_ZONES.values() for pos in zona)
        if (x, y) in special_positions and original_board[x][y] == SPECIAL:
            new_board[x][y] = RED
        else:
            new_board[x][y] = NORMAL

    special_positions = set(pos for zona in SPECIAL_ZONES.values() for pos in zona)
    valor_original = original_board[new_x][new_y]
    
    if (new_x, new_y) in special_positions and valor_original == SPECIAL:
        new_board[new_x][new_y] = GREEN if player == GREEN else RED

    # Colocar Yoshi encima
    new_board[new_x][new_y] = YOSHI_GREEN if player == GREEN else YOSHI_RED

    return new_board, (new_x, new_y)

def contar_casillas(board):
    """
    Cuenta el número total de casillas verdes y rojas pintadas en el tablero.
    Devuelve una tupla: (cantidad_verde, cantidad_rojo)
    """
    green_cells = np.sum(board == GREEN)
    red_cells = np.sum(board == RED)
    return green_cells, red_cells

def evaluate_board(board):
    """Función de evaluación heurística para el algoritmo minimax"""
    green_positions = np.argwhere(board == YOSHI_GREEN)
    red_positions = np.argwhere(board == YOSHI_RED)

    if green_positions.size == 0 or red_positions.size == 0:
        if green_positions.size == 0:
            return float('-inf')  # Verde perdió
        return float('inf')      # Rojo perdió

    green_pos = tuple(green_positions[0])
    red_pos = tuple(red_positions[0])

    cell_scores = {
        GREEN: np.sum(board == GREEN),
        RED: np.sum(board == RED)
    }

    mobility = {
        GREEN: len(get_knight_moves(board, green_pos)),
        RED: len(get_knight_moves(board, red_pos))
    }

    return (
        2 * (cell_scores[GREEN] - cell_scores[RED]) +  # Casillas pintadas
        0.5 * (mobility[GREEN] - mobility[RED])       # Movilidad
    )

def is_terminal(board):
    """Determina si el juego ha terminado (no quedan zonas especiales sin pintar)"""
    return not np.any(board == SPECIAL)

if __name__ == "__main__":
    print("Este archivo contiene las reglas del juego y no debe ejecutarse directamente.")
    print("Ejecuta 'control_juego.py' para iniciar el juego.")
