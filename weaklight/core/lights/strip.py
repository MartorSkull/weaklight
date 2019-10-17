import rpi_ws281x
from .segment import Segment

class Strip(rpi_ws281x.PixelStrip):
    ''' Strip
    This class extends the PixelStrip and allows segmentating and controlling
    the different segments on their own.

    Keyword argument:
    num -- The number of leds the strip has
    pin -- The pin in which the data port of strip is connected
    name -- The name of the strip
    freq_hz -- The frequency of the display signal in hertz
    dma -- The dma channel
    invert -- A bool indicating if its necesary to invert the output
    brightness -- The brightness of the strip
    channel -- The PWM channel to use 
    '''
    def __init__(self, 
                 length, pin, name, freq_hz=800000, dma=10, 
                 invert=False, brightness=255, channel=0, 
                 strip_type=rpi_ws281x.ws.WS2811_STRIP_GRB, gamma=None, segments=[]):
        
        super(self.__class__, self).__init__(
            num=length, 
            pin=pin, 
            freq_hz=freq_hz, 
            dma=dma, 
            invert=invert, 
            brightness=brightness, 
            channel=channel, 
            strip_type=strip_type,
            gamma=gamma)

        self.num = length
        self.pin = pin
        self.freq_hz = freq_hz
        self.dma = dma
        self.invert = invert
        self.brightness = brightness
        self.channel = channel
        self.strip_type = strip_type
        self.gamma = gamma

        self.segments = []

        self.name = str(name)

        if len(segments)==0:
            self.segmented = False
        else:
            for segment in segments:
                self.segments.append(
                    Segment(segment['name'], self, segment['start'], segment['end']))
            self.segmented = True

    def setPixelColor(self, num, color):
        '''
        Sets the color of the pixel in the num position
        '''
        self._led_data[num]=color

    def setBuffer(self, buf):
        '''
        Sets the buffer to the one passed.
        '''
        if hasattr(buf, '__iter__') and len(buf)==self.num:
            self._led_data = buf
        else:
            raise TypeError(
                "The buffer must be iterable, and the same length as the strip")


    def showSegment(self, segment):
        '''
        Renders the given segment.
        '''
        if not self.segmented:
            raise UserWarning("This function should only be called if the strip is segmented.")
        for i in range(segment.startend[0],segment.startend[1]):
            self._led_data[i] = segment.buffer[i-segment.startend[0]]
        self.show()

    def getSegments(self):
        '''
        returns the segments
        '''
        if not self.segmented:
            return []
        return self.segments