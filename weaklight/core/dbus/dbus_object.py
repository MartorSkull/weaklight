import os
import xml.etree.ElementTree as ET

def add_annotation(name, value):
    '''
    A decorator to add an anotation to a method or a property
    '''
    def decorator(func):
        if (not hasattr(func, "__dbus_annotations__")):
            func.__dbus_annotations__ = {name: value}
        else:
            func.__dbus_annotations__[name] = value
        return func
    return decorator

def dbus_property(setter=None, access=None):
    '''
    A decorator to add dbus properties to the published 
    dbus object
    '''
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
    '''
    A decorator to add dbus methods to the published 
    dbus object
    '''
    func.__dbus_method__ = True
    return func

class DBusObject(object):
    '''
    A class that represents a dbus object. To add methods to be published
    it is required to use the decorators. When this class initializes it will 
    look for methods and properties and check the annotations in the python 
    method arguments to set the types.
    '''
    def __init__(self, address, name):
        self.name = "{}.{}".format(address, name)

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
        '''
        This method automatically handles the dbus properties and methods
        and creates the xml to publish in dbus
        '''
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
        '''
        Adds a method to the dbus xml
        '''
        # Create the element and give it its name
        meth_xml = ET.SubElement(self.interface, "method")
        meth_xml.set('name', method.__name__)
        
        # Add the argumnets
        self.__add_agruments__(method, meth_xml)

        # Set the annotations for dbus if any
        if (hasattr(method, "__dbus_annotations__")):
            self.set_annotations(meth_xml, method.__dbus_annotations__)

    def add_property(self, method):
        '''
        Adds a property to the dbus xml
        '''
        # Create the element and give it its name, access and type
        prop_xml = ET.SubElement(self.interface, "property")
        prop_xml.set('name', method.__name__)
        prop_xml.set('access', method.__prop_access__)
        
        # Check for the return annotation
        if (not hasattr(method, "__annotations__")):
            raise AttributeError(
            "The property {p} doesn't have the required return annotation")

        prop_xml.set('type', method.__annotations__["return"].get_char())

        # Set the annotations for dbus if any
        if (hasattr(method,"__dbus_annotations__")):
            self.set_annotations(prop_xml, method.__dbus_annotations__)

        # Make the method a property
        self.__add_property__(method, method.__prop_setter__)

    def set_annotations(self, element, annotations):
        '''
        Adds many dbus annotation to the xml element.
        '''
        for anns in annotations.keys():
            an = ET.SubElement(element, "annotation")
            an.set("name", anns)
            an.set("value", annotations[anns])

    def __add_agruments__(self, method, meth_xml):
        '''
        Reads the python annotations in the methon to detect and set the 
        types for the method parameters
        '''
        # Pass through all the annotations and set the arguments
        if (not method.__annotations__ and len(method.__dict__.keys) > 0):
            raise AttributeError(
                "The method {m} doesn't have the required annotations".format(
                    m=method.__name__))
        for arg in method.__annotations__.keys():
            xml_arg = ET.SubElement(meth_xml, "arg")
            xml_arg.set("type", method.__annotations__[arg].get_char())
            xml_arg.set("name", arg)
            # If the annotation denotes return value set the diretion to out
            xml_arg.set("direction", "in" if (arg != "return") else "out")

        return meth_xml

    def __add_property__(self, getter, setter=None):
        '''
        This method adds a property to the class.
        To make this work as a normal property we make the 
        class a perinstance.
        '''
        self.__make_perinstance__()
        setattr(self.__class__, getter.__name__, property(getter, setter))

    def __make_perinstance__(self):
        '''
        This method creates a new class so that when we modify and add 
        properties and the dbus xml we won't modify the object class
        '''
        # Get the class and check if its not already a perinstance
        cls = type(self)
        if not hasattr(cls, '__perinstance'):
            # Make a custom class that inherits from the main class mark it
            # and set it
            cls = type(cls.__name__, (cls,), {})
            cls.__perinstance = True
            self.__class__ = cls
