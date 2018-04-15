from enums import BuiltinFunction, Language


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
