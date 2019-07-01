#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import weaklight
import threading
import time
import colour

def Color(red, green, blue, white = 0):
        """Convert the provided red, green, blue color to a 24-bit color value.
        Each color component should be a value 0-255 where 0 is the lowest intensity
        and 255 is the highest intensity.
        """
        return (white << 24) | (red << 16)| (green << 8) | blue

def tracerInit(segment, color, trace=3):
    for i in range(trace):
        for a in range(trace):
            if i-a>0:
                w,r,g,b=((color >> 24)& 255), ((color >> 16) & 255), ((color >> 8) & 255), (color & 255)
                c = colour.Color(rgb=(float(r)/255,float(g)/255,float(b)/255))
                c.luminance *= 1.0-(1.0*a)/trace
                cr = (int(w)<<24)|int(c.red*255)<<16|int(c.green*255)<<8|int(c.blue*255)
                segment.setPixel(i-a, cr)
            else:
                continue
        time.sleep(30/1000.0)
        segment.show()

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def tracer(segment, color, trace=3):
    for a in _trace(segment.numPixels(), trace):
        for pix, scale in a[::-1]:
            w,r,g,b=((color >> 24)& 255), ((color >> 16) & 255), ((color >> 8) & 255), (color & 255)
            c = colour.Color(rgb=(float(r)/255,float(g)/255,float(b)/255))
            c.luminance *= scale
            cr = (int(w)<<24)|int(c.red*255)<<16|int(c.green*255)<<8|int(c.blue*255)
            segment.setPixel(pix, cr)
            del c
        segment.show()
        time.sleep(30/1000.0)
        for i in range(segment.numPixels()):
            segment.setPixel(i,0)

def _trace(length, dist):
    for i in [(dist-1, length-1, 1),(length-1, -1, -1),(0, dist, 1)]:
        for a in range(*i):
            l=[]
            for e in range(dist):
                pos=a-(e*i[2])
                if (pos>length-1) or (pos<0):
                    pos = i[0]-(pos-i[0])
                scale=1.0-(1.0*(e+0))/dist
                l.append([pos, scale])
            yield l


def rainbowCycle(segment, wait_ms=20, iterations=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(segment.numPixels()):
            segment.setPixel(i, wheel((int(i * 256 / segment.numPixels()) + j) & 255))
        segment.show()
        time.sleep(wait_ms/1000.0)

def threadRainbow(segment):
    while True:
        print("thread rainbow")
        rainbowCycle(segment)

def threadTracer(segment):
    tracerInit(segment, 0x00FF0000)
    while True:
        print("thread tracer")
        tracer(segment, 0x00FF0000)

class Interrupt(threading.Thread, weaklight.core.threads.InterruptMixin):
    pass

config = {
    "num": 33,
    "pin": 18,
    "name": "test",
    "brightness": 52,
    "segments": [{
            "name": "0-15",
            "range": (0, 15)
        },
        {
            "name": "15-33",
            "range": (15, 33)
        }
    ]
}

strip = weaklight.core.lights.Strip(**config)

strip.begin()

segments = strip.getSegments()

segment1Thread = Interrupt(target=threadTracer, args=[segments[1]])
segment1Thread.daemon = True

segment2Thread = Interrupt(target=threadRainbow, args=[segments[0]])
segment2Thread.daemon = True

segment1Thread.start()
segment2Thread.start()

while True:
    time.sleep(10)
