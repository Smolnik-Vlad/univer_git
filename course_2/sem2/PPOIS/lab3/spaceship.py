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
    def __load_image(pict=None):

        image = pygame.image.load('./images/ships/ship_1.png') if not pict else pygame.image.load(pict)

        return pygame.transform.scale(image, (70, 70))

    def __init__(self, x: int, y: int, speed: int, sprites):
        super().__init__()
        self.hp = 3
        self.game_points = 0
        self.__const_image = self.__class__.__load_image()
        self.image = self.__class__.__load_image()
        self.padded = False
        self.padded_time = None

        self.collision_rect = pygame.Rect(x, y, 20, 20)
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

    def start_padded_timer(self):
        self.padded_time = pygame.time.get_ticks()
        self.padded = True

    def __keys_actions(self, keys, delta_x, delta_y, bullet_fired, bullets):

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

        if keys[self.__class__.SPACE_KEY] and bullet_fired and Bullet.bullet_amount < 3:
            bullet = Bullet(self.rect.center, self.angle)
            self.sprites.add(bullet)
            bullets.add(bullet)
            Bullet.bullet_amount += 1

    def __padding_check(self):
        if self.padded:

            new_image = self.__load_image('./images/ships/save_round.png') if self.hp > 0 else self.__load_image(
                './images/ships/boom.png')

            new_image = pygame.transform.rotate(new_image, self.angle - 90)
            self.image.blit(new_image, (0, 0))
            current_time = pygame.time.get_ticks()
            if current_time - self.padded_time > 3000:
                self.padded_time = None
                self.padded = False

    def update(self, args: list):
        surface_size = args['surface_size']
        keys = pygame.key.get_pressed()
        bullet_fired: bool = args['bullet_fired']
        bullets: pygame.sprite.Group = args['bullets']

        delta_x = self.speed * math.cos(math.radians(self.angle))
        delta_y = self.speed * -math.sin(math.radians(self.angle))

        self.__keys_actions(keys, delta_x, delta_y, bullet_fired, bullets)

        self.__teleporting_to_the_opposite_site(surface_size)
        self.image = pygame.transform.rotate(self.__const_image, self.angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.collision_rect.center = self.rect.center

        self.__padding_check()

