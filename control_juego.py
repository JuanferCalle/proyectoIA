import pygame
import sys
import numpy as np
from zona_yoshi import *
from GUI_yoshi import draw_board
from minimax import minimax
from menu_niveles import seleccionar_nivel
from zona_yoshi import contar_zonas_ganadas

pygame.init()

# Configuración inicial
nivel = seleccionar_nivel()
screen = pygame.display.set_mode((CELL_SIZE * BOARD_SIZE, CELL_SIZE * BOARD_SIZE + 60))
pygame.display.set_caption("Yoshi's Zones")

# Inicializar tablero SOLO con normales y especiales
board = crear_tablero()

# Poner los Yoshis en posiciones aleatorias válidas
board, green_pos, red_pos = posiciones_iniciales_aleatorias(board)

# Debug: Asegúrate que los Yoshis no estén en zonas especiales ni coincidan
zonas_especiales = set(pos for zona in SPECIAL_ZONES.values() for pos in zona)
green_pos = tuple(np.argwhere(board == YOSHI_GREEN)[0])
red_pos = tuple(np.argwhere(board == YOSHI_RED)[0])
assert green_pos not in zonas_especiales, f"Yoshi verde en zona especial: {green_pos}"
assert red_pos not in zonas_especiales, f"Yoshi rojo en zona especial: {red_pos}"
assert green_pos != red_pos, "¡Los Yoshis coinciden!"
print("DEBUG: Yoshi verde en:", green_pos)
print("DEBUG: Yoshi rojo en:", red_pos)


# Determinar profundidad por nivel
if nivel == "facil":
    level_depth = 2
elif nivel == "medio":
    level_depth = 4
else:
    level_depth = 6

def move_yoshi_red(new_pos):
    global board
    try:
        red_pos = tuple(np.argwhere(board == YOSHI_RED)[0])
        if in_bounds(*new_pos) and board[new_pos[0]][new_pos[1]] not in (YOSHI_GREEN, YOSHI_RED, GREEN, RED):
            board, _ = apply_move(board, red_pos, new_pos, RED)
            return True
    except IndexError:
        print("Error: Yoshi Rojo no encontrado")
    return False

def machine_turn():
    global board
    try:
        green_pos = tuple(np.argwhere(board == YOSHI_GREEN)[0])
        red_pos = tuple(np.argwhere(board == YOSHI_RED)[0])
        
        _, best_move = minimax(board, green_pos, red_pos, 0, True, float('-inf'), float('inf'), level_depth)
        
        if best_move:
            board, _ = apply_move(board, green_pos, best_move, GREEN)
            return True
    except IndexError:
        print("Error: Yoshi Verde no encontrado")
    return False

def show_final_message():
    zonas_verde, zonas_rojo = contar_zonas_ganadas(board)
    if zonas_verde > zonas_rojo:
        message = "¡Gana el Yoshi Verde!"
    elif zonas_rojo > zonas_verde:
        message = "¡Gana el Yoshi Rojo!"
    else:
        message = "¡Empate!"
    
    font = pygame.font.SysFont(None, 48)
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(BOARD_SIZE*CELL_SIZE/2, (60 + CELL_SIZE*BOARD_SIZE)/2))

    
    s = pygame.Surface((BOARD_SIZE*CELL_SIZE, BOARD_SIZE*CELL_SIZE), pygame.SRCALPHA)
    s.fill((255, 255, 255, 128))
    screen.blit(s, (0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

#    Bucle principal
running = True
turno_humano = False  # Máquina empieza primero
display_board = board  # Tablero que se muestra (puede incluir movimientos posibles)

# Primer turno de la máquina
if not is_terminal(board):
    machine_turn()
    turno_humano = True

while running:
    # Si es turno del humano, mostrar movimientos posibles
    if turno_humano:
        try:
            red_pos = tuple(np.argwhere(board == YOSHI_RED)[0])
            display_board, possible_moves = show_possible_moves(board, red_pos)
        except IndexError:
            display_board = board
            possible_moves = []
    else:
        # Si es turno de la máquina, limpiar movimientos posibles
        display_board = clear_possible_moves(board)
        possible_moves = []
    
    draw_board(screen, display_board)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and turno_humano:
            try:
                mouse_pos = pygame.mouse.get_pos()
                clicked_col = mouse_pos[0] // CELL_SIZE
                if mouse_pos[1] < 60:
                    continue  # Ignorar clics fuera del tablero

                clicked_row = (mouse_pos[1] - 60) // CELL_SIZE
                
                red_pos = tuple(np.argwhere(board == YOSHI_RED)[0])
                possible_moves = get_knight_moves(board, red_pos)
                
                if (clicked_row, clicked_col) in possible_moves:
                    if move_yoshi_red((clicked_row, clicked_col)):
                        # Limpiar movimientos posibles antes de revisar si terminó
                        board = clear_possible_moves(board)

                        # Revisar si el juego terminó INMEDIATAMENTE después del movimiento humano
                        if is_terminal(board):
                            show_final_message()
                            running = False
                            break  # Sal de eventos para evitar doble mensaje

                        turno_humano = False

                        # Turno de la máquina (si no terminó el juego)
                        pygame.time.delay(500)
                        if machine_turn():
                            turno_humano = True

                        # Después del movimiento de la máquina, revisar si terminó (por si fue la IA la que cerró el juego)
                        if is_terminal(board):
                            show_final_message()
                            running = False
                            break
            except IndexError:
                print("Error en el movimiento del jugador")
                continue

    pygame.display.flip()

pygame.quit()
sys.exit()
