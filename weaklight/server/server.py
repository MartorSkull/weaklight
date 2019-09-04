import pydbus
from pgi.repository import GLib

import weaklight.core.dbus
from . import classes

class DBusServer(object):
    """Class to represent the server running in Dbus"""
    def __init__(self, address, strips, bus_type="system", socket=None):
        super(DBusServer, self).__init__()
        self.strips = []
        if (hasattr(strips, "__iter__")):
            self.strips = strips
        else:
            self.strips.append(strips)

        if (bus_type == "System"):
            self.bus = pydbus.SystemBus()
        elif (bus_type == "Session"):
            self.bus = pydbus.SessionBus()
        else:
            raise AttributeError("The bus type is not valid")
        self.address = address
        
    def start_server(self):
        loop = GLib.MainLoop()
        
        dbus_segments = []
        dbus_strips = []

        for strip in self.strips:
            if strip.segmented:
                for segment in strip.getSegments():
                    dbus_segments.append(classes.Segment(segment, self.address))
            dbus_strips.append(classes.Strip(strip, self.address))

        publish = self.bus.publish(self.address,
            *dbus_strips,
            *dbus_segments)

        loop.run()