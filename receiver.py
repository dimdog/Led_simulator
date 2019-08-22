import pygame
import time
import random
import serial
import struct

import strands
import redis
from patterns import RandomPattern, SimpleRandomPattern

ser = None
try:
    ser = serial.Serial('/dev/tty.usbmodem14201', baudrate=1000000)
except:
    ser = serial.Serial('/dev/tty.usbmodem14101', baudrate=1000000)

rand = random.Random()
pygame.init()
height = 600
width = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("LED SIMULATOR")

# make n strands of x length inputtable

s0 = strands.Strand(300)
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
#sm.patterns.append(rp1)
#sm.patterns.append(rp2)
#sm.patterns.append(rp3)
#sm.patterns.append(rp4)

done = False
r = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)
p = r.pubsub(ignore_subscribe_messages=True)
p.subscribe("beats")
if not ser:
    print ("NO SERIAL")


# Protocol for wire.
# 1. A number, to specify which strip is being accessed - e.g. `0`
# 2. A number, specifying which type of data we are sending
#   I. 0 means individual leds
#   II. 1 means color wipe
# 3. Data for the protocal type
#   Individual LEDS: R G B (Repeated)
#   Color Wipe R G B
def individual_leds():
    for i, pattern in enumerate(sm.patterns):
        # Protocol # 1
        ser.write(struct.pack('>B',i))
        # Protocol # 2
        ser.write(struct.pack('>B', 0))
        for color in pattern.strand.colors:
            if ser:
                ser.write(struct.pack('>B', min(254, color[0])))
                ser.write(struct.pack('>B', min(254,color[1])))
                ser.write(struct.pack('>B', min(254,color[2])))
                #printed = False
                #while ser.in_waiting or not printed:
                #    printed = True
                #    print(ser.readline())
        ser.write(struct.pack('>B', 255))

def wipe_all_strips():
    for i, pattern in enumerate(sm.patterns):
        for color in pattern.strand.colors[:1]:
            color_wipe(i, color)


def color_wipe(strip_number, color):
    # Protocol # 1
    ser.write(struct.pack('>B', strip_number))
    # Protocol # 2
    ser.write(struct.pack('>B', 1))
    # Protocol # 3
    #print("Red:{}, Green:{}, Blue:{}".format(color[0], color[1], color[2]))
    ser.write(struct.pack('>B', color[0]))
    ser.write(struct.pack('>B', color[1]))
    ser.write(struct.pack('>B', color[2]))
    #printed = False
    #while ser.in_waiting or not printed:
    #    printed = True
    #    print(ser.readline())


def init_serial():
    while not ser.in_waiting: # warm up the serial connection
        data = ser.write(struct.pack('>B', 255))
        time.sleep(0.01)
    while ser.in_waiting: # clear the buffer
        ser.readline()

init_serial()
while not done:
        for event in pygame.event.get():
            if event.type == 2: # keydown
                print(event)
                print(event.unicode)
            if event.type == pygame.QUIT:
                done = True
        msg = p.get_message()
        data = msg["data"] if msg else None
        for pattern in sm.patterns:
            pattern.msg(data)
        sm.display()
        individual_leds() # try sending everything!
        #wipe_all_strips()
        pygame.display.flip()


