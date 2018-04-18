import enum


class Language(enum.Enum):
    PYTHON = 0
    JAVA = 1
    CPP = 2
    BASH = 3

    def is_typed(self):
        return self in _TYPED_LANGUAGES

    def give_extension(self):
        return _EXTENSIONS[self]

    def give_starting_indent(self):
        return _STARTING_INDENT[self]


_EXTENSIONS = {
    Language.PYTHON: '.py',
    Language.JAVA: '.java',
    Language.CPP: '.cpp',
    Language.BASH: '.sh'}

_STARTING_INDENT = {
    Language.PYTHON: 0,
    Language.JAVA: 2,
    Language.CPP: 1,
    Language.BASH: 0}

_TYPED_LANGUAGES = (Language.CPP, Language.JAVA)


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

    def to_name(self):
        if self == VarType.INT:
            return "int"

        if self == VarType.FLOAT:
            return "double"

    @classmethod
    def from_value(cls, value):
        if type(value) is int:
            return cls.INT
        elif type(value) is float:
            return cls.FLOAT
        else:
            raise NotImplementedError

    @staticmethod
    def reduce(var_type1, var_type2):
        if var_type1 == var_type2:
            return var_type1
        elif {var_type1, var_type2} == {VarType.INT, VarType.FLOAT}:
            return VarType.FLOAT
        else:
            raise NotImplementedError()
