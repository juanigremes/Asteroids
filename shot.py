import pygame
import circleshape
from constants import SHOT_RADIUS, LINE_WIDTH

class Shot(circleshape.CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, (255,0,0), self.position, SHOT_RADIUS+0.5, 0)
        pygame.draw.circle(screen, (255,50,50), self.position, SHOT_RADIUS+0.25, 0)
        pygame.draw.circle(screen, (255,90,90), self.position, SHOT_RADIUS, 0)
        pygame.draw.circle(screen, (255,100,100), self.position, SHOT_RADIUS-0.5, 0)
        pygame.draw.circle(screen, (255,160,160), self.position, SHOT_RADIUS-1, 0)
        pygame.draw.circle(screen, (255,255,255), self.position, SHOT_RADIUS-2, 0)
        
        
    def update(self, delta_time, asteroid_field):
        self.position += self.velocity * delta_time
        if not asteroid_field.contiene(self.position):
            self.kill()


class EnemyShot(circleshape.CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, (0,255,0), self.position, SHOT_RADIUS+0.5, 0)
        pygame.draw.circle(screen, (50,255,50), self.position, SHOT_RADIUS+0.25, 0)
        pygame.draw.circle(screen, (90,255,90), self.position, SHOT_RADIUS, 0)
        pygame.draw.circle(screen, (100,255,100), self.position, SHOT_RADIUS-0.5, 0)
        pygame.draw.circle(screen, (160,255,160), self.position, SHOT_RADIUS-1, 0)
        pygame.draw.circle(screen, (255,255,255), self.position, SHOT_RADIUS-2, 0)
        
        
    def update(self, delta_time, asteroid_field):
        self.position += self.velocity * delta_time
        if not asteroid_field.contiene(self.position):
            self.kill()

       

    def split(self):
        self.kill()

    def get_points_value(self):
        return 1
