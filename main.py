import ast

import astcoder
import enums
import templates

INPUT_PATH = 'example.py'


def create_code(tree, language):
    coder = astcoder.AstCoder()

    header = templates.HEADER[language]
    footer = templates.FOOTER[language]
    starting_level = templates.STARTING_INDENT[language]

    code = []
    for node in tree.body:
        code.append(coder(node, language, starting_level))

    if header:
        code = [header] + code

    if footer:
        code = code + [footer]

    return '\n'.join(code)


def main():
    with open(INPUT_PATH, 'r') as f:
        code = f.read()

    tree = ast.parse(code)

    code = create_code(tree, enums.Language.PYTHON)
    with open("out.py", 'w') as code_file:
        code_file.write(code)

    code = create_code(tree, enums.Language.JAVA)
    with open("out.java", 'w') as code_file:
        code_file.write(code)

    code = create_code(tree, enums.Language.CPP)
    with open("out.cpp", 'w') as code_file:
        code_file.write(code)


if __name__ == "__main__":
    main()
