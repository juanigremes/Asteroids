import pygame
import circleshape
from logger import log_event
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
import random

class Asteroid(circleshape.CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, delta_time):
        self.position += self.velocity * delta_time

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")

        angle = random.uniform(20, 50)
        first_ast_vel = self.velocity.rotate(angle)*1.2
        second_ast_vel = self.velocity.rotate(-angle)*1.2
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        first_ast = Asteroid(self.position.x, self.position.y, new_radius)
        second_ast = Asteroid(self.position.x, self.position.y, new_radius)

        first_ast.velocity = first_ast_vel
        second_ast.velocity = second_ast_vel
