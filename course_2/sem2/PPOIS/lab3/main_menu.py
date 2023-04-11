import json
import os
import sys
from json import JSONDecodeError
from typing import List, Dict

import pygame
import pygame_gui

from game import Game


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


class EnterNameMenu:

    def __init__(self):
        self.window_size = (1000, 1000)
        self.screen = pygame.display.set_mode(self.window_size)
        self.manager = pygame_gui.UIManager(self.window_size)

        self.background_image = pygame.image.load("./images/battlefield/battlefield_1.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (1000, 1000))
        self.time_delta = pygame.time.Clock().tick(60) / 1000.0
        self.name = ''

        font = pygame.font.Font(None, 48)
        text = "Вы новый лидер! Введите свое имя для доски почета!"
        self.text_surface = font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect()

        # Центрируем прямоугольник на экране
        self.text_rect.center = self.screen.get_rect().center

        # Отрисовываем текст на экране


        # Создание текстового поля для ввода имени
        self.name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.window_size[0] // 2 - 150, 550), (300, 50)),
            manager=self.manager,
            object_id='#name_input'
        )

        # Создание кнопки "Сохранить"
        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_size[0] // 2 + 75, 650), (150, 50)),
            manager=self.manager,
            text='Сохранить',
            object_id='#save_button'
        )

        # Создание кнопки "Выйти"
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_size[0] // 2 - 225, 650), (150, 50)),
            manager=self.manager,
            text='Выйти',
            object_id='#quit_button'
        )

        self.screen.blit(self.text_surface, self.text_rect)
        pygame.display.flip()


    def run(self):
        done = False
        while not done:
            self.time_delta = pygame.time.Clock().tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                self.manager.process_events(event)

                # Обработка события нажатия на кнопку "Сохранить"
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.save_button:
                            self.name = self.name_input.get_text()
                            # Сохранение имени
                            done = True

                # Обработка события нажатия на кнопку "Выйти"
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.quit_button:
                            done = True

            self.screen.blit(self.background_image, (0, 0))
            self.manager.update(self.time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.update()
            self.screen.blit(self.text_surface, self.text_rect)
            pygame.display.flip()
        self.screen.blit(self.background_image, (0, 0))

        
        return self.name


class MainMenu:

    @staticmethod
    def __create_info_window():
        # создаем новое окно
        info_window = pygame.display.set_mode((1000, 1000))

        # загружаем картинку для заднего фона нового окна
        background_image = pygame.image.load("./images/battlefield/battlefield_1.jpg")
        background_image = pygame.transform.scale(background_image, (1000, 1000))

        # устанавливаем задний фон нового окна
        info_window.blit(background_image, (0, 0))

        font = pygame.font.Font(None, 36)
        text_lines = ["Vlad's Asteroid Adventure - это захватывающая игра-аркада,", "в которой вы берете на себя роль",
                      "космического пилота по имени Влад.", "Ваша задача - уничтожить астероиды,",
                      "которые угрожают вашей космической", "станции и всему человечеству.",
                      "Вы будете управлять своим космическим", "кораблем и стрелять в астероиды, которые",
                      "будут приближаться к вашей станции.", "Во время игры вы можете из астероидов",
                      "выбивать улучшение для коробля,", "собирайте их быстро!", "Вы также сможете соревноваться",
                      "с другими игроками за высокие места в", "таблице лидеров и стать настоящим",
                      "героем космоса. Примите вызов и", "отправляйтесь в увлекательное космическое",
                      "приключение в Vlad's Asteroid Adventure!"]

        text_surfaces = []
        for line in text_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            text_surfaces.append(text_surface)

        line_height = font.get_height()
        y = info_window.get_height() / 2 - (line_height * len(text_lines)) / 2
        for text_surface in text_surfaces:
            text_rect = text_surface.get_rect(center=(info_window.get_width() / 2, y))
            info_window.blit(text_surface, text_rect)
            y += line_height

        # отображаем новое окно
        pygame.display.update()

        # основной цикл обработки событий в окне информации
        info_window_opened = True
        while info_window_opened:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # закрыть окно информации и вернуться к основному окну
                    info_window_opened = False
                    info_window.blit(background_image, (0, 0))


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # закрыть окно информации и вернуться к основному окну
                        info_window_opened = False
                        info_window.blit(background_image, (0, 0))

        # закрыть окно информации и вернуться к основному окну

    @staticmethod
    def __create_rating_window():
        # создаем новое окно
        info_window = pygame.display.set_mode((1000, 1000))

        # загружаем картинку для заднего фона нового окна
        background_image = pygame.image.load("./images/battlefield/battlefield_1.jpg")
        background_image = pygame.transform.scale(background_image, (1000, 1200))

        # устанавливаем задний фон нового окна
        info_window.blit(background_image, (0, 0))

        font = pygame.font.Font(None, 36)
        list_of_names = []

        try:
            with open('./score_file.json', 'r') as f:
                rating_list = json.load(f)
                for i in rating_list[:10]:
                    list_of_names.append(f'{i[0]} -- {i[1]}')
                print(list_of_names)
                list_of_names.insert(0, 'Доска почета: ')
                text_surfaces = []
                for line in list_of_names:
                    text_surface = font.render(line, True, (255, 255, 255))
                    text_surfaces.append(text_surface)

                line_height = font.get_height()
                y = info_window.get_height() / 2 - (line_height * len(list_of_names)) / 2
                for text_surface in text_surfaces:
                    text_rect = text_surface.get_rect(center=(info_window.get_width() / 2, y))
                    info_window.blit(text_surface, text_rect)
                    y += line_height




        except FileNotFoundError:
            text_surface = font.render('Нету ни одной записи о игроках!', True, (255, 255, 255))
            line_height = font.get_height()
            y = info_window.get_height() / 2 - (line_height * len(list_of_names)) / 2
            text_rect = text_surface.get_rect(center=(info_window.get_width() / 2, y))
            info_window.blit(text_surface, text_rect)

        pygame.display.update()

        # основной цикл обработки событий в окне информации
        info_window_opened = True
        while info_window_opened:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # закрыть окно информации и вернуться к основному окну
                    info_window_opened = False
                    info_window.blit(background_image, (0, 0))

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # закрыть окно информации и вернуться к основному окну
                        info_window_opened = False
                        info_window.blit(background_image, (0, 0))

        # закрыть окно информации и вернуться к основному окну

    def __compare_scores(self, new_score):
        if os.path.exists(self.score_file):
            print("Score file already exists")
            with open(self.score_file, 'r+') as f:
                try:
                    dictionary: List[list] = json.load(f)
                    if dictionary and dictionary[0][1] < new_score:
                        name = EnterNameMenu().run()
                        if name:
                            dictionary.insert(0, [name, new_score])
                            f.seek(0)  # перемещаем курсор в начало файла
                            json.dump(dictionary, f)
                            f.truncate()
                except JSONDecodeError:
                    name = EnterNameMenu().run()
                    if name:
                        dictionary = [[name, new_score]]
                        json.dump(dictionary, f)

        else:
            with open(self.score_file, 'x') as f:
                name = EnterNameMenu().run()
                if name:
                    dictionary = [[name, new_score]]
                    json.dump(dictionary, f)

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption("Vlad\'s Asteroid Adventure")

        self.font = pygame.font.Font(None, 36)

        self.start_button = Button(400, 300, 200, 50, "Start Game")
        self.info_button = Button(400, 400, 200, 50, "Get Information")
        self.rating_button = Button(400, 500, 200, 50, "Player rating")
        self.exit_button = Button(400, 600, 200, 50, "Exit Game")

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.start_button)
        self.all_sprites.add(self.info_button)
        self.all_sprites.add(self.rating_button)
        self.all_sprites.add(self.exit_button)
        self.background_image = pygame.image.load('./images/battlefield/battlefield_1.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (1000, 1000))
        self.screen.blit(self.background_image, (0, 0))

        self.score_file = 'score_file.json'

    def run(self):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Проверка коллизии с кнопками
                    mouse_pos = pygame.mouse.get_pos()
                    if self.start_button.rect.collidepoint(mouse_pos):
                        print("Start Game")
                        game = Game('Vlad\'s Asteroid Adventure', width=1000, height=1000,
                                    back_image_filename='images/battlefield/battlefield_1.jpg',
                                    frame_rate=40)
                        print('action')
                        result = game.run()
                        print(result)
                        self.__compare_scores(result)
                    elif self.info_button.rect.collidepoint(mouse_pos):
                        self.__create_info_window()
                    elif self.rating_button.rect.collidepoint(mouse_pos):
                        self.__create_rating_window()
                    elif self.exit_button.rect.collidepoint(mouse_pos):
                        print("Exit Game")
                        done = True

            self.all_sprites.draw(self.screen)
            for sprite in self.all_sprites:
                sprite.draw(self.screen)
            pygame.display.update()
