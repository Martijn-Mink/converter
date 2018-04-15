import enum

import templates


class Type(enum.Enum):
    INT = 0

    def to_code(self, language):
        if self == Type.INT:
            return "int"


#
# class BuiltinFunction:
#
#     def __init__(self, name, token_function, argument_count):
#         self.name = name
#         self.token_function = token_function
#         self.argument_count = argument_count


class Literal:
    def __init__(self, value):
        self.value = value

    def to_code(self, language):
        return self.value


class Variable:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def to_code(self, language):
        return self.name


class Declaration:
    def __init__(self, variable):
        self.variable = variable

    def to_code(self, language):
        return templates.give_declaration(language,
                                          type=self.variable.type.to_code(language),
                                          name=self.variable.to_code(language))


class Assignment:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def to_code(self, language):
        return templates.give_assignment(language,
                                         lhs=self.lhs.to_code(language),
                                         rhs=self.rhs.to_code(language))


class Call:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def to_code(self, language):
        return templates.give_call(language,
                                   name=self.name,
                                   arguments=map(lambda x: x.to_code(language), self.arguments))


class BuiltinCall:
    def __init__(self, builtin_function, arguments):
        self.builtin_function = builtin_function
        self.arguments = arguments

    def to_code(self, language):
        return templates.give_builtin_call(language,
                                           builtin_function=self.builtin_function,
                                           arguments=map(lambda x: x.to_code(language), self.arguments))


class IfStatement:
    def __init__(self, condition, if_clause, else_clause):
        self.condition = condition
        self.if_clause = if_clause
        self.else_clause = else_clause
        self._level = None

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

        for statement in self.if_clause + self.else_clause:
            statement.level = level + 1

    def to_code(self, language):
        if_clause = '\n'.join(map(lambda x: x.to_code(language), self.if_clause))
        else_clause = '\n'.join(map(lambda x: x.to_code(language), self.else_clause))

        return templates.give_if_statement(language,
                                           self.level,
                                           condition=self.condition.to_code(language),
                                           if_clause=if_clause,
                                           else_clause=else_clause)


class Statement:
    def __init__(self, content):
        self.content = content
        self.level = None

    def to_code(self, language):
        return templates.give_statement(language,
                                        self.level,
                                        content=self.content.to_code(language))
