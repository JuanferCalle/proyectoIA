import pygame
import sys
import numpy as np

from zona_yoshi import *
from GUI_yoshi import draw_board
from minimax import minimax
from menu_niveles import seleccionar_nivel

pygame.init()

nivel = seleccionar_nivel()

screen = pygame.display.set_mode((CELL_SIZE * BOARD_SIZE, CELL_SIZE * BOARD_SIZE))
pygame.display.set_caption("Yoshi's Zones")

board = crear_tablero()

# Determinar profundidad por nivel
if nivel == "facil":
    level_depth = 1
elif nivel == "medio":
    level_depth = 3
else:
    level_depth = 5

# Función para mover al Yoshi rojo si es posible
def move_yoshi_red(move):
    global board
    red_pos = tuple(np.argwhere(board == YOSHI_RED)[0])
    new_x, new_y = red_pos[0] + move[0], red_pos[1] + move[1]

    if in_bounds(new_x, new_y) and board[new_x][new_y] not in (YOSHI_GREEN, YOSHI_RED, GREEN, RED):
        board, _ = apply_move(board, red_pos, (new_x, new_y), RED)

# Bucle principal
running = True
while running:
    draw_board(screen, board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            direction = None
            if event.key in [pygame.K_KP1, pygame.K_1]:
                direction = (2, -1)
            elif event.key in [pygame.K_KP2, pygame.K_2]:
                direction = (1, -2)
            elif event.key in [pygame.K_KP3, pygame.K_3]:
                direction = (1, 2)
            elif event.key in [pygame.K_KP4, pygame.K_4]:
                direction = (2, 1)
            elif event.key in [pygame.K_KP5, pygame.K_5]:
                direction = (-2, -1)
            elif event.key in [pygame.K_KP6, pygame.K_6]:
                direction = (-2, 1)
            elif event.key in [pygame.K_KP7, pygame.K_7]:
                direction = (-1, -2)
            elif event.key in [pygame.K_KP8, pygame.K_8]:
                direction = (-1, 2)

            if direction:
                red_positions = np.argwhere(board == YOSHI_RED)
                if red_positions.size > 0:
                    move_yoshi_red(direction)

                    if not is_terminal(board):
                        green_positions = np.argwhere(board == YOSHI_GREEN)
                        red_positions = np.argwhere(board == YOSHI_RED)

                        if green_positions.size > 0 and red_positions.size > 0:
                            green_pos = tuple(green_positions[0])
                            red_pos = tuple(red_positions[0])

                            _, best_move = minimax(board, green_pos, red_pos, 0, True, float('-inf'), float('inf'), level_depth)
                            if best_move:
                                board, _ = apply_move(board, green_pos, best_move, GREEN)

            if is_terminal(board):
                print("¡Fin del juego!")
                running = False
