class DbusType:
    '''
    This is a python representation of a dbus type.
    '''
    _char=None
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
    _array_type = None
    _char = 'a{}'
    def __init__(self, array_type, *args, **kwargs):
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
    _inner_types = []
    _char="({})"
    def __init__(self, *args):
        type_structure = ""
        for inner_type in args:
            # Check if the type is a DbusType
            if (not issubclass(inner_type.__class__, DbusType)):
                raise TypeError(
                    "The array type should be a subclass of DbusType")

            _inner_types.append(inner_type) 

    def get_char(self):
        type_structure = ""
        for inner_type in self._inner_types:
            type_structure += inner_type.get_char()

        return self._char.format(type_structure)



class Dict_Entry(Container):
    '''
    This class represents a dbus Dict_entry. This should only be used 
    within an array.
    '''
    _key_type = None
    _value_type = None
    _char = "\{{key}{value}\}"
    def __init__(self, key_type, value_type):
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
    Dict_Entry = Dict_Entry
    Variant = Variant