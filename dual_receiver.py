import pygame
import time
import random
import serial
import struct

import strands
import redis
from patterns import RandomPattern, SimpleRandomPattern
from ArduinoLed import ArduinoLEDStrip


rand = random.Random()
pygame.init()
height = 600
width = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("LED SIMULATOR")

# make n strands of x length inputtable

s0 = strands.Strand(320)
rp0 = SimpleRandomPattern(s0)
#rp0 = RandomPattern(s0)
sm = strands.PatternManager(screen, height, width)
sm.patterns.append(rp0)
#sm.patterns.append(rp1)
#sm.patterns.append(rp2)
#sm.patterns.append(rp3)
#sm.patterns.append(rp4)

done = False
r = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)



strip = None
strip2 = None
try:
    strip1 = ArduinoLEDStrip('/dev/tty.usbmodem14201', sm.patterns)
    strip2 = ArduinoLEDStrip('/dev/tty.usbmodem14101', sm.patterns)
except:
    print("No strips!")

while not done:
        for event in pygame.event.get():
            if event.type == 2: # keydown
                print(event)
                print(event.unicode)
                try:
                    a = int(event.unicode)
                    rp0.change_color_range(a)
                except:
                    pass
            if event.type == pygame.QUIT:
                done = True
        msg = r.rpop("beat_queue")
        data = msg
        for pattern in sm.patterns:
            pattern.msg(data)
        sm.display()
        if strip:
            strip.individual_leds()
        if strip2:
            strip2.individual_leds()
        #wipe_all_strips()
        pygame.display.flip()


