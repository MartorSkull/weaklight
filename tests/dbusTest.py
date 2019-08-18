#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from weaklight.server.bus_server import *
from weaklight.server.caps import Types as caps 
import pydbus

class Weaklight(DBusObject):
    last_sum = 0

    @add_annotation("org.freedesktop.DBus.Deprecated", "true")
    @dbus_method
    def sum(self, first: caps.Int, second: caps.Int) -> caps.Int:
        self.last_sum = first + second
        return self.last_sum

    @dbus_method
    def printAllItems(self, array: caps.Array(caps.String)):
        for i in array:
            print(i)

    def last_sum_set(self, value):
        self.last_sum = value

    @dbus_property(last_sum_set)
    def last_sum_get(self, *args) -> caps.Int:
        return self.last_sum



bus = pydbus.SessionBus()
loop = GLib.MainLoop()

publish = bus.publish("org.weaklight.pydbus",
    Weaklight("org.weaklight.pydbus.Weaklight")
)

loop.run()
