import pygame
import circleshape
from logger import log_event
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_IMAGE
import random

class Asteroid(circleshape.CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0

        rotaciones = [-2, -1, -0.5, 0.5, 1, 2]
        self.rot_speed = random.choice(rotaciones)

        image = pygame.image.load(ASTEROID_IMAGE)
        scale = int(50 * (radius/ASTEROID_MIN_RADIUS))
        scaled_image = pygame.transform.smoothscale(image, (scale,scale))
        final_image = pygame.transform.rotate(scaled_image, random.randint(0,180))

        self.og_image = final_image


    def draw(self, screen):
        image = pygame.transform.rotate(self.og_image, self.rotation)
        screen.blit(image, image.get_rect(center=self.position))
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    

    def update(self, delta_time):
        self.position += self.velocity * delta_time * 1.5
        self.rotation += delta_time * self.rot_speed * 15

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
