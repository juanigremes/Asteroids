# Imports
import sys
import pygame 
from logger import log_event
from constants import ASTEROID_SPAWN_RATE_SECONDS
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import highscore



# Main

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    start_menu(screen)



def start_menu(screen):
    #Menu de inicio
    font = pygame.font.Font("Starjedi.ttf", 50)
    background = pygame.image.load("fondo_menu.jpg").convert()
    background = pygame.transform.scale(background, screen.get_size())


    options = ["Jugar","Cambiar Fondo", "Salir"]
    selected = 0

    while True:

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if evento.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if evento.key == pygame.K_RETURN:
                    if selected == 0:
                        name_menu(screen)
                    elif selected == 1:
                        pygame.quit()
                        sys.exit()
                        #opciones para cambiar mapa, todavia no pasa nada
                    else:
                        pygame.quit()
                        sys.exit()

        screen.blit(background, (0,0))


        #options menu
        for i, option in enumerate(options):
            color = (255, 255, 255)
            if i == selected:
                color = (255, 222, 6)  # resaltado

            text = font.render(option, True, color)
            screen.blit(text, (300, 200 + i * 80))
        
        #highscore
        top_player, top_score = highscore.highscore
        high = font.render(f"{top_player}: {top_score}", True, (255,255,255))
        screen.blit(high, (50 , screen.get_height()-100))

        pygame.display.flip()



def name_menu(screen):
    font = pygame.font.Font("Starjedi.ttf", 50)
    background = pygame.image.load("fondo_juego.jpg").convert()
    background = pygame.transform.scale(background, screen.get_size())

    
    nombre_jugador = ""
    while True: 

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if nombre_jugador != "":
                        game_loop(screen, nombre_jugador)
                elif evento.key == pygame.K_BACKSPACE:
                    if nombre_jugador != "":
                        nombre_jugador = nombre_jugador[:-1]
                else:
                    nombre_jugador += evento.unicode

        screen.blit(background, (0,0))
        nombre = font.render("Nombre: (al menos un carácter)", True, (255,255,255))
        screen.blit(nombre, (screen.get_width()/4, screen.get_height()/3))    

        nombre_jugador_texto = font.render(nombre_jugador, True, (255,255,255))
        screen.blit(nombre_jugador_texto, (screen.get_width()/3, screen.get_height()/2))

        jugar = font.render("Jugar", True, (255,222,6))
        screen.blit(jugar, (screen.get_width()/4, screen.get_height()*(2/3)))

        pygame.display.flip()




def game_loop(screen, nombre_jugador):
    pygame.mixer.music.load("duel_of_the_fates.mp3")
    pygame.mixer.music.play(-1)


    font = pygame.font.Font("Starjedi.ttf", 50)
    background = pygame.image.load("fondo_juego.jpg").convert()
    background = pygame.transform.scale(background, screen.get_size())

    
   
    clock = pygame.time.Clock()
    delta_time = 0
    
    #groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()


    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    asteroid_field = AsteroidField()
    player = Player(screen.get_width()/2, screen.get_height()/2)

    asteroids_score = 0
    time_score = 0
    score = asteroids_score + time_score
    tiempo_acumulado = 0

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.blit(background, (0,0))

        updatable.update(delta_time)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                pygame.mixer.music.stop()
                game_over_menu(screen, nombre_jugador, score)
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroids_score += asteroid.get_points_value()
                    shot.kill()
                    asteroid.split()

        for drawable_elem in drawable:
            drawable_elem.draw(screen)


        delta_time = clock.tick(60) / 1000
        tiempo_acumulado += delta_time
        
        if tiempo_acumulado >= 6:
            time_score += 1
            asteroid_field.increment_spawn_rate()
            asteroid_field.increment_asteroid_speed()
            tiempo_acumulado = 0

        score = time_score + asteroids_score
        
        score_text = font.render(str(score), True, (255,255,255))
        screen.blit(score_text, (10,10))
        pygame.display.flip()


def game_over_menu(screen, nombre_jugador, score):
    font = pygame.font.Font("Starjedi.ttf", 50)
    background = pygame.image.load("fondo_juego.jpg").convert()
    background = pygame.transform.scale(background, screen.get_size())
    
    if score > highscore.highscore[1]:
        with open("highscore.py", "w") as f:
            f.write(f"highscore = [\"{nombre_jugador}\",{score}]")

    options = ["Reiniciar", "Menú de inicio", "Salir"]
    selected = 0

    while True:

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if evento.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if evento.key == pygame.K_RETURN:
                    if selected == 0:
                        game_loop(screen, nombre_jugador)
                    elif selected == 1:
                        start_menu(screen)
                    else:
                        pygame.quit()
                        sys.exit()

        screen.blit(background, (0,0))

        for i, option in enumerate(options):
            color = (255, 255, 255)
            if i == selected:
                color = (255, 222, 6)  # resaltado

            text = font.render(option, True, color)
            screen.blit(text, (300, 400 + i * 80))
        
        puntaje_texto = font.render(f"{nombre_jugador}: {score}", True, (255,255,255))
        screen.blit(puntaje_texto, (200,200))

        pygame.display.flip()



if __name__ == "__main__":
    main()
