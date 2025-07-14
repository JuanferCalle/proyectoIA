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

special_positions = set(pos for zona in SPECIAL_ZONES.values() for pos in zona)

def in_bounds(x, y):
    """Verifica si una posición está dentro del tablero"""
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def crear_tablero():
    board = np.full((BOARD_SIZE, BOARD_SIZE), NORMAL)
    for zona in SPECIAL_ZONES.values():
        for x, y in zona:
            board[x][y] = SPECIAL
    return board


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
    """
    Mueve un Yoshi, pinta la casilla especial y actualiza el tablero.
    - Restaura la casilla anterior.
    - Pinta la nueva si es SPECIAL.
    - Coloca el Yoshi.
    """
    new_board = clone_board(board)
    x, y = yoshi_pos
    new_x, new_y = move

    # Restaurar casilla anterior: si era SPECIAL y pintada, conserva el color
    if (x, y) in special_positions:
        if board[x][y] == YOSHI_GREEN or board[x][y] == GREEN:
            new_board[x][y] = GREEN
        elif board[x][y] == YOSHI_RED or board[x][y] == RED:
            new_board[x][y] = RED
        else:
            new_board[x][y] = SPECIAL
    else:
        new_board[x][y] = NORMAL

    # Pintar la nueva casilla si es SPECIAL
    if (new_x, new_y) in special_positions:
        new_board[new_x][new_y] = GREEN if player == GREEN else RED

    # Colocar sprite del Yoshi encima
    new_board[new_x][new_y] = YOSHI_GREEN if player == GREEN else YOSHI_RED

    return new_board, (new_x, new_y)

def contar_casillas(board):
    """
    Cuenta cuántas casillas especiales ha pintado cada jugador,
    incluyendo las que ocupan ahora con su Yoshi.
    """
    green_cells = np.sum(board == GREEN)
    red_cells   = np.sum(board == RED)

    # +1 adicional por cada YOSHI_* que esté sobre una casilla special pintada
    for (x, y) in special_positions:
        if board[x][y] == YOSHI_GREEN:
            green_cells += 1
        elif board[x][y] == YOSHI_RED:
            red_cells += 1

    return green_cells, red_cells

def evaluate_board(board):
    green_positions = np.argwhere(board == YOSHI_GREEN)
    red_positions = np.argwhere(board == YOSHI_RED)

    if green_positions.size == 0:
        return float('-inf')  
    if red_positions.size == 0:
        return float('inf')   

    green_pos = tuple(green_positions[0])
    red_pos = tuple(red_positions[0])

    green_cells = np.sum(board == GREEN)
    red_cells = np.sum(board == RED)

    green_moves = len(get_knight_moves(board, green_pos))
    red_moves = len(get_knight_moves(board, red_pos))

    if green_moves == 0:
        return float('-inf')
    if red_moves == 0:
        return float('inf')

    # Opcional: valorar casillas especiales pintadas
    special_positions = set(pos for zona in SPECIAL_ZONES.values() for pos in zona)
    special_green = sum(1 for x, y in special_positions if board[x, y] == GREEN)
    special_red = sum(1 for x, y in special_positions if board[x, y] == RED)

    # Heurística ponderada
    score = (
        3 * (green_cells - red_cells) +
        1 * (green_moves - red_moves) +
        2 * (special_green - special_red)
    )

    return score

def is_terminal(board):
    """Determina si el juego ha terminado (no quedan zonas especiales sin pintar)"""
    return not np.any(board == SPECIAL)

if __name__ == "__main__":
    print("Este archivo contiene las reglas del juego y no debe ejecutarse directamente.")
    print("Ejecuta 'control_juego.py' para iniciar el juego.")

def posiciones_iniciales_aleatorias(board):
    posiciones_especiales = set(pos for zona in SPECIAL_ZONES.values() for pos in zona)
    posiciones_validas = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)
                          if (i, j) not in posiciones_especiales]
    pos_yoshi_verde, pos_yoshi_rojo = random.sample(posiciones_validas, 2)
    # LIMPIA CUALQUIER YOSHI DEL TABLERO
    board[board == YOSHI_GREEN] = NORMAL
    board[board == YOSHI_RED] = NORMAL
    board[pos_yoshi_verde] = YOSHI_GREEN
    board[pos_yoshi_rojo] = YOSHI_RED
    return board, pos_yoshi_verde, pos_yoshi_rojo



def contar_zonas_ganadas(board):
    zonas_verde = 0
    zonas_rojo = 0
    for zona in SPECIAL_ZONES.values():
        verdes = sum(1 for x, y in zona if board[x][y] == GREEN)
        rojas = sum(1 for x, y in zona if board[x][y] == RED)
        if verdes + rojas == 5:  # La zona ya está completamente pintada
            if verdes > rojas:
                zonas_verde += 1
            elif rojas > verdes:
                zonas_rojo += 1
            # Empate en la zona: nadie suma
    return zonas_verde, zonas_rojo
