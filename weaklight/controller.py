import os

from .core import lights
from .server import DBusServer

class Controller:
    strips = []

    def __init__(self, config):
        self.config = config
        if (isinstance(config, map)):
            for stripsconfig in config['strips']:
                self.strips.append(lights.Strip(**stripsconfig))
        else:
            self.strips.append(lights.Strip(**config['strips']))

    def begin(self):
        for strip in self.strips:
            strip.begin()
        self.server = DBusServer(strips=self.strips, **self.config['dbus'])
        self.server.start_server()