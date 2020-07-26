# Hack assembler
#
# A instruction - @...
# C instruction - dest = comp ; jump

import fileinput
import re 

next_custom_symbol_address = 16

def assign_new_symbol_address():
    global next_custom_symbol_address
    addr = next_custom_symbol_address
    next_custom_symbol_address += 1
    return addr

def process_a_instruction(line, symbols):
    arg = line.replace('@','')
    address = 0
    try:
        address = int(arg)        
    except:
        #label
        if arg not in symbols:
            symbols[arg] = assign_new_symbol_address()
        address = symbols[arg]
    print(f'{address:016b}')
    return

def get_jump(jmp):
    return {
        '':'000',
        'JGT':'001',
        'JEQ':'010',
        'JGE':'011',
        'JLT':'100',
        'JNE':'101',
        'JLE':'110',
        'JMP':'111'
    }[jmp]

def get_destination(dst):
    return {
        '':'000',
        'M':'001',
        'D':'010',
        'MD':'011',
        'A':'100',
        'AM':'101',
        'AD':'110',
        'AMD':'111'
    }[dst]

def get_comp(comp):
    return {
        '0'     :'101010',
        '1'     :'111111',
        '-1'    :'111010',
        'D'     :'001100',
        'A'     :'110000',
        '!D'    :'001101',
        '!A'    :'110001',
        '-D'    :'001111',
        '-A'    :'110011',
        'D+1'   :'011111',
        'A+1'   :'110111',
        'D-1'   :'001110',
        'A-1'   :'110010',
        'D+A'   :'000010',
        'D-A'   :'010011',
        'A-D'   :'000111',
        'D&A'   :'000000',
        'D|A'   :'010101'
    }[comp]

def builtin_symbols():
    return {
        'R0':0,
        'R1':1,
        'R2':2,
        'R3':3,
        'R4':4,
        'R5':5,
        'R6':6,
        'R7':7,
        'R8':8,
        'R9':9,
        'R10':10,
        'R11':11,
        'R12':12,
        'R13':13,
        'R14':14,
        'R15':15,
        'SCREEN':16384,
        'KBD':24576
    }

def process_symbols(line, instruction_address, symbols):
    # (SYMBOL)
    # later as @SYMBOL
    m = re.match('\((.+?)\)', line)
    if(m):
        symbol_name = m.group(1) 
        symbols[symbol_name] = instruction_address
        return True
    return False

def process_c_instruction(line):
    # format:
    # dest = comp ; jump

    rest_jmp = line.split(';')
    jmp = ''
    dest = ''
    # deal with optional jump
    if(len(rest_jmp) == 2):
        jmp = rest_jmp[1]
    rest_jmp = rest_jmp[0]
    # deal with optional dest
    dest_comp = rest_jmp.split('=')
    if(len(dest_comp) == 2):
        (dest,comp) = dest_comp
    else:
        comp = dest_comp[0]

    # comp lookup table doesn't care about A/M
    c = get_comp(comp.replace('M','A'))
    d = get_destination(dest)
    j = get_jump(jmp)
    #a bit used on M access
    a = 'M' in comp
    print(f'111{a:b}{c}{d}{j}')

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

lines_without_symbols = []
# second pass: find symbols and strip symbol lines
symbols = builtin_symbols()
instruction_address = 0
for line in lines:
    if not (process_symbols(line, instruction_address, symbols)):
        lines_without_symbols.append(line)
        instruction_address+=1

# third pass: assemble
for line in lines_without_symbols:
    if(line.startswith('@')):
        process_a_instruction(line, symbols)
    else:
        process_c_instruction(line)
