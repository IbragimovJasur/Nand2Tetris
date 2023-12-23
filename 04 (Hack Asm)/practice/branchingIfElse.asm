// Computes: if R0>0
//              R1=1
//           else
//              R1=0


@R0
D=M    // D = RAM[0]

@POSITIVE
D;JGT   // If R0>0 goto line 8

@R1
M=0    // RAM[1] = 0
@END
0;JMP

(POSITIVE)
    @R1
    M=1    // RAM[1] = 1

(END)
    @10
    0;JMP
