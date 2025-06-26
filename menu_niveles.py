import pygame
import sys

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (100, 149, 237)
GRIS = (200, 200, 200)

# Inicializar pygame
pygame.init()
pantalla = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Selecciona el Nivel")
fuente = pygame.font.SysFont(None, 40)

# Crear botón
def crear_boton(texto, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    txt = fuente.render(texto, True, NEGRO)
    return (rect, txt, texto.lower())

# Botones: (rectángulo, texto_renderizado, nombre)
botones = [
    crear_boton("Fácil", 200, 100, 200, 60),
    crear_boton("Medio", 200, 180, 200, 60),
    crear_boton("Difícil", 200, 260, 200, 60),
]

def seleccionar_nivel():
    while True:
        pantalla.fill(BLANCO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for rect, texto, nombre in botones:
                    if rect.collidepoint(evento.pos):
                        return nombre  # ← Devolver nivel seleccionado

        # Dibujar botones
        for rect, texto, _ in botones:
            pygame.draw.rect(pantalla, AZUL, rect)
            pygame.draw.rect(pantalla, GRIS, rect, 2)
            pantalla.blit(texto, (rect.x + 60, rect.y + 15))

        pygame.display.flip()
