// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// Assumes that R0 >= 0, R1 >= 0, and R0 * R1 < 32768.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)


@R1
D=M
@n
M=D    // n = R1
@mult
M=0    // mult = 0

(LOOP)
    @n
    D=M
    @STOP
    D;JLE    // if n <= 0 goto STOP

    @R0
    D=M
    @mult
    M=D+M    // mult += R0

    @n
    M=M-1

    @LOOP
    0;JMP   // goto LOOP

(STOP)
    @mult
    D=M
    @R2
    M=D

(END)
    @END
    0;JMP
