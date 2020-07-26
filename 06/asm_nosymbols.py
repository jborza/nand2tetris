# Hack assembler
#
# A instruction
# C instruction

import fileinput
import sys

def process_a_instruction(line):
    a = int(line.replace('@',''))
    print(f'{a:016b}')

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

def process_c_instruction(line):
    # format:
    # dest = comp ; jump
    rest_jmp = line.split(';')
    jmp = ''
    dest = ''
    if(len(rest_jmp) == 2):
        jmp = rest_jmp[1]
    rest_jmp = rest_jmp[0]
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

for line in fileinput.input():
    line = line.strip()
    # skip comments
    if(line.startswith('//')):
        continue
    if(len(line) == 0):
        continue
    
    if(line.startswith('@')):
        process_a_instruction(line)
    else:
        process_c_instruction(line)
