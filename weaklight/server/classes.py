from weaklight.core.exceptions import *
from weaklight.core.dbus import *

class Segment(DBusObject):
    def __init__(self, segment, address):
        self.segment = segment
        super(self.__class__, self).__init__(
            name=self.segment.name, address=address)

    @dbus_method
    def setPixels(self, 
                  colors: Types.Array(Types.Int)) -> Types.Boolean:
        try:
            self.segment.setBuffer(colors)
            self.segment.show()
        except TypeError:
            return False
        return True

    @dbus_method
    def setPixel(self, 
                 num: Types.Int, 
                 color: Types.Int, 
                 brightness: Types.Double=1) -> Types.Boolean:
        try:
            self.segment.setPixel(num, color, brightness)
            self.segment.show()
        except OutOfRangeException:
            return False
        return True

    @dbus_property()
    def name(self) -> Types.Int:
        return self.segment.id

    @dbus_property()
    def length(self) -> Types.Int:
        return self.segment.length

    @dbus_property()
    def start(self) -> Types.Int:
        return self.segment.startend[0]

    @dbus_property()
    def end(self) -> Types.Int:
        return self.segment.startend[1]


class Strip(DBusObject):
    def __init__(self, strip, address):
        self.strip = strip
        
        super(self.__class__, self).__init__(
            name=self.strip.name, address=address)

    @dbus_method
    def setPixel(self, 
                 num: Types.Int, 
                 color: Types.Int, 
                 brightness: Types.Double=1) -> Types.Boolean:
        try:
            self.strip.setPixelColor(num, color)
            self.strip.show()
        except OutOfRangeException:
            return False
        return True

    @dbus_method
    def setPixels(self, 
                  colors: Types.Array(Types.Int)) -> Types.Boolean:
        try:
            self.strip.setBuffer(colors)
            self.strip.show()
        except TypeError:
            return False
        return True

    def segments(self) -> Types.Array(
                            Types.Struct(
                                Types.String,
                                Types.Int,
                                Types.Int)):
        return [(x.id,x.startend[0],x.startend[1]) for x in self.strip.getSegments()]

    @dbus_property()
    def length(self) -> Types.Int:
        return self.strip.num

    @dbus_property()
    def pin(self) -> Types.Int:
        return self.strip.pin

    @dbus_property()
    def frequency(self) -> Types.Int:
        return self.strip.freq_hz

    @dbus_property()
    def dma(self) -> Types.Int:
        return self.strip.dma

    @dbus_property()
    def invert(self) -> Types.Boolean:
        return self.strip.invert

    @dbus_property()
    def brightness(self) -> Types.Int:
        return self.strip.brightness

    @dbus_property()
    def channel(self) -> Types.Int:
        return self.strip.channel