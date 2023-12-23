// Flips value of R[0] and R[1]
// Algorithm:
// temp = R0
// R[0] = R[1]
// R[1] = temp


@R0
D=M    // D = RAM[0]
@temp
M=D    // RAM[temp] = R0

@R1
D=M    // D = RAM[1]
@R0
M=D    // RAM[0] = RAM[1]

@temp
D=M
@R1
M=D    // RAM[1] = temp

(END)
@END
0;JMP
