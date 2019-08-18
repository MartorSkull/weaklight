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
                 num, pin, name, freq_hz=800000, dma=10, 
                 invert=False, brightness=255, channel=0, 
                 strip_type=rpi_ws281x.ws.WS2811_STRIP_GRB, gamma=None, segments=[]):
        
        super(self.__class__, self).__init__(
            num=num, 
            pin=pin, 
            freq_hz=freq_hz, 
            dma=dma, 
            invert=invert, 
            brightness=brightness, 
            channel=channel, 
            strip_type=strip_type,
            gamma=gamma)

        self.segments = []

        self.buf = self._led_data

        if len(segments)==0:
            self.segments.append(Segment(name, self, (0, num-1)))
        else:
            for segment in segments:
                self.segments.append(
                    Segment(segment['name'], self, segment['range']))

    def setPixelColor(self, num, color):
        '''
        Sets the color of the pixel in the num position
        '''
        self.buf[num]=color

    def showSegment(self, segment):
        '''
        Renders the segment.
        '''
        for i in range(segment.startend[0], segment.startend[1]):
            self._led_data[i] = segment.buffer[i-segment.startend[0]]
        super(self.__class__, self).show()

    def getSegments(self):
        '''
        returns the segments
        '''
        return self.segments