import pygame
import circleshape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED

class Player(circleshape.CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, delta_time):
        self.rotation += PLAYER_TURN_SPEED * delta_time
        
    def move(self, delta_time):
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_vector_with_speed = rotated_vector * PLAYER_SPEED * delta_time
        self.position += rotated_vector_with_speed

    def update(self, delta_time):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rotate(-1 * delta_time)
        if keys[pygame.K_RIGHT]:
            self.rotate(delta_time)
        if keys[pygame.K_UP]:
            self.move(delta_time)
        if keys[pygame.K_DOWN]:
            self.move(-1 * delta_time)

