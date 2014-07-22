import pygame
from pygame.locals import *
import util
from sound import play_sound
from shape import Tile, Shape

class Tetris(object):
	W = 12		# the width