# Nand2Fpga project materials

## Part 7 Notes

### VM operations

|operation | result |
|-----|----- 
| add | x+y 
| sub | x-y
| neg | -y
| eq  | x == 0
| gt  | x > y
| lt  | x < y
| and | x and y
| or  | x or y
| not | not x


### Memory Segments

Memory segments to allow for various types of variables:
- argument
- local
- static
- constant
- this
- that
- pointer
- temp

Where they live?

- temp: 5-12
- pointer: 3-4 (*pointers* to this, that)
- static: [unit].[variable] (static var i in class Foo should result in assembly variable Foo.i)
- constant i - literal value of i
- local, argument, this, that - allocated dynamically

Then the compiler can "rewrite" symbolic variable names with their kind (argument, local, static) to a reference to memory segment + offset (such as static int s1 -> push static 1).

Then we just need to:
`push segment i` 
- i is nonnegative number

Those 8 segments exist to support a high-level object oriented language.

To move data between segments, we must use the stack.

e.g. let static 2 | argument 1
push argument 1
pop static 2

### EQ, LT, GT

I've ran into some trouble thinking about the implementation of EQ (x==y), GT (x>y), LT (x<y) vm opcodes

I initially thought I'd need to do something like 

```
"pop to d"
"pop to m"
D=D-M //if the result is zero, return -1 (true), else return 0 (false)
@FALSE
D;JNE
(TRUE)
"push constant -1"
@END
0;JMP
(FALSE)
"push constant 0"
(END)
```

This feels like way too many instructions and probably it can be reduced to converting (0=>-1, anything else=>0)

I ended up emitting this bytecode:

```
//pop x to d
@SP
M=M-1
A=M
D=M
//pop y yo d
@SP
M=M-1
A=M
//subtract, if x==y the result is 0
D=D-M
//eagerly set *sp=-1 (true)
@SP
A=M
M=-1
@ENDEQ.3
//if x==y, we're done, jump to the end
D;JEQ
//if we're here, x!=y, set *sp=0
@SP
A=M
M=0
(ENDEQ.3)
//increment SP
@SP
M=M+1
```

The job *should* be similar for `gt`/`lt` though:

`gt`:
```
"pop to d"
"pop to m"
D=D-M //if the result is positive, return -1 (true), else return 0 (false)
```

## Code density

Right after the module 7 (generating arithmetic/logic opcodes) the code density is around 10.4 (397 asm / 38 vm instructions). After optimizing push/pop instructions to load @SP only once and utilize multiple destinations this got better to 8.9 (340 asm / 38 vm instructions):

```py
def emit_push_d():
    #set address pointed by SP
    print('@SP')
    #increment SP value already, increase A to 1 more than we need
    print('AM=M+1')
    #decrement A from the previous step, SP is already incremented from the prvious step
    print('A=A-1')
    #*SP=D
    print('M=D')
```


