# Part 08 notes

function f n - function f has n local variables

call f n - call function f with n arguments

Before a function is called: 
- caller function has pushed n arguments to the stack

Called function:
- argument segment has been initialized to the actual arguments
- local segment allocated and initialized with zeroes
- static segment set to the static segment of the VM unit (class)
- working stack is empty
- this, that, pointer, temp are undefined upon entry
- pushes a return value to the stack before the return (what about void functions?)

After a function is called (caller view):
- pushed arguments have disappeared from the stack
- return value appears on the stack
- argument, local, static, this, that, pointer have been restored
- temp is undefined


### Stack frame layout:
| pointer | description |
|-----| -----| 
| ARG | argument 0
|  | argument 1
|  | ...
|  | argument N
| saved state | return address
| --- | saved LCL
| --- | saved ARG
| --- | saved THIS
| --- | saved THAT
| LCL | local 0
|  | local 1
|  | ...
|  | local N
| SP | ?

### Test program order

- Program Flow
    - BasicLoop
    - Fibonacci
- FunctionCalls
    - SimpleFunction
    - NestedCall
    - FibonacciElement
    - StaticsTest
