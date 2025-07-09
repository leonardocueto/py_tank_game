import pygame
import os
import sys
import lib.color as c
from lib.var import FONT_TYPE, TITLE, SCREEN_HEIGHT,SCREEN_WIDTH, BUTTON_HEIGHT, BUTTON_WIDTH


def load_sprite(path):
    """
    - acortamos el path con el os.path
    - cargamos la imagen a pygame
    - utilizamos convert_alpha ya que son todas las imagenes .png
    """
    return pygame.image.load(os.path.join("sprite", path)).convert_alpha()


def main_menu(screen):

    font = pygame.font.SysFont(FONT_TYPE, 36)
    #creamos el texto del titulo y lo posicionamos en el centro superior
    title = font.render(TITLE, True, c.WHITE)
    #centramos el titulo
    #width // 2 -> centro en x
    #height // 4 -> 1/4 de la pantalla en y 
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

    button_font = pygame.font.SysFont(FONT_TYPE, 28)
    
 

    #creamos los botones
    #restamos el tamaño del boton y dividimos entre 2 para obtener el centro en x
    #dividimos entre 2 para obtener el centro en y
    game_vs_1_button = pygame.Rect(
        (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
        SCREEN_HEIGHT // 2,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )

    game_vs_2_button = pygame.Rect(
        (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
        SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + 20,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )

    quit_button = pygame.Rect(
        (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
        SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + 90,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )

    game = False
    while not game:
        #llenamos el fondo
        screen.fill(c.DARK_GRAY)

        #dibujamos titulo
        screen.blit(title, title_rect.topleft)

        #dibujamos botones
        pygame.draw.rect(screen, c.GREEN, game_vs_1_button)
        pygame.draw.rect(screen, c.BLUE, game_vs_2_button)
        pygame.draw.rect(screen, c.RED, quit_button)

        #renderiza texto
        text_game_v1 = button_font.render("Jugador vs 1", True, c.WHITE)
        text_game_v2 = button_font.render("Jugador vs 2", True, c.WHITE)
        quit_text = button_font.render("Salir", True, c.WHITE)

        #dibujamos el texto centrado sobre los botones
        text_game_v1_rect = text_game_v1.get_rect(center=game_vs_1_button.center)
        text_game_v2_rect = text_game_v2.get_rect(center=game_vs_2_button.center)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        screen.blit(text_game_v1, text_game_v1_rect)
        screen.blit(text_game_v2, text_game_v2_rect)
        screen.blit(quit_text, quit_text_rect)

        #capturamos eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = True
            #capturamos evento mouse y si hizo clic
            if event.type == pygame.MOUSEBUTTONDOWN:
                #verificamos que boton se selecciono y retornamos una accion
                if game_vs_1_button.collidepoint(event.pos):
                    return "vs1" 
                elif game_vs_2_button.collidepoint(event.pos):
                    return "vs2"
                if quit_button.collidepoint(event.pos):
                    #salimos del bucle
                    game = True
        #actualiza pantalla
        pygame.display.flip()

    #cerramos pygame y pantalla
    pygame.quit()
    sys.exit()

def end_menu(screen,result):
    font = pygame.font.SysFont(FONT_TYPE, 42)

    #verificamos estado del juego
    if result == "ganaste":
        message = "Ganaste!"
        screen.fill(c.BG_GREEN)
    else:
        message = "Perdiste!"
        screen.fill(c.BG_RED)
    #renderizamos mensaje y su posicion
    title = font.render(message, True, c.WHITE)
    #posicionamos en 1/4 de y.
    #centramos en x
    title_rect = title.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT //4))
    button_font = pygame.font.SysFont(FONT_TYPE, 28)

    #botones de reiniciar y de salir
    restart_button = pygame.Rect(
        (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
        SCREEN_HEIGHT // 2,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )

    quit_button = pygame.Rect(
        (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
        SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + 20,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )

    menu_active = True

    while menu_active:
        
        #dibujamos titulo y botones
        screen.blit(title, title_rect.topleft)
        pygame.draw.rect(screen, c.BLUE, restart_button)
        pygame.draw.rect(screen, c.RED, quit_button)
        restart_text = button_font.render("Reiniciar", True, c.WHITE)
        quit_text = button_font.render("Salir", True, c.WHITE)
        screen.blit(restart_text, restart_text.get_rect(center = restart_button.center))
        screen.blit(quit_text, quit_text.get_rect(center = quit_button.center))

        #capturamos eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #capturamos evento mouse y si hizo clic
            if event.type == pygame.MOUSEBUTTONDOWN:
                #verificamos que boton se selecciono y retornamos una accion
                if restart_button.collidepoint(event.pos):
                    return "restart"
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()