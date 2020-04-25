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


class PatternManager(object):

    def __init__(self, screen, height, width):
        self.screen = screen
        self.height = height
        self.width = width
        self.patterns = []

    def change_color_range(self, color_range_number):
        for pattern in self.patterns:
            pattern.change_color_range(color_range_number)

    def display(self):
        # figure out how big the leds should be
        x_space = self.width / max([pattern.strand.length for pattern in self.patterns])
        y_space = self.height / len(self.patterns)
        for y,pattern in enumerate(self.patterns):
            for x,color in enumerate(pattern.strand.colors):
                #print("Drawing:{} @ ({}, {})".format((color.red, color.green, color.blue), int(x*x_space), int(y*y_space)))
                pygame.draw.circle(self.screen, (color.red, color.green, color.blue), (int(x*x_space+x_space/2), int(((y*y_space)+50))), int(x_space/2))


