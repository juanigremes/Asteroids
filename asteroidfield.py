import pygame
import random
from asteroid import Asteroid
from enemies import TieFighter
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.spawn_rate = ASTEROID_SPAWN_RATE_SECONDS
        self.speed_modifier = random.uniform(1,2.5)
        self.min_speed = 50
        self.max_speed = 100

    def spawn_asteroid(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius, self.speed_modifier)
        asteroid.velocity = velocity

    def spawn_tie_fighter(self, position, velocity):
        tie_fighter = TieFighter(position.x, position.y, PLAYER_RADIUS, self.speed_modifier, velocity)

    def update(self, dt, af):
        self.spawn_timer += dt
        if self.spawn_timer > self.spawn_rate:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(self.min_speed, self.max_speed)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(0, ASTEROID_KINDS)
            if kind == 0:
                self.spawn_tie_fighter(position, velocity)
            else:
                self.spawn_asteroid(ASTEROID_MIN_RADIUS * kind, position, velocity)

    def increment_spawn_rate(self):
        self.spawn_rate -= 0.1

    def increment_asteroid_speed(self):
        self.min_speed += 5
        self.max_speed += 5

    def contiene(self, coordenadas):
        margin = ASTEROID_MAX_RADIUS

        return (
            coordenadas.x > -margin
            and coordenadas.x < SCREEN_WIDTH + margin
            and coordenadas.y > -margin
            and coordenadas.y < SCREEN_HEIGHT + margin
        )
