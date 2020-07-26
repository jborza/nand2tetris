# Hack VM Translator
# stage 1 - handling stack arithmetic instructions:
# add = x+y
# sub = x-y
# neg = -y
# eq  = x == 0
# gt  = x > y
# lt  = x < y
# and = x and y
# or  = x or y
# not = not x
# push constant x

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
    print('D=M+1')
    print('M=D')

def handle_push_constant(constant):
    print(f'@{constant}')
    print('D=A')
    # store constant (in D) to address pointed by SP
    emit_push_d()

def emit_add():
    #pop x,y, add, push
    
    #decrement SP to point to X
    print('@SP')
    print('M=M-1')
    
    #pop x to D
    print('A=M')
    print('D=M')

    #decrement SP to point to Y
    print('@SP')
    print('M=M-1')

    #pop y "to M"
    print('A=M')

    #add to D
    print('D=D+M')
    
    #push result
    emit_push_d()


def initialize_vm():
    # set *sp=256
    print('@256')
    print('D=A')
    print('@SP')
    print('M=D')
    print('@0')
    print('D=A')

initialize_vm()
for line in lines:
    print(f'//{line}')
    m = re.match('push constant (.+?)', line)
    if(m):
        constant = m.group(1)
        handle_push_constant(constant)
    if(line == 'add'):
        emit_add();

        
    