import _ast
import ast
import os

INPUT_PATH = os.path.join('code', 'input.py')

PYANNOTATE_TEMPLATE = """import unittest
from pyannotate_runtime import collect_types

collect_types.init_types_collection()

import {module_name}


class TestPyannotateRun(unittest.TestCase):

    def test_pyannotate_run(self):
        collect_types.init_types_collection()
        with collect_types.collect():
            {script}
        collect_types.dump_stats("types.json")


if __name__ == '__main__':
    unittest.main()
"""



def get_annotation(function_definition_node, code_path):
    assert type(function_definition_node) == _ast.FunctionDef

    with open(code_path, 'r') as code_file:
        for i_line in range(function_definition_node.lineno):
            code_file.readline()

        annotation = code_file.readline()

    return annotation

def create_pyannotate_unittest(module_path, script_path):

    module = os.path.splitext(os.path.basename(module_path))[0]

    with open(script_path,'r') as f:
        script = f.readlines()

    return PYANNOTATE_TEMPLATE.format(module=module,script=script)

class AstTyper(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        print(get_annotation(node, INPUT_PATH))


def main():
    with open(INPUT_PATH, 'r') as f:
        code = f.read()

    tree = ast.parse(code)
    tree = AstTyper().visit(tree)


if __name__ == "__main__":
    main()
