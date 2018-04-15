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


class IfStatement:
    def __init__(self, condition, if_clause, else_clause):
        self.condition = condition
        self.if_clause = if_clause
        self.else_clause = else_clause

    def to_code(self, language):
        return templates.give_if_statement(language,
                                           condition=self.condition.to_code(language),
                                           if_clause=self.if_clause.to_code(language),
                                           else_clause=self.else_clause.to_code(language))


class Statement:
    def __init__(self, content):
        self.content = content

    def to_code(self, language):
        return templates.give_statement(language,
                                        content=self.content.to_code(language))


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
