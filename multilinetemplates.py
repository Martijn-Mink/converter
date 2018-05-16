HEADER_CPP = """#include <iostream>

int main() 
{"""

FOOTER_CPP = """    return 0;
}"""

IF_PYTHON = """INDENTif {test}:
{body}"""

ELSE_PYTHON = """INDENTelse:
{orelse}"""

IF_CPP = """INDENTif ({test})
INDENT{{
{body}
INDENT}}"""

ELSE_CPP = """INDENTelse
INDENT{{
{orelse}
INDENT}}"""

FUNCTION_DEFINITION_PYTHON = """INDENTdef {name}({argument_string}):
{body}"""

FUNCTION_DEFINITION_CPP = """INDENTdef {name}({argument_string}):
{body}"""
