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
            return VarType.reduce(self.find_var_type(node.left), self.find_var_type(node.right))

        elif type(node) is _ast.Compare:
            return VarType.BOOL

        else:
            raise NotImplementedError

    def __call__(self, node, language, level):
        if type(node) is _ast.Expr:
            template = templates.give_expr(language, level)
            value = self(node.value, language, level)
            return template.format(value=value)

        elif type(node) is _ast.Assign:
            target0 = node.targets[0].id  # Do not use self call here
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
            template = templates.give_name(language)
            return template.format(id=node.id)

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

            if function_name in BuiltinFunction.give_python_names():
                builtin_function = BuiltinFunction.from_python_name(function_name)
                template = templates.give_builtin_function(builtin_function, language)

                return template.format(args0=self(node.args[0], language, level))

        elif type(node) is _ast.NameConstant:
            return templates.give_bool_code(language, node.value)

        elif type(node) is _ast.Compare:
            # https://stackoverflow.com/questions/20449543/bash-equality-operators-eq
            template = templates.give_compare(language, node.ops[0])

            left = self(node.left, language, level)
            comparators0 = self(node.comparators[0], language, level)
            return template.format(left=left, comparators0=comparators0)

        else:
            raise NotImplementedError(str(type(node)) + " not implemented")
