import pygame

pygame.init()

info = pygame.display.Info()
ancho = info.current_w
alto = info.current_h

# Screen
SCREEN_WIDTH = ancho
SCREEN_HEIGHT = alto

# Player
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 320
PLAYER_SPEED = 230
PLAYER_SHOT_SPEED = 600
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.25
PLAYER_IMAGE = "imagenes/XWing.png"

# Shots
SHOT_RADIUS = 5

# Asteroids
ASTEROID_MIN_RADIUS = 15
ASTEROID_KINDS = 4
ASTEROID_SPAWN_RATE_SECONDS = 2.7
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_IMAGE = "imagenes/Asteroid.png"

#Enemies
TIE_IMAGE = "imagenes/Tie_Fighter.png"
TIE_SHOT_SPEED = 450
TIE_SHOOT_COOLDOWN_SECONDS = 0.3

# Draw
LINE_WIDTH = 2
