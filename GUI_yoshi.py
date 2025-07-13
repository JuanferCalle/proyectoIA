import pygame
from zona_yoshi import *
# Colores
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN_COLOR = (50, 205, 50)
RED_COLOR = (220, 20, 60)
SPECIAL_COLOR = (173, 216, 230)
HIGHLIGHT = (255, 255, 0, 150)  # Amarillo semitransparente

# Altura para marcador
TOP_MARGIN = 60

# Cargar imágenes de Yoshi
yoshi_verde_img = pygame.image.load("yoshi_verde.jpg")
yoshi_rojo_img = pygame.image.load("Yoshi_rojo.jpg")

# Escalar al tamaño de celda
yoshi_verde_img = pygame.transform.scale(yoshi_verde_img, (CELL_SIZE, CELL_SIZE))
yoshi_rojo_img = pygame.transform.scale(yoshi_rojo_img, (CELL_SIZE, CELL_SIZE))

def draw_board(screen, board, selected_pos=None, possible_moves=None):
    screen.fill(WHITE)
    
    
    # Dibujar tablero
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x, y = j * CELL_SIZE, TOP_MARGIN + i * CELL_SIZE
            cell = board[i][j]
            color = WHITE

            if cell == SPECIAL:
                color = SPECIAL_COLOR
            elif cell == POSSIBLE_MOVE:
                color = HIGHLIGHT
            elif cell == GREEN:
                color = GREEN_COLOR
            elif cell == RED:
                color = RED_COLOR
            
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

            # Resaltar movimientos posibles
            if possible_moves and (i, j) in possible_moves:
                highlight = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                highlight.fill(HIGHLIGHT)
                screen.blit(highlight, (x, y))

            # Resaltar posición seleccionada
            if selected_pos == (i, j):
                pygame.draw.rect(screen, (255, 215, 0), (x, y, CELL_SIZE, CELL_SIZE), 3)

            # Dibujar imágenes de Yoshi
            if cell == YOSHI_GREEN:
                screen.blit(yoshi_verde_img, (x, y))
            elif cell == YOSHI_RED:
                screen.blit(yoshi_rojo_img, (x, y))

    # Mostrar marcador arriba
    font = pygame.font.SysFont(None, 36)
    green_zones, red_zones = contar_casillas(board)
    green_text = font.render(f"Verde: {green_zones}", True, GREEN_COLOR)
    red_text = font.render(f"Rojo: {red_zones}", True, RED_COLOR)

    screen.blit(green_text, (10, 10))
    screen.blit(red_text, (BOARD_SIZE * CELL_SIZE - 150, 10))
  
    pygame.display.flip()
    