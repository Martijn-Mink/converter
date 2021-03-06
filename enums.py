import enum


class Language(enum.Enum):
    PYTHON = 0
    CPP = 1

    def give_extension(self):
        return _EXTENSIONS[self]

    def give_starting_indent(self):
        return _STARTING_INDENT[self]


_EXTENSIONS = {
    Language.PYTHON: '.py',
    Language.CPP: '.cpp'}

_STARTING_INDENT = {
    Language.PYTHON: 0,
    Language.CPP: 1}


class BuiltinFunction(enum.Enum):
    PRINT = 0

    def to_python_name(self):
        if self == BuiltinFunction.PRINT:
            return "print"
        else:
            raise NotImplementedError

    @classmethod
    def from_python_name(cls, name):
        for builtin_function in BuiltinFunction:
            if name == builtin_function.to_python_name():
                return builtin_function

    @staticmethod
    def give_python_names():

        names = []
        for builtin_function in BuiltinFunction:
            names.append(builtin_function.to_python_name())

        return names


class VarType(enum.Enum):
    INT = 0
    FLOAT = 1
    BOOL = 2

    def to_name(self, language):
        if self == VarType.INT:
            return "int"

        elif self == VarType.FLOAT:
            return "double"

        elif self == VarType.BOOL:
            if language == Language.JAVA:
                return "boolean"
            else:
                return "bool"

        else:
            raise NotImplementedError

    @classmethod
    def from_value(cls, value):
        if type(value) is int:
            return cls.INT
        elif type(value) is float:
            return cls.FLOAT
        else:
            raise NotImplementedError

    @staticmethod
    def combine(var_type1, var_type2):
        """Using implicit type conversions"""
        if var_type1 == var_type2:
            return var_type1
        elif {var_type1, var_type2} == {VarType.INT, VarType.FLOAT}:
            return VarType.FLOAT
        else:
            raise NotImplementedError()
