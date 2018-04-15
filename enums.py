import enum


class Language(enum.Enum):
    PYTHON = 0
    JAVA = 1
    CPP = 2

    def is_typed(self):
        return self in TYPED_LANGUAGES


TYPED_LANGUAGES = (Language.CPP, Language.JAVA)


class BuiltinFunction(enum.Enum):
    PRINT = 0
