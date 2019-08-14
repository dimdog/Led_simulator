import pygame
from collections import namedtuple

Color = namedtuple('Color', 'red green blue')


clock = None
screen = None

class Strand(object):

    def __init__(self, length):
        self.length = length
        self.colors = []

    def add_rgb(self, red, green, blue):
        color = Color(red=red, green=green, blue=blue)
        self.add_color(color)

    def add_color(self, color):
        self.colors.insert(0, color)
        self.colors = self.colors[:self.length]


class StrandManager(object):

    def __init__(self, screen, height, width):
        self.screen = screen
        self.height = height
        self.width = width
        self.strands = []

    def display(self):
        # figure out how big the leds should be
        x_space = self.width / len(self.strands)
        y_space = self.height / max([strand.length for strand in self.strands])
        for x,strand in enumerate(self.strands):
            for y,color in enumerate(strand.colors):
                #print("Drawing:{} @ ({}, {})".format((color.red, color.green, color.blue), int(x*x_space), int(y*y_space)))
                pygame.draw.circle(self.screen, (color.red, color.green, color.blue), (int(x*x_space)+50, int(((y*y_space)+y_space/2))), int(y_space/2))


