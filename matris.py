import pygame
from pygame import Rect, Surface
import random
import os
import kezmenu

from tetrominoes import list_of_tetrominoes
from tetrominoes import rotate

from scres import load_score, write_score

class BrokenMatrixException(Exception):
    pass

def get_sound(filename):
    return pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 
        "resources", filename))

BGCOLOR = (15, 15, 20)
BORDERCOLOR = (140, 140, 140)

BLOCKSIZE = 30
BORDERWIDTH = 10

MATRIS_OFFSET = 20

WIDTH =700
HEIGHT = 20 * BLOCKSIZE + BORDERWIDTH * 2 + MATRIS_OFFSET * 2

MATRIX_WIDTH = 10
MATRIX_HEIGHT = 22
VISIBLE_MATRIX_HEIGHT = MATRIX_HEIGHT - 2


class Matris(object):
    def __init__(self, size=(MATRIX_WIDTH, MATRIX_HEIGHT), blocksize = BLOCKSIZE):
        self.size = {'width': size[0], 'height': size[1]}
        self.blocksize = {'width': size[0], 'height': size[1]}
        self.surface = Surface((self.size['width'] * self.blocksize,
                                (self.size['height']-2) * self.blocksize))

        self.matrix = dict()
        for y in range(self.size['height']):
            for x in range(self.size['width']):
                self.matrix[(y,x)] = None

        self.next_tetromino = random.choice(list_of_tetrominoes)
        self.set_tetrominoes()
        self.tetromino_rotation = 0
        self.downwards_timer = 0
        self.base_downwards_speed = 0.4

        self.movement_keys = {'left': 0, 'right': 0}
        self.movement_keys_speed = 0.05
        self.movement_keys_timer = (-self.movement_keys_speed)*2

        self.level = 1
        self.score = 0
        self.lines = 0

        self.combo = 1 

        self.paused = False
        self.gameover = False

        self.hightscore = load_score()
        self.played_highscorebeaten_sound = False

        self.levelup_sound = get_sound("levelup.wav")
        self.gameover_sound = get_sound("gameover.wav")
        self.linescleared_sound = get_sound("linecleared.wav")
        self.hightscorebeaten_sound = get_sound("highscorebeaten.wav")

    def set_tetrominoes(self):
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = random.choice(list_of_tetrominoes)
        self.surface_of_next_tetromino = self.construct_surface_of_next_tetromino()
        self.tetromino_position = (0, 4) if len(self.current_tetromino.shape) == 2 else (0, 3)
        self.tetromino_rotation = 0
        self.tetromino_block = self.block(self.current_tetromino.color)
        self.shadow_block = self.block(self.current_tetromino.color, shadow = True)

    def hard_drop(self):
        amount = 0
        while self.request_movement('down'):
            amount += 1

        self.lock_tetromino()
        self.score += 10 * amount
        

     def update(self, timepassed):
        pressed = lambda key: event.type == pygame.KEYDOWN and event.key == key
        unpressed = lambda key: event.type == pygame.KEYUP and event.key == key

        events = pygame.event.get()

        for event in events:
            if pressed(pygame.K_p):
                self.surface.fill((0, 0, 0))
                self.paused = not self.paused
            elif event.type == pygame.QUIT:
                self.prepare_and_execute_gameover(playsound = False)
                exit()
            elif pressed(pygame.K_ESCAPE):
                self.prepare_and_execute_gameover(playsound = False)

        if self.paused:
            return

        for event in events:
            if pressed(pygame.K_SPACE):
                self.hard_drop()
            elif pressed(pygame.K_UP) or pressed(pygame.K_w):
                self.request_rotation()

            elif pressed(pygame.K_LEFT) or pressed(pressed.K_a):
                self.request_movement('left')
                self.movement_keys['left'] = 1
            elif pressed(pygame.K_RIGHT) or pressed(pygame.K_d):
                self.request_movement('right')
                self.movement_keys['right'] = 1

            elif unpressed(pygame.K_LEFT) or unpressed(pygame.K_a):
                self.movement_keys['left'] = 0
                self.movement_keys_timer = (-self.movement_keys_speed) * 2
            elif unpressed(pygame.K_RIGHT) or unpressed(pygame.K_d):
                self.movement_keys['right'] = 0
                self.movement_keys_timer = (-self.movement_keys_speed) * 2

        self.downwards_speed = self.base_downwards_speed ** (1 + self.level/10.)

        self.downwards_timer += timepassed
        downwards_speed = self.downwards_speed * 0.10 if any([pygame.key.get_pressed()[pygame.K_DOWN], 
                     pygame.key.get_pressed()[pygame.K_s]])    else self.downwards_speed
        if self.downwards_timer > downwards_speed:
            if not self.request_movement('down'):
                self.lock_tetromino()
            self.downwards_timer %= downwards_speed

        if any(self.movement_keys.values()):
            self.movement_keys_timer += timepassed
        if self.movement_keys_timer > self.movement_keys_speed:
            result = self.request_movement('right' if self.movement_keys['right'] else 'left')
            self.movement_keys_timer %= self.movement_keys_speed

        with_shadow = self.place_shadow()

        try:
            with_tetromino = self.blend(self.totated(), allow_failure = False, matrix = with_shadow)
        except BrokenMatrixException:
            self.prepare_and_execute_gameover()
            return

        for y in range(self.size['height']):
            for x in range(self.size['width']):
                block_location = Rect(x * self.blocksize, (y*self.blocksize - 2*self.blocksize), 
                    self.blocksize, self.blocksize)
                if with_tetromino[(y, x)] is None:
                    self.surface.fill(BGCOLOR, block_location)
                else:
                    if with_tetromino[(y,x)][0] == 'shadow':
                        self.surface.fill(BGCOLOR, block_location)

                    self.surface.blit(with_tetromino[(y,x)][1], block_location)

    def prepare_and_execute_gameover(self, playsound = True):
        if playsound:
            self.gameover_sound.play()
        write_score(self.score)
        self.gameover = True

    def palce_shadow(self):
        posY, posX = self.tetromino_position
        while self.blend(position = (posY, posX)):
            posY += 1

        position = (posY - 1, posX)

        return self.blend(position = position, block = self.shadow_block, 
            shadow = True) or  self.matrix
        



