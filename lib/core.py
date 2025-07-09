import pygame
import math
from lib.var import SCREEN_HEIGHT, SCREEN_WIDTH


class Decoration:
    
    #definimos constructor con coordenadas, imagen para decorar y angulo para rotar
    def __init__(self, x, y, image_surface, angle=0):
        self.__original_image = image_surface
        self.__angle = angle
        self.__image = pygame.transform.rotate(self.__original_image, self.__angle)
        self.rect = self.__image.get_rect(topleft=(x, y))
    
    #metodo para dibujar en pantalla
    def draw(self, surface):
        surface.blit(self.__image, self.rect.topleft)

class Obstacle:
    #definimos constructor con coordenadas, imagen de obstaculo y angulo para rotar
    def __init__(self, x, y, image_surface, angle=0):
        self.__original_image = image_surface
        self.__angle = angle
        self.__image = pygame.transform.rotate(self.__original_image, self.__angle)
        self.rect = self.__image.get_rect(center=(x, y))
    
    #meotodo para dibujar en pantalla
    def draw(self, surface):
        surface.blit(self.__image, self.rect.topleft)


class Bullet:

    #definimos constructor con coordenads, angulo, img bala, quien disparo y velocidad
    def __init__(self, x, y, angle, image_surface, owner = "player", speed=7):
        self.owner = owner 
        self.__original_image = image_surface
        self.__angle = angle
        self.__speed = speed
        #rota la img segun el angulo de disparo
        self.image = pygame.transform.rotate(self.__original_image, self.__angle)
        #rect para colisiones
        self.rect = self.image.get_rect(center=(x, y))
        
        #calculo disparo
        rad = math.radians(self.__angle)
        #velocidad de mov de la bala
        self.__direction_x = -math.sin(rad) * self.__speed
        self.__direction_y = -math.cos(rad) * self.__speed

    #metodo update mueve la bala calculada en las coordenadas
    def update(self):
        self.rect.x += self.__direction_x
        self.rect.y += self.__direction_y

    #dibuja la bala
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    #metodo para verificar si salio de la pantalla
    def is_off_screen(self):
        return not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).collidepoint(self.rect.center)
    
    #metodo para verificar si choca con un objeto
    def collide_with(self, target_rect):
        return self.rect.colliderect(target_rect)


class BaseTank:

    #definimos constructor con coordenadas, img tank, img cañon y cantidad de balas
    def __init__(self, x,y, image_surface, barrel_surface, bullets = 10):

        #generamos una copia del tank y cañon para rotaciones
        self._original_image = image_surface
        self.image = self._original_image
        self._barrel_original = barrel_surface
        self.barrel_image = self._barrel_original
        #rect para colision del tank
        self.rect = self.image.get_rect(center = (x,y))
        #rect par centrar el cañon
        self.barrel_rect = self.barrel_image.get_rect(center=self.rect.center)
        
        #propiedades del tank
        self.angle = 0
        self._speed = 3
        self.bullet_count = bullets
        self._health = 5
        self.alive = True
        self._cooldown = 0

    #metodo para recibir daño y controlar vida
    def take_damage(self, destroyed_sprite):
        self._health -= 1
        if self._health <= 0:
            self.alive = False
            self._original_image = destroyed_sprite
            self.image = self._original_image
            self.barrel_image = pygame.Surface((0,0))

    #dibuja el tanque y el cañon
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        surface.blit(self.barrel_image, self.barrel_rect.topleft)


class PlayerTank(BaseTank):
    def update(self, keys, obstacles):
        if not self.alive:
            return

        self._last_position = self.rect.center
        #controles
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle += self._speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle -= self._speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            rad = math.radians(self.angle)
            self.rect.x += self._speed * -math.sin(rad)
            self.rect.y += self._speed * -math.cos(rad)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:

            #grados a radianes
            rad = math.radians(self.angle)
            self.rect.x -= self._speed * -math.sin(rad)
            self.rect.y -= self._speed * -math.cos(rad)

        self._handle_colision_rotation(obstacles)

    def _handle_colision_rotation(self, obstacles):
        #rota la imagen
        self.image = pygame.transform.rotate(self._original_image, self.angle)
        #rect de la nueva posicion
        self.rect = self.image.get_rect(center=self.rect.center)
        #limite de pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        #verificacion para no superposicion
        collision = any(self.rect.colliderect(ob.rect) for ob in obstacles)
        if collision:
            self.rect.center = self._last_position
        #ajustamos el cañon en la nueva posicion
        self.barrel_image = pygame.transform.rotate(self._barrel_original, self.angle)
        rad = math.radians(self.angle)
        #ajustamos el cañon en la imagen
        barrel_position_x = -math.sin(rad) * 20
        barrel_position_y = -math.cos(rad) * 20
        self.barrel_rect = self.barrel_image.get_rect(
            center=(self.rect.centerx + barrel_position_x, self.rect.centery + barrel_position_y)
        )


class EnemyTank(BaseTank):

    def update(self, player, obstacles, shoot_callback):
        if not self.alive:
            return
        
        last_position = self.rect.center

        _shoot_range = 400
        
        #angulo en donde esta el jugador
        direction_x = player.rect.centerx - self.rect.centerx
        direction_y = player.rect.centery - self.rect.centery
        
        #angulo entre el enemigo y el jugador
        self.angle = math.degrees(math.atan2(-direction_x, -direction_y))
        rad = math.radians(self.angle)

        #Usamos la hipotenusa para obtener la distancia entre el enemy y el player
        distance = math.hypot(direction_x,direction_y)

        #movimiento del enemy
        if distance > _shoot_range:
            self.rect.x += self._speed * -math.sin(rad)
            self.rect.y += self._speed * -math.cos(rad)

        #rotamos el tank hacia el angulod el player 
        self.image = pygame.transform.rotate(self._original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


        
        self.rect.clamp_ip(pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))

        #si colisiona vuelve a la posicion anterior
        collision = any(self.rect.colliderect(obs.rect) for obs in obstacles)
        if collision:
            self.rect.center = last_position

        #posicion y rotacion del cañon
        self.barrel_image = pygame.transform.rotate(self._barrel_original, self.angle)
        direction__barrel_x = -math.sin(rad) * 20
        direction__barrel_y = -math.cos(rad) * 20
        self.barrel_rect = self.barrel_image.get_rect(center = (self.rect.centerx + direction__barrel_x, self.rect.centery + direction__barrel_y))

        
        self._cooldown -= 1


        if distance < _shoot_range and self._cooldown <= 0 and self.bullet_count > 0:
            shoot_callback(self.rect.centerx, self.rect.centery, self.angle)
            self.bullet_count -= 1
            self._cooldown = 60
        