import pygame
import sys
import math
import random
import lib.var as var
from lib.color import WHITE
from lib.core import Bullet, EnemyTank, PlayerTank, Decoration, Obstacle
from lib.func import load_sprite, main_menu, end_menu


def main():
    pygame.init()
    #creamos la ventana 
    screen = pygame.display.set_mode((var.SCREEN_WIDTH, var.SCREEN_HEIGHT))
    #titulo de la ventana
    pygame.display.set_caption(var.TITLE)
    #tiempo para limitar los fps
    clock = pygame.time.Clock()

    
    #limpio los estados
    var.ENEMIES.clear()
    var.ENEMIES_RECTS.clear()
    var.BULLETS.clear()
    var.PICKUP_ITEMS.clear()

    #sprites
    DIRT_TILE = load_sprite("environment/dirt.png")
    TANK_GREEN_IMG = load_sprite("tank/tank_green.png")
    BARREL_GREEN_TANK_IMG = load_sprite("tank/barrel_green.png")
    BARREL_RED_TANK_IMG = load_sprite("tank/barrel_red.png")
    TANK_RED_IMG = load_sprite("tank/tank_red.png")
    TREE_SMALL_IMG = load_sprite("environment/tree_small.png")
    TREE_LARGE_IMG = load_sprite("environment/tree_large.png")
    BARREL_GREY_IMG = load_sprite("environment/barrel_grey.png")
    STONE_OB = load_sprite("obstacles/stone_ob.png")
    SANDBAG_OB = load_sprite("obstacles/sandbag_ob.png")
    BULLET_BLUE_IMG = load_sprite("bullets/bullet_blue.png")
    BULLET_GREEN_IMG = load_sprite("bullets/bullet_green.png")
    BULLET_RED_IMG = load_sprite("bullets/bullet_red.png")
    HEART = pygame.transform.scale(load_sprite("tank/heart.png"), (24,24))

    #fondo dinamico
    TILE_WIDTH = DIRT_TILE.get_width()
    TILE_HEIGHT = DIRT_TILE.get_height()

    player = PlayerTank(50,550,TANK_GREEN_IMG,BARREL_GREEN_TANK_IMG)

    #menu principal
    result_vs = main_menu(screen)
    #definimos vs cuantos tanks jugaremos
    if result_vs == "vs1":
        enemy = EnemyTank(750,50, TANK_RED_IMG, BARREL_RED_TANK_IMG,999)
        var.ENEMIES.append(enemy)
    elif result_vs == "vs2":
        enemy = EnemyTank(750,50, TANK_RED_IMG, BARREL_RED_TANK_IMG,999)
        enemy2 = EnemyTank(750,700, TANK_RED_IMG, BARREL_RED_TANK_IMG,999)
        var.ENEMIES.append(enemy)
        var.ENEMIES.append(enemy2)

    DECORATIONS = [

        Decoration(100,100, BARREL_GREY_IMG, angle=95),
        Decoration(60, 520, BARREL_GREY_IMG, angle=50),
        Decoration(150, 300, BARREL_GREY_IMG, angle=90),
        Decoration(400, 80, BARREL_GREY_IMG, angle=-45),
        Decoration(620, 320, BARREL_GREY_IMG, angle=180),
        Decoration(700, 40, BARREL_GREY_IMG, angle=15),
        Decoration(390, 260, BARREL_GREY_IMG, angle=-20),

        #barriles bottomleft
        Decoration(20, 700, BARREL_GREY_IMG, angle=-20),
        Decoration(50, 680, BARREL_GREY_IMG, angle=40),
        Decoration(30, 680, BARREL_GREY_IMG, angle=20),
        #arboles topleft
        Decoration(0,0, TREE_LARGE_IMG),
        Decoration(20,35, TREE_SMALL_IMG),
        
        Decoration(600, 535, TREE_SMALL_IMG),
        Decoration(600, 600 - TREE_LARGE_IMG.get_height(), TREE_LARGE_IMG),
        Decoration(570, 500, TREE_SMALL_IMG),
        Decoration(50, 430, TREE_LARGE_IMG),
        Decoration(120, 460, TREE_SMALL_IMG),
        Decoration(700, 100, TREE_SMALL_IMG),
        Decoration(680, 180, TREE_LARGE_IMG),
        Decoration(720, 250, TREE_SMALL_IMG),
    ]


    OBSTACLES = [
        #obs topleft
        Obstacle(30, 145, STONE_OB),
        Obstacle(90, 145, STONE_OB),
        Obstacle(150, 145, STONE_OB),
        Obstacle(160, 91, STONE_OB, angle=90),
        Obstacle(160, 31, STONE_OB, angle=90),
        #obs buttomleft
        Obstacle(30, 650, STONE_OB),
        Obstacle(90, 650, STONE_OB),
        Obstacle(150, 650, STONE_OB),
        Obstacle(160, 741, STONE_OB, angle=90),
        Obstacle(160, 701, STONE_OB, angle=90),
        
        Obstacle(400, 400, STONE_OB, angle=0),
        Obstacle(460, 400, SANDBAG_OB, angle=0),
        Obstacle(520, 400, STONE_OB, angle=0),
        Obstacle(530, 450, STONE_OB, angle=90),

        Obstacle(640, 460, SANDBAG_OB, angle=90),
    ]


    #Bucle del game
    game = False
    while not game:
        
        #60 fps
        clock.tick(60)
        #capturamos eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = True
            if event.type == pygame.KEYDOWN:
                #si el jugador preciona el espacio se crea una bala y se le resta al jugador
                if event.key == pygame.K_SPACE and player.bullet_count > 0 and player.alive:
                    #usamos pitagoras para el disparo
                    rad = math.radians(player.angle)
                    direction_x = -math.sin(rad) * 70
                    direction_y = -math.cos(rad) * 70

                    #creamos una bala
                    bullet = Bullet(
                    player.rect.centerx + direction_x,
                    player.rect.centery + direction_y,
                    player.angle,
                    BULLET_GREEN_IMG,
                    )
                    #lista global de balas
                    var.BULLETS.append(bullet)
                    player.bullet_count -=1

        #Fondo (tierra)
        for y in range(0, var.SCREEN_HEIGHT, TILE_HEIGHT):
            for x in range(0, var.SCREEN_WIDTH, TILE_WIDTH):
                #reenderizamos fondo
                screen.blit(DIRT_TILE, (x, y))

        #Dibujar decoraciones (arboles y barriles oxidados)
        for decoration in DECORATIONS:
            #dibujamos decoraciones
            decoration.draw(screen)

        #Input y actualización
        keys = pygame.key.get_pressed()
        for e in var.ENEMIES:
            if e.alive:

                var.ENEMIES_RECTS.append(e)

        #le pasamos las propeidades al jugador 
        player.update(keys, OBSTACLES + var.ENEMIES_RECTS)

        #definimos una funcion para que el enemigo dispare
        #utilizamos el angulo para que salga la bala y lo multiplicamos x 70 para que no colisione con el cañon
        def shoot_callback(x,y,angle):
            var.BULLETS.append(
                Bullet(
                    x + -math.sin(math.radians(angle)) * 70,
                    y + -math.cos(math.radians(angle)) * 70,
                    angle,
                    BULLET_RED_IMG,
                    "enemy"
                )
            )
        #le pasamos las propiedades a cada enemigo
        for e in var.ENEMIES:
            e.update(player, OBSTACLES,shoot_callback)


        #Renderizado de spots de balas
        current_time = pygame.time.get_ticks()

        #limite para que salgan en cierto tiempo
        if current_time - var.last_pickup_time >= var.PICKUP_INTERVAL:
            #posicion aleatoria para que no salga el mismo spot
            spawn_pos = random.choice(var.PICKUP_SPOTS)
            rect = BULLET_BLUE_IMG.get_rect(center=spawn_pos)
            var.PICKUP_ITEMS.append(rect)
            var.last_pickup_time = current_time
        #itera y actualiza la lista de balas locales
        for bullet in var.BULLETS[:]:
            bullet.update()
            bullet.draw(screen)

            #Remover bala si se sale de la pantalla
            if bullet.is_off_screen():
                var.BULLETS.remove(bullet)
            #verificamos si la bala choca algun objeto/tank
            collided = any(bullet.collide_with(ob.rect) for ob in OBSTACLES)
            if collided:
                var.BULLETS.remove(bullet)
            #verifica si la bala enemiga colisiona con el jugador
            if bullet.owner == "enemy" and bullet.collide_with(player.rect):
                #removemos la bala del juego
                var.BULLETS.remove(bullet)
                #adjuntamos daño al personaje
                player.take_damage(load_sprite("tank/tank_black.png"))
                #si muere el jugador mostramos pantalla
                if not player.alive:
                    resultado = "perdiste"
                    decision = end_menu(screen, resultado)
                    if decision == "restart":
                        main()
                    
                    
            #verificamos si la bala del jugador dio al enemigo
            if bullet.owner == "player":
                hit = False
                #verificamos si la bala dio a algun enemigo
                for e in var.ENEMIES:
                    if not hit and bullet.collide_with(e.rect) and e.alive:
                        var.BULLETS.remove(bullet)
                        e.take_damage(load_sprite("tank/tank_black.png"))
                        hit = True
                        #si no hay enemigos mostramos la pantalla 
                        if not any(en.alive for en in var.ENEMIES):
                            resultado = "ganaste"
                            decision = end_menu(screen, resultado)
                            if decision == "restart":
                                main()

        #si el jugador toca una bala item sumamos 3 a nuestro inventario y eliminamos el pickup      
        for pickup in var.PICKUP_ITEMS[:]:
            if player.rect.colliderect(pickup):
                player.bullet_count += 3
                var.PICKUP_ITEMS.remove(pickup)


        #Dibujar obstaculos
        for obstacle in OBSTACLES:
            obstacle.draw(screen)

        #Dibujar jugador y enemigo
        player.draw(screen)
        for e in var.ENEMIES:
            e.draw(screen)

        #Contador balas y vida
        font = pygame.font.SysFont(var.FONT_TYPE, 24)
        text_bullet = font.render(f"{player.bullet_count} x", True, WHITE)
        screen.blit(text_bullet, (10, 10))
        screen.blit(BULLET_BLUE_IMG, (10 + text_bullet.get_width() + 4,10))
        
        for i in range(player._health):
            screen.blit(HEART, (10 + i * (HEART.get_width() + 5), 40))


        #dibujamos las balas items
        for pickup in var.PICKUP_ITEMS:
            screen.blit(BULLET_BLUE_IMG, pickup.topleft)


        #Actualizar pantalla para mostrar todos los elementos
        pygame.display.flip()
    #cierra pygame y finaliza el programa
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
