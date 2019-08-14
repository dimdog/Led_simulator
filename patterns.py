import time
import random


class Pattern(object):

    def __init__(self, strand):
        self.strand = strand
        self.rand = random.Random()

    def msg(self, msg):
        # take a message and return the strands colors
        return self.strand.colors


class RandomPattern(Pattern):

    def msg(self, msg):
        red = self.rand.randint(0,255)
        green = self.rand.randint(0,255)
        blue = self.rand.randint(0,255)
        self.strand.add_rgb(red, green, blue)
        return self.strand.colors

class SimpleRandomPattern(Pattern):

    def msg(self, msg):
        if msg:
            red = self.rand.randint(0,255)
            green = self.rand.randint(0,255)
            blue = self.rand.randint(0,255)
            self.strand.add_rgb(red, green, blue)
        return self.strand.colors


