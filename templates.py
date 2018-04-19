import _ast

import multilinetemplates
from enums import BuiltinFunction, Language

TAB = "    "

_NAME = {
    Language.PYTHON: "{id}",
    Language.JAVA: "{id}",
    Language.CPP: "{id}",
    Language.BASH: "${id}"
}

_PRINT = {
    Language.PYTHON: "print({args0})",
    Language.JAVA: "System.out.println({args0})",
    Language.CPP: "std::cout << {args0} << std::endl",
    Language.BASH: "echo {args0}"
}

_EXPRESSION = {
    Language.PYTHON: "{value}",
    Language.JAVA: "{value};",
    Language.CPP: "{value};",
    Language.BASH: "{value}"
}

_EVALUATION = {
    Language.PYTHON: "({contents})",
    Language.JAVA: "({contents})",
    Language.CPP: "({contents})",
    Language.BASH: "$(({contents}))"
}

_DECLARED_ASSIGN = {
    Language.PYTHON: "{target0} = {value}",
    Language.JAVA: "{var_type} {target0} = {value};",
    Language.CPP: "{var_type} {target0} = {value};",
    Language.BASH: "{target0}={value}"
}

_ASSIGN = {
    Language.PYTHON: "{target0} = {value}",
    Language.JAVA: "{target0} = {value};",
    Language.CPP: "{target0} = {value};",
    Language.BASH: "{target0}={value}"
}

_IF = {
    Language.PYTHON: multilinetemplates.IF_PYTHON,
    Language.JAVA: multilinetemplates.IF_JAVA_CPP,
    Language.CPP: multilinetemplates.IF_JAVA_CPP,
    Language.BASH: multilinetemplates.IF_BASH
}

_HEADER = {
    Language.PYTHON: None,
    Language.JAVA: multilinetemplates.HEADER_JAVA,
    Language.CPP: multilinetemplates.HEADER_CPP,
    Language.BASH: None
}

_FOOTER = {
    Language.PYTHON: None,
    Language.JAVA: multilinetemplates.FOOTER_JAVA,
    Language.CPP: multilinetemplates.FOOTER_CPP,
    Language.BASH: None
}


def give_builtin_function(builtin_function, language):
    if builtin_function == BuiltinFunction.PRINT:
        return _PRINT[language]


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


def give_evaluation(language):
    return _EVALUATION[language]


def give_compare(language, op):

    # Booleans are only supported in if statements currently
    template = "{contents}"
    #template = give_evaluation(language)

    if language != Language.BASH:
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
    else:
        if type(op) is _ast.Eq:
            template = template.format(contents="{left} -eq {comparators0}")
        elif type(op) is _ast.NotEq:
            template = template.format(contents="{left} -ne {comparators0}")
        elif type(op) is _ast.Gt:
            template = template.format(contents="{left} -gt {comparators0}")
        elif type(op) is _ast.Lt:
            template = template.format(contents="{left} -lt {comparators0}")
        elif type(op) is _ast.GtE:
            template = template.format(contents="{left} -ge {comparators0}")
        elif type(op) is _ast.LtE:
            template = template.format(contents="{left} -le {comparators0}")
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
