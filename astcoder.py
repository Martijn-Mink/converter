import _ast
import ast

import templates
from enums import Language, VarType

PATH = "example.py"


class AstCoder:

    def __init__(self):
        self.declared_names = {}

    def find_var_type(self, node):
        if type(node) is _ast.Num:
            return VarType.from_value(node.n)

        elif type(node) is _ast.Name:
            return self.declared_names[node.id]

        elif type(node) is _ast.BinOp:
            return VarType.combine(self.find_var_type(node.left), self.find_var_type(node.right))

        else:
            raise NotImplementedError

    def __call__(self, node, language, level):
        if type(node) is _ast.Expr:
            template = templates.give_expr(language, level)
            value = self(node.value, language, level)
            return template.format(value=value)

        elif type(node) is _ast.Assign:
            target0 = self(node.targets[0], language, level)
            value = self(node.value, language, level)

            if target0 in self.declared_names:
                template = templates.give_assign(language, level)
                code = template.format(target0=target0, value=value)
            else:
                var_type = self.find_var_type(node.value)

                template = templates.give_declared_assign(language, level)
                code = template.format(target0=target0, value=value, var_type=var_type.to_code(language))

                node.targets[0].var_type = var_type
                self.declared_names[target0] = var_type

            return code

        elif type(node) is _ast.Num:
            return str(node.n)

        elif type(node) is _ast.Str:
            return '"' + node.s + '"'

        elif type(node) is _ast.Name:
            return str(node.id)

        elif type(node) is _ast.If:
            template = templates.give_if(language, level)
            test = self(node.test, language, level)

            body = []
            for body_node in node.body:
                body.append(self(body_node, language, level + 1))
            body = "\n".join(body)

            orelse = []
            for orelse_node in node.orelse:
                orelse.append(self(orelse_node, language, level + 1))
            orelse = "\n".join(orelse)

            return template.format(test=test, body=body, orelse=orelse)

        elif type(node) is _ast.BinOp:
            template = templates.give_binop(language, node.op)

            left = self(node.left, language, level)
            right = self(node.right, language, level)
            return template.format(left=left, right=right)

        elif type(node) is _ast.Call:
            func = self(node.func, language, level)

        else:
            raise NotImplementedError(str(type(node)) + " not implemented")


def main():
    with open(PATH, 'r') as f:
        code = f.read()

    tree = ast.parse(code)
    coder = AstCoder()

    language = Language.CPP
    for node in tree.body:
        print(coder(node, language, 0))


if __name__ == "__main__":
    main()
#
# def convert_node(node, call_list):
#     if type(node) is _ast.Expr:
#         call_list.append(Statement)
#         convert_node(node.value, call_list)
#
#     elif type(node) is _ast.Assign:
#         call_list.append(Assignment)
#         convert_node(node.targets[0], call_list)
#         convert_node(node.value, call_list)
#
#     elif type(node) is _ast.Num:
#         call_list.append(Literal(node.n))
#
#     elif type(node) is _ast.Name:
#         call_list.append(Variable(node.id, type=None))
#
#     elif type(node) is _ast.BinOp:
#
#         if type(node.op) is _ast.Add:
#             call_list.append(BuiltinFunction.PLUS)
#             convert_node(node.left, call_list)
#             convert_node(node.right, call_list)
#         else:
#             raise NotImplementedError(str(type(node.op)) + " not implemented")
#
#     elif type(node) is _ast.If:
#         call_list.append(IfStatement)
#         convert_node(node.test, call_list)
#         for element in node.body:
#             convert_node(element, call_list)
#         for element in node.orelse:
#             convert_node(element, call_list)
#     else:
#         raise NotImplementedError(str(type(node)) + " not implemented")
#     return call_list
#
# #
# def main():
#     with open(PATH, 'r') as f:
#         code = f.read()
#
#     tree = ast.parse(code)
#     body = tree.body
#     statements = []
#
#     for body_element in body:
#         call_list = []
#         convert_node(body_element, call_list)
#         print(call_list)
#
#     #
#     #     if type(body_element) is _ast.Expr:
#     #         value = body_element.value
#     #
#     #         if type(value) is _ast.Num:
#     #             num_value = str(value.n)
#     #             statements.append(Statement(Literal(num_value)))
#     #
#     #         elif type(value) is _ast.Name:
#     #             statements.append(Statement(Variable(value.id, type=None)))
#     #
#     #         elif type(value) is _ast.BinOp:
#     #
#     #             if type(value.op) is _ast.Add:
#     #                 lhs = 1
#     #
#     #
#     #         else:
#     #             raise NotImplementedError()
#     #
#     #     elif type(body_element) is _ast.Assign:
#     #         lhs = Variable(body_element.targets[0].id, type=None)
#     #
#     #         value = body_element.value
#     #         if type(value) is _ast.Num:
#     #             num_value = str(value.n)
#     #             rhs = Literal(num_value)
#     #
#     #         elif type(value) is _ast.Name:
#     #             rhs = Variable(value.id, type=None)
#     #         else:
#     #             raise NotImplementedError
#     #
#     #         statements.append(Statement(Assignment(lhs, rhs)))
#     #
#     # for statement in statements:
#     #     statement.level = 0
#     #     print(statement.to_code(Language.CPP))
#
#
# if __name__ == "__main__":
#     main()
