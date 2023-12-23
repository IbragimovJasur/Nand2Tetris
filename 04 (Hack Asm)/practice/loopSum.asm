// Computes: 1+2+3 ... + R0
// Set R0 to some value before running code

@i
M=1    // i = 1

@R0
D=M
@n
M=D    // n = R0

@sum
M=0    // sum = 0

(LOOP)
    @i
    D=M
    @n
    D=D-M    // D = i-n
    @STOP
    D;JGT    // i>n

    @sum
    D=M
    @i
    D=D+M    // D = sum + i
    @sum
    M=D    // sum = D
    @i
    M=M+1    // i = i = 1

    @LOOP
    0;JMP

(STOP)
    @sum
    D=M
    @R1
    M=D    // R1=sum

(END)
    @END
    0;JMP
