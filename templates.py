import _ast

import multilinetemplates
from enums import BuiltinFunction, Language

TAB = "    "

_NAME = {
    Language.PYTHON: "{id}",
    Language.CPP: "{id}",
}

_PRINT = {
    Language.PYTHON: "print({args0})",
    Language.CPP: "std::cout << {args0} << std::endl"
}

_EXPRESSION = {
    Language.PYTHON: "{value}",
    Language.CPP: "{value};"
}

_EVALUATION = {
    Language.PYTHON: "({contents})",
    Language.CPP: "({contents})"
}

_DECLARED_ASSIGN = {
    Language.PYTHON: "{target0} = {value}",
    Language.CPP: "{var_type} {target0} = {value};"
}

_ASSIGN = {
    Language.PYTHON: "{target0} = {value}",
    Language.CPP: "{target0} = {value};"
}

_FUNCTION_DEFINITION = {
    Language.PYTHON: multilinetemplates.FUNCTION_DEFINITION_PYTHON,
    Language.CPP: multilinetemplates.FUNCTION_DEFINITION_CPP
}

_IF = {
    Language.PYTHON: multilinetemplates.IF_PYTHON,
    Language.CPP: multilinetemplates.IF_CPP
}

_ELSE = {
    Language.PYTHON: multilinetemplates.ELSE_PYTHON,
    Language.CPP: multilinetemplates.ELSE_CPP
}

_HEADER = {
    Language.PYTHON: None,
    Language.CPP: multilinetemplates.HEADER_CPP
}

_FOOTER = {
    Language.PYTHON: None,
    Language.CPP: multilinetemplates.FOOTER_CPP
}


def give_builtin_function_call(builtin_function, language):
    if builtin_function == BuiltinFunction.PRINT:
        return _PRINT[language]

def give_function_call(language):
    return "{func}({argument_string})"


def give_header(language):
    return _HEADER[language]


def give_footer(language):
    return _FOOTER[language]


def give_name(language):
    return _NAME[language]


def give_expr(language, level):
    indent = level * TAB
    template = indent + _EXPRESSION[language]
    return template


def give_assign(language, level):
    indent = level * TAB
    template = indent + _ASSIGN[language]
    return template


def give_declared_assign(language, level):
    indent = level * TAB
    template = indent + _DECLARED_ASSIGN[language]
    return template


def give_if(language, level):
    indent = level * TAB
    template = _IF[language].replace("INDENT", indent)
    return template


def give_else(language, level):
    indent = level * TAB
    template = _ELSE[language].replace("INDENT", indent)
    return template


def give_evaluation(language):
    return _EVALUATION[language]


def give_function_definition(language, level):
    indent = level * TAB
    return _FUNCTION_DEFINITION[language].replace("INDENT", indent)


def give_return(language, level):
    indent = level * TAB
    return indent + "return {value}"


def give_compare(language, op):
    # Booleans are only supported in if statements currently
    template = "{contents}"
    # template = give_evaluation(language)

    if type(op) is _ast.Eq:
        template = template.format(contents="{left} == {comparators0}")
    elif type(op) is _ast.NotEq:
        template = template.format(contents="{left} != {comparators0}")
    elif type(op) is _ast.Gt:
        template = template.format(contents="{left} > {comparators0}")
    elif type(op) is _ast.Lt:
        template = template.format(contents="{left} < {comparators0}")
    elif type(op) is _ast.GtE:
        template = template.format(contents="{left} >= {comparators0}")
    elif type(op) is _ast.LtE:
        template = template.format(contents="{left} <= {comparators0}")
    else:
        raise NotImplementedError("{}".format(op))

    return template


def give_binop(language, op):
    template = give_evaluation(language)

    if type(op) is _ast.Add:
        template = template.format(contents="{left} + {right}")
    elif type(op) is _ast.Sub:
        template = template.format(contents="{left} - {right}")
    elif type(op) is _ast.Mult:
        template = template.format(contents="{left} * {right}")
    else:
        raise NotImplementedError(str(type(op)) + " not implemented")

    return template


def give_bool_code(language, value):
    if language == Language.PYTHON:
        return str(value)
    else:
        return str(value).lower()


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
