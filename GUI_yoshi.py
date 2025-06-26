import pygame
from zona_yoshi import CELL_SIZE, BOARD_SIZE, SPECIAL, GREEN, RED, YOSHI_GREEN, YOSHI_RED

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN_COLOR = (50, 205, 50)
RED_COLOR = (220, 20, 60)
SPECIAL_COLOR = (173, 216, 230)

def draw_board(screen, board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x, y = j * CELL_SIZE, i * CELL_SIZE
            cell = board[i][j]
            color = WHITE

            if cell == SPECIAL:
                color = SPECIAL_COLOR
            elif cell == GREEN:
                color = GREEN_COLOR
            elif cell == RED:
                color = RED_COLOR
            elif cell == YOSHI_GREEN:
                color = GREEN_COLOR
            elif cell == YOSHI_RED:
                color = RED_COLOR

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

    pygame.display.flip()
