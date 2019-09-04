class DbusType:
    '''
    This is a python representation of a dbus type.
    '''
    def __init__(self, char):
        self._char = char

    def get_char(self):
        return self._char

class Container(DbusType):
    '''
    This is just a proxy container to classify the dbus container
    types
    '''
    _char=None

class Array(Container):
    '''
    This class represents a dbus array
    '''
    def __init__(self, array_type, *args, **kwargs):
        self._array_type = None
        self._char = 'a{}'
        # Check if the array type is a DbusType
        if (not issubclass(array_type.__class__, DbusType)):
            raise TypeError(
                "The array type should be a subclass of DbusType")

        self._array_type = array_type

    def get_char(self):
        return self._char.format(self._array_type.get_char())


class Struct(Container):
    '''
    This class represents a dbus struct
    '''
    def __init__(self, *args):
        self._inner_types = []
        self._char="({})"
        for inner_type in args:
            # Check if the type is a DbusType
            if (not issubclass(inner_type.__class__, DbusType)):
                raise TypeError(
                    "The array type should be a subclass of DbusType")

            self._inner_types.append(inner_type) 

    def get_char(self):
        type_structure = ""
        print(self._inner_types)
        for inner_type in self._inner_types:
            type_structure += inner_type.get_char()

        return self._char.format(type_structure)



class Dict_Entry(Container):
    '''
    This class represents a dbus Dict_entry. This should only be used 
    within an array.
    '''
    def __init__(self, key_type, value_type):
        self._key_type = None
        self._value_type = None
        self._char = "\{{key}{value}\}"
        type_structure = ""
        # Check if the key type is a DbusType and not a container
        if (issubclass(key_type.__class__, Container) 
                and not issubclass(key_type.__class__, DbusType)):
            raise TypeError(
                "The key type should not be a container but a basic Type")

        # Check if the value is a DbusType
        if (not issubclass(value_type.__class__, DbusType)):
            raise TypeError(
                "The value type should be a valid dbus type")

        self._key_type = key_type
        self._value_type = value_type

    def get_char(self):
        return self._char.format(key=self._key_type.get_char(), 
                                 value=self._value_type.get_char())


class Variant(Container):
    char="v"


class Types:
    Byte = DbusType('y')
    Boolean = DbusType('b')
    Int = DbusType('i')
    Int16 = DbusType('n')
    Int32 = DbusType('i')
    Int64 = DbusType('x')
    UInt16 = DbusType('q')
    UInt32 = DbusType('u')
    UInt64 = DbusType('t')
    Double = DbusType('d')
    String = DbusType('s')
    Object_Path = DbusType('o')
    Signature = DbusType('g')
    Unix_Fd = DbusType('h')
    Array = Array
    Struct = Struct
    Dict_Entry = Dict_Entry.__class__
    Variant = Variant.__class__