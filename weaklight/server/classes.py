import pydbus

from weaklight.core.exceptions import *

class Segment:
    """
    <node>
        <interface name='org.weaklight.Segment'>
            <method name='setPixels'>
                <arg name='colors' type='ad' direcction='in'/>
                <arg name='response' type='b' direction='out'/>
            </method>
            <method name='setPixel'>
                <arg name='num' type='i' direction='in'/>
                <arg name='color' type='i' direction='in'/>
                <arg name='scale' type='f' direction='in'/>
                <arg name='response' type='b' direction='out'/>
            </method>
            <property name='name' type='s' access='read'/>
            <property name='length' type='u' access='read'/>
            <property name='start' type='u' access='read'/>
            <property name='end' type='u' access='read'/>
        </interface>
    </node>
    """
    def __init__(self, segment):
        self.segment = segment

    def setPixels(self, colors):
        try:
            self.segment.setBuffer(colors)
        except TypeError:
            return False
        return True

    def setPixel(self, num, color, scale=1):
        try:
            self.segment.setPixel(num, color, scale)
        except OutOfRangeException:
            return False
        return True

    @Property
    def name(self):
        return self.segment.id

    @Property
    def length(self):
        return self.segment.length

    @Property
    def start(self):
        return self.segment.startend[0]

    @Property
    def end(self):
        return self.segment.startend[1]


#TODO: add the strip class
class Strip:
    """
    """
    def __init__(self, strip):
        pass