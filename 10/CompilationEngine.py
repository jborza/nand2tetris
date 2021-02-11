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

    def advanceSymbol(self, symbol):
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        else:
            raise SyntaxError('Symbol expected:' + symbol+ ', found end of stream')
        if self.tokenizer.symbol() != symbol:
            raise SyntaxError('Symbol expected:' + symbol)

    def advanceKeyword(self, keyword):
        if self.tokenizer.hasMoreTokens():
           self.tokenizer.advance()
        else:
            raise SyntaxError('Keyword expected:' + keyword+ ', found end of stream')
        if self.tokenizer.keyword() != keyword:
            raise SyntaxError('Keyword expected:' + keyword)

    def advanceTokenType(self, tokenType):
        if self.tokenizer.hasMoreTokens():
           self.tokenizer.advance()
        else:
            raise SyntaxError('Identifier expected, found end of stream')
        if self.tokenizer.token_type != 'identifier':
            raise SyntaxError('Identifier expected')

    def advanceKeywords(self, *args):
        if self.tokenizer.hasMoreTokens():
           self.tokenizer.advance()
        else:
            raise SyntaxError('Keywords expected:' + args+ ', found end of stream')
        if self.tokenizer.keyword() != keyword:
            raise SyntaxError('Keywords expected:' + args)

    def advanceAndGetType(self):
        if self.tokenizer.hasMoreTokens():
           self.tokenizer.advance()
        else:
            raise SyntaxError('type expected, found end of stream')
        if self.is_type():
            return self.tokenizer.token
        else:
            raise SyntaxError('type expected')

    def is_type(self):
        return self.tokenizer.keyword() in ['int', 'char', 'boolean'] or self.tokenizer.token_type == 'identifier'

    def advanceAndGetReturnType(self):
        self.advance()
        if self.is_type() or self.tokenizer.keyword() == 'void':
            return self.tokenizer.token
        else:
            raise SyntaxError('type expected')

    def advanceToClassName(self):
        self.advanceTokenType('identifier')
        return self.tokenizer.identifier()

    def advanceToVarName(self):
        self.advanceTokenType('identifier')
        return self.tokenizer.identifier()

    def advanceToSubroutineName(self):
        self.advanceTokenType('identifier')
        return self.tokenizer.identifier()

    def hasClassVarDec(self):
        pass

    def advance(self):
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        else:
            raise SyntaxError('found end of stream!')

    def compileClass(self):
        # 'class' className '{' classVarDec* subroutineDec* '}'
        print('<class>')
        self.advanceKeyword('class')
        self.xml_print_el()
        # classname
        self.advanceToClassName()
        className = self.tokenizer.identifier()
        self.xml_print_el()
        # {
        self.advanceSymbol('{')
        self.xml_print_el()

        self.advance()
        # classVarDec*
        while(self.tokenizer.keyword() in ['static', 'field']):
            self.compileClassVarDec()
           
        # subroutineDec*
        while (self.tokenizer.keyword() in ['constructor', 'function', 'method']):
            self.compileSubroutine()
           
        # }
        self.advanceSymbol('}')
        self.xml_print_el()
        print('</class>')

    def compileClassVarDec(self):    
        # ('static'|'field') type varName (',' varName)* ';'
        print('<classVarDec>')
        # ('static'|'field')
        self.xml_print_el()
        # type
        type = self.advanceAndGetType()
        self.xml_print_el()
        # varName
        varName = self.advanceToVarName()
        self.xml_print_el()
        # ;
        self.advanceSymbol(';')
        self.xml_print_el()
        print('</classVarDec>')
        self.advance()

    def compileSubroutine(self):
        print('<subroutineDec>')
        kind = self.tokenizer.keyword()
        self.xml_print_el()

        # ( 'void' | type )
        
        return_type = self.advanceAndGetReturnType()
        self.xml_print_el()

        # subroutineName
        name = self.advanceToSubroutineName()
        self.xml_print_el()

        # (
        self.advanceSymbol('(')
        self.xml_print_el()

        # TODO parameterList
        self.compileParameterList()

        # (
        self.advanceSymbol(')')
        self.xml_print_el()

        # subroutineBody
        self.compileSubroutineBody()

        print('</subroutineDec>')
        self.advance()
        pass

    def compileSubroutineBody(self):
        print('<subroutineBody>')
        # {
        self.advanceSymbol('{')
        self.xml_print_el()

        # varDec*
        #TODO a structure to represent the *
        self.varDec()

        # statementes
        self.compileStatements()

        # }
        self.advanceSymbol('}')
        self.xml_print_el()
        print('</subroutineBody>')


    def compileParameterList(self):
        print('<parameterList>')

        print('</parameterList>')

    def compileVarDec(self):
        pass

    def compileStatements(self):
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

#c = CompilationEngine('10/ArrayTest/Main.jack')
c = CompilationEngine('10/ExpressionLessSquare/Main.jack')

c.compileClass()