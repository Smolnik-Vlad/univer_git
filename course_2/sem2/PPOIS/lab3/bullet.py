import math
import random

import pygame.sprite


class Bullet(pygame.sprite.Sprite):
    bullet_amount: int = 0
    increase = 0

    @staticmethod
    def __load_image():
        image = pygame.image.load('./images/bullets/bullet_1.png')
        return pygame.transform.scale(image, (50 + Bullet.increase, 50 + Bullet.increase))

    def __init__(self, pos, angle):
        bullet_sounds = ['./sounds/bullet_sounds/bullet_sound_1.wav',
                         './sounds/bullet_sounds/bullet_sound_2.wav',
                         './sounds/bullet_sounds/bullet_sound_3.wav']
        bullet_sound = pygame.mixer.Sound(random.choice(bullet_sounds))
        super().__init__()
        self.image = self.__class__.__load_image()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.angle = angle
        bullet_sound.play()

    def update(self, args: list) -> None:
        surface_size = args['surface_size']
        self.rect.x += 15 * math.cos(math.radians(self.angle))
        self.rect.y -= 15 * math.sin(math.radians(self.angle))
        self.image = pygame.transform.rotate(self.__class__.__load_image(), self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.rect.right < 0 or self.rect.left > surface_size[0] or self.rect.bottom < 0 or \
                self.rect.top > surface_size[1]:
            self.kill()
            self.__class__.bullet_amount -= 1
