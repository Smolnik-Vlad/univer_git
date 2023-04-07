import math
import random

import pygame.sprite


class Asteroid(pygame.sprite.Sprite):
    asteroids_amount = 0

    @staticmethod
    def __load_image():
        asteroids_images = ['./images/asteroids/asteroid_1.png', './images/asteroids/asteroid_2.png']
        asteroid_image = random.choice(asteroids_images)

        image = pygame.image.load(asteroid_image)

        size = random.randint(50, 90)

        return pygame.transform.scale(image, (size, size))

    def __choosing_place_for_generation(self, surface_size: tuple):
        side = random.randint(1, 4)
        if side == 1:
            self.rect.x = random.randint(-80, -40)
            self.rect.y = random.randint(0, surface_size[1])
            self.angle = random.randint(-90, 90)
        if side == 2:
            self.rect.x = random.randint(0, surface_size[0])
            self.rect.y = random.randint(-80, -40)
            self.angle = random.randint(180, 360)

        if side == 3:
            self.rect.x = random.randint(surface_size[0] + 40, surface_size[0] + 80)
            self.rect.y = random.randint(0, surface_size[1])
            self.angle = random.randint(90, 270)

        if side == 4:
            self.rect.x = random.randint(0, surface_size[0])
            self.rect.y = random.randint(surface_size[1] + 40, surface_size[1] + 80)
            self.angle = random.randint(0, 180)

    def __init__(self, surface_size: tuple):
        super().__init__()
        self.image = self.__class__.__load_image()
        self.rect = self.image.get_rect()
        self.__choosing_place_for_generation(surface_size)
        self.speed = random.randint(1, 3)

    def update(self, args: dict) -> None:
        surface_size = args['surface_size']
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y -= self.speed * math.sin(math.radians(self.angle))
        if self.rect.right < -40 or self.rect.left > surface_size[0] + 40 or self.rect.bottom < -40 or \
                self.rect.top > surface_size[1] + 40:
            self.__class__.asteroids_amount -= 1
            self.kill()
