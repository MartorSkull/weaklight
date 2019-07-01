class DbusType:
    char=None
    def __init__(self, char):
        self.char = char

class Container(DbusType):
    char=None

class Array(Container):
    char='a{}'
    def __init__(self, array_type, *args, **kwargs):
        # Check if the array type is a DbusType
        if (not issubclass(array_type.__class__, DbusType)):
            raise TypeError(
                "The array type should be a subclass of DbusType")

        self.char = self.char.format(array_type.char)


class Struct(Container):
    char="({})"
    def __init__(self, *args):
        type_structure = ""
        for inner_type in args:
            # Check if the type is a DbusType
            if (not issubclass(inner_type.__class__, DbusType)):
                raise TypeError(
                    "The array type should be a subclass of DbusType")

            type_structure += inner_type.char

        self.char = self.char.format(type_structure)


class Dict_Entry(Container):
    def __init__(self, key_type, value_type):
        type_structure = ""
        # Check if the key type is a DbusType and not a container
        if (issubclass(key_type.__class__, Container) 
                and not issubclass(key_type.__class__, DbusType)):
            raise TypeError(
                "The key type should not be a subclass of container but a subclass of DbusType")

        # Check if the value is a DbusType
        if (not issubclass(value_type.__class__, DbusType)):
            raise TypeError(
                "The value type should be a subclass of DbusType")

        self.char = 'a{'+"{}{}".format(
                key_type.char, 
                value_type.char)+"}"


class Variant(DbusType):
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