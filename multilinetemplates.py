HEADER_CPP = """#include <iostream>

int main() 
{"""

FOOTER_CPP = """    return 0;
}"""

IF_PYTHON = """INDENTif {test}:
{body}
INDENTelse:
{orelse}"""

IF_CPP = """INDENTif ({test})
INDENT{{
{body}
INDENT}}
INDENTelse
INDENT{{
{orelse}
INDENT}}"""
