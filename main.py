from enums import Language, BuiltinFunction
from nodes import Statement, IfStatement, Declaration, Variable, Literal, Type, Assignment, Call, BuiltinCall


def main():
    literal_1 = Literal("1")
    literal_2 = Literal("2")
    literal_true = Literal("True")

    variable_x = Variable("x", Type.INT)
    variable_y = Variable("y", Type.INT)
    variable_z = Variable("z", Type.INT)

    declaration_x = Declaration(variable_x)
    declaration_y = Declaration(variable_y)
    declaration_z = Declaration(variable_z)

    assignment_x = Assignment(declaration_x, literal_1)
    assignment_y = Assignment(declaration_y, literal_2)

    statements = []
    statements.append(Statement(assignment_x))
    statements.append(Statement(assignment_y))

    if1 = IfStatement(condition=literal_true,
                      if_clause=2 * [Statement(Assignment(variable_x, literal_1))],
                      else_clause=2 * [Statement(Assignment(variable_x, literal_2))])

    if2 = IfStatement(condition=literal_true,
                      if_clause=2 * [Statement(Assignment(variable_x, literal_1))],
                      else_clause=2 * [Statement(Assignment(variable_x, literal_2))])

    if3 = IfStatement(condition=literal_true,
                      if_clause=2 * [Statement(Assignment(variable_x, literal_1))],
                      else_clause=[if2])

    statements.extend([if3, if1])

    call = Call("calc", [variable_x, literal_2])
    statements.append(Statement(call))

    call_bi = BuiltinCall(BuiltinFunction.PRINT, [variable_x, literal_2])
    statements.append(Statement(call_bi))

    for statement in statements:
        statement.level = 0

    for language in Language:
        print(language)
        for statement in statements:
            print(statement.to_code(language))


if __name__ == "__main__":
    main()
