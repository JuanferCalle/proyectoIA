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
        if in_bounds(nx, ny) and board[nx][ny] not in (GREEN, RED, YOSHI_GREEN, YOSHI_RED):
            moves.append((nx, ny))
    return moves

def clone_board(board):
    """Crea una copia profunda del tablero"""
    return np.copy(board)

def apply_move(board, yoshi_pos, move, player):
    """Aplica un movimiento al tablero y devuelve el nuevo estado"""
    new_board = clone_board(board)
    x, y = yoshi_pos
    new_x, new_y = move

    # Restaurar celda anterior
    debajo = GREEN if board[x][y] == YOSHI_GREEN else RED if board[x][y] == YOSHI_RED else NORMAL
    new_board[x][y] = debajo

    # Pintar solo si está en una posición válida y originalmente era SPECIAL
    # Pintar solo si era SPECIAL y la posición está dentro de las coordenadas especiales
    special_positions = set(pos for zona in SPECIAL_ZONES.values() for pos in zona)
    valor_original = board[new_x][new_y]
    if (new_x, new_y) in special_positions and valor_original == SPECIAL:
        new_board[new_x][new_y] = GREEN if player == GREEN else RED

    # Colocar Yoshi encima
    new_board[new_x][new_y] = YOSHI_GREEN if player == GREEN else YOSHI_RED

    return new_board, (new_x, new_y)

def contar_zonas(board):
    """Cuenta las zonas especiales ganadas por cada jugador"""
    green_zones = 0
    red_zones = 0
    
    for zone in SPECIAL_ZONES.values():
        green_count = sum(1 for x, y in zone if board[x][y] == GREEN)
        red_count = sum(1 for x, y in zone if board[x][y] == RED)
        
        if green_count > red_count:
            green_zones += 1
        elif red_count > green_count:
            red_zones += 1
            
    return green_zones, red_zones

def evaluate_board(board):
    """Función de evaluación heurística para el algoritmo minimax"""
    green_positions = np.argwhere(board == YOSHI_GREEN)
    red_positions = np.argwhere(board == YOSHI_RED)

    # Caso terminal: algún Yoshi no existe
    if green_positions.size == 0 or red_positions.size == 0:
        if green_positions.size == 0:
            return float('-inf')  # Verde perdió
        return float('inf')      # Rojo perdió

    green_pos = tuple(green_positions[0])
    red_pos = tuple(red_positions[0])

    # Métricas de evaluación
    zone_scores = contar_zonas(board)
    cell_scores = {
        GREEN: np.sum(board == GREEN),
        RED: np.sum(board == RED)
    }

    # Progreso en zonas no decididas
    zone_progress = 0
    for zone in SPECIAL_ZONES.values():
        green_count = sum(1 for x, y in zone if board[x][y] == GREEN)
        red_count = sum(1 for x, y in zone if board[x][y] == RED)
        if green_count + red_count < 4:  # Zona no completada
            zone_progress += (green_count - red_count)

    # Movilidad (movimientos posibles)
    mobility = {
        GREEN: len(get_knight_moves(board, green_pos)),
        RED: len(get_knight_moves(board, red_pos))
    }

    # Función de evaluación ponderada
    return (
        100 * (zone_scores[0] - zone_scores[1]) +  # Zonas ganadas
        5 * zone_progress +                       # Progreso en zonas
        2 * (cell_scores[GREEN] - cell_scores[RED]) +  # Casillas pintadas
        0.5 * (mobility[GREEN] - mobility[RED])   # Movilidad
    )

def is_terminal(board):
    """Determina si el juego ha terminado (no quedan zonas especiales sin pintar)"""
    return not np.any(board == SPECIAL)

if __name__ == "__main__":
    print("Este archivo contiene las reglas del juego y no debe ejecutarse directamente.")
    print("Ejecuta 'control_juego.py' para iniciar el juego.")
