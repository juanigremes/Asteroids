import pygame
import circleshape
from constants import SHOT_RADIUS, LINE_WIDTH

class Shot(circleshape.CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, SHOT_RADIUS, LINE_WIDTH)
    
    def update(self, delta_time):
        self.position += self.velocity * delta_time


