# Jack language
## Program structure

The basic element is **class**.

Each class contains **field** and **static variable** declarations.

Then a sequence of **subroutine** declarations.
 - method - belong to the instance
 - function - belong to the class
 - constructor

## Type of tokens:

### White space and comments
  - //
  - /* ... */
### Symbols
  - ( ) [ ] { }
  - , (variable list separator)
  - ; (statement terminator)
  - = (assignment and comparison operator)
  - . (class member)
  - `+ - * / / & | ~ < >`
### Reserved words 
  - `class constructor method function`
  - `int boolean char void`
  - `var static field`
  - `let do if else while return`
  - `true false null`
  - `this`

### Constants
    - integer constants
    - string constants `"stuff"`
    - boolean constants `true false`
    - `null`

### Identifiers
    - A-z a-z 0-9 _
    - a number cannot bethe first character
    - case sensitive

## Variables

### Primitive types
- int - 16 bit signed
- boolean - true and false
- char - unicode character

### Object types
- declaration of object variables are only reference (a pointer)
- memory allocated in the constructor
- two builtin types: `Array`, `String`

#### Arrays
- 0-indexed
- initialized by `Array.new(length)`
- untyped

#### Strings
- "a string"

### Type conversions
- weakly typed, automatically converted from one type to another
- integer can be assigned to a reference variable, treated as a location in memory
- object can be converted into Array, fields can be accessed as array entries and vice versa

### Variable kinds and scope
- static `static`
- field `field`
- local `var`
- parameter - only in parameter list

### Statements
- let (assignment)
- if ... else
- while
- do (function call, ignoring the returned value)
- return; / Return expression;

### Expression
- constant
- variable name in scope
- this
- array element name[expression]
- subroutine call
- expression prefixed with unary operator ~ or -
- expression `operator` expression - 
  - operators (`+ - * / & | < > =`)
- `(`expression`)` in parentheses

> Priority not defined in the language, use parentheses

### Subroutine calls
- number and type of arguments must match

### Construction and destruction
- constructor should compile a request to allocate enough memory for the members
- destructor calls Memory.deAlloc(object)

### Standard library
- Math
- String
- Array
- Output
- Screen
- Keyboard
- Memory
- Sys

## Compiling and running
- each program in a separate directory
