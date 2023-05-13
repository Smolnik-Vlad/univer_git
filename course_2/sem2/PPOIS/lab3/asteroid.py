import math
import random

import pygame.sprite


class Asteroid(pygame.sprite.Sprite):
    asteroids_amount = 0

    @staticmethod
    def __load_image(size=None):
        asteroids_images = ['./images/asteroids/asteroid_1.png', './images/asteroids/asteroid_2.png']
        asteroid_image = random.choice(asteroids_images)

        image = pygame.image.load(asteroid_image)

        size = random.randint(50, 90) if not size else int(size)

        return pygame.transform.scale(image, (size, size)), size

    def __choosing_place_for_generation(self, surface_size: tuple):
        side = random.randint(1, 4)
        x, y = 0, 0
        if side == 1:
            x = random.randint(-80, -40)
            y = random.randint(0, surface_size[1])
            self.angle = random.randint(-90, 90)
        if side == 2:
            x = random.randint(0, surface_size[0])
            y = random.randint(-80, -40)
            self.angle = random.randint(180, 360)

        if side == 3:
            x = random.randint(surface_size[0] + 40, surface_size[0] + 80)
            y = random.randint(0, surface_size[1])
            self.angle = random.randint(90, 270)

        if side == 4:
            x = random.randint(0, surface_size[0])
            y = random.randint(surface_size[1] + 40, surface_size[1] + 80)
            self.angle = random.randint(0, 180)

        return x, y

    def __init__(self, surface_size: tuple, params: dict = None, first_time=True):
        super().__init__()
        if first_time:
            self.image, self.size = self.__load_image()
            x, y = self.__choosing_place_for_generation(surface_size)
            self.acceleration = not bool(random.randint(0, 4))

        else:
            self.image, self.size = self.__load_image(params['size'])
            x, y = params['x'], params['y']
            self.acceleration = False
            self.angle = random.randint(0, 360)

        self.rect = pygame.Rect(x, y, self.size / 1.7, self.size / 1.7)
        self.speed = random.randint(1, 3)

    def update(self, args: dict) -> None:
        surface_size = args['surface_size']
        if self.acceleration:
            self.speed += 0.1
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y -= self.speed * math.sin(math.radians(self.angle))
        if self.rect.right < -40 or self.rect.left > surface_size[0] + 40 or self.rect.bottom < -40 or \
                self.rect.top > surface_size[1] + 40:
            self.__class__.asteroids_amount -= 1
            self.kill()

    def draw_collision(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
