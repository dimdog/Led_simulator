import pygame
import time
import random

import strands
from patterns import RandomPattern

pygame.init()
height = 600
width = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("LED SIMULATOR")

rand = random.Random()
s0 = strands.Strand(160)
rp0 = RandomPattern(s0)
s1 = strands.Strand(160)
rp1 = RandomPattern(s1)
s2 = strands.Strand(160)
rp2 = RandomPattern(s2)
s3 = strands.Strand(160)
rp3 = RandomPattern(s3)
s4 = strands.Strand(160)
rp4 = RandomPattern(s4)
sm = strands.PatternManager(screen, height, width)
sm.patterns.append(rp0)
sm.patterns.append(rp1)
sm.patterns.append(rp2)
sm.patterns.append(rp3)
sm.patterns.append(rp4)

done = False

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        for pattern in sm.patterns:
            pattern.msg(None)
        sm.display()

        pygame.display.flip()


