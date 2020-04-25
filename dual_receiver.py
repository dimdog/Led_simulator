import pygame
import time
import random
import serial
import struct

import strands
import redis
from patterns import RandomPattern, SimpleRandomPattern

ser = None
ser2 = None
try:
    ser = serial.Serial('/dev/tty.usbmodem14201', baudrate=1000000)
    ser2 = serial.Serial('/dev/tty.usbmodem14101', baudrate=1000000)
except:
    pass

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


# Protocol for wire.
# 1. A number, to specify which strip is being accessed - e.g. `0`
# 2. A number, specifying which type of data we are sending
#   I. 0 means individual leds
#   II. 1 means color wipe
# 3. Data for the protocal type
#   Individual LEDS: R G B (Repeated)
#   Color Wipe R G B
def individual_leds(serial):
    for i, pattern in enumerate(sm.patterns):
        # Protocol # 1
        serial.write(struct.pack('>B',i))
        # Protocol # 2
        serial.write(struct.pack('>B', 0))
        for color in pattern.strand.colors:
            if serial:
                serial.write(struct.pack('>B', min(254, color[0])))
                serial.write(struct.pack('>B', min(254,color[1])))
                serial.write(struct.pack('>B', min(254,color[2])))
                #printed = False
                #while serial.in_waiting or not printed:
                #    printed = True
                #    print(serial.readline())
        serial.write(struct.pack('>B', 255))

def wipe_all_strips():
    for i, pattern in enumerate(sm.patterns):
        for color in pattern.strand.colors[:1]:
            if ser:
                color_wipe(ser, i, color)
            if ser2:
                color_wipe(ser2, i, color)


def color_wipe(serial, strip_number, color):
    # Protocol # 1
    serial.write(struct.pack('>B', strip_number))
    # Protocol # 2
    serial.write(struct.pack('>B', 1))
    # Protocol # 3
    #print("Red:{}, Green:{}, Blue:{}".format(color[0], color[1], color[2]))
    serial.write(struct.pack('>B', color[0]))
    serial.write(struct.pack('>B', color[1]))
    serial.write(struct.pack('>B', color[2]))
    #printed = False
    #while serial.in_waiting or not printed:
    #    printed = True
    #    print(serial.readline())


def init_serial(serial):
    while not serial.in_waiting: # warm up the serial connection
        data = serial.write(struct.pack('>B', 255))
        time.sleep(0.01)
    while serial.in_waiting: # clear the buffer
        serial.readline()

if ser:
    init_serial(ser)
if ser2:
    init_serial(ser2)
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
        if ser:
            individual_leds(ser)
        if ser2:
            individual_leds(ser2)
        #wipe_all_strips()
        pygame.display.flip()


