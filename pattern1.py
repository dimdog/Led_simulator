import pygame
import strands
import time
import random

pygame.init()
height = 600
width = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("LED SIMULATOR")

rand = random.Random()
s = strands.Strand(50)
s2 = strands.Strand(50)
s3 = strands.Strand(50)
s4 = strands.Strand(50)
sm = strands.StrandManager(screen, height, width)
sm.strands.append(s)
sm.strands.append(s2)
sm.strands.append(s3)
sm.strands.append(s4)

done = False

def add_random_to_strand(strand):
    red = rand.randint(0,255)
    green = rand.randint(0,255)
    blue = rand.randint(0,255)
    strand.add_rgb(red, green, blue)


while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        for strand in sm.strands:
            add_random_to_strand(strand)
        sm.display()

        pygame.display.flip()


