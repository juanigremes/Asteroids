import pygame
import math
import circleshape
from shot import Shot
from constants import PLAYER_IMAGE, PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS


class Player(circleshape.CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0

        self.shoot_right = True

        image = pygame.image.load(PLAYER_IMAGE)
        image = pygame.transform.rotate(image, 90)
        self.og_image = pygame.transform.smoothscale(image, (70,70))

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        self.image = pygame.transform.rotate(self.og_image, -self.rotation)
        screen.blit(self.image, self.image.get_rect(center=self.position))
        #pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, delta_time):
        self.rotation += PLAYER_TURN_SPEED * delta_time
        
    def move(self, delta_time):
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_vector_with_speed = rotated_vector * PLAYER_SPEED * delta_time
        self.position += rotated_vector_with_speed
    
    def shoot(self):
        if self.shot_cooldown_timer > 0:
            return
        self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        xdis, ydis = calcular_disparo(self.position, self.rotation, self.shoot_right)
        self.shoot_right = not self.shoot_right
        shot = Shot(xdis, ydis)
        shot_direction = pygame.Vector2(0,1)
        shot.velocity = shot_direction.rotate(self.rotation) * PLAYER_SHOT_SPEED

    def update(self, delta_time):
        self.shot_cooldown_timer -= delta_time

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.shoot()
        
        if keys[pygame.K_LEFT]:
            self.rotate(-1 * delta_time)
        if keys[pygame.K_RIGHT]:
            self.rotate(delta_time)
        
        if keys[pygame.K_UP]:
            self.move(delta_time)
        if keys[pygame.K_DOWN]:
            self.move(-1 * delta_time)

def calcular_disparo(center, rotation, shoot_right):
    if shoot_right:
        angulo = math.radians(rotation)
    else:
        angulo = math.radians(rotation+180)
    x2 = center.x + 30 * math.cos(angulo)
    y2 = center.y + 30 * math.sin(angulo)
    return x2, y2
