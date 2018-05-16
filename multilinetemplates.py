HEADER_CPP = """#include <iostream>

int main() 
{"""

FOOTER_CPP = """    return 0;
}"""

IF_PYTHON = """INDENTif {test}:
{body}"""

ELSE_IF_PYTHON = """INDENTelif {test}:
{body}"""

ELSE_PYTHON = """INDENTelse:
{orelse}"""

IF_CPP = """INDENTif ({test})
INDENT{{
{body}
INDENT}}"""

ELSE_IF_CPP = """INDENTelse if ({test})
INDENT{{
{body}
INDENT}}"""

ELSE_CPP = """INDENTelse
INDENT{{
{orelse}
INDENT}}"""
