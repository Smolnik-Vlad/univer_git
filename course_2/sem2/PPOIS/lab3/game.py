import sys
from collections import defaultdict

import pygame

from asteroid import Asteroid
from bullet import Bullet
from spaceship import SpaceShip


class Game:

    def __init__(self,
                 caption,
                 width,
                 height,
                 back_image_filename,
                 frame_rate):
        self.background_image = pygame.image.load(back_image_filename)  # задаем картинку
        self.frame_rate = frame_rate  # задаем частоту кадров
        self.game_over = False
        self.sprites = pygame.sprite.Group()  # объекты игры
        self.spaceship = SpaceShip(250, 250, 7, self.sprites)
        self.sprites.add(self.spaceship)
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        pygame.mixer.pre_init(44100, 16, 2, 4096)  # активируем модуль для взаимодействия со звуком
        pygame.init()  # сам модуль
        pygame.font.init()  # работа со шрифтами
        self.surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)  # отображение дисплея
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

    def __set_background_size(self):
        new_window_size = self.surface.get_size()
        self.background_image = pygame.transform.scale(self.background_image, new_window_size)

    def run(self):
        while not self.game_over:

            bullet_fired = False

            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bullet_fired = True
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    bullet_fired = False

            for asteroid in self.asteroids:
                if asteroid.rect.colliderect(self.spaceship.collision_rect):
                    print('BOOM! spaceship')

            # if self.asteroids.rect.colliderect(self.spaceship.rect):
            #     print('BOOM!')

            list_of_args_for_stripe = {'surface_size': self.surface.get_size(),
                                       'bullet_fired': bullet_fired,
                                       'screen': self.surface,
                                       'bullets': self.bullets}

            if Asteroid.asteroids_amount < 10:
                asteroid = Asteroid(self.surface.get_size(), self.surface)
                self.asteroids.add(asteroid)
                self.sprites.add(asteroid)
                Asteroid.asteroids_amount += 1

            # for a in self.asteroids:
            #     a.draw_collision(self.surface)
            # pygame.sprite.collide_circle()
            hits = pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True)
            if hits:
                Bullet.bullet_amount -= 1
                Asteroid.asteroids_amount -= 1
                print('BOOM!')

            self.sprites.update(list_of_args_for_stripe)
            self.surface.blit(self.background_image, (0, 0))
            self.__set_background_size()
            self.sprites.draw(self.surface)

            pygame.display.update()
            self.clock.tick(self.frame_rate)
