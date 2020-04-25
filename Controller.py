import pygame
import time
import strands
import redis
from patterns import RandomPattern, SimpleRandomPattern
from ArduinoLed import ArduinoLEDStrip

class Controller(object):

    def __init__(self, patterns, led_strips=None, redis_url="localhost", height=600, width=800):
        self.redis = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)
        pygame.init()
        screen = pygame.display.set_mode((width, height))

        self.led_strips = led_strips or []
        self.pm = strands.PatternManager(screen, height, width)
        for pattern in patterns:
            self.pm.patterns.append(pattern) # make a goddamn add function
        pygame.display.set_caption("LED SIMULATOR")
        self.exit = False

    def loop(self):
        while not self.exit:
                for event in pygame.event.get():
                    if event.type == 2: # keydown
                        try:
                            a = int(event.unicode)
                            self.pm.change_color_range(a)
                        except:
                            pass
                    if event.type == pygame.QUIT:
                        done = True
                msg = self.redis.rpop("beat_queue")
                data = msg
                for pattern in self.pm.patterns:
                    pattern.msg(data)
                self.pm.display()
                for led_strip in self.led_strips:
                    led_strip.individual_leds()
                pygame.display.flip()


# make n strands of x length inputtable

s0 = strands.Strand(320)
s1 = strands.Strand(320)
s2 = strands.Strand(320)
s3 = strands.Strand(320)
s4 = strands.Strand(320)
rp0 = SimpleRandomPattern(s0)
rp1 = SimpleRandomPattern(s1)
rp2 = SimpleRandomPattern(s2)
rp3 = SimpleRandomPattern(s3)
rp4 = SimpleRandomPattern(s4)
#rp0 = RandomPattern(s0)

strip = None
strip2 = None
led_strips = []
try:
    strip1 = ArduinoLEDStrip('/dev/tty.usbmodem14201', sm.patterns)
    strip2 = ArduinoLEDStrip('/dev/tty.usbmodem14101', sm.patterns)
    led_strips = [strip1, strip2]
except:
    print("No strips!")

c = Controller([rp0, rp1, rp2, rp3, rp4], led_strips=led_strips)


c.loop()
