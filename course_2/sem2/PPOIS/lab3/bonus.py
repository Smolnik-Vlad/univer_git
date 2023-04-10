import pygame


class Bonus(pygame.sprite.Sprite):

    @staticmethod
    def __load_image():
        image = pygame.image.load('./images/update/update.png')
        return pygame.transform.scale(image, (50, 50))

    def __init__(self, center):
        super().__init__()
        self.image = self.__load_image()
        self.rect = self.image.get_rect(center=center)
        self.bonus_start_time = pygame.time.get_ticks()
        print(self.bonus_start_time)

    def update(self, args):
        current_time = pygame.time.get_ticks()
        if current_time - self.bonus_start_time > 5000:
            self.kill()

