from weaklight.core import lights
import os
import threading

class Controller:
    def __init__(self, stripsconfig):
        for config in stripsconfig:
            self.strips.append(lights.Strip(**config))
        
        for strip in self.strips:
            for segment in strip.getSegments():
                self.segments[segment.name] = segment