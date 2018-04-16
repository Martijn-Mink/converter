import enum


class Language(enum.Enum):
    PYTHON = 0
    JAVA = 1
    CPP = 2

    def is_typed(self):
        return self in TYPED_LANGUAGES


class VarType(enum.Enum):
    INT = 0
    FLOAT = 1

    def to_code(self, language):
        if self == VarType.INT:
            return "int"

        if self == VarType.FLOAT:
            return "float"

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
        if var_type1 == var_type2:
            return var_type1
        elif {var_type1, var_type2} == {VarType.INT, VarType.FLOAT}:
            return VarType.FLOAT
        else:
            raise NotImplementedError()


TYPED_LANGUAGES = (Language.CPP, Language.JAVA)


class BuiltinFunction(enum.Enum):
    PRINT = 0
    PLUS = 1
