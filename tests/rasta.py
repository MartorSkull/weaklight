#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import weaklight
import rpi_ws281x
import threading
import time

def Color(red, green, blue, white = 0):
        """Convert the provided red, green, blue color to a 24-bit color value.
        Each color component should be a value 0-255 where 0 is the lowest intensity
        and 255 is the highest intensity.
        """
        return (white << 24) | (red << 16)| (green << 8) | blue


config = {
    "num": 33,
    "pin": 18,
    "name": "test",
    "brightness": 52,
    "segments": [{
            "name": "0-11",
            "range": (0, 11)
        },
        {
            "name": "11-33",
            "range": (11, 22)
        },        
        {
            "name": "22-33",
            "range": (22, 33)
        }
    ],
    "strip_type": rpi_ws281x.ws.WS2811_STRIP_GRB,
}

strip = weaklight.core.lights.Strip(**config)

strip.begin()

segments = strip.getSegments()


for led in range(segments[0].length):
    segments[0].setPixel(led, Color(255,0,0))

for led in range(segments[1].length):
    segments[1].setPixel(led, Color(255,255,0))

for led in range(segments[2].length):
    segments[2].setPixel(led, Color(0,255,0))


for segment in segments:
    segment.show()
