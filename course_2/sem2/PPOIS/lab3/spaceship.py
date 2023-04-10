import math

import pygame

from bullet import Bullet


class SpaceShip(pygame.sprite.Sprite):
    W_KEY = pygame.K_w
    S_KEY = pygame.K_s
    A_KEY = pygame.K_a
    D_KEY = pygame.K_d
    E_KEY = pygame.K_e
    Q_KEY = pygame.K_q
    SPACE_KEY = pygame.K_SPACE

    @staticmethod
    def __load_image():
        image = pygame.image.load('./images/ships/ship_1.png')
        return pygame.transform.scale(image, (70, 70))

    def __init__(self, x: int, y: int, speed: int, sprites):
        super().__init__()
        print("Starting")
        self.__const_image = self.__class__.__load_image()
        self.image = self.__class__.__load_image()

        self.collision_rect = pygame.Rect(x, y, 17, 17)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.angle = 0
        self.rotation_speed = 5

        self.sprites: pygame.sprite.Group = sprites

    def __teleporting_to_the_opposite_site(self, surface_size: tuple):

        if self.rect.left > surface_size[0]:
            self.collision_rect.right = 0
            self.rect.right = 0
        elif self.rect.right < 0:
            self.collision_rect.left = surface_size[0]
            self.rect.left = surface_size[0]
        elif self.rect.bottom < 0:
            self.collision_rect.top = surface_size[1]
            self.rect.top = surface_size[1]
        elif self.rect.top > surface_size[1]:
            self.collision_rect.bottom = 0
            self.rect.bottom = 0

    def update(self, args: list):
        surface_size = args['surface_size']
        keys = pygame.key.get_pressed()
        bullet_fired: bool = args['bullet_fired']
        bullets: pygame.sprite.Group = args['bullets']

        delta_x = self.speed * math.cos(math.radians(self.angle))
        delta_y = self.speed * -math.sin(math.radians(self.angle))

        if keys[self.__class__.A_KEY]:
            self.angle += self.rotation_speed
            self.angle %= 360

        if keys[self.__class__.D_KEY]:
            self.angle -= self.rotation_speed
            self.angle %= 360

        if keys[self.__class__.W_KEY]:
            self.collision_rect.x += delta_x
            self.rect.x += delta_x
            self.collision_rect.y += delta_y
            self.rect.y += delta_y

        if keys[self.__class__.S_KEY]:
            self.collision_rect.x -= delta_x
            self.rect.x -= delta_x
            self.collision_rect.y -= delta_y
            self.rect.y -= delta_y

        if keys[self.__class__.SPACE_KEY] and bullet_fired and Bullet.bullet_amount < 6:
            bullet = Bullet(self.rect.center, self.angle)
            self.sprites.add(bullet)
            bullets.add(bullet)
            Bullet.bullet_amount += 1

        self.__teleporting_to_the_opposite_site(surface_size)
        self.image = pygame.transform.rotate(self.__const_image, self.angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.collision_rect.center = self.rect.center
