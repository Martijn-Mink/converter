import _ast

from enums import BuiltinFunction, Language

TAB = "    "


def give_expr(language, level):
    indent = level * TAB

    if language == Language.PYTHON:
        template = indent + "{value}"
    else:
        template = indent + "{value};"

    return template


def give_assign(language, level):
    indent = level * TAB

    if language == Language.PYTHON:
        template = indent + "{target0} = {value}"
    else:
        template = indent + "{target0} = {value};"

    return template


def give_if(language, level):
    indent = level * TAB

    if language == Language.PYTHON:
        template = indent + "if {test}:\n" \
                   + "{body}\n" \
                   + indent + "else:\n" \
                   + "{orelse}"
    else:
        template = indent + "if ({test})\n" \
                   + indent + "{{\n" \
                   + "{body}\n" \
                   + indent + "}}\n" \
                   + indent + "else\n" \
                   + indent + "{{\n" \
                   + "{orelse}\n" \
                   + indent + "}}"

    return template


def give_binop(language, op):
    if type(op) is _ast.Add:
        template = "{left} + {right}"
    elif type(op) is _ast.Sub:
        template = "{left} - {right}"
    elif type(op) is _ast.Mult:
        template = "{left} * {right}"
    else:
        raise NotImplementedError(str(type(op)) + " not implemented")

    return template


##########


def give_declaration(language, type, name):
    return "{type} {name}".format(type=type, name=name)


def give_assignment(language, lhs, rhs):
    template = "{lhs} = {rhs}"
    return template.format(lhs=lhs, rhs=rhs)


def give_if_statement(language, level, condition, if_clause, else_clause):
    indent = level * "    "

    if language == Language.PYTHON:
        template = indent + "if {condition}:\n" \
                   + "{if_clause}\n" \
                   + indent + "else:\n" \
                   + "{else_clause}"
    else:
        template = indent + "if ({condition})\n" \
                   + indent + "{{\n" \
                   + "{if_clause}\n" \
                   + indent + "}}\n" \
                   + level * "    " + "else:\n" \
                   + indent + "{{\n" \
                   + "{else_clause}\n" \
                   + indent + "}}"

    return template.format(condition=condition, if_clause=if_clause, else_clause=else_clause)


def give_statement(language, level, content):
    if language == Language.PYTHON:
        template = level * "    " + "{content}"
    else:
        template = level * "    " + "{content};"

    return template.format(content=content)


def give_call(language, name, arguments):
    template = "{name}({argument_string})"
    argument_string = ", ".join(arguments)

    return template.format(name=name, argument_string=argument_string)


def give_builtin_call(language, builtin_function, arguments):
    if builtin_function == BuiltinFunction.PRINT:

        if language == Language.PYTHON:
            return give_call(language, "print", arguments)

        if language == Language.CPP:
            template = "std::cout << {argument_string} << std::endl"
        else:
            template = "System.out.println({argument_string})"

        argument_string = ", ".join(arguments)

        return template.format(argument_string=argument_string)

    elif builtin_function == BuiltinFunction.PLUS:
        return " + ".join(arguments)
