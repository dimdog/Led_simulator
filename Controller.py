import pygame
import time
import redis
from strands import PatternManager

class Controller(object):

    def __init__(self, patterns, led_strips=None, redis_url="localhost", height=600, width=800):
        self.redis = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)
        pygame.init()
        screen = pygame.display.set_mode((width, height))

        self.led_strips = led_strips or []
        self.pm = PatternManager(screen, height, width)
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


