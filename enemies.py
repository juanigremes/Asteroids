import pygame
import math
import circleshape
from logger import log_event
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, TIE_IMAGE, TIE_SHOT_SPEED, TIE_SHOOT_COOLDOWN_SECONDS, VULTURE_IMAGE, VULTURE_TURN_CLOSE_COOLDOWN, VULTURE_TURN_MIDRANGE_COOLDOWN, VULTURE_TURN_FAR_COOLDOWN
from shot import EnemyShot
import random

class TieFighter(circleshape.CircleShape):

    def __init__(self, x, y, radius, speed_modif, velocity):
        super().__init__(x, y, radius)
        self.rotation = velocity.angle_to((0,1))
        
        self.shot_cooldown_timer = 0
        self.shot_count = 0

        self.velocity = velocity 

        self.speed_modifier = speed_modif

        image = pygame.image.load(TIE_IMAGE)
        scale = 60
        scaled_image = pygame.transform.smoothscale(image, (scale,scale))
        final_image = pygame.transform.rotate(scaled_image, self.rotation)
        self.og_image = final_image

        shot_sound = pygame.mixer.Sound("sonido/TieFighter_shot.wav")
        shot_sound.set_volume(0.3)
        self.shot_sound = shot_sound



    def draw(self, screen):
        screen.blit(self.og_image, self.og_image.get_rect(center=self.position))
        #pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, delta_time, asteroid_field):
        self.position += self.velocity * delta_time * self.speed_modifier
        self.shot_cooldown_timer -= delta_time
        if not asteroid_field.contiene(self.position):
            self.kill()

        
    def split(self):
        self.kill()
        log_event("asteroid_split")

    def get_points_value(self):
        return 10

    def shoot(self):
        if self.shot_cooldown_timer > 0:
            return
        self.shot_count += 1
        if self.shot_count == 3:
            self.shot_cooldown_timer = 1 + TIE_SHOOT_COOLDOWN_SECONDS
            self.shot_count = 0
        else:
            self.shot_cooldown_timer = TIE_SHOOT_COOLDOWN_SECONDS

        xdis, ydis = calcular_disparo(self.position, -self.rotation)
        shot1 = EnemyShot(xdis, ydis)
        shot1_direction = pygame.Vector2(0,1).rotate(-self.rotation)
        shot1.velocity = shot1_direction * TIE_SHOT_SPEED + self.velocity

        xdis, ydis = calcular_disparo(self.position, -self.rotation+180)
        shot2 = EnemyShot(xdis, ydis)
        shot2_direction = pygame.Vector2(0,1).rotate(-self.rotation)
        shot2.velocity = shot2_direction * TIE_SHOT_SPEED + self.velocity

        self.shot_sound.play()


def calcular_disparo(center, rotation):
    angulo = math.radians(rotation)
    x2 = center.x + 15 * math.cos(angulo)
    y2 = center.y + 15 * math.sin(angulo)
    return x2, y2


class VultureDroid(circleshape.CircleShape):
    
    def __init__(self, x, y, radius, velocity, player):
        super().__init__(x, y, radius)
        
        self.rotation = velocity.angle_to((0,1))
        self.velocity = velocity 

        image = pygame.image.load(VULTURE_IMAGE)
        scale = 60
        scaled_image = pygame.transform.smoothscale(image, (scale,scale))
        final_image = pygame.transform.rotate(scaled_image, self.rotation)
        self.og_image = final_image

    def draw(self, screen):
        screen.blit(self.og_image, self.og_image.get_rect(center=self.position))
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, delta_time, asteroid_field):
        self.position += self.velocity * delta_time 

        #esto lo tengo que eliminar
        if not asteroid_field.contiene(self.position):
            self.kill()
        
    def split(self):
        self.kill()
        log_event("asteroid_split")

    def get_points_value(self):
        return 15


