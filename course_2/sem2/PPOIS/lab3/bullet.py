import math

import pygame.sprite


class Bullet(pygame.sprite.Sprite):
    @staticmethod
    def __load_image():
        image = pygame.image.load('./images/bullets/bullet_1.png')
        return pygame.transform.scale(image, (50, 50))

    def __init__(self, pos, angle):
        super().__init__()
        self.image = self.__class__.__load_image()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.angle = angle

    def update(self, args: list) -> None:
        surface_size = args['surface_size']
        self.rect.x += 10 * math.cos(math.radians(self.angle))
        self.rect.y -= 10 * math.sin(math.radians(self.angle))
        self.image = pygame.transform.rotate(self.__class__.__load_image(), self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.rect.right < 0 or self.rect.left > surface_size[0] or self.rect.bottom < 0 or \
                self.rect.top > surface_size[1]:
            self.kill()
