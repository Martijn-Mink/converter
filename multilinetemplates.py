HEADER_CPP = """#include <iostream>

int main() 
{"""

FOOTER_CPP = """    return 0;
}"""

HEADER_JAVA = """public class GeneratedCode
{
    public static void main(String[] args)
    {"""

FOOTER_JAVA = """    }
}"""

IF_PYTHON = """INDENTif {test}:
{body}
INDENTelse:
{orelse}"""

IF_JAVA_CPP = """INDENTif ({test})
INDENT{{
{body}
INDENT}}
INDENTelse
INDENT{{
{orelse}
INDENT}}"""

IF_BASH = """INDENTif [{test}]
INDENTthen    
{body}
INDENTelse
{orelse}
INDENTfi
"""

