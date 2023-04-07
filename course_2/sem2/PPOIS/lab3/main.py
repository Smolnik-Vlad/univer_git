from game import Game

if __name__ == '__main__':
    game = Game('Gamename', width=768, height=768, back_image_filename='images/battlefield/battlefield_1.jpg',
                frame_rate=40)
    game.run()
