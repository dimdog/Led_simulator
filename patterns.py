import time
import random
import colour

# Red --> OrangeRed (Default)
# Red --> Tomato (warming up)
# DarkOrange --> OrangeRed (good)
# DarkCyan --> Red (PARTY)
# Red --> Blue (PARTY!!)
# Green --> Blue (Good for blue mode) 
class Pattern(object):

    def __init__(self, strand):
        self.strand = strand
        self.rand = random.Random()
        self.counter = 0
        self.color = None
        color1 = colour.Color("Green")
        color2 = colour.Color("Blue")
        self.set_color_range(color1, color2)


    def set_color_range(self, color1, color2):
        hsl_cs = colour.color_scale(color1.get_hsl(), color2.get_hsl(), 100)
        rgb_cs = [colour.hsl2rgb(a) for a in hsl_cs]
        self.scaled_cs = []
        for a in rgb_cs:
            self.scaled_cs.append((round(a[0] * 255), round(a[1] * 255), round(a[2] * 255)))

    def msg(self, msg):
        # take a message and return the strands colors
        return self.strand.colors

    def change_color_range(self, mode):
        # (1) Red --> OrangeRed (Default)
        # (2) Red --> Tomato (warming up)
        # (3) DarkOrange --> OrangeRed (good)
        # (4) DarkCyan --> Red (PARTY)
        # (5) Red --> Blue (PARTY!!)
        # (6) Green --> Blue (Good for blue mode) 
        if mode == 1:
            self.set_color_range(colour.Color("Red"), colour.Color("OrangeRed"))
        elif mode == 2:
            self.set_color_range(colour.Color("Red"), colour.Color("Tomato"))
        elif mode == 3:
            self.set_color_range(colour.Color("DarkOrange"), colour.Color("OrangeRed"))
        elif mode == 4:
            self.set_color_range(colour.Color("DarkCyan"), colour.Color("Red"))
        elif mode == 5:
            self.set_color_range(colour.Color("Red"), colour.Color("Blue"))
        elif mode == 6:
            self.set_color_range(colour.Color("Green"), colour.Color("Blue"))


class RandomPattern(Pattern):

    def msg(self, msg):
        red = self.rand.randint(0,255)
        self.strand.add_rgb(red,0, 0)
        return self.strand.colors

class SimpleRandomPattern(Pattern):
    """Silver, Firebrick"""

    def msg(self, msg):
        if not self.color:
            col = self.rand.randint(0, 100)
            self.color = self.scaled_cs[col]

        if msg == "Beat":
            col = self.rand.randint(0, 100)
            self.color = self.scaled_cs[col]
            for i in range(50):
                self.strand.add_rgb(self.color[0], self.color[1], self.color[2])
        else:
            add = 1
            try: 
                msg = int(msg)
                add += max(0, msg)
            except:
                pass
            col = self.rand.randint(0, 100)
            self.color = self.scaled_cs[col]
            for i in range(add):
                self.strand.add_rgb(self.color[0], self.color[1], self.color[2])
        return self.strand.colors


