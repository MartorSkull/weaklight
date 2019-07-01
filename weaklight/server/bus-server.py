import os
import xml.etree.ElementTree as ET

from pgi.repository import GLib
import pydbus

def add_annotation(name, value):
    def decorator(func):
        if (not hasattr(func, "__dbus_annotations__")):
            func.__dbus_annotations__ = {name: value}
        else:
            func.__dbus_annotations__[name] = value
        return func
    return decorator

def dbus_property(setter=None, access=None):
    def decorator(func):
        func.__dbus_property__ = True
        func.__prop_setter__ = setter

        # Set the access to each default
        if (access):
            func.__prop_access__ = access
        elif (setter):
            func.__prop_access__ = "readwrite"
        else:
            func.__prop_access__ = "read"    

        return func
    return decorator
        
def dbus_method(func):
    func.__dbus_method__ = True
    return func

class DBusObject(object):
    def __init__(self, name):
        self.name = name

        # Create the xml and set the interface
        self.xml = ET.Element('node')
        self.interface = ET.SubElement(self.xml, "interface")
        self.interface.set("name", self.name)

        # Handle the attributes
        self.__handle_attr__()

        # We make it a perinstace so we don't modify the other instances and dump the xml
        self.__make_perinstance__()
        self.__class__.dbus = str(ET.tostring(self.xml), encoding="UTF-8")

    def __handle_attr__(self):
        # We get all the non hidden attributes from the class
        user_attr = [attr for attr in dir(self) if not attr.startswith("__")]
        flag = False
        for attr in user_attr:
            # we get the attributes and check if we need to add them to the xml
            attr = getattr(self, attr)
            if (hasattr(attr, "__dbus_method__")):
                self.add_method(attr)
            elif (hasattr(attr, "__dbus_property__")):
                self.add_property(attr)

    def add_method(self, method):
        # Create the element and give it its name
        meth_xml = ET.SubElement(self.interface, "method")
        meth_xml.set('name', method.__name__)
        
        # Add the argumnets
        self.__add_agruments__(method, meth_xml)

        # Set the annotations for dbus if any
        if (hasattr(method, "__dbus_annotations__")):
            self.set_annotations(meth_xml, method.__dbus_annotations__)

    def add_property(self, method):
        # Create the element and give it its name, access and type
        prop_xml = ET.SubElement(self.interface, "property")
        prop_xml.set('name', method.__name__)
        prop_xml.set('access', method.__prop_access__)
        
        # Check for the return annotation
        if (not hasattr(method, "__annotations__")):
            raise AttributeError(
            "The property {p} doesn't have the required return annotation")

        prop_xml.set('type', method.__annotations__["return"].char)

        # Set the annotations for dbus if any
        if (hasattr(method,"__dbus_annotations__")):
            self.set_annotations(prop_xml, method.__dbus_annotations__)

        # Make the method a property
        self.__add_property__(method, method.__prop_setter__)

    def set_annotations(self, element, annotations):
        for anns in annotations.keys():
            an = ET.SubElement(element, "annotation")
            an.set("name", anns)
            an.set("value", annotations[anns])

    def __add_agruments__(self, method, meth_xml):
        # Pass through all the annotations and set the arguments
        if (not method.__annotations__ and len(method.__dict__.keys) > 0):
            raise AttributeError(
                "The method {m} doesn't have the required annotations".format(
                    m=method.__name__))
        for arg in method.__annotations__.keys():
            xml_arg = ET.SubElement(meth_xml, "arg")
            xml_arg.set("type", method.__annotations__[arg].char)
            xml_arg.set("name", arg)
            # If the annotation denotes return value set the diretion to out
            xml_arg.set("direction", "in" if (arg != "return") else "out")

        return meth_xml

    def __add_property__(self, getter, setter=None):
        self.__make_perinstance__()
        setattr(self.__class__, getter.__name__, property(getter, setter))

    def __make_perinstance__(self):
        # Get the class and check if its not already a perinstance
        cls = type(self)
        if not hasattr(cls, '__perinstance'):
            # Make a custom class that inherits from the main class mark it
            # and set it
            cls = type(cls.__name__, (cls,), {})
            cls.__perinstance = True
            self.__class__ = cls
