import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
CYAN = (0, 255, 255)
VERDE = (0, 255, 0)
NARANJA = (255, 165, 0)
ROJO = (255, 0, 0)
MAGENTA = (255, 0, 255)
AMARILLO = (255, 255, 0)

# Definir dimensiones de la pantalla
ANCHO = 300
ALTO = 600
TAMANO_BLOQUE = 30

# Definir formas de las piezas del Tetris
formas = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]]  # Z
]

# Clase para representar la pieza del Tetris
class Pieza:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.forma = random.choice(formas)
        self.color = random.choice([AZUL, CYAN, VERDE, NARANJA, ROJO, MAGENTA, AMARILLO])

    def rotar(self):
        self.forma = [list(row) for row in zip(*self.forma[::-1])]

    def dibujar(self, pantalla):
        for y, fila in enumerate(self.forma):
            for x, bloque in enumerate(fila):
                if bloque:
                    pygame.draw.rect(pantalla, self.color, pygame.Rect((self.x + x) * TAMANO_BLOQUE, (self.y + y) * TAMANO_BLOQUE, TAMANO_BLOQUE, TAMANO_BLOQUE), 0)

    def mover(self, dx):
        self.x += dx

# Función para verificar colisiones
def colision(bloques, pieza):
    forma = pieza.forma
    offset_x, offset_y = pieza.x, pieza.y
    for y, fila in enumerate(forma):
        for x, bloque in enumerate(fila):
            if bloque and (x + offset_x < 0 or x + offset_x >= ANCHO // TAMANO_BLOQUE or y + offset_y >= ALTO // TAMANO_BLOQUE or (x + offset_x, y + offset_y) in bloques):
                return True
    return False

# Función para eliminar líneas completas
def eliminar_lineas(bloques):
    lineas_completas = 0
    for y in range(ALTO // TAMANO_BLOQUE):
        if all((x, y) in bloques for x in range(ANCHO // TAMANO_BLOQUE)):
            for i in range(y, 0, -1):
                for j in range(ANCHO // TAMANO_BLOQUE):
                    bloques.discard((j, i))
                    bloques.add((j, i + 1))
            lineas_completas += 1
    return lineas_completas

# Función principal del juego
def main():
    # Inicializar pantalla
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Tetris")

    # Reloj para controlar la velocidad de actualización de la pantalla
    reloj = pygame.time.Clock()

    # Inicializar variables del juego
    pieza_actual = Pieza(ANCHO // TAMANO_BLOQUE // 2, 0)
    bloques = set()
    puntaje = 0
    juego_terminado = False
    juego_pausado = False

    # Bucle principal del juego
    while True:
        # Procesamiento de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and not juego_terminado and not juego_pausado:
                    pieza_actual.mover(-1)
                    if colision(bloques, pieza_actual):
                        pieza_actual.mover(1)
                elif evento.key == pygame.K_RIGHT and not juego_terminado and not juego_pausado:
                    pieza_actual.mover(1)
                    if colision(bloques, pieza_actual):
                        pieza_actual.mover(-1)
                elif evento.key == pygame.K_DOWN and not juego_terminado and not juego_pausado:
                    pieza_actual.y += 1
                    if colision(bloques, pieza_actual):
                        pieza_actual.y -= 1
                elif evento.key == pygame.K_UP and not juego_terminado and not juego_pausado:
                    pieza_actual.rotar()
                    if colision(bloques, pieza_actual):
                        pieza_actual.rotar()
                        pieza_actual.rotar()
                        pieza_actual.rotar()
                elif evento.key == pygame.K_SPACE and not juego_terminado and not juego_pausado:
                    while not colision(bloques, pieza_actual):
                        pieza_actual.y += 1
                    pieza_actual.y -= 1
                elif evento.key == pygame.K_p:
                    juego_pausado = not juego_pausado

        if juego_pausado or juego_terminado:
            continue

        # Actualizar juego
        if not colision(bloques, pieza_actual):
            pieza_actual.y += 1
        else:
            for y, fila in enumerate(pieza_actual.forma):
                for x, bloque in enumerate(fila):
                    if bloque:
                        bloques.add((pieza_actual.x + x, pieza_actual.y + y))
            lineas_completas = eliminar_lineas(bloques)
            puntaje += lineas_completas * 100
            pieza_actual = Pieza(ANCHO // TAMANO_BLOQUE // 2, 0)
            if colision(bloques, pieza_actual):
                juego_terminado = True

        # Dibujar en pantalla
        pantalla.fill(NEGRO)
        for bloque in bloques:
            pygame.draw.rect(pantalla, (255, 255, 255), pygame.Rect(bloque[0] * TAMANO_BLOQUE, bloque[1] * TAMANO_BLOQUE, TAMANO_BLOQUE, TAMANO_BLOQUE))
        pieza_actual.dibujar(pantalla)

        # Actualizar pantalla
        pygame.display.flip()

        # Control de velocidad de actualización de la pantalla
        reloj.tick(5)

# Iniciar el juego
if __name__ == "__main__":
    main()
