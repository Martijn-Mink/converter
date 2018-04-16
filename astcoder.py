import _ast

import templates
from enums import VarType, BuiltinFunction


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
                code = template.format(target0=target0, value=value, var_type=var_type.to_name(language))

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
            orelse = '\n'.join(orelse)

            return template.format(test=test, body=body, orelse=orelse)

        elif type(node) is _ast.BinOp:
            template = templates.give_binop(language, node.op)

            left = self(node.left, language, level)
            right = self(node.right, language, level)
            return template.format(left=left, right=right)

        elif type(node) is _ast.Call:
            function_name = node.func.id

            if function_name in BuiltinFunction.give_names():
                builtin_function = BuiltinFunction.from_name(function_name)
                template = builtin_function.to_template(language)

                return template.format(1)

        elif type(node) is _ast.NameConstant:
            return templates.give_bool_code(language, node.value)

        else:
            raise NotImplementedError(str(type(node)) + " not implemented")
