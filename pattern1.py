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
        red = rand.randint(0,255)
        green = rand.randint(0,255)
        blue = rand.randint(0,255)
        self.strand.add_rgb(red, green, blue)
        return self.strand.colors




