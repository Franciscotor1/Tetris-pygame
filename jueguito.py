import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Configuración de la pantalla
ANCHO = 400
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Esquiva los obstáculos")

# Clase para representar el jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

# Clase para representar los obstáculos
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO + 10:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocidad_y = random.randrange(1, 8)

# Crear grupos de sprites
todos_los_sprites = pygame.sprite.Group()
jugador = Jugador()
todos_los_sprites.add(jugador)
obstaculos = pygame.sprite.Group()

# Crear obstáculos
for i in range(8):
    obstaculo = Obstaculo()
    todos_los_sprites.add(obstaculo)
    obstaculos.add(obstaculo)

# Reloj para controlar la velocidad de actualización de la pantalla
reloj = pygame.time.Clock()

# Bucle principal del juego
ejecutando = True
while ejecutando:
    # Procesamiento de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Actualizar
    todos_los_sprites.update()

    # Colisiones
    if pygame.sprite.spritecollide(jugador, obstaculos, False):
        ejecutando = False

    # Dibujar en la pantalla
    pantalla.fill(BLANCO)
    todos_los_sprites.draw(pantalla)

    # Actualizar pantalla
    pygame.display.flip()

    # Control de velocidad de actualización de la pantalla
    reloj.tick(60)

# Salir del juego
pygame.quit()
sys.exit()
