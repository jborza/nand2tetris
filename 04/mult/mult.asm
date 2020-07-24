// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// pseudocode:
// R2 = 0
// for i in range(0,R0) do:
//   R2 = R2 + R1

//negative numbers? not in the sample file, so ignore them for the time being.

//////////////

// R2 = 0
@R2
M=0

// i = 0
@i
M=0

(LOOP)
// for i in range (0,R0) do

// D = R2
@R2
D=M
// D = R2 + R1
@R1
D=D+M
// R2 = D
@R2
M=D

// i++
@i
M=M+1

// compare i to R0
D=M
@R0
D=M-D
// d is zero if i == R1, then we fall over the jump. if it's greater, we jump to loop
@LOOP
D; JGT
(END)
@END
0; JMP //infinite loop