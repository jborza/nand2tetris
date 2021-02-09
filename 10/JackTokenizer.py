import os
import re

TOKENTYPE_KEYWORD = "keyword"
TOKENTYPE_SYMBOL = "symbol"
TOKENTYPE_IDENTIFIER = "identifier"
TOKENTYPE_INT_CONST = "integerConstant"
TOKENTYPE_STRING_CONST = "stringConstant"
TOKENTYPE_INVALID = "invalid"

def keyword_list():
    return {"class", "constructor", "function", "method", "field", "static",
            "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do",
            "if", "else", "while", "return"}

def symbol_list():
    return ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]

def escape_symbol(symbol):
    if symbol == '<':
        return '&lt;'
    elif symbol == '>':
        return '&gt;'
    elif symbol == '&':
        return '&amp;'
    else:
        return symbol

def symbol_map():
    return dict([(symbol, escape_symbol(symbol)) for symbol in symbol_list()])

# returns (token, type) tuple
def tokenType(token, token_was_string):
    #string constant
    if token_was_string:
        return token, TOKENTYPE_STRING_CONST
    if token in keywords:
        return token, TOKENTYPE_KEYWORD
    if token in symbols:
        return escape_symbol(token), TOKENTYPE_SYMBOL
    #integer constant - 
    if token.isnumeric():
        numValue = int(token)
        if(numValue >= 0 and numValue <= 32767):
            return numValue, TOKENTYPE_INT_CONST
    #identifier [A-Za-z_][A-Za-z_0-9]*
    if re.match("^[A-Za-z_][A-Za-z0-9_]*$", token):
        return token, TOKENTYPE_IDENTIFIER
    return None, TOKENTYPE_INVALID

def hasMoreTokens(input_stream):
    return len(input_stream) > 0

# should be called only if hasMoreTokens is true
# returns (token, input_stream, token_was_string)
def advance(input_stream):
    #trim leading spaces
    token_was_string = False
    input_stream = input_stream.strip()
    current_token = ""
    #special case - the first character is a symbol
    firstchar = input_stream[0]
    if firstchar in symbols:
        #consume just one character
        return firstchar, input_stream[1:], False
    
    if firstchar == '"':
        #look forward to the matching "
        next_quote = input_stream.index('"', 1)
        current_token = input_stream[1:next_quote] 
        return current_token, input_stream[next_quote+1:], True

    #consume character by character until we get to one of the terminators (symbol or whitespace)
    #example foo+3;
    while True:
        if(len(input_stream) == 0):
            print("NO INPUT!!")
            return None, None, False
        
        char = input_stream[0]
        if char == " " or char in symbols:
            #end the current token
            return current_token, input_stream, False
        current_token += char
        input_stream = input_stream[1:]

def initialize(filename):
    file = open(filename, 'r')

    contents = file.read()
    #strip single line comments
    contents = re.sub("//.*?\n", " ", contents)    
    contents = re.sub("/\*.+\*/", " ", contents)
    #tabs and newlines to spaces
    contents = re.sub("\s", " ", contents)
    return contents.strip()

def tokenize(filename):
    #read file line by line
    input_stream = initialize(filename) # contents.strip()
    
    #and advance token by token
    print("<tokens>")
    while(hasMoreTokens(input_stream)):
        token, input_stream, token_was_string = advance(input_stream)
        input_stream = input_stream.strip()
        token_value, token_type = tokenType(token, token_was_string)
        print(f"<{token_type}> {token_value} </{token_type}>")
    print("</tokens>")


keywords = keyword_list()
symbols = symbol_map()

class JackTokenizer:

    def __init__(self, filename):
        self.input_stream = initialize(filename)

    def advance(self):
        self.token, self.input_stream, self.token_was_string = advance(self.input_stream)
        self.input_stream = self.input_stream.strip()        
        self.token, self.token_type = tokenType(self.token, self.token_was_string)

    def hasMoreTokens(self):
        return hasMoreTokens(self.input_stream)

    def valid_token_or_none(self, valid_type):
        if(self.token_type != valid_type):
            return None
        return self.token

    def keyword(self):
        return self.valid_token_or_none(TOKENTYPE_KEYWORD)

    def symbol(self):
        return self.valid_token_or_none(TOKENTYPE_SYMBOL)

    def identifier(self):
        return self.valid_token_or_none(TOKENTYPE_IDENTIFIER)

    def intVal(self):
        return self.valid_token_or_none(TOKENTYPE_INT_CONST)

    def stringVal(self):
        return self.valid_token_or_none(TOKENTYPE_STRING_CONST)

#tokenize('10/ArrayTest/Main.jack')