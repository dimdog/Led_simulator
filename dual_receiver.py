from patterns import RandomPattern, SimpleRandomPattern
import strands
from ArduinoLed import ArduinoLEDStrip
from Controller import Controller
# make n strands of x length inputtable

s0 = strands.Strand(40)
s1 = strands.Strand(40)
s2 = strands.Strand(40)
s3 = strands.Strand(40)
s4 = strands.Strand(40)
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

