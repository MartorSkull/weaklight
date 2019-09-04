from weaklight.core.exceptions import *
import colour

class Segment:
    def __init__(self, name, strip, start, end):
        self.name = str(name)
        self.strip = strip
        self.length = end-start
        if self.length<1:
            raise AttributeError(
                "The start of the range can't be bigger than the end.")
        self.startend = (start,end)

        self.buffer = [0 for i in range(self.length)]

    def setBuffer(self, buf):
        '''
        Sets the buffer to the one passed.
        '''
        if hasattr(buf, '__iter__') and len(buf)==self.length:
            self.buffer = buf
        else:
            raise TypeError(
                "The buffer must be iterable, and the same length as the segment")

    def setPixel(self, num, color, scale=1):
        '''
        Sets the pixel in the position num to the color and the brightness
        '''
        if num>self.length-1 or num<0:
            raise OutOfRangeException(
                "The last pixel of the segment {name} is {length}.".format(
            name=self.name,
                length=self.length-1))

        self.buffer[num] = self._apply_scale(color, scale)

    def show(self):
        '''
        Renders the segment 
        '''
        self.strip.showSegment(self)

    def numPixels(self):
        '''
        Returns the length of the segment
        '''
        return self.length

    def _apply_scale(self, color, scale):
        '''
        Used to scale the color in brightness
        '''
        # The scale should be a float between 0 and 1
        if scale<0 or scale>1:
            raise ValueError(
                "Scale must be a float between 0 and 1.")
        
        # Pass the color to it's separate colors
        r,g,b=((color >> 16) & 255), ((color >> 8) & 255), (color & 255)
        # The Color class takes floats between 0 and 1
        c = colour.Color(rgb=(float(r)/255,float(g)/255,float(b)/255))
        # Modify the luminance
        c.luminance *= scale
        # Recreate the color and return it
        cr = int(c.red*255)<<16|int(c.green*255)<<8|int(c.blue*255)
        
        return cr