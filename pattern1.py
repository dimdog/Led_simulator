import pygame
import strands
import time
import random

pygame.init()
height = 300
width = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("LED SIMULATOR")

rand = random.Random()
s = strands.Strand(10)
sm = strands.StrandManager(screen, height, width)
sm.strands.append(s)

done = False

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        red = rand.randint(0,255)
        green = rand.randint(0,255)
        blue = rand.randint(0,255)
        s.add_rgb(red, green, blue)
        sm.display()

        pygame.display.flip()


