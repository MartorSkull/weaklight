#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from weaklight.core.dbus import *
from weaklight.core.dbus import Types as caps 
import pydbus
from pgi.repository import GLib

class Weaklight(DBusObject):
    last_sum = 0
    hello = "hello"

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
    def last_sum_get(self, *args) -> caps.Struct(caps.Int, caps.String):
        return (self.last_sum, self.hello)



bus = pydbus.SessionBus()
loop = GLib.MainLoop()

publish = bus.publish("org.weaklight.pydbus",
    Weaklight("org.weaklight.pydbus","Weaklight")
)

loop.run()
