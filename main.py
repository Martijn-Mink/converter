import ast
import os

import astcoder
import enums
import templates

INPUT_PATH = os.path.join('code', 'input.py')


def create_code(tree, language):
    coder = astcoder.AstCoder()

    header = templates.give_header(language)
    footer = templates.give_footer(language)
    starting_level = language.give_starting_indent()

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

    for language in enums.Language:
        code = create_code(tree, language)
        output_path = os.path.join('code', 'GeneratedCode' + language.give_extension())
        with open(output_path, 'w') as code_file:
            code_file.write(code)


if __name__ == "__main__":
    main()
