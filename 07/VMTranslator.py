# Hack VM Translator
# stage 1 - handling stack arithmetic instructions:
# add = x+y
# sub = x-y
# neg = -y
# eq  = x == y (docs say x==0)
# gt  = x > y
# lt  = x < y
# and = x and y
# or  = x or y
# not = not x
# push constant x
# boolean true is -1, false is 0

####
# memory access:
# pop segment i
# push segment i

####
# branching
# label label
# goto label
# if-goto label

####
# function
# function functionName nVars
# call functionName nArgs
# return

import fileinput
import re 

# first pass: strip comments and blank lines
lines = []
for line in fileinput.input():
    line = line.strip()
    # skip comments
    if(line.startswith('//')):
        continue
    if(len(line) == 0):
        continue
    if '//' in line:
        line = line[:line.index('//')].strip()
    lines.append(line)

# push D register to stack
def emit_push_d():
    #set address pointed by SP
    print('@SP')
    print('A=M')
    #now M points to M[SP]
    print('M=D')
    # increment SP
    print('@SP')
    print('M=M+1')

def handle_push_constant(constant):
    # store constant (in D) to address pointed by SP
    print(f'@{constant}')
    print('D=A')
    print('@SP')
    #increment SP value already, increase A to 1 more than we need
    print('AM=M+1')
    #decrement A from the previous step
    print('A=A-1')
    #*SP=D
    print('M=D')

def emit_pop_to_d():
    #decrement SP to point to X
    print('@SP')
    print('M=M-1')
    
    #pop x to D
    print('A=M')
    print('D=M')

def emit_pop_to_m():
    #decrement SP to point to Y
    print('@SP')
    print('M=M-1')

    #pop y "to M"
    print('A=M')

def emit_xy_operation(operand):
    #pop x,y, operation, push
    #pop x
    emit_pop_to_d()

    #decrement SP to point to Y
    #pop y
    emit_pop_to_m()

    #perform operation between D and M
    print(f'D={operand}')
    
    #push result
    emit_push_d()

#unary operations
def emit_unary(operation):
    #pop x
    emit_pop_to_m()
    #do operation
    print(f'D={operation}M')
     #push result
    emit_push_d()

def emit_boolean(operation):
    global branch_counter
    branch_counter+=1
    #pop x
    emit_pop_to_d()
    #pop y to m
    emit_pop_to_m()
    # we can subtract them
    # later jump if the result is unexpected (not negative, not equal, not positive)
    print('D=M-D')
    #set up stack
    print('@SP')
    print('A=M')
    #eagerly set result to equal (true)
    print('M=-1')
    #jump to 'notequal' part to return 0
    print(f'@ENDCMP.{branch_counter}')
    print(f'D;{operation}')
    #not equal - set *SP=0
    print('@SP')
    print('A=M')
    print('M=0')
    print(f'(ENDCMP.{branch_counter})')
    #increase SP
    print('@SP')
    print('M=M+1')

#vm opcode implementation 

def emit_add():
    emit_xy_operation('D+M')

def emit_sub():
    emit_xy_operation('M-D')

def emit_and():
    emit_xy_operation('D&M')

def emit_or():
    emit_xy_operation('D|M')

def emit_neg():
    emit_unary('-')

def emit_not():
    emit_unary('!')

def emit_lt():
    #x<y
   emit_boolean('JLT')

def emit_gt():
    #x>y
    emit_boolean('JGT')

def emit_eq():
    emit_boolean('JEQ')

branch_counter = 0

def initialize_vm():
    # set *sp=256
    print('@256')
    print('D=A')
    print('@SP')
    print('M=D')

initialize_vm()
for line in lines:
    print(f'//{line}')
    m = re.match('push constant (.+)', line)
    if(m):
        constant = m.group(1)
        handle_push_constant(constant)
    elif(line == 'add'):
        emit_add()
    elif line == 'sub':
        emit_sub()
    elif(line == 'neg'):
        emit_neg()
    elif(line == 'eq'):
        emit_eq()
    elif(line == 'gt'):
        emit_gt()
    elif(line == 'lt'):
        emit_lt()
    elif(line == 'and'):
        emit_and()
    elif(line == 'or'):
        emit_or()
    elif(line == 'not'):
        emit_not()
    else:
        raise Exception(f'Unknown operation:{line}')
