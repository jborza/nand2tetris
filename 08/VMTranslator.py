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
import os
import re 
import sys

TEMP_ADDRESS = 5
TEMP_END_ADDRESS = 12
POINTER_ADDRESS = 13
POINTER_END_ADDRESS = 14

branch_counter = 0

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
    #increment SP value already, increase A to 1 more than we need
    print('AM=M+1')
    #decrement A from the previous step, SP is already incremented from the prvious step
    print('A=A-1')
    #*SP=D
    print('M=D')    

def get_segment_address(segment):
    return {
        'local':'@LCL',
        'argument':'@ARG',
        'this':'@THIS',
        'that':'@THAT'
    }[segment]

def get_module_name():
    filename = sys.argv[1]
    return os.path.splitext(os.path.basename(filename))[0]

def load_segment_offset_address_to_d(segment, offset):
    offsetInt = int(offset)

    #special cases:
    #fold temp+offset into a single load
    if(segment == 'temp'):
        print(f'@{TEMP_ADDRESS + offsetInt}')
        print('D=A')
        return

    #special resolution of pointer segment
    elif(segment == 'pointer'):
        if(offsetInt == 0):
            print(f'@THIS')
        elif(offsetInt == 1):
            print(f'@THAT')
        else:
             raise Exception(f'Invalid pointer {offset}')
        print('D=A')
        return

    #special handling for static variables
    elif(segment == 'static'):
        print(f'@{get_module_name()}.{offset}')
        print('D=A')
        return

    segment_addres = get_segment_address(segment)
    print(segment_addres)
    #do D=M[segment] + offset, but optimize offset s0 and 1 
    if(offsetInt == 0): #D=M[segment]
        print('D=M')
    elif(offsetInt == 1): #D=M[segment]+1
        print('D=M+1')
    else: #general case D=M[segment] + offset
        print('D=M')
        print(f'@{offset}')
        print('D=D+A')

def emit_pop(segment, offset):
    #M[@segment + offset] = M[@SP]
    load_segment_offset_address_to_d(segment, offset)
    #save address to R13
    print('@R13')
    print('M=D')
    #pop value from SP to D
    emit_pop_to_d()
    #use R13 as pointer
    print('@R13')
    print('A=M')
    #M[R13] = D
    print('M=D')

def emit_push(segment, offset):
    if(segment == 'constant'):
        emit_push_constant(offset)
        return
    #M[SP] = M[segment + offset]
    #get destination address to D
    load_segment_offset_address_to_d(segment, offset)
    #read target value into D: D=M[segment + offset]
    print('A=D')
    print('D=M')
    #store D into M[SP]
    emit_push_d()

def emit_push_constant(constant):
    # store constant (in D) to address pointed by SP
    print(f'@{constant}')
    print('D=A')
    emit_push_d()

def emit_pop_to_d():
    #decrement SP to point to X
    print('@SP')
    #pop y "to M" and decrement value of SP
    print('AM=M-1')
    
    #move M (value of x) to D
    print('D=M')

def emit_pop_to_m():
    #decrement SP to point to Y
    print('@SP')
    #pop y "to M" and decrement value of SP
    print('AM=M-1')


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

def emit_flow_control(flow_statement, flow_label_name):
    if(flow_statement == 'label'):
        print(f'({get_module_name()}.{flow_label_name})')
    elif(flow_statement == 'goto'):
        print(f'@{get_module_name()}.{flow_label_name}')
        print('0;JMP')
    else: #if-goto
        #we have to pop the stack and do something if it's 0 or -1 - so jump on negative?
        emit_pop_to_m()
        print(f'@{get_module_name()}.{flow_label_name}')
        print('M;JLT')

def initialize_vm():
    # set *sp=256
    print('@256')
    print('D=A')
    print('@SP')
    print('M=D')
    # set local=300
    print('@300')
    print('D=A')
    print('@LCL')
    print('M=D')
    # set argument=400
    print('@400')
    print('D=A')
    print('@ARG')
    print('M=D')
    # #set this=3000
    # print('@3000')
    # print('D=A')
    # print('@THIS')
    # print('M=D')
    # # set that=3010
    # print('@3010')
    # print('D=A')
    # print('@THAT')
    # print('M=D')

initialize_vm()

for line in lines:
    print(f'//{line}')
    match_push = re.match('push (constant|local|static|argument|this|that|temp|pointer) (.+)', line)
    match_pop = re.match('pop (local|static|argument|this|that|temp|pointer) (.+)', line)
    match_flow = re.match('(label|goto|if-goto) (.+?)', line)

    if(match_push):
        offset = match_push.group(2)
        segment = match_push.group(1)
        emit_push(segment, offset)
    elif(match_pop):
        offset = match_pop.group(2)
        segment = match_pop.group(1)
        emit_pop(segment, offset)
    elif(match_flow):
        flow_statement = match_flow.group(1)
        flow_label_name = match_flow.group(2)
        emit_flow_control(flow_statement, flow_label_name)
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
