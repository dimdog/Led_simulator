import serial
import struct

class ArduinoLEDStrip(object):

    def __init__(self, path, patterns, baudrate=None):
        self.patterns = patterns

        self.baudrate = baudrate or 1000000
        self.path = path or '/dev/tty.usbmodem14201'
        self.serial = serial.Serial(self.path, baudrate=self.baudrate)
        while not self.serial.in_waiting: # warm up the serial connection
            data = self.serial.write(struct.pack('>B', 255))
            time.sleep(0.01)
        while self.serial.in_waiting: # clear the buffer
            self.serial.readline()

    # Protocol for wire.
    # 1. A number, to specify which strip is being accessed - e.g. `0`
    # 2. A number, specifying which type of data we are sending
    #   I. 0 means individual leds
    #   II. 1 means color wipe
    # 3. Data for the protocal type
    #   Individual LEDS: R G B (Repeated)
    #   Color Wipe R G B
    def individual_leds(self):
        for i, pattern in enumerate(self.patterns):
            # Protocol # 1
            self.serial.write(struct.pack('>B',i))
            # Protocol # 2
            self.serial.write(struct.pack('>B', 0))
            for color in pattern.strand.colors:
                self.serial.write(struct.pack('>B', min(254, color[0])))
                self.serial.write(struct.pack('>B', min(254,color[1])))
                self.serial.write(struct.pack('>B', min(254,color[2])))
            self.serial.write(struct.pack('>B', 255))

    def color_wipe(self, strip_number, color):
        # strip number is almost always 0, but we can configure multiple strips on one arduino
        # Protocol # 1
        self.serial.write(struct.pack('>B', strip_number))
        # Protocol # 2
        self.serial.write(struct.pack('>B', 1))
        # Protocol # 3
        #print("Red:{}, Green:{}, Blue:{}".format(color[0], color[1], color[2]))
        self.serial.write(struct.pack('>B', color[0]))
        self.serial.write(struct.pack('>B', color[1]))
        self.serial.write(struct.pack('>B', color[2]))


