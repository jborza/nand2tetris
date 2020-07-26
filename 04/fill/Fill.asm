// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

//TODO 
//first loop: listen to keyboard input and store pressed/nonpressed to variable (R1) 
//inner loop: for i in 0 to screen_length to set ram[i+screen_base] <= R1
//better version: redraw on key state change

// SCREEN=16384, KBD=24576
// screen size: 512x256

//pseudocode:
//@color = @kbd
(BEGIN)
//reset @color
@0
D=A
@color
M=D
@KBD
D=M
//@R0
//M=D
//set color to 1 if D > 0
@WASZERO
D; JEQ //jump if no key pressed
@0
D=!A
@color
M=D
(WASZERO)
//for i from 16384 to 24576
@i
M=0

@SCREEN
D=A
// i = @screen
@i
M=D

(LOOP)
//load @color, store to address where @i points
// *@i = @color
@color
D=M
@i
A=M
M=D
//@i++
@i
M=M+1
D=M

//until i < @KBD
@KBD
D=A-D
@LOOP
D; JGT
//jump to beginning of the program
(END)
@BEGIN
0; JMP 