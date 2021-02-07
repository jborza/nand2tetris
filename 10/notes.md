## 10 - Compiler I: Syntax analysis

Typically two main modules - **syntax analysis** and **code generation**.

### Syntax analysis:
- tokenizing (grouping input characters into language atoms), aka lexical analysis
- parsing (matching the atoms to the syntax rules)

### Grammars
- Context-free grammars
  - allows specifying how to combine tokens (**terminals**) into higher level elements (**non-terminals**)

e.g. 

```
whileStatement: 'while' '(' expression ')'
                    statement
statement: whileStatement
            | ifStatement
            | ...
            | '{' statementSequence '}'
statementSequence: ...            
expression: ...
```

Output of the parser is a **parse tree**

#### Recursive descent parsing

- Top-down approach - using a nested structure defined by the language grammar
- for every rule describing **non-terminal** we design a recursive routine to parse the non-terminal
  - if it encounters **terminals**, the routine can process them directly
  - if it encounters **non-terminals**, it can recursively call the non-terminal parsing routine

#### LL(0) Grammars

Whenever a non-terminal has several alternative derivation rules, the first token suffices to resolve which rule to use without ambiguity.

These can be handled simply and elegantly by recursive descent algorithms.

If the first token doesn't suffice, we need to look ahead to the next token.

### Jack Grammar

Conventions:

**'xxx'**: terminals
xxx: non-terminals
(): grouping
x|y: either x or y can appear
x?: x appears 0 or 1 times
x*: x appears 0 or more times

See Elements of Computing Systems, p.208

### Suggested implementation

3 modules:
- JackAnalyzer - top level driver that sets up and invokes other modules
- JackTokenizer - tokenizer
- CompilationEngine - recursive top down parser

Analyzer: 
- operates on a given source (single .jack file or directory with .jack files)
- for each source:
  - call tokenizer


#### Testing

For every `Xxx.jack` the authors provided `XxxT.xml` with the tokenizer output and `Xxx.xml` with parser output.