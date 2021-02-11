#Gets input from JackTokenizer and emits its parsed structure into an output file / stream
#consists of series of CompileXXX routines, one for every syntactic element XXX of Jack grammar

# The contract between these routines is that each
# compilexxx() routine should read the syntactic construct xxx from the input,
# advance() the tokenizer exactly beyond xxx, and output the parsing of xxx. Thus,
# compilexxx() may only be called if indeed xxx is the next syntactic element of the
# input.


# - Top-down approach - using a nested structure defined by the language grammar
#- for every rule describing **non-terminal** we design a recursive routine to parse the non-terminal
#  - if it encounters **terminals**, the routine can process them directly
#  - if it encounters **non-terminals**, it can recursively call the non-terminal parsing routine

from JackTokenizer import *

tokenizer = None

def xmlprint(el, value):
    print(f'<{el}> {value} </{el}>')


class CompilationEngine:


    def __init__(self, filename):
        self.tokenizer = JackTokenizer(filename)

    def compile(self, filename):
        input_stream = initialize(filename)
        compileClass()

    def xml_print_el(self):
        xmlprint(self.tokenizer.token_type, self.tokenizer.token)

    def compileClass(self):
        # 'class' className '{' classVarDec* subroutineDec* '}'
        # first we expect keyword class
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        if self.tokenizer.keyword() != 'class':
            raise('class expected')
        print('<class>')
        self.xml_print_el()
        # classname
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        if self.tokenizer.token_type != 'identifier':
            raise('identifier expected')
        self.xml_print_el()
        # open bracket
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        if self.tokenizer.symbol() != '{':
            raise('{ expected after class opening')
        self.xml_print_el()
        # classVarDec*

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        # subroutineDec*
        while (self.tokenizer.keyword() in ['constructor', 'function', 'method']):
            self.compileSubroutine()
        pass

    def compileClassVarDec(self):
        # ('static'|'field') type varName (',' varName)* ';'
        pass

    def compileSubroutine(self):
        print('subroutine')
        pass

    def compileParameterList():
        pass

    def compileVarDec():
        pass

    def compileStatements():
        pass

    def compileDo():
        pass

    def compileLet():
        pass

    def compileWhile():
        pass

    def compileReturn():
        pass

    def compileIf():
        pass

    def compileExpression():
        pass

    # if identifier: variable, array entry, subroutine call
    def compileTerm():
        # single lookahead token - can be [ ( or .
        pass

    # comma separated list of expressions
    def compileExpressionList():
        pass

c = CompilationEngine('10/ArrayTest/Main.jack')
c.compileClass()