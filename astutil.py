import _ast
import ast

from nodes import Statement, Literal, Variable, Assignment, IfStatement
from enums import BuiltinFunction

PATH = "example.py"


def convert_node(node, call_list):
    if type(node) is _ast.Expr:
        call_list.append(Statement)
        convert_node(node.value, call_list)

    elif type(node) is _ast.Assign:
        call_list.append(Assignment)
        convert_node(node.targets[0], call_list)
        convert_node(node.value, call_list)

    elif type(node) is _ast.Num:
        call_list.append(Literal(node.n))

    elif type(node) is _ast.Name:
        call_list.append(Variable(node.id, type=None))

    elif type(node) is _ast.BinOp:

        if type(node.op) is _ast.Add:
            call_list.append(BuiltinFunction.PLUS)
            convert_node(node.left, call_list)
            convert_node(node.right, call_list)
        else:
            raise NotImplementedError(str(type(node.op)) + " not implemented")

    elif type(node) is _ast.If:
        call_list.append(IfStatement)
        convert_node(node.test, call_list)
        for element in node.body:
            convert_node(element, call_list)
        for element in node.orelse:
            convert_node(element, call_list)
    else:
        raise NotImplementedError(str(type(node)) + " not implemented")
    return call_list


def main():
    with open(PATH, 'r') as f:
        code = f.read()

    tree = ast.parse(code)
    body = tree.body
    statements = []

    for body_element in body:
        call_list = []
        convert_node(body_element, call_list)
        print(call_list)

    #
    #     if type(body_element) is _ast.Expr:
    #         value = body_element.value
    #
    #         if type(value) is _ast.Num:
    #             num_value = str(value.n)
    #             statements.append(Statement(Literal(num_value)))
    #
    #         elif type(value) is _ast.Name:
    #             statements.append(Statement(Variable(value.id, type=None)))
    #
    #         elif type(value) is _ast.BinOp:
    #
    #             if type(value.op) is _ast.Add:
    #                 lhs = 1
    #
    #
    #         else:
    #             raise NotImplementedError()
    #
    #     elif type(body_element) is _ast.Assign:
    #         lhs = Variable(body_element.targets[0].id, type=None)
    #
    #         value = body_element.value
    #         if type(value) is _ast.Num:
    #             num_value = str(value.n)
    #             rhs = Literal(num_value)
    #
    #         elif type(value) is _ast.Name:
    #             rhs = Variable(value.id, type=None)
    #         else:
    #             raise NotImplementedError
    #
    #         statements.append(Statement(Assignment(lhs, rhs)))
    #
    # for statement in statements:
    #     statement.level = 0
    #     print(statement.to_code(Language.CPP))


if __name__ == "__main__":
    main()
